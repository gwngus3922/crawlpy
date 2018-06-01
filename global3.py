import asyncio
import os
import threading
import multiprocessing
import smtplib
from email.mime.text import MIMEText
import urllib
import json
import urllib.error
from urllib.parse import urlencode
import urllib.parse
from urllib import request
from urllib.error import HTTPError
import urllib3
import json

errmsg = ""
listshop = []
def test():
    global errmsg
    global listshop
    req = urllib.request.Request("http://test.moamoa.co.kr/crawl/v1/shop_list.php")
    resp = urllib.request.urlopen(req)
    try:
        pyt_dict = json.loads(resp.read().decode("utf-8").encode("utf-8").decode('unicode-escape'))
        listshop = pyt_dict["Shop_List"]
        # print(pyt_dict["Shop_List"])
    except HTTPError as e:
        print(e.read())
        print("에러")

    
