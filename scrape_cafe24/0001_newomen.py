import requests
import os
import sys
import time
from requests.compat import urljoin, quote_plus
from bs4 import BeautifulSoup
import socket
import socks
from collections import defaultdict
import re
from urllib.parse import urlencode
import urllib.parse
from urllib import request
from urllib.error import HTTPError
import urllib3
import json
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, '..')
# cafe24
# 특이사항
# 품절여부는 옵션에
import global3
import DBconnect
# socks.set_default_proxy(socks.SOCKS5,"lcalhost",9150)
# socket.socket = socks.socksocketo
shopname = "뉴먼"
basicurl = "http://www.newomen.co.kr/" #바꿔
addurl = "product/list.html?cate_no=" #바꿔
pageurl = "&page=" #바꿔
# 
# 
indexcate = ["25","26","42","43","44","46","82"]
category = ["New Arrivals","Outer","Top","Bottom","Dress","Shoes & Acc","Sale"]
num = 0
#바꿔

crawl = defaultdict(list)
# 크롤링 배열


def maingo(url,cate,idx):
    
    r = requests.get("".join((basicurl,addurl,idx))) #바꿔
    # print(" ".join((basicurl,addurl,idx)))
    if r.status_code != 200: # http 코드 오류시
        print(r.status_code)
        time.sleep(3)
        return
    html = r.text
    soup = BeautifulSoup(html,'html.parser')
    print("".join((basicurl,addurl,idx)))
    nowcate = soup.find("div",{"class" : "xans-product-headcategory"}).get_text() #바꿔
    if nowcate.upper() != cate:
        print("다르다")
        print(cate)
        print(nowcate)
        global3.errmsg += basicurl+cate+ "변경됨\n"
    menu = soup.find("ul",{"class" : "menuCategory"}).find_all("li") #바꿔
        
    if menu == []:
        print("소분류 없다")
        firstscrape("".join((basicurl,addurl,idx)),"",cate) # 바꿔
    else:
        for name in menu:
            try:
                
                link = urljoin(basicurl,name.find("a").get("href")) # 바꿔
                soncate = name.find("a").get_text() #바꿔

            except AttributeError :
                print("에러를 포착했다")
            else:
                
                firstscrape(link,soncate,cate)
    return global3.errmsg         


