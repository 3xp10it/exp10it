import pdb
import argparse
import re
from exp10it import send_http_package
cookie = '''BIGipServerPOOL_PACLOUD_PRDR2016121905441=789911980.26745.0000; esales_app_flag=office-smart; JSESSIONID=p5FBVzXeQeSUtfiEnu534sNZCGWpi7PhiSEhF0MczUKaw8YiTHsd!479443737'''
yangguang_packet = '''POST /toYGAward.do HTTP/1.1
Host: smartoffice.pa18.com
Content-Type: application/x-www-form-urlencoded
Origin: file://
Cookie: %s
Connection: close
Accept: application/json, text/plain, */*
User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13A342
Accept-Language: zh-cn
Content-Length: 0

''' % cookie
hongbao_packet = '''POST /toXJAward.do HTTP/1.1
Host: smartoffice.pa18.com
Content-Type: application/x-www-form-urlencoded
Origin: file://
Cookie: %s
Connection: close
Accept: application/json, text/plain, */*
User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13A342
Accept-Language: zh-cn
Content-Length: 0

''' % cookie
hongbao_special_packet = '''POST /toSpecialXJAward.do HTTP/1.1
Host: smartoffice.pa18.com
Content-Type: application/json;charset=utf-8
Origin: file://
Cookie: %s
Connection: close
Accept: application/json, text/plain, */*
User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13A342
Accept-Language: zh-cn
Content-Length: 0

''' % cookie

parser = argparse.ArgumentParser()
parser.add_argument("--type")
args = parser.parse_args()
if args.type == "1":
    # 阳光普照
    while True:
        result = send_http_package(yangguang_packet, "https")
        if re.search(r"登录超时", result):
            print(result + "\n请更新cookie")
            break
        result = eval(result)
        if 'awardStatus' in result and result['awardStatus'] in ['1', '3']:
            print(result)
            print("恭喜...")
            break
        else:
            print(result)
            continue
if args.type == "2":
    # 红包雨,现金奖
    while True:
        result = send_http_package(hongbao_packet, "https")
        if re.search(r"登录超时", result):
            print(result + "\n请更新cookie")
            break
        result = eval(result)
        if 'awardStatus' in result and result['awardStatus'] == "1":
            print(result)
            print("恭喜...")
            break
        else:
            print(result)
            continue
if args.type == "3":
    # 红包雨,特殊现金奖
    while True:
        result = send_http_package(hongbao_special_packet, "https")
        if re.search(r"登录超时", result):
            print(result + "\n请更新cookie")
            break
        result = eval(result)
        pdb.set_trace()
        if 'awardStatus' in result and result['awardStatus'] == "1":
            print(result)
            print("恭喜...")
            break
        else:
            print(result)
            continue
