# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from exp10it import get_url_belong_main_target_domain
from exp10it import get_target_table_name_info


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        current_url = item['current_url']
        code = item['code']
        title = item['title']
        content = item['content']
        if "^" in current_url:
            pure_url=current_url.split("^")[0]
        eles:
            pure_url=current_url
        main_target_domain = get_url_belong_main_target_domain(pure_url)
        pang_table_name =
        sub_table_name =
        url_table_name = get_http_domain_from_url(
            current_url).split("/")[-1].replace(".", "_") + "_urls"
        target_table_info = get_target_table_name_info(current_url)
        if target_table_info['target_is_main_and_table_is_targets']:
        if target_table_info['target_is_main_and_table_is_first_targets']:
        if target_table_info['target_is_only_pang']:
        if target_table_info['target_is_only_sub']:
        if target_table_info['target_is_pang_and_sub']:

        primary_key =
        primary_value =
        write_string_to_sql(str(code), DB_NAME, url_table_name,
                            'code', primary_key, primary_value)
        return item