def firstscrape(url,soncate,parentcate):
    global num
    r = requests.get(url)
    # print(r.status_code)
    html = r.text
    soup = BeautifulSoup(html,'html.parser')
    print(url)
    try:
        pagenum = soup.find("div",{"class" : "xans-product-normalpaging"}).find_all("li",{"class" : "xans-record-"}).__len__() #페이지수 바꿔
    except AttributeError:
        return
    # print(pagenum)
    i = 0
    while i < pagenum:
        if i != 0:
            r = requests.get("".join((url,pageurl,str(i+1)))) # 페이지 수만큼 요청 바꿔
            html = r.text
            soup = BeautifulSoup(html,'html.parser')
        try:
            menu = soup.find("ul",{"class" : "prdList grid3"}).find_all("li",{"id" : re.compile("anchorBoxId_*")}) # 추천탭있을때 바꿔
        except IndexError:
            menu = soup.find("ul",{"class" : "prdList grid3"}).find_all("li",{"class" : "xans-record-"}) # 없을때 바꿔
        #예외에 대한 처리 (샵마다 다름)
        for name in menu:
            
            try:
                prpk = name.get("id") #PK고유값 바꿔
                
                primg = name.find("div",{"class":"thumbnail"}).find("img").get("src") #이미지주소바꿔
                # print(primg)
                prname = name.find("li",{"class" : "item_name"}).find("span").get_text() #이름바꿔
                # print(prname)
                prlink = name.find("div",{"class" : "thumbnail"}).find("a").get("href") #링크 바꿔

                c = name.find("ul",{"class" : "xans-product-listitem"}) #가격 큰 박스부분 바꿔
                prpricebf = c.find_all("li")[0].find_all("span")[0].get_text() #할인전가격 #바꿔
                # print(prpricebf)
                prprice = c.find_all("li")[1].find_all("span")[0].get_text() #할인가격 #바꿔
                # print(prprice)
                if prprice == prpricebf: # 예외처리
                    prprice = "0"
                    
                else:
                    # prprice = prprice.replace("원","") #바꿔
                    prprice = prprice.replace(",","")
                # prpricebf = prpricebf.replace("원","") #바꿔
                prpricebf = prpricebf.replace(",","")
                

                # 전항목 수정 사항
            except AttributeError :
                print("싼맛없다")
                prprice = "0"
                prpricebf = prpricebf.replace("원","") #바꿔
                prpricebf = prpricebf.replace(",","")
                
                
            except IndexError :
                print("싼맛없다")
                prprice = "0"
                prpricebf = prpricebf.replace("원","") #바꿔
                prpricebf = prpricebf.replace(",","")
            
            
            
            
            try:
                prsoldout = name.find("ul",{"class" : "icon"}).find("img",{"alt" : "품절"}) #바꿔 품절
            except AttributeError :
                prsoldout = "0"
            else:
                prsoldout = "1"
            if primg == None:
                print("태그없다")
                global3.errmsg += basicurl+soncate+"샵 구조 바뀐듯\n" 
            else:
                    
                num += 1
                print(num,basicurl)
                print(urljoin(basicurl,primg))
                print(prname)
                print(prpricebf)
                print(prprice)
                
                print(prpk.split("_")[1])
                crawl["prpk"].append(prpk.split("_")[1]) #바꿔 
                crawl["primg"].append(primg)
                crawl["prname"].append(prname)
                crawl["prpricebf"].append(prpricebf)
                crawl["prprice"].append(prprice)
                crawl["prsoldout"].append(prsoldout) # 0이 품절 x 1이 품절 ㅇ
                
                crawl["prcate"].append(parentcate.upper())
                crawl["prsmcate"].append(soncate.upper())
                nexturl =  urljoin(basicurl,prlink)
                crawl["prlink"].append(nexturl)
                

                detaila.detailscrapego(nexturl,crawl,i,prpricebf) # 다음으로 넘기기 협약시에 하고 아니면 닫아놓기
        i += 1


