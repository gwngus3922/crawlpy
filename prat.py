import requests
import os
from requests.compat import urljoin, quote_plus
from bs4 import BeautifulSoup
from celery import Celery

r = requests.get('http://intheshu.com/product/list.html?cate_no=24')
q = "http://intheshu.com/"
print(r.status_code)
html = r.text
soup = BeautifulSoup(html,'html.parser')

menu = soup.find_all("ul",{"class" : "prdList grid3"})[1].find_all("li")
# print(menu)
for name in menu:
    try:
        a = name.find("img",{"class" : "thumb"}).get("src")
        b = name.find("p",{"class" : "name"}).find("a").find_all("span")[1].get_text()
        c = name.find_all("li",{"class" :"xans-record-"})
        d = c[0].find_all("span")[1].get_text()
        e = c[1].find_all("span")[1].get_text()
        f = name.find("div",{"class" : "thumbnail"}).find("a",).get("href")
    except AttributeError as e:
        print("에러를 포착했다")
    else:
        if a == None:
            print("태그없다")
        else:
            print(a)
            print(b)
            print(d)
            print(e)
            print( urljoin(q,f))


            
