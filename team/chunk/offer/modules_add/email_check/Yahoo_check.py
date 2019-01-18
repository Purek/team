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
import time
from modules_add.Cam4 import Cam4_reg as web_reg
import json

def writelog(runinfo,e=''):
    file=open(os.getcwd()+"\log.txt",'a+')
    file.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" : \n"+runinfo+"\n"+e+'\n')
    file.close()

def Yahoo_Check(submit,str_1,str_2):
    writelog(submit['email']+'login start:')
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')

    # rows = len(ua)
    ua = submit['ua']
    options.add_argument('user-agent="%s"' % ua)
    options.add_argument("--disable-infobars")
    chrome_driver = webdriver.Chrome(chrome_options=options)
    chrome_driver.implicitly_wait(20)  # 最长等待8秒
    i = 0
    while i <=3:
        print(i)
        if chrome_driver.title != 'Yahoo':
            print(chrome_driver.title)
            chrome_driver.get('https://www.yahoo.com/')
            i = i + 1
        else:
            print(chrome_driver.title)
            sleep(3)
            break

    # sleep(1000) 
    try:
        if chrome_driver.title != 'Yahoo':
            chrome_driver.close()
            chrome_driver.quit()
            return 0
        #sleep(500)
        chrome_driver.find_element_by_id('uh-signin').click()
        print('click singin ok')
    except:
        chrome_driver.close()
        chrome_driver.quit()
        return 0
        print('cannot find singin by id')

    j = 0
    while chrome_driver.page_source.find('This site can’t be reached')!=-1:
        chrome_driver.refresh()
        j += 1
        if j >= 3:
            break
   
    if chrome_driver.page_source.find('This site can’t be reached')!=-1:
        chrome_driver.close()
        chrome_driver.quit()
        return 0  


    # 登陆
    chrome_driver.find_element_by_id('login-username').send_keys(submit['email'])
    try:
        sleep(3)
        chrome_driver.find_element_by_id('login-signin').click()
    except:
        print('login name failed')
        chrome_driver.close()
        chrome_driver.quit()
        return 0

    sleep(2)
    try:
        chrome_driver.find_element_by_id('login-passwd').send_keys(submit['email_pwd'])
    except:
        print('login pwd failed')
    sleep(2)
    chrome_driver.find_element_by_id('login-signin').click()
    sleep(5)

    j = 0
    while chrome_driver.page_source.find('This site can’t be reached')!=-1:
        chrome_driver.refresh()
        j += 1
        if j >= 3:
            break
   
    if chrome_driver.page_source.find('This site can’t be reached')!=-1:
        chrome_driver.close()
        chrome_driver.quit()
        return 0  


    # save cookies
    cookies = chrome_driver.get_cookies()
    print(cookies)
    try:
        with open('cookies\cookies_email\\yahoo\\'+submit['email']+".txt",'w') as fp:
            json.dump(cookies, fp) 
    except Exception as e:
        print(str(e))

    try:
        chrome_driver.find_element_by_css_selector('#uh-mail-link > i').click()
    except:
        chrome_driver.close()
        chrome_driver.quit()
        return 0
        print('into mail from main failed')
    if 'overview' in chrome_driver.current_url:
        chrome_driver.close()
        chrome_driver.quit()
        writelog('overview.mail.yahoo.com')
        return -1

    j = 0
    while chrome_driver.page_source.find('This site can’t be reached')!=-1:
        chrome_driver.refresh()
        j += 1
        if j >= 3:
            break
   
    if chrome_driver.page_source.find('This site can’t be reached')!=-1:
        chrome_driver.close()
        chrome_driver.quit()
        return 0   


    writelog('mail.yahoo.com login successed')


# login success
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
    #sleep(1*60)
    # chrome_driver.refresh()
    try:
        list0 = chrome_driver.find_elements_by_tag_name("button")
        [a.click() for a in list0 if "Done" in str(a.get_attribute('innerText'))]
    except:
        print('meiyou done biaoqian')
    
    try:
        list1 = chrome_driver.find_elements_by_tag_name("a")
        [a.click() for a in list1 if str_1 in str(a.get_attribute('innerHTML'))]
    except:
        print('........not found')
    try:
        # chrome_driver.maximize_window()
        if chrome_driver.find_element_by_link_text(str_2):
            chrome_driver.find_element_by_link_text(str_2).click()
            rantime = random.randint(3,5)
            sleep(rantime*60)
            #add logic,save cookies to floder cookies
            chrome_driver.get("http://www.cam4.com/female")
            sleep(10)
            j = 0
            while chrome_driver.page_source.find('This site can’t be reached')!=-1:
                chrome_driver.refresh()
                j += 1
                if j > 3:
                    break            
            if chrome_driver.page_source.find('This site can’t be reached')==-1:                
                cookies = chrome_driver.get_cookies()
                print(cookies)
                with open('cookies\cookies_cam4\\'+submit['email']+".txt",'w') as fp:
                    json.dump(cookies, fp) 
            chrome_driver.close()
            chrome_driver.quit()
            return 3
    except:
        print("can't find verify button")
        # spam
        try:
            try:
                list_more = chrome_driver.find_elements_by_tag_name('li')
                [a.click() for a in list_more if 'More' in str(a.get_attribute('innerText'))]
                print('clicking more')
                #chrome_driver.find_element_by_link_text('More').click()
            except:
                print('can not find more')
            try:
                sleep(5)
                chrome_driver.find_element_by_link_text('Spam').click()
                print('clicking spam')
            except:
                print('cannot find spam')

            sleep(10)
            list3 = chrome_driver.find_elements_by_class_name("o_h")
            try:
                [a.click() for a in list3 if str_1 in str(a.get_attribute('innerText'))]
                print('not  sure if find cam4')
            except:
                print('cam4 not find')
            try:
                # chrome_driver.maximize_window()
                if chrome_driver.find_element_by_link_text(str_2):
                    print('yes we find cam4 and we are clicking verify')
                    chrome_driver.find_element_by_link_text(str_2).click()
                    rantime = random.randint(3,5)
                    sleep(rantime*60)
                    #add logic,save cookies to floder cookies
                    chrome_driver.get("http://www.cam4.com/female")
                    sleep(10)
                    j = 0
                    while chrome_driver.page_source.find('This site can’t be reached')!=-1:
                        chrome_driver.refresh()
                        j += 1
                        if j > 3:
                            break
                    if chrome_driver.page_source.find('This site can’t be reached')==-1:                
                        cookies = chrome_driver.get_cookies()
                        print(cookies)
                        with open('cookies\cookies_cam4\\'+submit['email']+".txt",'w') as fp:
                            json.dump(cookies, fp)                     
                    chrome_driver.close()
                    chrome_driver.quit()
                    return 3
            except:
                print("can't find verify button")
                chrome_driver.save_screenshot(submit['name']+'.png')
                # sleep(5)
                chrome_driver.close()
                chrome_driver.quit()
                return 2
        except:
            print('inbox not found')
            chrome_driver.save_screenshot(submit['name']+'.png')
            chrome_driver.close()
            chrome_driver.quit()
            return 2



if __name__=='__main__':
    submit={}
    submit['name'] = 'coco'
    submit['email'] = 'JaneWintere@yahoo.com'
    submit['email_pwd'] = 'Ge7D8sem'
    # submit['ua'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'
    Yahoo_Check(submit,'Cam4','Verify Your Account')
