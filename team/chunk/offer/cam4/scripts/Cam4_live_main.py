import sys
sys.path.append("../..")
import xlrd
import random
from xlutils.copy import copy
import os
import time
from modules_add.Cam4 import Cam4_live as live
from modules_add.ip_test import ip_test


def writelog(runinfo,e=''):
    file=open(os.getcwd()+"\live_log.txt",'a+')
    file.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" : \n"+runinfo+"\n"+e+'\n')
    file.close()




def submit_Dict(submit1):
    submit = {}
    submit['name'] = submit1[0]
    submit['pwd'] = submit1[1]
    submit['email'] = submit1[2]
    submit['email_pwd'] = submit1[3]
    submit['email_assist'] = submit1[4]
    submit['ua'] = submit1[5]
    submit['status'] = submit1[6]
    submit['city'] = submit1[7]
    return submit




def get_Account():
    path_excel = '..\config\c4mconfig.xlsx'
    workbook = xlrd.open_workbook(path_excel)
    sheet = workbook.sheet_by_index(0)
    rows = sheet.nrows
    print(rows)
    list_rows = random.sample(range(rows),rows)
    list_rows2 = [x for x in list_rows if sheet.row_values(x)[6] == 'success']
    print(list_rows)
    live_num = random.randint(10,20)  
    flag_live_num = 0
    for i in list_rows2:
        if i == 0:
            continue
        flag_live_num += 1
        if flag_live_num == live_num:
            print('all live excuted: '+str(flag_live_num-1))
            writelog('all live excuted'+str(flag_live_num-1))
            break
        writelog('account '+str(i)+' start')
        #get submit 
        workbook = xlrd.open_workbook(path_excel)
        sheet = workbook.sheet_by_index(0)
        book2 = copy(workbook)
        sheet2 = book2.get_sheet(0)
        submit1 = sheet.row_values(i)
        print(submit1)
        try:
            submit = submit_Dict(submit1)
        except:
            print('submit get wrong')
            continue
        # change ip
        city,count = ip_test.ip_Test(submit['city'])

        #login model
        back = 0
        try:
            back = live.Cam4_live(submit)
            sheet2.write(i,6,back)
        except Exception as e:
            writelog('login return with error',str(e))
            sheet2.write(i,6,back)

        writelog(str(flag_live_num)+': '+submit['name']+str(back))
        rantime = random.randint(3,5)
        sleep(rantime*60) 



if __name__=='__main__':
    get_Account()