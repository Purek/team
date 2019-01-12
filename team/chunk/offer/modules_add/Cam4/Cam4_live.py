from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import random
import json



# site = 'http://www.cam4.com/female'    
def Cam4_live(submit):
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    ua = submit['ua']
    options.add_argument('user-agent="%s"' % ua)
    options.add_argument("--disable-infobars")
    chrome_driver = webdriver.Chrome(chrome_options=options)
    chrome_driver.get('http://www.cam4.com/female')
    with open('cookies\cookies_cam4\\'+submit['email']+".txt", 'r') as fp:
        cookies = json.load(fp)
        for cookie in cookies:
            chrome_driver.add_cookie(cookie)
    chrome_driver.get('http://www.cam4.com/female')

    try:
        chrome_driver.find_element_by_id('promotionsConsentModalLink').click()
        print('find no thanks')
    except:
        print('not find no thanks')
        
    randtime = random.randint(3,5)
    sleep(randtime)
    time_num =random.randint(3,6)
    for i in range(time_num):
        num = random.randint(1,20)
        try:
            chrome_driver.get('http://www.cam4.com/female')
            #directoryDiv > div:nth-child(7) > div > a.clearfix > img
            #directoryDiv > div:nth-child(16) > div > a.clearfix > img
            #chrome_driver.find_element_by_xpath('//*[@id="directoryDiv"]/div['+str(num)+']/div/a[2]').click()
            #chrome_driver.find_element_by_css_selector('directoryDiv > div:nth-child(16) > div > a.clearfix > img')
            a = '#directoryDiv > div:nth-child('+str(num)+') > div > a.clearfix > img'
            chrome_driver.find_element_by_css_selector(a).click()
            
            print('==================')
        except:
            chrome_driver.get('http://www.cam4.com/female')
            print('no vedio find')
        sleep_time = random.randint(1,3)
        sleep(sleep_time*60)
    return 1





if __name__=='__main__':
    submit={}
    submit['email'] = 'RobertThomasu@yahoo.com'
    submit['ua'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'
    Cam4_live(submit)
