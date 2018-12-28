# 调用格式
# ip_Test(city),city可用指定，也可以为空，为空则全美随机
# import sys
# sys.path.append("../..")
from selenium import webdriver
from time import sleep
import re
import os


def ip_new(city):
    print(',,,')
    if city == '':
        arg = ' -changeproxy/US'
    else:
        arg = ' -changeproxy/US/All/' + city
    print('changing ip ....')
    a = os.system('..\..\911S5\ProxyTool\AutoProxyTool.exe%s' % (arg))
    # os.system('/../../911S5/ProxyTool/1.py')
    #os.system('D:/项目/911S5/ProxyTool/AutoProxyTool.exe%s' % (arg))
    print(a)



# 测试ip
# city如果是'',则从us全国获取ip,否则用指定的city去获取ip
def ip_Test(city): 
    ip_new(city)
    sleep(5)
    # path='C:/cam4/driver'
    # executable_path=path
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    chrome_driver = webdriver.Chrome(chrome_options=options)
    print('preparing...')
    chrome_driver.implicitly_wait(20)  # 最长等待20秒
    print('getting site...')
    chrome_driver.get('https://whoer.net')
    sleep(5)
    i = 0
    while i <=3:
        try:
            str_1=chrome_driver.find_element_by_xpath("html/body/div/div/div/div[2]/div/div/div[2]/div/a/span").text
            break
        except:
            chrome_driver.get('https://whoer.net')
            sleep(5)
            i = i + 1            
    try:
        # str_1=chrome_driver.find_element_by_xpath("html/body/div/div/div/div[2]/div/div/div[2]/div/a/span").text
        str_2=chrome_driver.find_element_by_xpath('//*[@id="content"]/div[7]/div[1]/div[1]/div[1]/div[1]/div[2]/dl/dd[3]/span[2]').text
        totalCount = int(re.sub("\D", "", str_1))
        city = str_2
        sleep(3)
        chrome_driver.close()
        chrome_driver.quit()
        print(str_1)
        print(str_2)
        print('当前ip匿名度是：'+str(totalCount))
    except:
        print("can't connet to whoer,change ip...")        
        chrome_driver.close()
        chrome_driver.quit()
        city,totalCount=ip_Test(city)
     
    if totalCount < 90:
        city,totalCount=ip_Test(city)
        return city,totalCount
    else:
        
        return city,totalCount

if __name__=='__main__':
    # city,totalCount = ip_Test('')
    # print('============')
    # print(city)
    # city,totalCount = ip_Test('Dallas')
    # print('------------------')
    # print('------------------')
    # print('------------------')
    # print(city)
    ip_new('Houston')


