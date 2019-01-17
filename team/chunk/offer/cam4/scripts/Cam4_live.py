from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import random
import json
import xlrd




# site = 'http://www.cam4.com/female'    
def Cam4_live(submit):
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    ua = submit['ua']
    options.add_argument('user-agent="%s"' % ua)
    options.add_argument("--disable-infobars")
    chrome_driver = webdriver.Chrome(chrome_options=options)
    chrome_driver.get('http://www.cam4.com/female')
    with open('cookies\cookies_cam4\\'+submit['email']+".txt", 'r') as fp:
        cookies = json.load(fp)
        for cookie in cookies:
            chrome_driver.add_cookie(cookie)
    chrome_driver.get('http://www.cam4.com/female')
    try:
        chrome_driver.find_element_by_id('promotionsConsentModalLink').click()
        print('find no thanks')
    except:
        print('not find no thanks')
    randtime = random.randint(10,15)
    # sleep(randtime*10)
    time_num =random.randint(3,6)
    for i in range(time_num):
        num = random.randint(1,20)
        try:
            chrome_driver.find_element_by_xpath('//*[@id="directoryDiv"]/div['+str(num)+']/div/a[2]').click()
            # //*[@id="directoryDiv"]/div[1]/div/a[2]
            chrome_driver.get('http://www.cam4.com/female')
            print('asdasdasdasd')            
        except:
            chrome_driver.get('http://www.cam4.com/female')
            print('no vedio find')
        sleep_time = random.randint(1,3)
        sleep(sleep_time*60)
    chrome_driver.close()
    chrome_driver.quit()
    return 1

def submit_Dict(submit1):
    submit = {}
    submit['email'] = submit1[2]
    submit['ua'] = submit1[5]
    return submit



if __name__=='__main__':
    path_excel = '..\\config\\huoyue.xlsx'
    workbook = xlrd.open_workbook(path_excel)
    sheet = workbook.sheet_by_index(0)
    rows = sheet.nrows
    print(rows)
    # if rows != 2:
        # print('offer\\cam4\\config\\huoyue.xlsx')
        # break
    submit1 = sheet.row_values(1)
    submit=submit_Dict(submit1)
    # submit = {}
    # submit['email'] = 'LillieHallk@aol.com'
    # submit['ua'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'
    Cam4_live(submit)
