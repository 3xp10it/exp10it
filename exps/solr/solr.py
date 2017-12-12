import requests
import os
import sys
exp10it_module_path = os.path.expanduser("~") + "/mypypi"
sys.path.insert(0, exp10it_module_path)
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from exp10it import COMMON_NOT_WEB_PORT_LIST
from exp10it import get_http_domain_from_url
from exp10it import CLIOutput
from exp10it import get_target_open_port_list

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
current_dir = os.path.split(os.path.realpath(__file__))[0]

check_addr = "/solr"

# 判断漏洞是否存在
target = sys.argv[1]
print("checking solr vul for "+target)

check_url_list = []

http_domain = get_http_domain_from_url(target)
if http_domain != target:
    if "." in target.split("/")[-1]:
        check_url_list.append(target[:-(len(target.split("/")[-1]) + 1)])
    else:
        if target[-1] == "/":
            check_url_list.append(target[:-1])
        else:
            check_url_list.append(target)
    check_url_list.append(http_domain)

open_port_list = get_target_open_port_list(target)

for port in open_port_list:
    if port not in COMMON_NOT_WEB_PORT_LIST:
        check_url_list.append(http_domain + ":" + port)


def check(url):
    #print("正在检测第%d个url:%s" % (statusNum,url))
    vuln_url = url + check_addr

    content = requests.get(vuln_url, verify=False, timeout=10)
    if content.status_code == 200:
        string_to_write = "Congratulations! solr漏洞存在:\n" + vuln_url + "\n"
        CLIOutput().good_print(string_to_write)
        with open("%s/result.txt" % current_dir, "a+") as f:
            f.write(string_to_write)
    else:
        print(content.status_code)


from concurrent import futures
with futures.ThreadPoolExecutor(max_workers=15) as executor:
    executor.map(check, check_url_list)
