# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    code = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    current_url = scrapy.Field()
    resources_file_list = scrapy.Field()
    # eg.sub_domains_list=['http://wit.freebuf.com']
    sub_domains_list = scrapy.Field()
    like_admin_login_url=scrapy.Field()
    like_webshell_url=scrapy.Field()
