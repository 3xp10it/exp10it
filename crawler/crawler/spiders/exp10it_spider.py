import re
import pdb
import sys
import os
from urllib.parse import urlparse
import scrapy
from scrapy_splash import SplashRequest
from crawler.items import CrawlerItem
exp10it_module_path = os.path.expanduser("~")+"/mypypi"
sys.path.insert(0, exp10it_module_path)
from exp10it import RESOURCE_FILE_PATTERN
from exp10it import collect_urls_from_html
from exp10it import get_request
from exp10it import get_url_cookie
from exp10it import url_is_sub_domain_to_http_domain
from exp10it import get_http_domain_from_url
from exp10it import get_url_belong_main_target_domain
from exp10it import like_admin_login_content
from exp10it import check_url_has_webshell_content
from crawler.settings import IPProxyPoolUrl
import random
import requests

target_url_to_crawl="http://e.pingan.com/pa18shoplife/"
#http://192.168.93.139/dvwa/vulnerabilities/xss_r/?name=?name=?name=?name=?name=

def get_url_templet_list(url):
    # eg,url=http://www.baidu.com/?a=1&b=2
    # return_list:
    # ['http://www.baidu.com/?a=1&b=2',
    # 'http://www.baidu.com/?a=*&b=2',
    # 'http://www.baidu.com/?a=1&b=*',
    # 'http://www.badiu.com/?a=*&b=*']
    if "?" not in url:
        return []
    import itertools
    parsed=urlparse(url)
    query_string=parsed.query
    query_list=query_string.split("&")
    # query_list=['a=1','b=2']
    query_len=len(query_list)
    return_list=[]
    for i in range(0,query_len+1):
        a=list(itertools.combinations(query_list,i))
        # a=[('a=1',),('b=2',)]
        each_return_string=""
        for each in a:
            each_return_string=""
            for each_query in query_list:
                if each_query not in str(each):
                    each_query=re.sub(r"(?<=\=)[^\=]*","*",each_query)
                    each_return_string+=(each_query+"&")
                else:
                    each_return_string+=(each_query+"&")
            #print(each_return_string)
            return_list.append(url.replace(query_string,each_return_string[:-1]))
    return return_list



def get_random_proxy():
    IPPOOL = eval(requests.get(IPProxyPoolUrl).text)
    random_choose = random.choice(IPPOOL)
    proxy_addr = "http://" + \
        str(random_choose[0]) + ":" + str(random_choose[1])

    return [str(random_choose[0]),random_choose[1]]


