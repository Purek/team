# v1.0.1
# 修改雅虎邮箱取cam邮件
# v1.0.2 增加cam注册输入账户时的随机延迟
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from datetime import date,datetime
import xlrd
from xlutils.copy import copy
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from name_get import name_get as ng
import re
import random
import os


# 测试ip
def ip_Test(): 
    path='C:/cam4/driver'
    executable_path=path
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    chrome_driver = webdriver.Chrome(chrome_options=options)
    print('preparing...')
    chrome_driver.implicitly_wait(10)  # 最长等待8秒
    print('getting site...')
    chrome_driver.get('https://whoer.net')
    sleep(5)
    try:
        str_1=chrome_driver.find_element_by_xpath("html/body/div/div/div/div[2]/div/div/div[2]/div/a/span").text
    except:
        try:
            chrome_driver.get('https://whoer.net')
            str_1=chrome_driver.find_element_by_xpath("html/body/div/div/div/div[2]/div/div/div[2]/div/a/span").text
        except:
            chrome_driver.close()
            chrome_driver.quit()           
            return 0
    sleep(3)
    chrome_driver.close()
    chrome_driver.quit()
    totalCount = int(re.sub("\D", "", str_1))
    print('当前ip匿名度是：'+str(totalCount))
    if totalCount < 90:
        return 0
    else:
        return 1



# 网站注册
def web_Submit(submit): 
    path='../driver'
    executable_path=path
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
    chrome_driver.find_element_by_xpath("//*[@id='paymentForm']/a/span").click()
    
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
        submit['name'] = ng.gen_one_word_digit(lowercase=False)
        status,submit['name'] = web_Submit(submit)

    return status,submit['name']
   
# aol邮箱验证 
def email_Check_Aol(submit):
    path='../driver'
    executable_path=path
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    # ua = submit['ua']
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
    prefs = {"profile.managed_default_content_settings.images":2}
    options.add_experimental_option("prefs",prefs)
    options.add_argument('user-agent="%s"' % ua)
    chrome_driver = webdriver.Chrome(chrome_options=options)
    print('preparing...')
    chrome_driver.implicitly_wait(10)  # 最长等待8秒
    print('getting site...')
    chrome_driver.get("https://login.aol.com/?.src=guce-mail&lang=&done=https%3A%2F%2Fmail.aol.com%2F")
    # chrome_driver.get("https://www.google.com")
    print('loading finished...')
    chrome_driver.find_element_by_id('login-username').send_keys(submit['email'])
    chrome_driver.find_element_by_id('login-signin').click()
    chrome_driver.find_element_by_id('login-passwd').send_keys(submit['email_pwd'])
    chrome_driver.find_element_by_id('login-signin').click()
    sleep(5)

    try: 
        chrome_driver.find_element_by_xpath('//*[@id="dijit__WidgetsInTemplateMixin_1"]/div/div[1]').click()
    except:
        print('no ads1')
    try:
        chrome_driver.find_element_by_xpath('//*[@id="dijit__WidgetsInTemplateMixin_2"]/div/div[1]').click()
    except:
        print('no ads2')
    
    try:
        chrome_driver.find_element_by_xpath('//*[@id="uniqName_4_4"]').click()
    except:
        print('no getstarted')
    # inbox里查找cam4
    try:
        chrome_driver.find_element_by_xpath('//*[@id="inboxNode"]').click()
        sleep(3)
        list1 = chrome_driver.find_elements_by_class_name("dojoxGrid-row")
        [a.click() for a in list1 if "Cam4" in str(a.get_attribute('innerHTML'))]
        try:
            chrome_driver.maximize_window()
            if chrome_driver.find_element_by_link_text('Verify Your Account'):
                chrome_driver.find_element_by_link_text('Verify Your Account').click()
                rantime = random.randint(1,3)
                sleep(rantime*60)
                chrome_driver.close()
                chrome_driver.quit()
                return 1
        except:
            print("can't find verify button")
            # spam
            try:
                chrome_driver.find_element_by_xpath('//*[@id="dijit__Widget_1"]/div[3]/div[4]/div/span').click()
                sleep(5)
                list3 = chrome_driver.find_elements_by_class_name("dojoxGrid-row")
                print(list3)
                [a.click() for a in list3 if "Cam4" in str(a.get_attribute('innerHTML'))]
            except:
                print('inbox not found')

            try:
                chrome_driver.maximize_window()
                if chrome_driver.find_element_by_link_text('Verify Your Account'):
                    chrome_driver.find_element_by_link_text('Verify Your Account').click()
                    rantime = random.randint(1,3)
                    sleep(rantime*60)
                    chrome_driver.close()
                    chrome_driver.quit()
                    return 1
            except:
                print("can't find verify button")
                # sleep(5)
                chrome_driver.close()
                chrome_driver.quit()
                return 0
    except:
        print('Cam4 not found in inbox')
        # chrome_driver.close()
        # chrome_driver.quit()
        return 0

