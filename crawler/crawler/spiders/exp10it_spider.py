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
      assert(splash:go{splash.args.url,http_method=splash.args.http_method,body=splash.args.body})
      assert(splash:wait(0.5))
      return splash:html()
    end
    """

    def start_requests(self):
        urls = [
            'https://www.bing.com'
            #'https://httpbin.org/post^sss=lalala'
        ]
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
        for url in urls:
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
        yield item

    def parse_post(self, response):
        # post请求
        item = CrawlerItem()
        item['code'] = response.status
        item['resources_file_list'] = []
        title = response.xpath('//title/text()').extract()
        item['title'] = title if title != [] else None
        item['content'] = response.text
        item['current_url'] = response.meta['current_url']
        yield item
