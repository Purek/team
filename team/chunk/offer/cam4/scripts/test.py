from selenium import webdriver
from time import sleep
import json
import sys
sys.path.append("../..")

# def test(submit):
#     options = webdriver.ChromeOptions()
#     options.add_argument('--incognito')
#     ua = submit['ua']
#     options.add_argument('user-agent="%s"' % ua)
#     options.add_argument("--disable-infobars")
#     chrome_driver = webdriver.Chrome(chrome_options=options)
#     chrome_driver.get("https://www.baidu.com")
#     # sleep(10*60)
#     cookies = chrome_driver.get_cookies()
#     print(cookies)
#     with open("cookies/aol@hotmail.txt", 'w') as fp:
#         json.dump(cookies, fp)

# submit={}
# submit['ua'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
# test(submit)
import json
import os
import random



# with open('cookies\\'+"aol@hotmail.txt", 'r') as fp:
#     cookies = json.load(fp)
num = random.randint(1,20)
a = '//*[@id="directoryDiv"]/div['+str(num)+']/div/a[2]'
print(a)

# print(cookies)
# with open('cookies\cookies_email\\'+"1.com.txt", 'w') as fp:
#     json.dump(cookies, fp) 

# dir1 = os.path.abspath('')
# dir2 = dir1 + '\cookies_email\\aol\\'
# with open(dir2+"1.com.txt", 'w') as fp:
#     json.dump(cookies, fp) 
