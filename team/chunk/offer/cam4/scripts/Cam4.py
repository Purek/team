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
    site = sheet.cell(1,8).value
    print(site)
    # submit = {}
    flag = 0
    # city,count = ip_test.ip_Test('')
    for i in list_rows:
        print(i)
        workbook = xlrd.open_workbook(path_excel)
        sheet = workbook.sheet_by_index(0)
        book2 = copy(workbook)
        sheet2 = book2.get_sheet(0)
        if sheet.cell(i,0).value != '':
            continue 
        submit1 = sheet.row_values(i)
        submit = submit_Dict(submit1)

        if 'aol.com' in submit['email']:
            print('aol')
            try:
                # if login fail,change email
                flag = Aol_check.Aol_Check(submit,'Cam4','Verify Your Account')
                print(flag)
                if flag == 0:
                    sheet2.write(i,6,'login failed')
                elif flag == 1:
                    sheet2.write(i,6,'login success but verify failed')
                    sheet2.write(i+1,7,city)
                else:
                    sheet2.write(i,6,'login success')
                    sheet2.write(i,7,city)
                    rantime = random.randint(10,15)
                    sleep(rantime*60)                     
                    city,count = ip_test.ip_Test('')                    
            except Exception as e:
                sheet2.write(i,6,'login failed')
                writelog('aol login error',str(e))     
        elif 'yahoo.com' in submit['email']:
            print('yahoo')
            try:
                # if login fail,change email
                flag = Yahoo_check.Yahoo_Check(submit,'Cam4','Verify Your Account')
                print(flag)
                if flag == 0:
                    sheet2.write(i,6,'login failed')
                elif flag == 1:
                    sheet2.write(i,6,'login success but verify failed')
                    sheet2.write(i,7,city)
                else:
                    sheet2.write(i,7,city)
                    rantime = random.randint(10,15)
                    sleep(rantime*60)                     
                    city,count = ip_test.ip_Test('')
            except Exception as e:
                sheet2.write(i,6,'login failed')
                writelog('yahoo login error',str(e))     
        elif 'gmail' in submit['email']:
            print('gmail')
            try:
                # if login fail,change email
                flag = Gmail_check.Gmail_Check(submit,'Cam4','Verify Your Account')
                print(flag)
                if flag == 0:
                    sheet2.write(i,6,'login failed')
                elif flag == 1:
                    sheet2.write(i,6,'login success but verify failed')
                    sheet2.write(i,7,city)
                else:
                    sheet2.write(i,7,city)
                    rantime = random.randint(10,15)
                    sleep(rantime*60)             
                    city,count = ip_test.ip_Test('')
            except Exception as e:
                sheet2.write(i,6,'login failed')
                writelog('gmail login error',str(e))   
    book2.save('..\config\c4mconfig.xlsx')
    print('成功保存')                


if __name__=='__main__':
    print('...')
    choose_Mail()

