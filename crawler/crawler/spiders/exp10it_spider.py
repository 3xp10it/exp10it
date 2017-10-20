import re
import scrapy
from scrapy_splash import SplashRequest
from exp10it import collect_urls_from_url
from exp10it import RESOURCE_FILE_PATTERN

class Exp10itSpider(scrapy.Spider):
    name = "exp10it"

    def start_requests(self):
        urls = [
                'http://192.168.8.240:8000/xxxx'
        ]
        for url in urls:

            #yield SplashRequest(url, self.parse, args={'wait': 0.5, 'dont_redirect': True},meta={'handle_httpstatus_all': True})
            #yield scrapy.Request(url, self.parse, meta={'handle_httpstatus_all': True})
            yield scrapy.Request(url, self.parse, meta={'handle_httpstatus_all': True,'splash': {
                'args': {
                    'html': 1,
                    'png': 1,
                    },
                'splash_url': url
            }
            }
            )


    def parse(self, response):
        input("start .........")
        print("status code is:\n")
        #input(response.code)
        print("body is:\n")
        #input(response.body)
        help(response.meta)
        print(response.meta)
        input(6666666)
        urls=collect_urls_from_url(response.url)['y1']
        for url in urls:
            '''
            # 两类url不访问
            if re.search(r"(logout)|(logoff)|(exit)|(signout)|(signoff)", url, re.I):
                print("current url is:%s,I will not crawl this url" % url)
                continue
            if re.match(RESOURCE_FILE_PATTERN, each):
                if each not in resource_files:
                    # 资源类型文件不放入任务队列里,直接写到数据库中
                    resource_files.append(each)
                    if url_belong_to_main_target[0]:
                        auto_write_string_to_sql(each,DB_NAME,table_name[0],"resource_files","http_domain",http_domain)
                    else:
                        for each_table in current_not_main_target_table_name:
                            auto_write_string_to_sql(each, DB_NAME, each_table, "resource_files", "http_domain", http_domain)
                continue

            # 正常递归爬取
            a=SplashRequest(url, self.parse, args={'wait': 0.5})
            help(a)
            input(6666666)
            yield a
            '''
            pass