#yahoo验证
def email_Check_yahoo(submit):
    path='../driver'
    executable_path=path
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    # prefs = {"profile.managed_default_content_settings.images":2}
    # options.add_experimental_option("prefs",prefs)
    chrome_driver = webdriver.Chrome(chrome_options=options)
    print('preparing...')
    chrome_driver.implicitly_wait(10)  # 最长等待8秒
    print('getting site...')
    chrome_driver.get("https://login.yahoo.com/?.src=ym&lang=&done=https%3A%2F%2Fmail.yahoo.com%2F")
    # chrome_driver.get("https://www.google.com")
    print('loading finished...')
    # 登陆

    chrome_driver.find_element_by_id('login-username').send_keys(submit['email'])
    sleep(3)
    chrome_driver.find_element_by_id('login-signin').click()
    sleep(2)
    chrome_driver.find_element_by_id('login-passwd').send_keys(submit['email_pwd'])
    sleep(2)
    chrome_driver.find_element_by_id('login-signin').click()
    sleep(5)
    list0 = chrome_driver.find_elements_by_tag_name("button")
    try:
        [a.click() for a in list0 if "Done" in str(a.get_attribute('innerText'))]
    except:
        print('meiyou done biaoqian')
    list1 = chrome_driver.find_elements_by_tag_name("a")
    try:
        [a.click() for a in list1 if "Cam4" in str(a.get_attribute('innerHTML'))]
    except:
        print('........')
    try:
        chrome_driver.maximize_window()
        if chrome_driver.find_element_by_link_text('Verify Your Account'):
            chrome_driver.find_element_by_link_text('Verify Your Account').click()
            rantime = random.randint(1,3)
            sleep(rantime*60)
            chrome_driver.close()
            chrome_driver.quit()
            return 1
    except:
        print("can't find verify button")
        # spam
        try:
            try:
                chrome_driver.find_element_by_link_text('More').click()
            except:
                print('no more')
            chrome_driver.find_element_by_link_text('Spam').click()
            list3 = chrome_driver.find_elements_by_class_name("o_h")
            try:
                [a.click() for a in list3 if "Cam4" in str(a.get_attribute('innerText'))]
            except:
                print('===========')
            try:
                chrome_driver.maximize_window()
                if chrome_driver.find_element_by_link_text('Verify Your Account'):
                    chrome_driver.find_element_by_link_text('Verify Your Account').click()
                    rantime = random.randint(1,3)
                    sleep(rantime*60)
                    chrome_driver.close()
                    chrome_driver.quit()
                    return 1
            except:
                print("can't find verify button")
                # sleep(5)
                chrome_driver.close()
                chrome_driver.quit()
                return 0
        except:
            print('inbox not found')
            chrome_driver.close()
            chrome_driver.quit()
            return 0

