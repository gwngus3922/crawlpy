from selenium import webdriver
import time
import json
import smtplib
from email.mime.text import MIMEText
from collections import defaultdict

# driver = webdriver.Chrome('/Users/nohjuhyun/Downloads/chromedriver')
# driver.get("http://intheshu.com/product/detail.html?product_no=3521&cate_no=1&display_group=3")
# driver.implicitly_wait(2)
# # driver.execute_script("window.stop()")
# # time.sleep(3)
# # driver.execute_script("window.stop();")

# driver.find_element_by_xpath("//select[@option_sort_no='1']/option[text()='블랙(Black)']").click()
# driver.implicitly_wait(1)
# a = driver.find_elements_by_xpath("//select[@option_sort_no='2']//*")
# # print(a.text)
# for i in a:
#     print(i.text)

# driver.close()
def report():
    smtp = smtplib.SMTP('smtp.live.com', 587)
    smtp.ehlo()      # say Hello
    smtp.starttls()  # TLS 사용시 필요
    smtp.login('gwngus3922@outlook.com', 'shwn30708')
 
    msg = MIMEText('본문 테스트 메시지')
    msg['Subject'] = '크롤링 리포트'
    msg['To'] = 'gwngus3922@gmail.com'
    smtp.sendmail('gwngus3922@outlook.com','gwngus3922@gmail.com', msg.as_string())
 
    smtp.quit()

datew = defaultdict(list)
datew["aaa"].append("awd")
datew["aaa"].append("awd")
print(datew)
# report()