apple_id="1731977663@qq.com"
apple_id_pass="063913Dx"
zhifubao_username="18013790233"
zhifumima="zhifumima"

likes_num=3
try_index=2


import os
import time
from exp10it import get_request
from exp10it import moduleExist
from exp10it import get_string_from_command
import re
from exp10it import get_http_domain_from_url




proxyUrl=""

cookie=""

def buy_ipx():
    if moduleExist("selenium") is False:
        os.system("pip3 install selenium")
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException
    result = get_string_from_command("phantomjs --help")
    if re.search(r"(not found)|(不是内部或外部命令)|(Unknown command)", result,re.I):
        if systemPlatform == "Darwin":
            os.system("brew install phantomjs")
        elif systemPlatform == 'Linux':
            os.system("apt-get install phantomjs")
        elif systemPlatform == 'Windows':
            import wget
            try:
                wget.download(
                    "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-windows.zip", out="phantomjs.zip")
            except:
                print(
                    "Please download phantomjs from the official site and add the executeable file to your path")
                input("下载速度太慢,还是手工用迅雷下载吧,下载后将可执行文件phantomjs.exe存放到PATH中,再按任意键继续...")
    import time
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait 
    from selenium.webdriver.support import expected_conditions

    if proxyUrl == "" or proxyUrl == 0:
        service_args_value = ['--ignore-ssl-errors=true',
                              '--ssl-protocol=any', '--web-security=false']
    if proxyUrl != "" and proxyUrl != 0:
        proxyType = proxyUrl.split(":")[0]
        proxyValueWithType = proxyUrl.split("/")[-1]
        service_args_value = ['--ignore-ssl-errors=true', '--ssl-protocol=any', '--web-security=false',
                              '--proxy=%s' % proxyValueWithType, '--proxy-type=%s' % proxyType]
        #service_args_value.append('--load-images=no')  ##关闭图片加载
        service_args_value.append('--disk-cache=yes')  ##开启缓存

    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    dcap = dict(DesiredCapabilities.PHANTOMJS)

    ua = "Mozilla/4.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.33 Safari/532.0"
    #headers = {'User-Agent': '%s' % get_random_ua(),'Cookie': '%s' % cookie}
    if cookie!="":
        headers = {'User-Agent': '%s' % ua,'Cookie': '%s' % cookie}
    else:
        headers = {'User-Agent': '%s' % ua}
    for key in headers:
        capability_key = 'phantomjs.page.customHeaders.{}'.format(key)
        webdriver.DesiredCapabilities.PHANTOMJS[capability_key] = headers[key]
    driver = webdriver.PhantomJS(service_args=service_args_value)

    driver.implicitly_wait(300)
    driver.set_page_load_timeout(300)

    print("目前没有登录,现在访问收藏夹,尝试跳转到登录页面")
    driver.get("https://www.apple.com/cn/shop/favorites")

    WebDriverWait(driver, 300).until( 
      expected_conditions.element_to_be_clickable( 
        (By.NAME, 'login-appleId')
      ) 
    )
    user_text_box=driver.find_element_by_name('login-appleId')
    user_text_box.clear()
    user_text_box.send_keys(apple_id)
    pass_text_box=driver.find_element_by_name('login-password')
    pass_text_box.clear()
    pass_text_box.send_keys(apple_id_pass)
    login_button=driver.find_element_by_id('sign-in')
    print("现在点击登录按钮")
    login_button.click()

    import random
    #driver.get_screenshot_as_file("/tmp/PhantomJSPic")
    title = driver.title
    print(title)
    content = driver.page_source


    while True:
        pic_links=driver.find_elements_by_class_name('relatedlink')
        if pic_links and len(pic_links)>0:
            print(len(pic_links))
            break
        else:
            time.sleep(1)
            continue

    #attention!!!!!!!!这里要修改,[1]和[2]是iphonex
    pic_links[try_index-1].click()

    #driver.get_screenshot_as_file("/tmp/PhantomJSPic0")


    WebDriverWait(driver, 300).until( 
      expected_conditions.element_to_be_clickable( 
        (By.NAME, 'add-to-cart')
      ) 
    )


    add_to_cart_link=driver.find_element_by_name('add-to-cart')
    add_to_cart_link.click()
    print("现在加入到购物车")

    #driver.get_screenshot_as_file("/tmp/PhantomJSPic1")


    WebDriverWait(driver, 300).until( 
      expected_conditions.element_to_be_clickable( 
        (By.ID, 'cart-actions-checkout')
      ) 
    )


    jie_zhang_link=driver.find_element_by_id('cart-actions-checkout')
    print("现在点击结帐")
    jie_zhang_link.click()

    #driver.get_screenshot_as_file("/tmp/PhantomJSPic2")

    WebDriverWait(driver, 300).until( 
      expected_conditions.element_to_be_clickable( 
        (By.NAME, 'login-appleId')
      ) 
    )
    user_text_box=driver.find_element_by_name('login-appleId')
    user_text_box.clear()
    user_text_box.send_keys('1731977663@qq.com')
    pass_text_box=driver.find_element_by_name('login-password')
    pass_text_box.clear()
    pass_text_box.send_keys('063913Dx')
    login_button=driver.find_element_by_id('sign-in')
    print("现在点击登录按钮")
    login_button.click()
    driver.get_screenshot_as_file("/tmp/PhantomJSPic3")

    WebDriverWait(driver, 300).until( 
      expected_conditions.element_to_be_clickable( 
        (By.ID ,'cart-continue-button')
      ) 
    )
    continue_button1=driver.find_element_by_id('cart-continue-button')
    continue_button1.click()
    continue_button2=driver.find_element_by_id('shipping-continue-button')
    continue_button2.click()

    WebDriverWait(driver, 300).until( 
      expected_conditions.element_to_be_clickable( 
        (By.ID ,'payment-form-options-Alipay-0')
      ) 
    )

    zhifubao_button=driver.find_element_by_id('payment-form-options-Alipay-0')
    zhifubao_button.click()
    payment_continue_button=driver.find_element_by_id('payment-continue-button')
    payment_continue_button.click()

    WebDriverWait(driver, 300).until( 
      expected_conditions.element_to_be_clickable( 
        (By.ID ,'invoice-next-step')
      ) 
    )
    
    invoice_next_step_button=driver.find_element_by_id('invoice-next-step')
    invoice_next_step_button.click()

    WebDriverWait(driver, 300).until( 
      expected_conditions.element_to_be_clickable( 
        (By.ID ,'terms-accept')
      ) 
    )

    terms_accept_button=driver.find_element_by_id('terms-accept')
    terms_accept_button.click()

    WebDriverWait(driver, 300).until( 
      expected_conditions.element_to_be_clickable( 
        (By.ID ,'terms-continue-button')
      ) 
    )

    terms_continue_button=driver.find_element_by_id('terms-continue-button')
    terms_continue_button.click()

    WebDriverWait(driver, 300).until( 
      expected_conditions.element_to_be_clickable( 
        (By.ID ,'place-order-button')
      ) 
    )

    place_order_button=driver.find_element_by_id('place-order-button')
    place_order_button.click()

    WebDriverWait(driver, 300).until( 
      expected_conditions.element_to_be_clickable( 
        (By.ID ,'payNow')
      ) 
    )

    pay_now_button=driver.find_element_by_id('payNow')
    pay_now_button.click()


    WebDriverWait(driver, 300).until( 
      expected_conditions.element_to_be_clickable( 
        (By.ID,'J_tLoginId')
      ) 
    )


    zhifubao_username_box=driver.find_element_by_id('J_tLoginId')
    zhifubao_username_box.click()
    zhifubao_username_box.clear()
    zhifubao_username_box.send_keys(zhifubao_username)

    zhifubao_pass_box=driver.find_element_by_id('payPasswd_rsainput')
    zhifubao_pass_box.click()
    #zhifubao_pass_box.clear()
    zhifubao_pass_box.send_keys(zhifumima)

    driver.get_screenshot_as_file("/tmp/PhantomJSPic4")
    os.system("open /tmp/PhantomJSPic4")

    time.sleep(3)

    print("现在在支付宝中确认付款")
    driver.get_screenshot_as_file("/tmp/PhantomJSPic5")
    driver.find_element_by_id('J_newBtn').click()

    os.system("open /tmp/PhantomJSPic5")

    WebDriverWait(driver, 300).until( 
      expected_conditions.url_contains( 
        'standard/lightpay/lightPayCashier.htm'
      ) 
    )

    tmp=driver.find_element_by_id('payPassword_rsainput')
    tmp.click()
    tmp.send_keys(zhifumima)

    driver.get_screenshot_as_file("/tmp/PhantomJSPic6")

    print("最后确认付款")
    tmp=driver.find_element_by_id('J_authSubmit')
    tmp.click()


def checkStartTime():
    return
    while True:
        a=time.strftime('%H:%M:%S',time.localtime(time.time()))
        print(a)
        if  (a[0:2]=="15" and a[3:5]=="00" and a[6:8]=="59") or (a[0:2]=="15" and int(a[4])>=1):
            break
        else:
            print("还没到点...")
            time.sleep(0.5)
            continue


checkStartTime()
buy_ipx()
os.system("pkill phantomjs")
