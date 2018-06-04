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
# makeshop
# 
# 특이사항

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

sys.path.insert(0, '..')
import global3
import DBconnect
# from detailscrape import _0003_evajunie    # 이름 바꾸시고

# socks.set_default_proxy(socks.SOCKS5,"lcalhost",9150)
# socket.socket = socks.socksocketo
shopname= "폭스타일"
basicurl = "http://www.4xtyle.com/"
addurl = "shop/shopbrand.html?xcode=" 
pageurl = "&page=" 
category = ["헤이하버(HEYHOVER)","귀걸이","귀찌","목걸이","반지","쥬얼리 세트","팔찌&발찌","헤어악세사리","14K/10K","시계","패션아이템","FASHION ITEM","SALE!"]
indexcate = ["123","084","084","086","061","003","036","060","098","035","010","073"]

# 5개 다 수정

errmsg = ""
crawl = defaultdict(list)
# 크롤링 배열


def main(url,cate,idx):
    global errmsg
    r = requests.get("".join((basicurl,addurl,idx))) # 순서 수정
    # print(" ".join((basicurl,addurl,idx)))
    if r.status_code != 200: # http 코드 오류시
        print(r.status_code)
        time.sleep(3)
        return
    html = r.text
    soup = BeautifulSoup(html,'html.parser')
    nowcate = soup.find("div",{"class":"product_category"}).find("h1").get_text()
    if nowcate != cate:
        print("다르다")
        errmsg += basicurl+cate+ "변경됨\n"
    try:
        menu = soup.find("div",{"class" : "menu"}).find_all("li") # 수정
        
    except AttributeError:
        print("소분류 없다")
        firstscrape("".join((basicurl,addurl,idx)),cate,cate) # 수정
    else:
        for name in menu:
            if name.find("a").get_text() == "품절임박":
                break
            
            try:
                
                link = urljoin(basicurl,name.find("a").get("href")) # 수정
                soncate = name.find("a").get_text() # 수정
                
            except AttributeError :
                print("에러를 포착했다")
            else:
                
                firstscrape(link,soncate,cate) # 수정
    return errmsg


def firstscrape(url,soncate,parentcate):
    global num
    r = requests.get(url)
    # print(r.status_code)
    html = r.text
    soup = BeautifulSoup(html,'html.parser')
    pagenum = soup.find("ul",{"class" : "paging"}).find_all("li").__len__()-1 #페이지 수 수정 
    if pagenum > 1:
        pagenum -= 1
    # print(pagenum)
    i = 0
    while i < pagenum:
        if i != 0:
            r = requests.get("".join((url,pageurl,str(i+1)))) # 페이지 수만큼 요청 
            html = r.text
            soup = BeautifulSoup(html,'html.parser')
        
            
        try:
            menu = soup.find("div",{"class" : "cate_item product_list"}).find("ul").find_all("li") # 추천탭있을때 

        except IndexError:
            menu = soup.find("div",{"class" : "cate_item product_list"}).find("ul").find_all("li") # 추천탭있을때 

        for name in menu:
            
            try:
                prpricebf = name.find("p",{"class":"price"}).find("span",{"class" :"disbefore_sales_p"}).get("data-salesprice") #할인전가격
            except AttributeError :
                # IndexError
                # print("싼맛없다")
                prpricebf = name.find("p",{"class":"price"}).find("span",{"class" :"sales_p"}).get("data-salesprice")
                prprice = "0"
                # prpricebf = prpricebf.replace("원","")
                # prpricebf = prpricebf.replace(",","")
                # prsalebool = "0"
            else:
                prprice = name.find("p",{"class":"price"}).find("span",{"class" :"discount_p"}).get("data-discountprice")
                # prpricebf = prpricebf.replace("원","")
                # prpricebf = prpricebf.replace(",","")
                # prprice = prprice.replace("원","")
                # prprice = prprice.replace(",","")
                # prsalebool = "1"
                #가격 처리부분 (논리고민)

            try:

                # print(name)
                # prpk = name.find("li",{"class" : "SMS_main_display_order_stock"}).find("b").get("data-product-code")
                
                primg = name.find("p",{"class" :"thum"}).find("img").get("src")
                prname = name.find("p",{"class" : "name"}).find("a").get_text()
                
                 #할인가격
                # if prprice == prpricebf: # 예외처리
                #     prpricebf = "0"
                #     #뭐로할지 결정
                # else:
                #     prpricebf = prpricebf.replace("₩","")
                #     prpricebf = prpricebf.replace(",","")
                
                prlink = name.find("p",{"class" : "thum"}).find("a").get("href")

                # 전항목 수정 사항
            except AttributeError:
                print("에러를 포착했다")

            
            else:
                if primg == None:
                    print("태그없다")
                    errmsg += basicurl+soncate+"샵 구조 바뀐듯\n"
                else:
                    print(num,basicurl)
                    num += 1
                    # try:
                    #     prsoldout = name.find("li",{"class" : "icons"}).find("b").get_text()
                    #     if prsoldout == "품절"
                    #         prsoldout = "1"
                    # except AttributeError:
                    prsoldout = "0"
                    # else:
                        
                    print(urljoin(basicurl,primg))
                    print(prname.encode("windows-1252").decode('cp949'))
                    print(prpricebf)
                    print(prprice)
                    # print(prpk[-4:])

                    # crawl["prpk"].append(prpk)
                    crawl["primg"].append(primg)
                    crawl["prname"].append(prname.encode("windows-1252").decode('cp949'))
                    crawl["prpricebf"].append(prpricebf)
                    crawl["prprice"].append(prprice)
                    crawl["prsoldout"].append(prsoldout) # 0이 품절 x 1이 품절 ㅇ
                    # crawl["prsalebool"].append(prsalebool)
                    crawl["prcate"].append(parentcate)
                    crawl["prsmcate"].append(soncate)
                    nexturl =  urljoin(basicurl,prlink)
                    crawl["prlink"].append(nexturl)
                    # nextfunc = _0005_secretlabel.detail

                    detaila.detailscrapego(nexturl) # 다음으로 넘기기 협약시에 하고 아니면 닫아놓기
        i += 1

