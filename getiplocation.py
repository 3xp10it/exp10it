from exp10it import get_http_domain_from_url
from exp10it import get_string_from_command
from exp10it import get_one_useful_proxy
from exp10it import get_request
import re
import os
import urllib


def getip(domain):
    os.system("ping %s" % domain)
    return "113.116.175.200"


def getdomainlist():
    domainList = []
    with open("domain.txt", "r+") as f:
        for each in f:
            http_domain = get_http_domain_from_url(each)
            domain = http_domain.split("/")[-1]
            domainList.append(domain)
        return domainList


def getPingIP(domain):
    ip = ""
    content = get_string_from_command("dig mx a +short %s" % domain)
    find = re.search(r"(([\d]{1,3}\.){3}\d{1,3})", content)
    if find:
        ip = find.group(1)
    return ip


def getloca(ip):
    url = "http://ip.taobao.com/service/getIpInfo.php?ip=%s" % ip
    html = get_request(url, "seleniumPhantomJS")['content']
    print("html type is")
    print(type(html))
    if html is None:
        return ip + "    " + "failed"
    if re.search("<html>", html) and "{" in html:
        html = re.search(">(\{[\s\S]+\})<", html).group(1)
        print(html)
    if re.search("<html>", html) and "{" not in html:
        return ip + "    " + "failed"
    htmldic = eval(html)
    country = htmldic['data']['country']
    city = htmldic['data']['city']
    region = htmldic['data']['region']
    return ip + "    " + country + ":" + city + ":" + region


domainList = getdomainlist()
with open("result.txt", "a+") as f:
    for each in domainList:
        ip = getPingIP(each)
        if ip != "":
            # print(ip)
            string2write = re.sub("\s$", "", each) + "    " + getloca(ip)
            print(string2write)
            f.write(string2write + "\n")
print("finished!!!!!!!!!!!!!!!!!!")
