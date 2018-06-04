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
import global3

    
global3.test()
def httpconnect(crawl,shopname):
    mallpk = ""
    for i in global3.listshop:
                
        if i["MallName"] == shopname:
            print("발견!")
            mallpk = i["MallPK"]

    data = urllib.parse.urlencode(
        {
        'MallPK' : mallpk
        }
    ).encode("utf-8")
    req = urllib.request.Request("http://test.moamoa.co.kr/crawl/v1/check_shop.php" , data = data)
    resp = urllib.request.urlopen(req)
    try:
        pyt_dict = json.loads(resp.read().decode("utf-8").encode("utf-8").decode('unicode-escape'))
        print(crawl["prpk"])
        print(pyt_dict["Product_List"])
        for idx,i in enumerate(crawl["prpk"]):
            i = 1
            
            for j in pyt_dict["Product_List"]:

                if j["ProductID"] == i:
                    print(i["ProductID"])
                    print("성공")
                    data = urllib.parse.urlencode(
                    {
                        'MallPK' : mallpk,
                        'ProductID' : crawl["prpk"][idx],
                        'ProductName' : crawl["prname"][idx],
                        'ProductImage' : crawl["primg"][idx],
                        'ProductPrice' : crawl["prpricebf"][idx],
                        'ProductPricesale' : crawl["prprice"][idx],
                        'ProductCategory' : crawl["prcate"][idx],
                        'ProductSearch' : crawl["prsmcate"][idx],
                        'ProductUrl' : crawl["prlink"][idx],
                        'ProductOption' : crawl["proption"][idx],
                        'Producthtml' : crawl["html"][idx],
                        'ProductHighImage' : crawl["highimg"][idx]
                    }
                    ).encode("utf-8")
                    req = urllib.request.Request("http://test.moamoa.co.kr/crawl/v1/mall_product_detail_update.php" , data = data)
                    resp = urllib.request.urlopen(req)
                    i = 0
                    break
            if i == 1:
                print("인설트")
                print(idx)
                data = urllib.parse.urlencode(
                    {
                        'MallPK' : mallpk,
                        'ProductID' : crawl["prpk"][idx],
                        'ProductName' : crawl["prname"][idx],
                        'ProductImage' : crawl["primg"][idx],
                        'ProductPrice' : crawl["prpricebf"][idx],
                        'ProductPricesale' : crawl["prprice"][idx],
                        'ProductCategory' : crawl["prcate"][idx],
                        'ProductSearch' : crawl["prsmcate"][idx],
                        'ProductUrl' : crawl["prlink"][idx],
                        'ProductOption' : crawl["proption"][idx],
                        'Producthtml' : crawl["html"][idx],
                        'ProductHighImage' : crawl["highimg"][idx]
                    }
                    ).encode("utf-8")
                req = urllib.request.Request("http://test.moamoa.co.kr/crawl/v1/mall_product_detail_input.php" , data = data)
                resp = urllib.request.urlopen(req)
    except HTTPError as e:
        print(e.read())
        print("에러")