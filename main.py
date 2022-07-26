from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import time,random
import requests
import json
import pickle
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

db_settings = {
    "host": os.getenv("dbip"),
    "port": int(os.getenv("dbport")),
    "user": os.getenv("dbuser"),
    "password": os.getenv("dbpassword"),
    "charset": "utf8"
}
conn = pymysql.connect(**db_settings)
cursor = conn.cursor()

cursor.execute("create database if not exists exam3_2;")
cursor.execute("drop table if exists exam3_2.exam3_2;")
cursor.execute("create table exam3_2.exam3_2(no serial,sentence varchar(500));")
conn.commit()

ua = UserAgent(path='/home/jeff/.local/lib/python3.8/site-packages/fake_useragent/fake_useragent.json')    
option = Options() 
option.add_argument("--headless")
option.add_argument("user-agent=" + ua.random)
option.add_argument("--no-sandbox")
option.add_argument("--disable-gpu")
#option.add_argument("--disable-javascript")
option.add_argument("--disable-extensions")
option.add_argument("--disable-browser-side-navigation")
option.add_argument("--disable-dev-shm-usage")
option.add_argument("--disable-infobars")
option.add_argument("blink-settings=imagesEnabled=false")
option.add_argument("--ignore-certificate-errors") 
option.add_argument("--disable-site-isolation-trials")
#option.add_argument('--proxy-server={}'.format('118.163.13.200:8080'))
#preferences = {
#    "webrtc.ip_handling_policy": "disable_non_proxied_udp",
#    "webrtc.multiple_routes_enabled": False,
#    "webrtc.nonproxied_udp_enabled": False
#}
#option.add_experimental_option("prefs", preferences)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
driver.implicitly_wait(10)

ft = open("exam3_1.txt","w",encoding='UTF-8')
fp = open('exam3_3.pickle','wb')
try:
    for p in range(1,199):
        url = "https://gogakuru.com/english/phrase/genre/180_%E5%88%9D%E7%B4%9A%E3%83%AC%E3%83%99%E3%83%AB.html?pageID={}&layoutPhrase=1&orderPhrase=1&condMovie=0&perPage=50&flow=enSearchGenre&condGenre=180".format(p)
        
        driver.get(url)
        t= driver.find_elements(by=By.CSS_SELECTOR, value="#cmain > form > div > div.list_wrapper table tr td.summary ")
        for i in t:
            ft.write(i.text+"\n")
 
            cursor.execute("insert exam3_2.exam3_2(sentence) values(%s);",i.text)
            conn.commit()
            
            pickle.dump(i.text,fp)
        
        time.sleep(random.uniform(7, 10))
        driver.implicitly_wait(5)
except Exception as message:
    ft.close()
    print("txt closed")
    conn.close()
    print("db closed")
    fp.close()
    print("pickle closed")
    driver.quit()
    print("driver closed")
    print("------GG------")
    print(message)

else:
    ft.close()
    print("txt closed")
    conn.close()
    print("db closed")
    fp.close()
    print("pickle closed")
    driver.quit()
    print("driver closed")
    print("completed")
    
    
