from exp10it import get_input_intime
from exp10it import checkvpn
from exp10it import homePath
import re
import os
import time

def sqlmap_crawl(origin_http_url_or_file, tor_or_not, post_or_not):
    # this function use sqlmap's "--crawl" option to find sqli urls.
    if re.match("(http://)|(https://)", origin_http_url_or_file):
        origin_http_url=re.sub(r'(\s)$', "", origin_http_url_or_file)
        sqlmap_string='''/usr/share/sqlmap/sqlmap.py -u "%s" --crawl=3 --delay 2 --smart -v 4 --threads 4 --batch --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3''' % (
            origin_http_url, origin_http_url)
        forms_sqlmap_string='''/usr/share/sqlmap/sqlmap.py -u "%s" --crawl=3 --delay 2 --smart -v 4 --threads 4 --batch --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3 --forms''' % (
            origin_http_url, origin_http_url)
        tor_sqlmap_string='''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -u "%s" --crawl=3 --delay 2 --smart -v 4 --threads 4 --batch --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3''' % (
            origin_http_url, origin_http_url)
        tor_forms_sqlmap_string='''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -u "%s" --crawl=3 --delay 2 --smart -v 4 --threads 4 --batch --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3 --forms''' % (
            origin_http_url, origin_http_url)
        # print("sqlmap_string is:%s" % sqlmap_string)
        if not tor_or_not:
            print("sqlmap_string is:%s" % sqlmap_string)
            print("forms_sqlmap_string is:%s" % forms_sqlmap_string)
            while 1:
                if checkvpn():
                    os.system("/usr/bin/python2.7 %s" % sqlmap_string)
                    if post_or_not:
                        os.system(
                            "/usr/bin/python2.7 %s" %
                            forms_sqlmap_string)
                    break
                else:
                    time.sleep(1)
                    print("vpn is off,scan will continue till vpn is on")

        elif tor_or_not:
            print("tor_sqlmap_string is:%s" % tor_sqlmap_string)
            print("tor_forms_sqlmap_string is:%s" % tor_forms_sqlmap_string)
            while 1:
                if checkvpn():
                    os.system("/usr/bin/python2.7 %s" % tor_sqlmap_string)
                    if post_or_not:
                        os.system(
                            "/usr/bin/python2.7 %s" %
                            tor_forms_sqlmap_string)
                    break
                else:
                    time.sleep(1)
                    print("vpn is off,scan will continue till vpn is on")


    else:
        fp=open(origin_http_url_or_file, "r+")
        all_urls=fp.readlines()
        fp.close()
        for each in all_urls:
            origin_http_url=re.sub(r'(\s)$', "", each)
            sqlmap_string='''/usr/share/sqlmap/sqlmap.py -u "%s" --crawl=3 --delay 2 --smart -v 4 --threads 4 --batch --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3''' % (
                origin_http_url, origin_http_url)
            forms_sqlmap_string='''/usr/share/sqlmap/sqlmap.py -u "%s" --crawl=3 --delay 2 --smart -v 4 --threads 4 --batch --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3 --forms''' % (
                origin_http_url, origin_http_url)
            tor_sqlmap_string='''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -u "%s" --crawl=3 --delay 2 --smart -v 4 --threads 4 --batch --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3''' % (
                origin_http_url, origin_http_url)
            tor_forms_sqlmap_string='''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -u "%s" --crawl=3 --delay 2 --smart -v 4 --threads 4 --batch --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3 --forms''' % (
                origin_http_url, origin_http_url)
            # print("sqlmap_string is %s" % sqlmap_string)
            if not tor_or_not:
                print("sqlmap_string is:%s" % sqlmap_string)
                print("forms_sqlmap_string is:%s" % forms_sqlmap_string)
                while 1:
                    if checkvpn():
                        os.system("/usr/bin/python2.7 %s" % sqlmap_string)
                        if post_or_not:
                            os.system(
                                "/usr/bin/python2.7 %s" %
                                forms_sqlmap_string)
                        break
                    else:
                        time.sleep(1)
                        print("vpn is off,scan will continue till vpn is on")

            elif tor_or_not:
                print("tor_sqlmap_string is:%s" % tor_sqlmap_string)
                print(
                    "tor_forms_sqlmap_string is:%s" %
                    tor_forms_sqlmap_string)
                while 1:
                    if checkvpn():
                        os.system("/usr/bin/python2.7 %s" % tor_sqlmap_string)
                        if post_or_not:
                            os.system(
                                "/usr/bin/python2.7 %s" %
                                tor_forms_sqlmap_string)
                        break
                    else:
                        time.sleep(1)
                        print("vpn is off,scan will continue till vpn is on")

