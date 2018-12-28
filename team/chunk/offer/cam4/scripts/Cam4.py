import sys
sys.path.append("../..")
from modules_add.name_get import name_get as ng
from modules_add.ip_test import ip_test
from selenium import webdriver
from modules_add.email_check import Aol_check 
from modules_add.email_check import Gmail_check 
from modules_add.email_check import Yahoo_check 
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from datetime import date,datetime
import xlrd
from xlutils.copy import copy
from selenium.webdriver.common.by import By
from time import sleep
import re
import random
import os
import datetime

def web_Submit(submit): 
    # path='../driver'
    # executable_path=path
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    ua = submit['ua']
    # ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
    options.add_argument('user-agent="%s"' % ua)
    chrome_driver = webdriver.Chrome(chrome_options=options)
    print('preparing...')
    chrome_driver.implicitly_wait(10)  # 最长等待8秒
    print('getting site...')

    chrome_driver.get("http://click.prodailyfinance.com/click.php?c=1&key=02q01o3378537qrqy3s9clei")
    print('loading finished...')
    try:
        chrome_driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]").click()      #18+
    except:
        chrome_driver.close()
        chrome_driver.quit()
        return '',''
    chrome_driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[1]").click()      #question2
    chrome_driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]").click()      #question3
    chrome_driver.find_element_by_xpath("/html/body/div[1]/div[4]/span").click()            #create account

    sleep(3)
    chrome_driver.switch_to_frame('myForm')
    chrome_driver.find_element_by_xpath("//*[@id='userName']").send_keys(submit['name'])
    rantime = random.randint(3,5)
    sleep(rantime)   
    chrome_driver.find_element_by_xpath("//*[@id='newPassword']").send_keys(submit['pwd'])
    rantime = random.randint(3,5)
    sleep(rantime)   
    chrome_driver.find_element_by_xpath("//*[@id='email']").send_keys(submit['email'])
    sleep(3)
    try:
        chrome_driver.find_element_by_xpath("//*[@id='paymentForm']/a/span").click()
    except:
        chrome_driver.save_screenshot('../png/'+submit['name']+'.png')
        chrome_driver.close()
        chrome_driver.quit()
        print('form not ok')
        return 'fail',''
    # print(chrome_driver.page_source)
    status = 'fail'
    sleep(3)
    if chrome_driver.page_source.find('Please verify your email address to complete your registration') != -1:
        status = 'success'
        chrome_driver.close()
        chrome_driver.quit()
    else:
        chrome_driver.save_screenshot('../png/'+submit['name']+'.png')
        chrome_driver.close()
        chrome_driver.quit()
        # submit['name'] = ng.gen_one_word_digit(lowercase=False)
        # status,submit['name'] = web_Submit(submit)

    return status,submit['name']


#读取配置文件
path_excel = '..\config\c4mconfig.xlsx'
workbook = xlrd.open_workbook(path_excel)
sheet = workbook.sheet_by_index(0)
rows = sheet.nrows
print(rows)
i = 0
while i <= rows-1:
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))#现在
    if i != 0:
        rantime = random.randint(15,40)
        print('wait for %d minutes'%rantime)
        sleep(rantime*60)
    city,count = ip_test.ip_Test('')
    print('city:')
    print(city)
    print('annomonity:')
    print(count)
    workbook = xlrd.open_workbook(path_excel)
    sheet = workbook.sheet_by_index(0)
    submit = {}
    submit['name'] = ng.gen_one_word_digit(lowercase=False)
    submit['pwd'] = sheet.cell(i+1,1).value
    submit['email'] = sheet.cell(i+1,2).value
    submit['email_pwd'] = sheet.cell(i+1,3).value
    submit['email_assist'] = sheet.cell(i+1,4).value
    submit['ua'] = sheet.cell(i+1,5).value
    submit['site'] = sheet.cell(1,7).value
    submit['status'] = ''
    book2 = copy(workbook)
    sheet2 = book2.get_sheet(0)
    sheet2.write(i+1,0,submit['name'])
    try:
        print('...')
        submit['status'],submit['name'] = web_Submit(submit)
        if submit['name'] == '':
            break
        sheet2.write(i+1,0,submit['name'])
        if submit['status'] == 'success':
            flag = 0
            if 'aol.com' in submit['email']:
                try:
                    flag = Aol_check.Aol_Check(submit,'Cam4','Verify Your Account')
                except:
                    sheet2.write(i+1,6,'email check failed')
                if flag == 1:
                    print('success')
                    sheet2.write(i+1,6,'success')
                else:
                    print('emailcheck  failed')
                    sheet2.write(i+1,6,'email check failed')
            elif 'yahoo.com' in submit['email']:
                try:
                    flag = Yahoo_check.Yahoo_Check(submit,'Cam4','Verify Your Account')
                except:
                    sheet2.write(i+1,6,'email check failed')
                if flag == 1:
                    print('success')
                    sheet2.write(i+1,6,'success')
                else:
                    print('emailcheck  failed')
                    sheet2.write(i+1,6,'email check failed')
            elif 'gmail' in submit['email']:
                try:
                    flag = Gmail_check.Gmail_Check(submit,'Cam4','Verify Your Account')
                except:
                    sheet2.write(i+1,6,'email check failed')
                if flag == 1:
                    print('success')
                    sheet2.write(i+1,6,'success')
                else:
                    print('emailcheck  failed')
                    sheet2.write(i+1,6,'email check failed')
            else:
                print('this email not checked')
                sheet2.write(i+1,6,'email not in function')
        else:
            print('fail to register')
            sheet2.write(i+1,6,'register failed')
    except:
        print('failed')
        sheet2.write(i+1,6,'email commit failed')
    finally:
        book2.save('..\config\c4mconfig.xlsx')
        print('成功保存')
        i = i + 1