class detaila():
    a = 0
    

    def __init__(self):
         pass

    def detailscrapego(url,param,idx,prbf):
        r = requests.get(url)
        
        if r.status_code != 200 :
            time.sleep(3)
        
        html = r.text
        soup = BeautifulSoup(html,'html.parser')
        javascript = soup.find(text=re.compile("option_stock_data"))
        # print(javascript)
        proption = ""
        try:
            awd = re.findall("option_stock_data+([^;]*;+)",javascript)
            asd = re.findall("\"(P[0-9|A-Z]{7,14}).\":{.\"stock_price.\":.\"([0-9]{1,10})\.[0-9]{1,4}.\",.\"use_stock.\":(false|true),.\"use_soldout.\":.\"(F|T).\",.\"is_display.\":.\"(F|T).\",.\"is_selling.\":.\"(F|T).\",.\"option_price.\":([0-9]{1,11}),.\"option_name.\":.\"(.*?).\",.\"option_value.\":.\"(.*?).\",.\"stock_number.\":([0-9|-]{1,10}),.\"option_value_orginal.\":\[.\"(.*?).\"\],.\"use_stock_original.\":.\"([T|F]).\",.\"use_soldout_original.\":.\"([T|F]).\",.\"use_soldout_today_delivery.\":(.*?),.\"is_auto_soldout.\":.\"([T|F]).\",.\"is_mandatory.\":.\"([T|F]).\",.\"option_id.\":.\"(.*?).\",.\"is_reserve_stat.\":.\"(.*?).\",.\"item_image_file.\":(.*?),.\"origin_option_added_price.\":.\"(.*?).\"}",awd[0])
            
            for i in asd:
                print(i[8].replace("\\\\","\\").encode("utf-8").decode('unicode-escape')) #옵션이름
                print(i[2]) #품절여부
                print(i[9]) #재고
                print(i[16]) #옵션인덱스
                print(i[6]) #옵션가격 (추가가격아님))
                soldout = "F"
                if i[2] == "false":
                    soldout = "F"
                else:
                    soldout = "T"
                optprice = str(int(i[6])-int(prbf))
                optstr = i[8].replace("\\\\","\\").encode("utf-8").decode('unicode-escape').replace('-','^*').replace(' ','')
                proption += i[16] + "^@" + optprice + "^$" + soldout + "^%" + optstr +">><<" 
        except AttributeError:
            proption = "789^@0^$F^%NULL"
        except IndexError:
            proption = "789^@0^$F^%NULL"
        # ab = asd[0][7].replace("\\\\","\\")
        # url = u+ab
        # abc = ab.encode("utf-8").decode('unicode-escape')
        # abc = ab.encode("latin-1").decode('unicode-escape').encode('utf-8').decode('utf-8')
        # print(abc)
        # print( ab.unicode)
            # ab.decode("utf-8","ignore"))
        # print(str(ab.encode("utf-8"),"utf-8").decode("utf-8"))
        print(proption)
        try:
            
            highimage = soup.find("div",{"class" : "thumbnail"}).find("img").get("src") #하이이미지 # 바꿔
            # detailimagearray = soup.find("div",{"class":"cont"}).find_all("img") # 디테일 이미지
            detailimagearray = "<head>"
            detailimagearray += '<base href="http://www.newomen.co.kr/" target="_blank">' #바꿔
            temp = soup.find("head").find_all("link",{"type" : "text/css"}) 
            for i in temp:
                detailimagearray += str(i)
            detailimagearray += "</head><body>"
            detailimagearray += str(soup.find("div",{"class": "cont"})) #바꿔
            detailimagearray += str(soup.find("</body>"))

            # option = soup.find("div",{"class" : "df-detail-fixed-scroll"}).find_all("select")
            # if option.__len__() > 1:
            #     #갓뎀 개발해야됨
            #     driver = webdriver.Chrome('/Users/nohjuhyun/Downloads/chromedriver') # 컴터마다 다르게
            #     driver.get(url)
            #     driver.implicitly_wait(2)
            #     # driver.execute_script("window.stop()")
            #     # time.sleep(3)
            #     # driver.execute_script("window.stop();")

            #     driver.find_element_by_xpath("//select[@option_sort_no='1']").click()
            #     driver.implicitly_wait(1)
            #     a = driver.find_elements_by_xpath("//select[@option_sort_no='2']//*")
            #     # print(a.text)
            #     for i in a:
            #         print(i.text)
            #         # 코드 넣기

            #     driver.close()

            # else:
            #     print(1)
            #     # optiontagarray = option.find("select").find_all("option")
            #     # for i in optiontagarray:
            #     #     optionarray.append(i.get_text())   
        except AttributeError as e:
            print("에러에러")
            print(e)
    # print(menu)
        else :
            
            
            # print(detailimage)
            # print(highimage)
            # print(optionarray)
            crawl["highimg"].append(highimage)
            crawl["html"].append(detailimagearray)
            crawl["proption"].append(proption)
            
            
            

# 실행 for 구문

for i,val in enumerate(category):
        # print(i)
        maingo(basicurl,val,indexcate[i])
        # time.sleep(1)
print(shopname)
DBconnect.httpconnect(crawl,category,shopname)
    # conn = httplib ("test.moamoa.co.kr/crawl/v1/check_shop.php")
    # conn.request("POST", "" , data,)
    # response = conn.getresponse()
    # print(response.status,response.reason)
# db넣는 구문