from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import random
import json



# site = 'http://www.cam4.com/female'    
def AOl_login(submit):
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    ua = submit['ua']
    options.add_argument('user-agent="%s"' % ua)
    options.add_argument("--disable-infobars")
    chrome_driver = webdriver.Chrome(chrome_options=options)
    chrome_driver.get('http://login.aol.com')
    with open('cookies\cookies_cam4\\'+submit['email']+".txt", 'r') as fp:
        cookies = json.load(fp)
        for cookie in cookies:
            chrome_driver.add_cookie(cookie)
    chrome_driver.get('http://login.aol.com')


if __name__=='__main__':
    # need to be loaded on 'cam4\scripts\\' floder to read cookies
    submit={}
    submit['email'] = ''
    submit['ua'] = ''
    AOl_login(submit)