class detaila():
    a = 0
    
    def __init__(self):
         pass
    def detailscrapego(url):
        r = requests.get(url)
        
        if r.status_code != 200 :
            time.sleep(3)
        proption = ""
        html = r.text
        soup = BeautifulSoup(html,'html.parser')
        javascript = soup.find(text=re.compile("optionJsonData"))
        javascript = javascript.encode("windows-1252").decode('cp949')
        print("옵션크롤링")
        option1 = re.findall("sto_sort:\'([0-9]{1,2})\',sto_matrix:\'[0-9:0-9,]{1,20}\',sto_code:\'\',opt_values:\'([0-9|A-Z|가-힣|a-z|(|)]{1,20})\',sto_price:\'([0-9]{1,10})\',",javascript)
        option2 = re.findall("sto_state:\'([A-Z]{1,10})\'",javascript)
        # realidx = re.findall("product_uid = \'([0-9]{1,10})\'",javascript)
        
        for idx,i in enumerate(option1):
                # print(i[1]) #옵션이름
                # print(i[2]) #품절여부
                # print(i[0]) #옵션인덱스
                # print(i[2]) #옵션가격 (추가가격)
                soldout = "F"
                if option2[idx] == "SALE":
                    soldout = "F"
                else:
                    soldout = "T"
                optstr = i[1].encode("utf-8").decode('unicode-escape').replace(',','^*').replace(' ','')
                proption += i[0] + "^@" + i[2] + "^$" + soldout + "^%" + optstr +">><<" 


        try:
            prpk = soup.find("div",{"class" : "crema-product-score"}).get("data-product-code")
            highimage = soup.find("div",{"class" : "thum"}).find("a").find("img").get("src") #하이이미지
            detailimagearray = soup.find("div",{"class":"prd-detail"})

            # 셀레니움 동적 크롤링 필요시 사용
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

        except AttributeError:
            print("에러에러")
        else :
            print(prpk)
            crawl["detailimg"].append(detailimagearray)

            crawl["prpk"].append(prpk)
            crawl["highimg"].append(highimage)
            crawl["proption"].append(proption)


# 실행 for 구문
num = 0
for i,val in enumerate(category):
    print(i)
    main(basicurl,val,indexcate[i])
    # time.sleep(1)
DBconnect.httpconnect(crawl,category,shopname)
# db넣는 구문