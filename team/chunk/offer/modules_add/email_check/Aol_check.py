from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from datetime import date,datetime
import xlrd
from xlutils.copy import copy
from selenium import webdriver
from selenium.webdriver.common.by import By
# from xlutils.copy import copy
from time import sleep
# from name_get import name_get as ng
import re
import os



def Aol_Check(submit,str_1,str_2):
    options = webdriver.ChromeOptions()
    # ua = submit['ua']
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
    prefs = {"profile.managed_default_content_settings.images":2}
    options.add_experimental_option("prefs",prefs)
    options.add_argument('user-agent="%s"' % ua)
    chrome_driver = webdriver.Chrome(chrome_options=options)
    print('preparing...')
    chrome_driver.implicitly_wait(10)  # 最长等待8秒
    print('getting site...')
    chrome_driver.get("https://login.aol.com/?.src=guce-mail&lang=&done=https%3A%2F%2Fmail.aol.com%2F")
    # chrome_driver.get("https://www.google.com")
    print('loading finished...')
    try:
        chrome_driver.find_element_by_id('login-username').send_keys(submit['email'])
        chrome_driver.find_element_by_id('login-signin').click()
        chrome_driver.find_element_by_id('login-passwd').send_keys(submit['email_pwd'])
        chrome_driver.find_element_by_id('login-signin').click()
        sleep(5)
    except:
        chrome_driver.close()
        chrome_driver.quit()
        return 0

    try: 
        chrome_driver.find_element_by_xpath('//*[@id="dijit__WidgetsInTemplateMixin_1"]/div/div[1]').click()
    except:
        print('no ads1')
    try:
        chrome_driver.find_element_by_xpath('//*[@id="dijit__WidgetsInTemplateMixin_2"]/div/div[1]').click()
    except:
        print('no ads2')
    
    try:
        chrome_driver.find_element_by_xpath('//*[@id="uniqName_4_4"]').click()
    except:
        print('no getstarted')
    # inbox里查找cam4
    try:
        chrome_driver.find_element_by_xpath('//*[@id="inboxNode"]').click()
        sleep(3)
        list1 = chrome_driver.find_elements_by_class_name("dojoxGrid-row")
        [a.click() for a in list1 if str_1 in str(a.get_attribute('innerHTML'))]
        try:
            chrome_driver.maximize_window()
            if chrome_driver.find_element_by_link_text(str_2):
                chrome_driver.find_element_by_link_text(str_2).click()
                sleep(15)
                chrome_driver.close()
                chrome_driver.quit()
                return 1
        except:
            print("can't find verify button")
            # spam
            try:
                chrome_driver.find_element_by_xpath('//*[@id="dijit__Widget_1"]/div[3]/div[4]/div/span').click()
                sleep(5)
                list3 = chrome_driver.find_elements_by_class_name("dojoxGrid-row")
                print(list3)
                [a.click() for a in list3 if str_1 in str(a.get_attribute('innerHTML'))]
            except:
                print('inbox not found')

            try:
                chrome_driver.maximize_window()
                if chrome_driver.find_element_by_link_text(str_2):
                    chrome_driver.find_element_by_link_text(str_2).click()
                    sleep(15)
                    chrome_driver.close()
                    chrome_driver.quit()
                    return 1
            except:
                print("can't find verify button")
                # sleep(5)
                chrome_driver.close()
                chrome_driver.quit()
                return 0
    except:
        print(' not found in inbox')
        # chrome_driver.close()
        # chrome_driver.quit()
        return 0
    



    # spam
    
if __name__=='__main__':
    submit={}
    submit['email'] = 'nicholas.buckle@aol.com'
    submit['email_pwd'] = 'WKwc9YBIJDd5ml593'
    Aol_Check(submit,'Cam4','Verify your account')