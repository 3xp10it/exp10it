import re
import sys
import os
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


class Exp10itSpider(scrapy.Spider):
    name = "exp10it"
    lua_script = """
    function main(splash, args)
      assert(splash:go(args.url))
      assert(splash:wait(0.5))
      return splash:html()
    end
    """

    def start_requests(self):
        urls = [
            'http://192.168.43.190/login.php'
            #'https://www.bing.com'
        ]
        for url in urls:
            yield SplashRequest(url, self.parse, endpoint='execute', magic_response=True, meta={'handle_httpstatus_all': True}, args={'lua_source': self.lua_script})

    def parse(self, response):
        item = CrawlerItem()
        cookie = get_url_cookie(response.url)
        print(6666666666666666)
        print(response.url)
        item['code'] = response.status
        item['current_url'] = response.url
        item['resources_file_list'] = []
        if response.status == 200:
            urls = collect_urls_from_html(response.text, response.url)
            title = response.xpath('//title/text()').extract()
            item['title'] = title if title != [] else None
            item['content'] = response.text
        else:
            a = get_request(response.url, cookie=cookie)
            item['title'] = a['title']
            item['content'] = a['content']
            urls = collect_urls_from_html(a['content'], response.url)
        print(urls)
        for url in urls:
            if "^" in url:
                # post请求
                pass
                # yield SplashPostRequest()
            else:
                # get请求
                match_resource = re.match(RESOURCE_FILE_PATTERN, url)
                match_logoff = re.search(
                    r"(logout)|(logoff)|(exit)|(signout)|(signoff)", url, re.I)
                if match_resource:
                    item['resources_file_list'].append(url)
                elif match_logoff:
                    pass
                else:
                    yield SplashRequest(url, self.parse, endpoint='execute', magic_response=True, meta={'handle_httpstatus_all': True}, args={'lua_source': self.lua_script})
        yield item
