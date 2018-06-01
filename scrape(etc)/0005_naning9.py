# 미완
import requests
import os
import sys
import time
from requests.compat import urljoin, quote_plus
from bs4 import BeautifulSoup
import socket
import socks    
from collections import defaultdict

# cafe24
# 특이사항
# 구조적문제 크롤링방지가 있음.

sys.path.insert(0, './detailscrape')
# from detailscrape import _0001_intheshu    # 협약시 이름 바꾸시고

# socks.set_default_proxy(socks.SOCKS5,"lcalhost",9150)
# socket.socket = socks.socksocket

basicurl = "http://www.naning9.com/"  
addurl = "shop/list.php?cate=" 
pageurl = "&page="
indexcate = ["0O","0S","0T","0V","0U","0W","0X","18","11","0a"]
category = ["NEW5%","TOP","OUTER","PANTS","SKIRTS&DRESS","SHOES&BAG","ACCESSORY","SUMMER","ONLY9","SALE"]
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
    nowcate = soup.find("ul",{"class" : "group group_category"}).find("a",{"class":"active"}).get_text() # 수정
    if nowcate != cate:
        print("다르다")
        errmsg += basicurl+cate+ "변경됨\n"
    try:
        menu = soup.find("ul",{"class" : "group group_category"}).find_all("li") # 수정
        
    except AttributeError:
        print("소분류 없다")
        firstscrape("".join((basicurl,addurl,idx)),cate,cate) # 수정
    

    else:
        if len(menu) == 1 :
            print("소분류 없다")
            firstscrape("".join((basicurl,addurl,idx)),cate,cate)

        else :
            for name in menu:
                
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
    global errmsg
    r = requests.get(url)
    # print(r.status_code)
    html = r.text
    soup = BeautifulSoup(html,'html.parser')
    print(url)
    try:
        pagenum = soup.find("div",{"class" : "list_wrapper"}).find("div",{"class" : "item_list cle"}).find_all("div",{"class":"list_cell"}).__len__() #페이지 수 수정
    except AttributeError:
        return 
    # print(pagenum)
    i = 0
    while i < pagenum:
        if i != 0:
            r = requests.get("".join((url,pageurl,str(i+1)))) # 페이지 수만큼 요청 
            html = r.text
            soup = BeautifulSoup(html,'html.parser')
        # try:
        print(soup)
        menu = soup.find("div",{"class" : "list_wrapper"}).find("div",{"class" : "item_list cle"}).find_all("div",{"class":"list_cell"}) # 추천탭있을때 
        # except IndexError:
        #     menu = soup.find("ul",{"class" : "prdList column4"}).find_all("li") # 없을때 
        #예외에 대한 처리 (샵마다 다름)
        for name in menu:
            try:
                c = name.find("ul")
                # print(menu)
            except AttributeError:
                print("할인없다")
                prprice = "0"   
                prpricebf = name.find_all("p",{"class" :"inblock dis"}) #할인전가격
            else:
                # print(c)
                prpricebf = c.find("s").get_text() #할인전가격
                prprice = name.find_all("p",{"class" :"inblock dis"}) #할인가격
                prprice = prprice.replace(",","")
            prpricebf = prpricebf.replace(",","")
                
            
            try:
                prpk = name.find("a").get("href")
                prpk = prpk.split("index_no=",1)[1].split("&cate",1)[0]
                primg = name.find("a").find("a").find("img").get("src")
                prname = name.find("li",{"class" : "item_name dsc_gray"}).get_text()
                prlink = name.find("a").get("href")
                prsoldout = name.find("li",{"class" : "icon_set"}).find("span").find("img").get(src)
                # http://cdn-naning9.bizhost.kr/files/icon/1471863163_0.gif
                # 전항목 수정 사항
            except AttributeError :
                print("에러를 포착했다")
                errmsg += basicurl+soncate+"태그에러발생\n"
                #리포팅작성

            except IndexError :
                print("인덱스에러")
            else:
                if primg == None:
                    print("태그없다")
                    errmsg += basicurl+soncate+"샵 구조 바뀐듯\n"
                else:
                    print(num,basicurl)
                    num += 1
                    # print(urljoin(basicurl,primg))
                    # print(prname)
                    # print(prpricebf)
                    # print(prprice)
                    # print(prpk[-4:])
                    crawl["prpk"].append(prpk)
                    crawl["primg"].append(primg)
                    crawl["prname"].append(prname)
                    crawl["prpricebf"].append(prpricebf)
                    crawl["prprice"].append(prprice)
                    if prsoldout == "http://cdn-naning9.bizhost.kr/files/icon/1471863163_0.gif":
                        crawl["prsoldout"].append(1)
                    else:
                        crawl["prsoldout"].append(0) # 0이 품절 x 1이 품절 ㅇ

                    crawl["prcate"].append(parentcate)
                    crawl["prsmcate"].append(soncate)
                    nexturl =  urljoin(basicurl,prlink)
                    crawl["prlink"].append(nexturl)
                    # nextfunc = _0001_intheshu.detaila
                    # nextfunc.detailscrapego(nextfunc,nexturl) # 다음으로 넘기기 협약시에 하고 아니면 닫아놓기
        i += 1

# 실행 for 구문
num = 0
for i,val in enumerate(category):
    # print(i)
    main(basicurl,val,indexcate[i])
    # time.sleep(1)

# db넣는 구문