class Exp10itSpider(scrapy.Spider):
    name = "exp10it"
    collected_urls = []
    domain = ""
    start_url = ""

    def add_url_templet_to_collected_urls(self, url):
        url=re.sub(r"(#[^\?]*)$","",url)
        parsed = urlparse(url)
        if len(parsed)<4:
            pdb.set_trace()
        url_page = parsed[0] + "://" + parsed[1] + \
            (parsed[2] if "^" not in parsed[2] else parsed[2].split('^')[0])
        param_part = parsed[2].split("^")[1] if "^" in url else parsed[4]
        param_list = param_part.split("&")
        pure_param_list = []
        if param_list != ['']:
            for each in param_list:
                each_param_name = each.split("=")[0]
                if len(each.split("="))==1:
                    each_param_value=""
                else:
                    each_param_value = each.split("=")[1]
                if re.search(r"(\d+)|([\u4e00-\u9fa5]+)|([A-Z]+)|(\s+)|(\D+\d+)", each_param_value):
                    pure_param_list.append(each_param_name + "=*")
                else:
                    pure_param_list.append(each)
            pure_param_list.sort()
            pure_param_part = ""
            for each in pure_param_list:
                pure_param_part += (each + "&")
            if "^" in url:
                pure_url = url_page + "^" + pure_param_part[:-1]
            elif "?" in url and "^" not in url:
                pure_url = url_page + "?" + pure_param_part[:-1]
            else:
                pure_url = url_page + "" + pure_param_part[:-1]
        else:
            if re.search(r"\.html?$", url, re.I):
                num_part = url.split("/")[-1].split(".")[0]
                if re.match(r"\d+", num_part):
                    pure_url = url[:-len(url.split("/")[-1])] + \
                        "*." + url.split(".")[-1]
                else:
                    pure_url=url
            else:
                pure_url = url

        if pure_url not in self.collected_urls:
            self.collected_urls.append(pure_url)

    def start_requests(self):
        urls = [
            #'https://www.bing.com'
            #'https://httpbin.org/post^sss=lalala'
            #'http://www.freebuf.com'
            target_url_to_crawl
            #'http://3xp10it.cc'
            #'http://www.ip138.com/'
            #'http://httpbin.org/ip'
            #'http://geekpwn.freebuf.com'
        ]
        self.domain = urlparse(urls[0]).hostname
        self.path=urlparse(urls[0]).path
        self.cookie= get_url_cookie(urls[0])
        a=get_random_proxy()
        print(a)
        self.lua_script = """
        function main(splash, args)
          assert(splash:go{splash.args.url,http_method=splash.args.http_method,body=splash.args.body,headers={
              ['Cookie']='%s',
              }
              }
              )
          assert(splash:wait(6))


          return { url = splash:url(),  cookies = splash:get_cookies(), html = splash:html(), }
        end
        """ % (self.cookie)


        self.start_url = urls[0]
        for url in urls:
            if "^" in url:
                post_url_list = url.split("^")
                post_url = post_url_list[0]
                post_data = post_url_list[1]
                yield SplashRequest(post_url, callback=self.parse_post, endpoint='execute',
                                    magic_response=True, meta={'handle_httpstatus_all': True, 'current_url': url},
                                    args={'lua_source': self.lua_script, 'http_method': 'POST',
                                        'body': post_data})
            else:
                if url=="http://m.pingan.com/":
                    input(6666666666)
                    pdb.set_trace()
                yield SplashRequest(url, self.parse_get, endpoint='execute',
                                    magic_response=True, meta={'handle_httpstatus_all': True},
                                    args={'lua_source': self.lua_script})

    def parse_get(self, response):
        item = CrawlerItem()
        item['code'] = response.status
        item['current_url'] = response.url
        item['resources_file_list'] = []
        item['sub_domains_list'] = []
        item['like_admin_login_url'] = False
        item['like_webshell_url'] = False


        if response.status == 200:
            urls = collect_urls_from_html(response.text, response.url)
            title_list = response.xpath('//title/text()').extract()
            item['title'] = None if len(title_list)==0 else title_list[0]
            item['content'] = response.text
        else:
            a = get_request(response.url, cookie=self.cookie)
            item['title'] = a['title']
            item['content'] = a['content']
            urls = collect_urls_from_html(a['content'], response.url)

        if like_admin_login_content(item['content']):
            item['like_admin_login_url'] == True
        if check_url_has_webshell_content(item['current_url'], item['content'], item['code'], item['title'])['y1']:
            item['like_webshell_url'] == True

        if item['current_url']=="http://m.pingan.com/":
            pdb.set_trace()
        yield item

        url_main_target_domain = get_url_belong_main_target_domain(
            self.start_url)

        for url in urls:
            url_templet_list=get_url_templet_list(url)
            url_http_domain = get_http_domain_from_url(url)
            if url=="http://m.pingan.com/":
                pdb.set_trace()
            if url_is_sub_domain_to_http_domain(url, urlparse(url)[0] + "://" + url_main_target_domain) and url_http_domain not in item['sub_domains_list']:
                item['sub_domains_list'].append(url_http_domain)
            if urlparse(url).hostname != self.domain:
                continue
            if url in self.collected_urls:
                continue
            _flag=0
            for _ in url_templet_list:
                if _ in self.collected_urls:
                    _flag=1
                    break
            if _flag==1:
                continue
            
            self.add_url_templet_to_collected_urls(url)

            if "^" in url:
                # post类型url
                post_url_list = url.split("^")
                post_url = post_url_list[0]
                post_data = post_url_list[1]
                yield SplashRequest(post_url, callback=self.parse_post, endpoint='execute',
                                    magic_response=True, meta={'handle_httpstatus_all': True, 'current_url': url},
                                    args={'lua_source': self.lua_script, 'http_method': 'POST',
                                          'body': post_data})
            else:
                # get类型url
                match_resource = re.match(RESOURCE_FILE_PATTERN, url)
                match_logoff = re.search(
                    r"(logout)|(logoff)|(exit)|(signout)|(signoff)", url, re.I)
                if match_resource:
                    item['resources_file_list'].append(url)
                elif match_logoff:
                    pass
                else:
                    if url=="http://m.pingan.com/":
                        pdb.set_trace()
                    yield SplashRequest(url, self.parse_get, endpoint='execute', magic_response=True, meta={'handle_httpstatus_all': True}, args={'lua_source': self.lua_script})

    def parse_post(self, response):
        # post请求
        item = CrawlerItem()
        item['code'] = response.status
        item['resources_file_list'] = []
        item['sub_domains_list'] = []
        title_list = response.xpath('//title/text()').extract()
        item['title'] = None if len(title_list)==0 else title_list[0]
        item['content'] = response.text
        item['current_url'] = response.meta['current_url']
        item['like_admin_login_url'] = False
        item['like_webshell_url'] = False
        if like_admin_login_content(item['content']):
            item['like_admin_login_url'] == True
        if check_url_has_webshell_content(item['current_url'], item['content'], item['code'], item['title'])['y1']:
            item['like_webshell_url'] == True

        if item['current_url']=="http://m.pingan.com/":
            pdb.set_trace()
        yield item