# gmail验证
def email_Check_Gmail(submit):
    path='../driver'
    executable_path=path
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    # ua = submit['ua']
    # ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
    # prefs = {"profile.managed_default_content_settings.images":2}
    # options.add_experimental_option("prefs",prefs)
    # options.add_argument('user-agent="%s"' % ua)
    chrome_driver = webdriver.Chrome(chrome_options=options)
    print('preparing...')
    chrome_driver.implicitly_wait(10)  # 最长等待8秒
    print('getting site...')
    chrome_driver.get("https://mail.google.com/")
    # chrome_driver.get("https://www.google.com")
    print('loading finished...')
    # 登陆
    chrome_driver.find_element_by_name('identifier').send_keys(submit['email'])
    chrome_driver.find_element_by_class_name('RveJvd').click()
    chrome_driver.find_element_by_name('password').send_keys(submit['email_pwd'])
    # chrome_driver.find_element_by_id('passwordNext').click()
    sleep(3)
    list1 = chrome_driver.find_elements_by_class_name('U26fgb')
    [a.click() for a in list1 if 'Next' in str(a.get_attribute('innerHTML'))]
    # [a.click() for a in list1 if '下一步' in str(a.get_attribute('innerHTML'))]

    try:
        chrome_driver.find_element_by_class_name('TnvOCe').send_keys(Keys.ENTER)

    # 添加辅助邮箱地址
        chrome_driver.find_element_by_name('knowledgePreregisteredEmailResponse').send_keys(submit['email_assist'])
        chrome_driver.find_element_by_class_name('U26fgb').send_keys(Keys.ENTER)
        chrome_driver.find_element_by_class_name('U26fgb').send_keys(Keys.ENTER)
    except:
        print('no assistance needed')
    try:
        chrome_driver.find_element_by_name('welcome_dialog_next').click()
        chrome_driver.find_element_by_name('ok').click()
    except:
        print('no next')


    chrome_driver.find_element_by_css_selector('[data-tooltip = "Inbox"').click()
    list1 = chrome_driver.find_elements_by_tag_name('tr')
    try:
        [a.click() for a in list1 if "Cam4" in str(a.get_attribute('innerText'))]
        try:
            chrome_driver.find_element_by_link_text('Verify Your Account').click()
            rantime = random.randint(1,3)
            sleep(rantime*60)
            chrome_driver.close()
            chrome_driver.quit()
            return 1
        except:
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
                        [a.click() for a in list3 if "Cam4" in str(a.get_attribute('innerText'))]
                        sleep(5)
                        try:
                            list4 = chrome_driver.find_elements_by_tag_name('a')
                            print(len(list4))
                            [a.click() for a in list4 if "Verify Your Account" in str(a.get_attribute('innerText'))]
                            # chrome_driver.find_element_by_link_text('Verify Your Account').click()
                            rantime = random.randint(1,3)
                            sleep(rantime*60)
                            chrome_driver.close()
                            chrome_driver.quit()
                            return 1
                        except:
                            return 0
                    except:
                        return 0     
                except:
                    print('no spam')
                    return 0
            except:
                print('cant find more')
                return 0
    except:
        print('cam4 not received')
        return 0


#读取配置文件
path_excel = 'C:/cam4/config/c4mconfig.xlsx'
workbook = xlrd.open_workbook(path_excel)
sheet = workbook.sheet_by_index(0)
rows = sheet.nrows
print(rows)
i = 0
while i < rows-1:
# for i in range(rows-1):
    if i != 0:
        rantime = random.randint(15,40)
        sleep(rantime*60)
    arg = ' -changeproxy/US'
    os.system('C:/cam4/911S5/ProxyTool/AutoProxyTool.exe%s' % (arg))
    ipcheck = 0
    while ipcheck == 0:
        ipcheck = ip_Test('')
        if ipcheck == 0:
            print('ip not good')
            arg = ' -changeproxy/US'
            os.system('C:/cam4/911S5/ProxyTool/AutoProxyTool.exe%s' % (arg))
        else:
            print('....')
            workbook = xlrd.open_workbook(path_excel)
            sheet = workbook.sheet_by_index(0)
            submit = {}
            submit['name'] = ng.gen_one_word_digit(lowercase=False)
            submit['pwd'] = sheet.cell(i+1,1).value
            submit['email'] = sheet.cell(i+1,2).value
            submit['email_pwd'] = sheet.cell(i+1,3).value
            submit['email_assist'] = sheet.cell(i+1,4).value
            submit['ua'] = sheet.cell(i+1,5).value
            submit['status'] = ''
            book2 = copy(workbook)
            sheet2 = book2.get_sheet(0)
            sheet2.write(i+1,0,submit['name'])
            try:
                submit['status'],submit['name'] = web_Submit(submit)
                if submit['name'] == '':
                    break
                sheet2.write(i+1,0,submit['name'])
                if submit['status'] == 'success':
                    flag = 0
                    if 'aol.com' in submit['email']:
                        try:
                            flag = email_Check_Aol(submit)
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
                            flag = email_Check_yahoo(submit)
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
                            flag = email_Check_Gmail(submit)
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
                    print('fail to commit')
                    sheet2.write(i+1,6,'email not in function')
            except:
                print('failed')
                sheet2.write(i+1,6,'email commit failed')
            finally:
                book2.save('C:/cam4/config/c4mconfig.xlsx')
                print('成功保存')
                i = i + 1






















