import sys
sys.path.append("../..")
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
from modules_add.name_get import name_get as ng
import time
import json


def writelog(runinfo,e=''):
    file=open(os.getcwd()+"\log.txt",'a+')
    file.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" : \n"+runinfo+"\n"+e+'\n')
    file.close()



def Aol_Check(submit,str_1,str_2):
    writelog(submit['email']+'login start:')
#return 0means login failed ,1 means login successed but verify failed,2 means verify success
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    ua = submit['ua']
    options.add_argument('user-agent="%s"' % ua)
    options.add_argument("--disable-infobars")
    chrome_driver = webdriver.Chrome(chrome_options=options)
    chrome_driver.implicitly_wait(20)  # 最长等待8秒
    chrome_driver.get("https://login.aol.com")
    i = 0
    while i <=3:
        try:
            chrome_driver.find_element_by_id('login-username').send_keys(submit['email'])
            break
        except Exception as e:
            writelog('accessing aol.com',str(e))
            chrome_driver.get("https://login.aol.com")
            sleep(5)
            i = i + 1  
    try:
        chrome_driver.find_element_by_id('login-signin').click()
        sleep(3)
        chrome_driver.find_element_by_id('login-passwd').send_keys(submit['email_pwd'])
        sleep(5)
        chrome_driver.find_element_by_id('login-signin').click()
        sleep(5)
    except Exception as e:
        writelog('aol.com login failed',str(e))
        chrome_driver.close()
        chrome_driver.quit()
        return 0
    cookies = chrome_driver.get_cookies()
    try:
        with open('cookies\cookies_email\\aol\\'+submit['email']+".txt",'w') as fp:
            json.dump(cookies, fp) 
    except Exception as e:
        print(str(e))
    try:
        chrome_driver.find_element_by_css_selector('#mod-mail-preview-1 > div.navicon.navicon-mail').click()
        #chrome_driver.find_element_by_xpath('//*[@id="navigation-menu-channels"]/div/ul/li[2]/a')
    except Exception as e:
        writelog('mail.aol.com login failed',str(e))
        print('into aol main,can not find mail entrency with css_selector')
        chrome_driver.close()
        chrome_driver.quit()
        return 0
    j = 0
    while chrome_driver.page_source.find('This site can’t be reached')!=-1:
        chrome_driver.refresh()
        j += 1
        if j >= 3:
            break
   
    #这里还要再加个判断，用title,这步之后返回都是1和2
    writelog('mail.aol.com login successed')

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
    #sleep(3*60)  
    chrome_driver.refresh()   
    try: 
        chrome_driver.find_element_by_xpath('//*[@id="mod-mail-preview-1"]/div[2]').click()
    except Exception as e:
        print('no ads1')
    try:
        chrome_driver.find_element_by_xpath('//*[@id="dijit__WidgetsInTemplateMixin_2"]/div/div[1]').click()
    except Exception as e:
        print('no ads2')
    
    try:
        chrome_driver.find_element_by_xpath('//*[@id="uniqName_4_4"]').click()
    except Exception as e:
        print('no getstarted')
    # inbox里查找cam4
    try:
        chrome_driver.find_element_by_xpath('//*[@id="inboxNode"]').click()
        sleep(3)
        list1 = chrome_driver.find_elements_by_class_name("dojoxGrid-row")
        [a.click() for a in list1 if str_1 in str(a.get_attribute('innerHTML'))]
        try:
            # chrome_driver.maximize_window()
            sleep(5)
            if chrome_driver.find_element_by_link_text(str_2):
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
            print("can't find verify button")
            # spam
            try:
                chrome_driver.find_element_by_xpath('//*[@id="dijit__Widget_1"]/div[3]/div[4]/div/span').click()
                sleep(5)
                list3 = chrome_driver.find_elements_by_class_name("dojoxGrid-row")
                print(list3)
                [a.click() for a in list3 if str_1 in str(a.get_attribute('innerHTML'))]
            except Exception as e:
                print('inbox not found')

            try:
                # chrome_driver.maximize_window()
                sleep(5)
                if chrome_driver.find_element_by_link_text(str_2):
                    chrome_driver.find_element_by_link_text(str_2).click()
                    rantime = random.randint(2,5)
                    sleep(rantime*60)  
                    chrome_driver.get("http://www.cam4.com/female")
                    sleep(10)
                    cookies = chrome_driver.get_cookies()
                    print(cookies)
                    with open('cookies\cookies_cam4\\'+submit['email']+".txt", 'w') as fp:
                        json.dump(cookies, fp) 
                    chrome_driver.close()
                    chrome_driver.quit()
                    return 2
            except Exception as e:
                print("can't find verify button")
                chrome_driver.save_screenshot(submit['name']+'.png')
                # sleep(5)
                chrome_driver.close()
                chrome_driver.quit()
                return 1
    except Exception as e:
        print(' not found in inbox')
        chrome_driver.save_screenshot(submit['name']+'.png')
        chrome_driver.close()
        chrome_driver.quit()
        return 1
    



    # spam
    
if __name__=='__main__':
    submit={}
    submit['name'] = ng.gen_one_word_digit(lowercase=False)
    submit['pwd'] = 'AOmOCA5x'
    submit['ua'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    submit['email'] = 'MelissaWilkinsonw@aol.com'
    submit['email_pwd'] = 'AOmOCA5x'
    Aol_Check(submit,'Cam4','Verify your account')
