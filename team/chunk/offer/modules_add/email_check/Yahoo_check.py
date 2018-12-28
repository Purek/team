

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



def Yahoo_Check(submit,str_1,str_2):
    # path='../driver'
    # executable_path=path
    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    options.add_experimental_option("prefs",prefs)
    chrome_driver = webdriver.Chrome(chrome_options=options)
    print('preparing...')
    chrome_driver.implicitly_wait(10)  # 最长等待8秒
    print('getting site...')
    chrome_driver.get("https://login.yahoo.com/?.src=ym&lang=&done=https%3A%2F%2Fmail.yahoo.com%2F")
    # chrome_driver.get("https://www.google.com")
    print('loading finished...')
    # 登陆

    chrome_driver.find_element_by_id('login-username').send_keys(submit['email'])

    chrome_driver.find_element_by_id('login-signin').click()
    chrome_driver.find_element_by_id('login-passwd').send_keys(submit['email_pwd'])
    chrome_driver.find_element_by_id('login-signin').click()
    sleep(5)

    list1 = chrome_driver.find_elements_by_class_name("o_h")
    try:
        [a.click() for a in list1 if "Cam4" in str(a.get_attribute('innerHTML'))]
    except:
        print('........')
    try:
        chrome_driver.maximize_window()
        if chrome_driver.find_element_by_link_text('Verify Your Account'):
            chrome_driver.find_element_by_link_text('Verify Your Account').click()
            sleep(15)
            chrome_driver.close()
            chrome_driver.quit()
            return 1
    except:
        print("can't find verify button")
        # spam
        try:
            chrome_driver.find_elements_by_class_name("D_F")
            sleep(5)
            list3 = chrome_driver.find_elements_by_class_name("o_h")
            print(list3)
            try:
                [a.click() for a in list3 if "Cam4" in str(a.get_attribute('innerHTML'))]
            except:
                print('===========')
            try:
                chrome_driver.maximize_window()
                if chrome_driver.find_element_by_link_text('Verify Your Account'):
                    chrome_driver.find_element_by_link_text('Verify Your Account').click()
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
            print('inbox not found')
            chrome_driver.close()
            chrome_driver.quit()
            return 0
if __name__=='__main__':
    submit={}
    submit['email'] = 'doyle.cornelia@yahoo.com'
    submit['email_pwd'] = 'TemOvDwxzU64'
    Yahoo_Check(submit,'Cam4','Verify Your Account')