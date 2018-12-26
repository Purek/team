

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



def email_Check_Gmail(submit):
    path='../driver'
    executable_path=path
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    # ua = submit['ua']
    # ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
    # prefs = {"profile.managed_default_content_settings.images":2}
    # options.add_experimental_option("prefs",prefs)
    # options.add_argument('user-agent="%s"' % ua)
    chrome_driver = webdriver.Chrome(chrome_options=options)
    print('preparing...')
    chrome_driver.implicitly_wait(10)  # 最长等待8秒
    print('getting site...')
    chrome_driver.get("https://mail.google.com/")
    # chrome_driver.get("https://www.google.com")
    print('loading finished...')
    # 登陆
    chrome_driver.find_element_by_name('identifier').send_keys(submit['email'])
    chrome_driver.find_element_by_class_name('RveJvd').click()
    chrome_driver.find_element_by_name('password').send_keys(submit['email_pwd'])
    # chrome_driver.find_element_by_id('passwordNext').click()
    sleep(3)
    list1 = chrome_driver.find_elements_by_class_name('U26fgb')
    [a.click() for a in list1 if 'Next' in str(a.get_attribute('innerHTML'))]
    try:
        chrome_driver.find_element_by_class_name('TnvOCe').send_keys(Keys.ENTER)

    # 添加辅助邮箱地址
        chrome_driver.find_element_by_name('knowledgePreregisteredEmailResponse').send_keys(submit['email_assist'])
        chrome_driver.find_element_by_class_name('U26fgb').send_keys(Keys.ENTER)
        chrome_driver.find_element_by_class_name('U26fgb').send_keys(Keys.ENTER)
    except:
        print('no assistance needed')
    try:
        chrome_driver.find_element_by_name('welcome_dialog_next').click()
        chrome_driver.find_element_by_name('ok').click()
    except:
        print('no next')


    chrome_driver.find_element_by_css_selector('[data-tooltip = "Inbox"').click()
    list1 = chrome_driver.find_elements_by_tag_name('tr')
    try:
        [a.click() for a in list1 if "Cam4" in str(a.get_attribute('innerText'))]
        try:
            chrome_driver.find_element_by_link_text('Verify Your Account').click()
            rantime = random.randint(1,3)
            sleep(rantime*60)
            chrome_driver.close()
            chrome_driver.quit()
            return 1
        except:
            print('goto more')
            list2 = chrome_driver.find_elements_by_tag_name('span')
            try:
                [a.click() for a in list2 if "More" in str(a.get_attribute('innerText'))]
                print('we find more')
                sleep(5)
                try:
                    chrome_driver.find_element_by_css_selector('[data-tooltip = "Spam"').click()
                    print('we find spam')
                    sleep(5)
                    try:
                        list3 = chrome_driver.find_elements_by_tag_name('tr')
                        [a.click() for a in list3 if "Cam4" in str(a.get_attribute('innerText'))]
                        #sleep(20)
                        try:
                            list4 = chrome_driver.find_elements_by_tag_name('a')
                            print('aaaaaaaaaaaaa')
                            [a.click() for a in list4 if "Verify Your Account" in str(a.get_attribute('innerText'))]
                            print('bbbbbbbbbbbbbbb')
                            # chrome_driver.find_element_by_link_text('Verify Your Account').click()
                            print('ccccccccccccccc')
                            rantime = random.randint(2,6)
                            sleep(80*60)
                            chrome_driver.close()
                            chrome_driver.quit()
                            return 1
                        except:
                           
                            return 0
                    except:
                        return 0     
                except:
                    print('no spam')
                    return 0
            except:
                print('cant find more')
                return 0
    except:
        print('cam4 not received')
        return 0
    

submit={}
submit['email'] = 'Whyet.Christ@gmail.com'
submit['email_pwd'] = 'BVXHuNaNuipJvbW'
submit['email_assist'] = 'AlfredBen6@yahoo.com'
email_Check_Gmail(submit)