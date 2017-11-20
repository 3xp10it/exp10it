import re
import sys
import os
from urllib.parse import urlparse
import scrapy
from scrapy_splash import SplashRequest
from crawler.items import CrawlerItem
exp10it_module_path = os.path.abspath(os.path.dirname(
    __file__) + os.path.sep + ".." + os.path.sep + ".." + os.path.sep + "..")
sys.path.insert(0, exp10it_module_path)
from exp10it import collect_urls_from_url
from exp10it import RESOURCE_FILE_PATTERN
from exp10it import collect_urls_from_html
from exp10it import get_request
from exp10it import get_url_cookie
from exp10it import url_is_sub_domain_to_http_domain
from exp10it import get_http_domain_from_url
from exp10it import get_url_belong_main_target_domain
from exp10it import like_admin_login_content
from exp10it import check_url_has_webshell_content
import random
import requests


def get_random_proxy():
    IPPOOL = eval(requests.get(
        "http://192.168.89.190:8000/?types=0&count=50&country=国内").text)
    random_choose = random.choice(IPPOOL)
    proxy_addr = "http://" + \
        str(random_choose[0]) + ":" + str(random_choose[1])

    return [str(random_choose[0]),random_choose[1]]


class Exp10itSpider(scrapy.Spider):
    name = "exp10it"
    collected_urls = []
    domain = ""
    start_url = ""
    a=get_random_proxy()
    print(a)
    lua_script = """
    function main(splash, args)
      assert(splash:go{splash.args.url,http_method=splash.args.http_method,body=splash.args.body})
      assert(splash:wait(0.5))

      splash:on_request(function(request)
          request:set_proxy{
              host = "%s",
              port = %d
          }
      end)

      return splash:html()
    end
    """ % (a[0],a[1])

    def url_has_been_collected(self, url):
        parsed = urlparse(url)
        url_page = parsed[0] + "://" + parsed[1] + \
            (parsed[2] if "^" not in parsed[2] else parsed[2].split('^')[0])
        param_part = parsed[2].split("^")[1] if "^" in url else parsed[4]
        param_list = param_part.split("&")
        pure_param_list = []
        if param_list != ['']:
            for each in param_list:
                each_param_name = each.split("=")[0]
                each_param_value = each.split("=")[1]
                if re.match(r"\d+", each_param_value):
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
                pure_url = url

        if pure_url not in self.collected_urls:
            self.collected_urls.append(pure_url)
            return False
        else:
            return True

    def start_requests(self):
        urls = [
            #'https://www.bing.com'
            #'https://httpbin.org/post^sss=lalala'
            #'http://www.freebuf.com'
            #'http://www.ip138.com/'
            'http://httpbin.org/ip'
            #'http://geekpwn.freebuf.com'
        ]
        self.domain = urlparse(urls[0]).hostname
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
                yield SplashRequest(url, self.parse_get, endpoint='execute',
                                    magic_response=True, meta={'handle_httpstatus_all': True},
                                    args={'lua_source': self.lua_script})

    def parse_get(self, response):
        item = CrawlerItem()
        cookie = get_url_cookie(response.url)
        item['code'] = response.status
        item['current_url'] = response.url
        item['resources_file_list'] = []
        item['sub_domains_list'] = []
        item['like_admin_login_url'] = False
        item['like_webshell_url'] = False

        print(response.text)
        input(444444)

        if response.status == 200:
            input(33333333333)
            urls = collect_urls_from_html(response.text, response.url)
            title = response.xpath('//title/text()').extract()
            item['title'] = title if title != [] else None
            item['content'] = response.text
        else:
            a = get_request(response.url, cookie=cookie)
            item['title'] = a['title']
            item['content'] = a['content']
            urls = collect_urls_from_html(a['content'], response.url)

        if like_admin_login_content(item['content']):
            item['like_admin_login_url'] == True
        if check_url_has_webshell_content(item['current_url'], item['content'], item['code'], item['title'])['y1']:
            item['like_webshell_url'] == True

        yield item

        url_main_target_domain = get_url_belong_main_target_domain(
            self.start_url)
        for url in urls:
            url_http_domain = get_http_domain_from_url(url)
            if url_is_sub_domain_to_http_domain(url, urlparse(url)[0] + "://" + url_main_target_domain) and url_http_domain not in item['sub_domains_list']:
                item['sub_domains_list'].append(url_http_domain)
            if urlparse(url).hostname != self.domain:
                continue
            if self.url_has_been_collected(url):
                continue

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
                    yield SplashRequest(url, self.parse_get, endpoint='execute', magic_response=True, meta={'handle_httpstatus_all': True}, args={'lua_source': self.lua_script})

    def parse_post(self, response):
        # post请求
        item = CrawlerItem()
        item['code'] = response.status
        item['resources_file_list'] = []
        item['sub_domains_list'] = []
        title = response.xpath('//title/text()').extract()
        item['title'] = title if title != [] else None
        item['content'] = response.text
        item['current_url'] = response.meta['current_url']
        item['like_admin_login_url'] = False
        item['like_webshell_url'] = False
        if like_admin_login_content(item['content']):
            item['like_admin_login_url'] == True
        if check_url_has_webshell_content(item['current_url'], item['content'], item['code'], item['title'])['y1']:
            item['like_webshell_url'] == True
        yield item
