import requests
import sys
import re
import os
from exp10it import get_target_table_name_list
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from exp10it import COMMON_NOT_WEB_PORT_LIST
from exp10it import get_http_domain_from_url
from exp10it import execute_sql_in_db
from exp10it import CLIOutput

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
modulePath = __file__[:-len(__file__.split("/")[-1])]

check_addr="/solr"

#判断漏洞是否存在
target=sys.argv[1]

check_url_list=[]

http_domain=get_http_domain_from_url(target)
if http_domain!=target:
    if "." in target.split("/")[-1]:
        check_url_list.append(target[:-(len(target.split("/")[-1])+1)])
    else:
        if target[-1]=="/":
            check_url_list.append(target[:-1])
        else:
            check_url_list.append(target)
    check_url_list.append(http_domain)



target_table_name = get_target_table_name_list(target)[0]
result = execute_sql_in_db("select port_scan_info from %s where http_domain='%s'" %
                           (target_table_name, target), "exp10itdb")
if len(result) > 0:
    nmap_result_string = result[0][0]
    a = re.findall(r"(\d+)/(tcp)|(udp)\s+open", nmap_result_string, re.I)
    open_port_list = []
    for each in a:
        if each[0] not in openPortList and each[0] not in COMMON_NOT_WEB_PORT_LIST:
            open_port_list.append(each[0])
            check_url_list.append(http_domain+":"+each[0])

def check(url):
    #print("正在检测第%d个url:%s" % (statusNum,url))
    vuln_url = url+check_addr

    content = requests.get(vuln_url,verify=False,timeout=10)
    if content.status_code ==200:
        string_to_write="Congratulations! solr漏洞存在:\n"+vuln_url+"\n"
        CLIOutput().good_print(string_to_write)
        with open("%sresult.txt" % modulePath,"a+") as f:
            f.write(string_to_write)
    else:
        print(content.status_code)

from concurrent import futures
with futures.ThreadPoolExecutor(max_workers=15) as executor:
    executor.map(check,check_url_list)