def sqlmap_g_nohuman(http_url_or_file, tor_or_not, post_or_not):
    # this function use sqlmap's "-g" option to find sqli urls,but this "-g"
    # option can only get 100 results due to google api restriction,but in
    # this mode,there is no need for us human to handle any situation.
    if re.match("(http://)|(https://)", http_url_or_file):
        domain_url=http_url_or_file[7:] if re.match(
            "(http://)", http_url_or_file) else http_url_or_file[8:]
        sqlmap_string='''/usr/share/sqlmap/sqlmap.py -g "site:%s inurl:php|asp|aspx|jsp" --delay 2 --smart --batch -v 4 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3''' % (
            domain_url, http_url_or_file)
        forms_sqlmap_string='''/usr/share/sqlmap/sqlmap.py -g "site:%s inurl:php|asp|aspx|jsp" --delay 2 --smart --batch -v 4 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3 --forms''' % (
            domain_url, http_url_or_file)
        tor_sqlmap_string='''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -g "site:%s inurl:php|asp|aspx|jsp" --delay 2 --smart --batch -v 4 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3''' % (
            domain_url, http_url_or_file)
        tor_forms_sqlmap_string='''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -g "site:%s inurl:php|asp|aspx|jsp" --delay 2 --smart --batch -v 4 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3 --forms''' % (
            domain_url, http_url_or_file)
        # print("sqlmap_string is:%s" % sqlmap_string)
        # sqlmap_string='''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5
        # --check-tor -g site:%s allinurl:"php"|"php page="|"php id="|"php
        # tid="|"php pid="|"php cid="|"php path="|"php cmd="|"php file="|"php
        # cartId="|"php bookid="|"php num="|"php idProduct="|"php ProdId="|"php
        # idCategory="|"php intProdID="|"cfm storeid="|"php catid="|"php
        # cart_id="|"php order_id="|"php catalogid="|"php item="|"php title="|"php
        # CategoryID="|"php action="|"php newsID="|"php newsid="|"php
        # product_id="|"php cat="|"php parent_id="|"php view="|"php itemid="'''
        if not tor_or_not:
            print("sqlmap_string is:%s" % sqlmap_string)
            print("forms_sqlmap_string is:%s" % forms_sqlmap_string)
            while 1:
                if checkvpn():
                    os.system("/usr/bin/python2.7 %s" % sqlmap_string)
                    if post_or_not:
                        os.system(
                            "/usr/bin/python2.7 %s" %
                            forms_sqlmap_string)
                    break
                else:
                    time.sleep(1)
                    print("vpn is off,scan will continue till vpn is on")
        elif tor_or_not:
            print("tor_sqlmap_string is:%s" % tor_sqlmap_string)
            print("tor_forms_sqlmap_string is:%s" % tor_forms_sqlmap_string)
            while 1:
                if checkvpn():
                    os.system("/usr/bin/python2.7 %s" % tor_sqlmap_string)
                    if post_or_not:
                        os.system(
                            "/usr/bin/python2.7 %s" %
                            tor_forms_sqlmap_string)
                    break
                else:
                    time.sleep(1)
                    print("vpn is off,scan will continue till vpn is on")

    else:
        fp=open(http_url_or_file, "r+")
        all_urls=fp.readlines()
        fp.close()
        for each in all_urls:
            domain_url=each[7:] if re.match("(http://)", each) else each[8:]
            sqlmap_string='''/usr/share/sqlmap/sqlmap.py -g "site:%s inurl:php|asp|aspx|jsp" --delay 2 --smart --batch -v 4 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3''' % (
                domain_url, each)
            forms_sqlmap_string='''/usr/share/sqlmap/sqlmap.py -g "site:%s inurl:php|asp|aspx|jsp" --delay 2 --smart --batch -v 4 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3 --forms''' % (
                domain_url, each)
            tor_sqlmap_string='''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -g "site:%s inurl:php|asp|aspx|jsp" --delay 2 --smart --batch -v 4 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3''' % (
                domain_url, each)
            tor_forms_sqlmap_string='''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -g "site:%s inurl:php|asp|aspx|jsp" --delay 2 --smart --batch -v 4 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3 --forms''' % (
                domain_url, each)
            # print("sqlmap_string is:%s" % sqlmap_string)
            # sqlmap_string='''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5
            # --check-tor -g site:%s allinurl:"php"|"php page="|"php id="|"php
            # tid="|"php pid="|"php cid="|"php path="|"php cmd="|"php file="|"php
            # cartId="|"php bookid="|"php num="|"php idProduct="|"php ProdId="|"php
            # idCategory="|"php intProdID="|"cfm storeid="|"php catid="|"php
            # cart_id="|"php order_id="|"php catalogid="|"php item="|"php title="|"php
            # CategoryID="|"php action="|"php newsID="|"php newsid="|"php
            # product_id="|"php cat="|"php parent_id="|"php view="|"php itemid="'''
            if not tor_or_not:
                print("sqlmap_string is:%s" % sqlmap_string)
                print("forms_sqlmap_string is:%s" % forms_sqlmap_string)
                while 1:
                    if checkvpn():
                        os.system("/usr/bin/python2.7 %s" % sqlmap_string)
                        if post_or_not:
                            os.system(
                                "/usr/bin/python2.7 %s" %
                                forms_sqlmap_string)
                        break
                    else:
                        time.sleep(1)
                        print("vpn is off,scan will continue till vpn is on")
            elif tor_or_not:
                print("tor_sqlmap_string is:%s" % tor_sqlmap_string)
                print(
                    "tor_forms_sqlmap_string is:%s" %
                    tor_forms_sqlmap_string)
                while 1:
                    if checkvpn():
                        os.system("/usr/bin/python2.7 %s" % tor_sqlmap_string)
                        if post_or_not:
                            os.system(
                                "/usr/bin/python2.7 %s" %
                                tor_forms_sqlmap_string)
                        break
                    else:
                        time.sleep(1)
                        print("vpn is off,scan will continue till vpn is on")


