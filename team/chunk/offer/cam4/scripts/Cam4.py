import xlrd
from xlutils.copy import copy
from time import sleep
import random
import datetime
from selenium import webdriver
import sys
sys.path.append("../..")
from modules_add.name_get import name_get as ng
import os
import time
from modules_add.ip_test import ip_test
from modules_add.email_check import Aol_check 
from modules_add.email_check import Gmail_check 
from modules_add.email_check import Yahoo_check 
import json





# path_excel = '..\config\c4mconfig.xlsx'
# workbook = xlrd.open_workbook(path_excel)
# sheet = workbook.sheet_by_index(0)
# rows = sheet.nrows
# print(rows)
# submit={}
# # for i in range(9):
# i=-1
#     # submit['name'] = ng.gen_one_word_digit(lowercase=False)
# submit['pwd'] = sheet.cell(i+1,1).value
# submit['email'] = sheet.cell(i+1,2).value
# submit['email_pwd'] = sheet.cell(i+1,3).value
# submit['email_assist'] = sheet.cell(i+1,4).value
# submit['ua'] = sheet.cell(i+1,5).value
# submit['status'] = ''
# print(submit)
# print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))#现在

# rantime = random.randint(15,40)
# print('wait for %d minutes'%rantime)
# sleep(rantime)
def writelog(runinfo,e=''):
    file=open(os.getcwd()+"\log.txt",'a+')
    file.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" : \n"+runinfo+"\n"+e+'\n')
    file.close()


def submit_Dict(submit1):
    submit = {}
    submit['name'] = ng.gen_one_word_digit(lowercase=False)
    submit['pwd'] = submit1[1]
    submit['email'] = submit1[2]
    submit['email_pwd'] = submit1[3]
    submit['email_assist'] = submit1[4]
    submit['ua'] = submit1[5]
    submit['status'] = submit1[6]
    submit['city'] = submit1[7]
    return submit



# choose a mail from excel,
def choose_Mail():
    path_excel = '..\config\c4mconfig.xlsx'
    workbook = xlrd.open_workbook(path_excel)
    sheet = workbook.sheet_by_index(0)
    rows = sheet.nrows
    print(rows)
    list_rows = random.sample(range(rows),rows)
    print(list_rows)
    # site = sheet.cell(1,8).value
    site = 'www.baidu.com'
    print(site)
    # submit = {}
    #every five times not access to email,chang ip,record with flag_ip
    #everytime chang ip,reset flag_ip
    flag = 0
    city,count = ip_test.ip_Test('')
    if count == -1:
        writelog('911 wrong for 4 times')
        return
    print('==================')
    flag_ip = 0
    for i in list_rows:
        print(i)
        if flag_ip >= 3:
            city,count = ip_test.ip_Test('')
            if count == -1:
                writelog('911 wrong for 4 times')
                return
            flag_ip = 0
        workbook = xlrd.open_workbook(path_excel)
        sheet = workbook.sheet_by_index(0)
        book2 = copy(workbook)
        sheet2 = book2.get_sheet(0)
        if sheet.cell(i,0).value != '':
            continue 
        submit1 = sheet.row_values(i)
        try:
            submit = submit_Dict(submit1)
        except:
            print('submit get wrong')
        if 'aol.com' in submit['email']:
            print('aol')
            try:
                # if login fail,change email
                flag = Aol_check.Aol_Check(submit,'Cam4','Verify Your Account')
                print(flag)
                if flag == 0:
                    sheet2.write(i,6,'email login failed')
                    flag_ip = flag_ip + 1
                elif flag == 1:
                    sheet2.write(i,6,'register failed')
                elif flag == 2:
                    sheet2.write(i,6,'verify failed')
                    flag_ip = 10
                    sheet2.write(i,0,'bad email')
                else:
                    sheet2.write(i,6,'success')
                    sheet2.write(i,7,city)
                    sheet2.write(i,0,submit['name'])
                    rantime = random.randint(20,30)
                    print('sleep for %d minutes'%rantime)
                    print('==================')                
                    sleep(rantime*60)
                    city,count = ip_test.ip_Test('')
                    if count == -1:
                        writelog('911 wrong for 4 times')
                        return    
                    flag_ip = 0
                book2.save('..\config\c4mconfig.xlsx')
            except Exception as e:
                sheet2.write(i,6,'login failed or registerd')
                writelog('aol login error',str(e))   
                book2.save('..\config\c4mconfig.xlsx')  
        elif 'yahoo.com' in submit['email']:
            print('yahoo')
            submit['ua'] = get_ua_yahoo() 
            try:
                # if login fail,change email
                flag = Yahoo_check.Yahoo_Check(submit,'Cam4','Verify Your Account')
                print(flag)
                if flag == 0:
                    sheet2.write(i,6,'email login failed')
                    flag_ip = flag_ip + 1
                elif flag == 1:
                    sheet2.write(i,6,'register failed')
                elif flag == 2:
                    sheet2.write(i,6,'verify failed')
                    flag_ip = 10
                    sheet2.write(i,0,'bad email')
                elif flag == 3:
                    sheet2.write(i,6,'success')
                    sheet2.write(i,7,city)
                    sheet2.write(i,0,submit['name'])
                    sheet2.write(i,5,submit['ua'])
                    rantime = random.randint(20,30)
                    print('sleep for %d minutes'%rantime)
                    print('==================')                
                    sleep(rantime*60)
                    city,count = ip_test.ip_Test('')
                    if count == -1:
                        writelog('911 wrong for 4 times')
                        return                
                    flag_ip = 0
                else:
                    sheet2.write(i,6,'overview yahoo')
                    sheet2.write(i,0,'bademail')
                book2.save('..\config\c4mconfig.xlsx')
            except Exception as e:
                sheet2.write(i,6,'login failed')
                writelog('yahoo login error',str(e)) 
                book2.save('..\config\c4mconfig.xlsx')    
        elif 'gmail' in submit['email']:
            print('gmail')
            try:
                # if login fail,change email
                flag = Gmail_check.Gmail_Check(submit,'Cam4','Verify Your Account')
                print(flag)
                if flag == 0:
                    sheet2.write(i,6,'email login failed')
                    flag_ip = flag_ip + 1
                elif flag == 1:
                    sheet2.write(i,6,'register failed')
                elif flag == 2:
                    sheet2.write(i,6,'verify failed')
                    flag_ip = 10
                    sheet2.write(i,0,'bad email')
                else:
                    sheet2.write(i,6,'success')
                    sheet2.write(i,7,city)
                    sheet2.write(i,0,submit['name'])
                    rantime = random.randint(20,30)
                    print('sleep for %d minutes'%rantime)
                    print('==================')                
                    sleep(rantime*60)
                    city,count = ip_test.ip_Test('')
                    if count == -1:
                        writelog('911 wrong for 4 times')
                        book2.save('..\config\c4mconfig.xlsx')
                        return                    
                    flag_ip = 0
                book2.save('..\config\c4mconfig.xlsx')
            except Exception as e:
                sheet2.write(i,6,'login failed')
                writelog('gmail login error',str(e))   
                book2.save('..\config\c4mconfig.xlsx')              



def get_ua_yahoo():
    ua = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 OPR/56.0.3051.116',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 OPR/56.0.3051.116',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    ]
    num = random.randint(1,len(ua)-1)
    return ua
    





if __name__=='__main__':
    print('...')
    choose_Mail()

    # submit={}
    

    # submit['ua'] = get_ua_yahoo()    
    # print(submit['ua'])

