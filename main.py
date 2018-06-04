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
import global3
import sys
import inspect

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append("/home/ec2-user/Python-3.4.2/crawlpy")
print(os.path.dirname(global3.__file__))
nowpath = os.path.dirname(global3.__file__)
sys.path.insert(0, '.')
errmsg = ""

def test():
    
    index = 0
    for filename in os.listdir(nowpath+"/scrape_cafe24"):
        if index != 0 :
            t = multiprocessing.Process(target=go, args=(filename,))
            t.start()
        index += 1
    
    # s = multiprocessing.Process(target=report, args=()) # 리포트
    # s.start()

    # report()

    # res = await loop.run_in_executor(None,os.system,"python3 ./scrape/"+urls[idx])
    
def go(idx):
    msg = os.system("python3 ./scrape_cafe24/"+idx)
    # print(msg)
    print(idx)
    # print("오잉")
    # errmsg += msg

def report():
    global errmsg
    smtp = smtplib.SMTP('smtp.live.com', 587)
    smtp.ehlo()      # say Hello
    smtp.starttls()  # TLS 사용시 필요
    smtp.login('gwngus3922@outlook.com', 'shwn30708')
 
    msg = MIMEText(errmsg) # 내용
    msg['Subject'] = '크롤링 리포트'
    msg['To'] = 'gwngus3922@gmail.com' # 받는사람
    smtp.sendmail('gwngus3922@outlook.com','gwngus3922@gmail.com', msg.as_string())
 
    smtp.quit()



loop = asyncio.get_event_loop()
loop.run_until_complete(test())
loop.close()
