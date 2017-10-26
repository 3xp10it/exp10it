import os
from exp10it import get_request
from exp10it import moduleExist
from exp10it import get_string_from_command
import re
from exp10it import get_http_domain_from_url




cookie="xp_ci=3z1ry4JHz20Dz5T6zCG5z2odBaj4g;geo=CN;ccl=3VzIb1J6Nhnx9p3ArtagyA==;s_cc=true;dssid2=e2603de8-1b64-4981-b007-eaf2d9ef80d7;dssf=1;pxro=2;as_loc=32cdde61b38afff24faaeaac84fb80a3e860582e0ffe17744a5363a745266add8765038379fb6287742cd75de34788e4187b7f33a3dc6e87b6867bcc52b457faa5288013f9de98d568749f53254aee6f15149c7724ee295e0bc7f850d01a4887847d71e4726855edc1d5fe605996a0e8a2513433a6d27561107301cf6e5d62f463d05af3d05c24e919c073dfc0ed9a89;as_pcts=HTcXHfiBGXpU0AqWKsEw1fvZVKmKj2BkV1Ul3REJA+XkS1uDPQa5JOINmbIIzZ4kKfrN6;s_vnum_n2_us=4%7C3;s_pathLength=homepage%3D1%2C;s_invisit_n2_cn=3;s_vnum_n2_cn=3%7C3%2C0%7C1;as_rec=SKHHAHFCP4UTC24AJUT44KKJ4CPKXH27H79CXCDFKC49YJDHU;as_disa=SP9DX2F7C2YH47XH22UF99H2ACU77Y2F4HYKTX22J7YYC7XKPP2HH99UPJP2UHTJTKDCXFPTCXU9FJ9PJ9DPK7CAPJ2AJ7HX9D77F44APPJ2XTY4YCJKJ7KA7YUDCCJ77CYFKU9HHKPT9K9XCKU792KCFDFCATTYD;as_cn=5YW05Y2O~87d69e57b4c1119ced709ab4f9bca42e5a481f24a9d665ceae4cd971d0a55016;as_ltn_cn=1aosJBeWHnSgCtSGht8hiWrteQFd35Hr8l9YhrBXF1C8%2Bo2Zdjc%2Bjr/EROWlKwNKAq5q92QxqnRIgg6rpUvtJRUJol%2B%2B1GT6ACl7XiPAbW%2BjW7bbYRdX9CyEdBua1XWQivngM5BedBzTTnGc9QFdYXXjWfxDjA2LWjLldNuA2x/kFvkwM4Edg%2BaboNqjkXt%2B8sOpt15gLwUKQRwJ2LFNlHN3rA%3D%3D;as_metrics=%257B%2522store%2522%253A%257B%2522sid%2522%253A%2522wFP7F7CXH9P4TJY9X%2522%257D%257D;s_sq=applecnhome%252Capplestoreww%252Capplestoreapaccnzh%3D%2526c.%2526a.%2526activitymap.%2526page%253Dapple%252520-%252520index%25252Ftab%252520%252528cn%252529%2526link%253D%2525E6%252594%2525B6%2525E8%252597%25258F%252520%2525283%252529%252520-%252520%25252Fcn%25252Fshop%25252Ffavorites%252520-%252520ac-globalnav%2526region%253Dac-globalnav%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dapple%252520-%252520index%25252Ftab%252520%252528cn%252529%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.apple.com%25252Fcn%25252Fshop%25252Ffavorites%2526ot%253DA;as_dc=nc;as_sfa=Mnxjbnxjbnx8emhfQ058Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE=;as_metrics=%7B%22store%22%3A%7B%22sid%22%3A%22wFP7F7CXH9P4TJY9X%22%7D%7D;s_vi=[CS]v1|2C852E4F85031A3B-4000119B80008D94[CE];s_fid=01976D4638FAA229-37D99262CA2722D3"
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
    user_text_box.send_keys('1731977663@qq.com')
    pass_text_box=driver.find_element_by_name('login-password')
    pass_text_box.clear()
    pass_text_box.send_keys('063913Dx')
    login_button=driver.find_element_by_id('sign-in')
    print("现在点击登录按钮")
    login_button.click()

    import random
    driver.get_screenshot_as_file("/tmp/PhantomJSPic")
    title = driver.title
    print(title)
    content = driver.page_source
    pic_links=driver.find_elements_by_class_name('relatedlink')
    print(len(pic_links))

    #attention!!!!!!!!这里要修改,[1]和[2]是iphonex
    pic_links[0].click()
    driver.get_screenshot_as_file("/tmp/PhantomJSPic0")
    add_to_cart_link=driver.find_element_by_name('add-to-cart')
    add_to_cart_link.click()
    print("现在加入到购物车")
    driver.get_screenshot_as_file("/tmp/PhantomJSPic1")
    #attention!!!!!!!!这里可以设置抢2台
    jie_zhang_link=driver.find_element_by_id('cart-actions-checkout')
    print("现在点击结帐")
    jie_zhang_link.click()
    driver.get_screenshot_as_file("/tmp/PhantomJSPic2")

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

    """
    WebDriverWait(driver, 300).until( 
      expected_conditions.visibility_of_all_elements_located( 
        (By.CLASSNAME ,'qrcode-img-area')
      ) 
    )
    """

    WebDriverWait(driver, 300).until( 
      expected_conditions.element_to_be_clickable( 
        (By.ID,'J_tLoginId')
      ) 
    )

    #time.sleep(3)

    zhifubao_username_box=driver.find_element_by_id('J_tLoginId')
    zhifubao_username_box.clear()
    zhifubao_username_box.send_keys('18013790233')

    zhifubao_pass_box=driver.find_element_by_id('payPasswd_rsainput')
    #zhifubao_pass_box.clear()
    zhifubao_pass_box.send_keys('zhifumima')

    driver.get_screenshot_as_file("/tmp/PhantomJSPic4")
    os.system("open /tmp/PhantomJSPic4")

    """
    WebDriverWait(driver, 300).until( 
      expected_conditions.element_to_be_clickable( 
        (By.ID,'J_newBtn')
      ) 
    )
    """

    print("现在在支付宝中确认付款")
    driver.find_element_by_id('J_newBtn').click()
    driver.get_screenshot_as_file("/tmp/PhantomJSPic5")

    zhifubao_pass_box=driver.find_element_by_id('payPasswd_rsainput')
    zhifubao_pass_box.clear()
    zhifubao_pass_box.send_keys('zhifumima')

    driver.find_element_by_id('J_newBtn').click()
    driver.get_screenshot_as_file("/tmp/PhantomJSPic5")

    WebDriverWait(driver, 300).until( 
      expected_conditions.element_to_be_clickable( 
        (By.ID,'J_authSubmit')
      ) 
    )

    tmp=driver.find_element_by_id('payPassword_rsainput')
    tmp.clear()
    tmp.send_keys("zhifumima")
    driver.get_screenshot_as_file("/tmp/PhantomJSPic6")

    print("最后确认付款")
    tmp=driver.find_element_by_id('J_authSubmit')
    tmp.click()



    os.system("open /tmp/PhantomJSPic4")
    os.system("open /tmp/PhantomJSPic5")
    os.system("open /tmp/PhantomJSPic6")



buy_ipx()
os.system("pkill phantomjs")
