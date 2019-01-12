from selenium import webdriver
from time import sleep
import xlrd
import random
import os

def writelog(runinfo,e=''):
    file=open(os.getcwd()+"\log.txt",'a+')
    file.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" : \n"+runinfo+"\n"+e+'\n')
    file.close()



def web_Submit(submit):
    # path='../driver'
    # executable_path=path
    path_excel = '..\..\cam4\config\c4mconfig.xlsx'
    workbook = xlrd.open_workbook(path_excel)
    sheet = workbook.sheet_by_index(0)
    site = sheet.cell(1,8).value
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    ua = submit['ua']
    # ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
    options.add_argument('user-agent="%s"' % ua)
    chrome_driver = webdriver.Chrome(chrome_options=options)
    #writelog('preparing...')
    chrome_driver.implicitly_wait(20)  # 最长等待8秒
    #writelog('getting site...')
    # chrome_driver.get("http://click.prodailyfinance.com/click.php?c=1&key=02q01o3378537qrqy3s9clei")
    chrome_driver.get(site)
    i = 0
    while i <=3:
        if 'Join CAM4' in chrome_driver.title:
            break
        else:
            writelog(chrome_driver.title)
            chrome_driver.get(site)
            sleep(5)
            i = i + 1   
    try:
        if 'Join CAM4' in chrome_driver.title:
            chrome_driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]").click()      #18+
            chrome_driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]").click()      #18+
        else:
            chrome_driver.close()
            chrome_driver.quit()
            return 0           
    except Exception as e:
        writelog('get site but cannot click',e)
        chrome_driver.close()
        chrome_driver.quit()
        return 0
    try:
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
    except:
        writelog('something error in registration',e)
        chrome_driver.close()
        chrome_driver.quit()
        return 0

    sleep(3)
    title = chrome_driver.title
    writelog(title)
    url = chrome_driver.current_url
    writelog(url)
    try:
        chrome_driver.find_element_by_xpath("//*[@id='paymentForm']/a/span").click()

    except Exception as e:
        writelog('form in a bad shape',e)
        chrome_driver.close()
        chrome_driver.quit()
        writelog('form not ok')
        return 0
    # writelog(chrome_driver.page_source)
    status = 'fail'
    sleep(3)
    if chrome_driver.title != title or chrome_driver.url != url:
        status = 'success'
        rantime = random.randint(3,5)
        sleep(rantime*60)  
        chrome_driver.close()
        chrome_driver.quit()
        return 1
    else:
        chrome_driver.close()
        chrome_driver.quit()
        return 0
        # submit['name'] = ng.gen_one_word_digit(lowercase=False)
        # status,submit['name'] = web_Submit(submit)

    

if __name__=='__main__':
    submit={}
    submit['ua'] = ''
    # site='http://www.baidu.com'
    web_Submit(submit)