def sqli_scan(target):
    #这里只能直接对target进行sqli检测,不考虑旁站或子站的sqli情况
    # target要求是http...格式,不能是纯domain
    http_domain=target

    print(
        '''do you want use 'tor' service in your sqli action? sometimes when your network is not very well,
is not a good idea to use tor,but when your targets has waf,use tor is better.
input Y(y) or N(n) default [N]:>''', end='')
    print('\n')
    choose_tor=get_input_intime('n', 5)
    print('\n')
    if choose_tor == 'Y' or choose_tor == 'y':
        bool_tor=True
    else:
        bool_tor=False

    print(
        '''do you want use 'post' request in your sqli scan? sometimes when you want a faster speed,
use 'get' request is enough,do no need to use 'post' request,meanwhile,when there exists some waf,
use 'get' and 'post' will try too many times's request which will make the waf block you ip,so in these cases,do not use 'post' request,
but use only 'get' request without 'post' request,the number of sqli points will be less in the common sense,
input Y(y) or N(n) default [N]:>''', end='')
    print('\n')
    choose_post=get_input_intime('n', 5)
    print('\n')
    if choose_post == 'Y' or choose_post == 'y':
        post_or_not=True
    else:
        post_or_not=False

    print('''there are two kinds of sqli blew:
1.use "sqlmap_crawl"
2.use "sqlmap-g-nohuman"
input your number here:''', end='')
    print('\n')
    num=str(get_input_intime(1, 5))
    print('\n')
    if num == str(1):
        while(1):
            if checkvpn():
                # 不管scan_way的值为多少,首先对main target进行sqli扫描
                sqlmap_crawl(
                    http_domain, bool_tor, post_or_not)
                break
            else:
                time.sleep(1)
                print("vpn is off,scan will continue till vpn is on")

    if num == str(2):
        while(1):
            if checkvpn():
                # 不管scan_way的值为多少,首先对main target进行sqli扫描
                if http_domain_sqli_scaned == 0:
                    sqlmap_g_nohuman(
                        http_domain, bool_tor, post_or_not)
                break
            else:
                time.sleep(1)
                print("vpn is off,scan will continue till vpn is on")

    domain=http_domain.split("/")[-1]
    logFile=homePath+"/.sqlmap/output/%s/log" % domain
    content=""
    if os.path.exists(logFile)==True:
        with open(homePath+"/.sqlmap/output/%s/log" % domain,"r+") as f:
            content=f.read()
    if len(content)!=0:
        return content
    else:
        return "Sorry,no sqli vul."


if __name__=='__main__':
    import sys
    http_domain=sys.argv[1]
    sqli_scan(http_domain)
