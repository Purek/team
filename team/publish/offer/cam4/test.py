import xlrd
from xlutils.copy import copy
from name_get import name_get as ng
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from datetime import date,datetime
import xlrd
from xlutils.copy import copy
from selenium import webdriver
# from xlutils.copy import copy
from time import sleep
from name_get import name_get as ng
import re

# from winreg import *
# import http.client
# import subprocess
# import requests
# import random
# import xlrd
# import xlwt
# import sys
# import os
# path_excel = '../config/c4mconfig.xlsx'
# workbook = xlrd.open_workbook(path_excel)
# print(workbook.sheet_names())
# book2 = copy(workbook)
# sheet = book2.get_sheet(0)
# submit = ['name','pwd','email','ua','status']
# for i in range(4):
#     sheet.write(0,i,submit[i])

# print(ng.gen_one_word_digit(lowercase=False))

# book2.save('../config/c4mconfig.xlsx')

def ip_Test(): 
    path='../driver'
    executable_path=path
    options = webdriver.ChromeOptions()
    # ua = submit['ua']
    # ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
    # ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    # options.add_argument('user-agent="%s"' % ua)
    chrome_driver = webdriver.Chrome(chrome_options=options)
    print('preparing...')
    chrome_driver.implicitly_wait(10)  # 最长等待8秒
    print('getting site...')
    chrome_driver.get('https://whoer.net')
    str_1=chrome_driver.find_element_by_xpath("html/body/div/div/div/div[2]/div/div/div[2]/div/a/span").text)
    totalCount = int(re.sub("\D", "", str_1))
    if totalCount <= 90:
        return 0
    else:
        return 1
    chrome_driver.close()
    chrome_driver.quit()
    # return ''

# web_Submit()


str_1 = '您的匿名性: 64%'
totalCount = int(re.sub("\D", "", str_1))
print(totalCount)
print(type(totalCount))
