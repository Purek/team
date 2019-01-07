

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
import random
from modules_add.Cam4 import Cam4_reg as web_reg
import json

def writelog(runinfo,e=''):
    file=open(os.getcwd()+"\log.txt",'a+')
    file.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" : \n"+runinfo+"\n"+e+'\n')
    file.close()

def Gmail_Check(submit,str_1,str_2):
    writelog(submit['email']+'login start:')
    # path='../driver'
    # executable_path=path
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument("--disable-infobars")
    ua = submit['ua']
    options.add_argument('user-agent="%s"' % ua)
    chrome_driver = webdriver.Chrome(chrome_options=options)
    chrome_driver.implicitly_wait(20)  # 最长等待8秒
    chrome_driver.get("https://mail.google.com/")
    i = 0
    while i <=3:
        try:
            chrome_driver.find_element_by_name('identifier').send_keys(submit['email'])
            break
        except Exception as e:
            chrome_driver.get("https://mail.google.com/")
            sleep(5)
            i = i + 1   
    # chrome_driver.get("https://www.google.com")
    print('loading finished...')
    # 登陆
    try:
        chrome_driver.find_element_by_class_name('RveJvd').click()
    except Exception as e:
        writelog('mail.google.com login failed',str(e))
        chrome_driver.close()
        chrome_driver.quit()
        return 0
    try:
        chrome_driver.find_element_by_name('password').send_keys(submit['email_pwd'])
    except Exception as e:
        writelog('mail.google.com login failed',str(e))
        chrome_driver.close()
        chrome_driver.quit()
        return 0        
    # chrome_driver.find_element_by_id('passwordNext').click()
    sleep(3)
    try:
        list1 = chrome_driver.find_elements_by_class_name('U26fgb')
        [a.click() for a in list1 if 'Next' in str(a.get_attribute('innerHTML'))]
    except Exception as e:
        print('No next.....')
    try:
        chrome_driver.find_element_by_class_name('TnvOCe').send_keys(Keys.ENTER)

    # 添加辅助邮箱地址
        chrome_driver.find_element_by_name('knowledgePreregisteredEmailResponse').send_keys(submit['email_assist'])
        chrome_driver.find_element_by_class_name('U26fgb').send_keys(Keys.ENTER)
        chrome_driver.find_element_by_class_name('U26fgb').send_keys(Keys.ENTER)
    except Exception as e:
        print('no assistance needed')
    
    writelog('mail.aol.com login successed')
    cookies = chrome_driver.get_cookies()
    print(cookies)
    try:
        with open('cookies\cookies_email\\gmail\\'+submit['email']+".txt",'w') as fp:
            json.dump(cookies, fp) 
    except Exception as e:
        print(str(e))
    try:
        flag = web_reg.web_Submit(submit)
        if flag == 0:
            writelog('register failed')
            chrome_driver.close()
            chrome_driver.quit()
            return 1
        else:
            writelog('register success')
    except Exception as e:
        writelog('register failed with error:',str(e))
        chrome_driver.close()
        chrome_driver.quit()
        return 1
    # sleep(5*60)
    # chrome_driver.refresh()
    try:
        chrome_driver.find_element_by_name('welcome_dialog_next').click()
        chrome_driver.find_element_by_name('ok').click()
    except Exception as e:
        print('no next')

    try:
        chrome_driver.find_element_by_css_selector('[data-tooltip = "Inbox"').click()   
    except Exception as e:
        print('ok')
    try:
        list1 = chrome_driver.find_elements_by_tag_name('tr')
        [a.click() for a in list1 if str_1 in str(a.get_attribute('innerText'))]
        sleep(10)
        try:
            chrome_driver.find_element_by_link_text(str_2).click()
            rantime = random.randint(2,5)
            sleep(rantime*60)
            #add logic,save cookies to floder cookies
            chrome_driver.get("http://www.cam4.com/female")
            sleep(10)
            cookies = chrome_driver.get_cookies()
            print(cookies)
            with open('cookies\cookies_cam4\\'+submit['email']+".txt",'w') as fp:
                json.dump(cookies, fp) 
            chrome_driver.close()
            chrome_driver.quit()
            return 2
        except Exception as e:
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
                        [a.click() for a in list3 if str_1 in str(a.get_attribute('innerText'))]
                        sleep(10)
                        try:
                            list4 = chrome_driver.find_elements_by_tag_name('a')
                            print('aaaaaaaaaaaaa')
                            [a.click() for a in list4 if str_2 in str(a.get_attribute('innerText'))]
                            print('bbbbbbbbbbbbbbb')
                            # chrome_driver.find_element_by_link_text(str_2).click()
                            print('ccccccccccccccc')
                            rantime = random.randint(2,5)
                            sleep(rantime*60)
                            #add logic,save cookies to floder cookies
                            chrome_driver.get("http://www.cam4.com/female")
                            sleep(10)
                            cookies = chrome_driver.get_cookies()
                            print(cookies)
                            with open('cookies\cookies_cam4\\'+submit['email']+".txt",'w') as fp:
                                json.dump(cookies, fp)                             
                            chrome_driver.close()
                            chrome_driver.quit()
                            return 2
                        except Exception as e:
                            writelog('verify failed with error:',str(e))
                            chrome_driver.close()
                            chrome_driver.quit()
                            return 1
                    except Exception as e:
                        chrome_driver.close()
                        chrome_driver.quit()
                        return 1     
                except Exception as e:
                    print('no spam')
                    chrome_driver.close()
                    chrome_driver.quit()
                    return 1
            except Exception as e:
                print('cant find more')
                chrome_driver.close()
                chrome_driver.quit()
                return 1
    except Exception as e:
        print('cam4 not received')
        chrome_driver.close()
        chrome_driver.quit()
        return 1
    

if __name__=='__main__':
    submit={}
    submit['email'] = 'Whyet.Christ@gmail.com'
    submit['email_pwd'] = 'BVXHuNaNuipJvbW'
    submit['email_assist'] = 'AlfredBen6@yahoo.com'
    Gmail_Check(submit,'Cam4','Verify Your Account')
