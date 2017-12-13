# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from exp10it import get_url_belong_main_target_domain
from exp10it import get_target_table_name_info
from exp10it import get_http_domain_from_url
from exp10it import get_url_start_url
from exp10it import DB_NAME
from exp10it import TARGETS_TABLE_NAME
from exp10it import FIRST_TARGETS_TABLE_NAME
from exp10it import execute_sql_in_db
from exp10it import LOG_FOLDER_PATH
from exp10it import write_string_to_sql
from exp10it import get_start_url_urls_table
from urllib.parse import urlparse
import re

class CrawlerPipeline(object):
    def process_item(self, item, spider):
        current_url = item['current_url']
        parsed=urlparse(current_url)
        hostname=parsed.hostname
        code = item['code']
        title = item['title']
        content = item['content']

        if "^" in current_url:
            pure_url=current_url.split("^")[0]
        else:
            pure_url=current_url

        http_domain=get_http_domain_from_url(current_url)
        main_target_domain = get_url_belong_main_target_domain(pure_url)
        pang_table_name = main_target_domain.replace(".","_")+"_pang"
        sub_table_name =main_target_domain.replace(".","_")+"_sub"

        target_table_info = get_target_table_name_info(current_url)

        if not target_table_info['target_is_pang_or_sub']:
            url_start_url=get_url_start_url(pure_url)
            url_table_name=get_start_url_urls_table(url_start_url)
        else:
            url_table_name=get_http_domain_from_url(pure_url).split("/")[-1].replace(".","_")+"_urls"


        # 1.write [current_url],[code],[title],[content],[like_admin_login_url],[like_webshell_url] to database
        primary_key="url"
        primary_value=current_url
        write_string_to_sql(str(code), DB_NAME, url_table_name,
                'code', primary_key, primary_value)
        write_string_to_sql(title, DB_NAME, url_table_name,
                'title', primary_key, primary_value)
        write_string_to_sql(content, DB_NAME, url_table_name,
                'content', primary_key, primary_value)
        if item['like_admin_login_url']:
            write_string_to_sql('1', DB_NAME, url_table_name,
                    'like_admin_login_url', primary_key, primary_value)
        if item['like_webshell_url']:
            write_string_to_sql('1', DB_NAME, url_table_name,
                    'like_webshell_url', primary_key, primary_value)

        # 2.write [resources_file_list],[like_admin_login_urls] && [like_webshell_urls],[sub_domains_list] to database

        # write [resources_file_list]
        if target_table_info['target_is_pang_or_sub'] and not target_table_info['target_is_pang_and_sub']:
            _table_name=pang_table_name if target_table_info['target_is_only_pang'] else sub_table_name
            _table_name_list=[_table_name]
            primary_key='http_domain'
            primary_value=http_domain
        elif target_table_info['target_is_pang_and_sub']:
            _table_name_list=[pang_table_name,sub_table_name]
            primary_key='http_domain'
            primary_value=http_domain
        elif target_table_info['target_is_main_and_table_is_targets']:
            _table_name_list=[TARGETS_TABLE_NAME]
            primary_key='start_url'
            primary_value=url_start_url
        elif target_table_info['target_is_main_and_table_is_first_targets']:
            _table_name_list=[FIRST_TARGETS_TABLE_NAME]
            primary_key='start_url'
            primary_value=url_start_url
        for each in item['resources_file_list']:
            for each_table in _table_name_list:
                auto_write_string_to_sql(each,DB_NAME,each_table,"resource_files",primary_key,primary_value)

        # write [like_admin_login_urls] and [like_webshell_urls]
        for each_table in _table_name_list:
            if item['like_admin_login_url']:
                    auto_write_string_to_sql(current_url,DB_NAME,each_table,"like_admin_login_urls",primary_key,primary_value)
            if item['like_webshell_url']:
                    auto_write_string_to_sql(current_url,DB_NAME,each_table,"like_webshell_urls",primary_key,primary_value)

        # write [sub_domains_list] to database
        if target_table_info['target_is_main']:
            if not re.match(r"(\d+\.){3}\d+",hostname):
                _result=execute_sql_in_db("select http_domain from %s" % sub_table_name,DB_NAME)
                exist_sub_domains_list=[]
                for each in _result:
                    exist_sub_domains_list.append(each[0])
                for each in item['sub_domains_list']:
                    if each not in exist_sub_domains_list:
                        # write to database
                        sql="insert ignore into `%s`(http_domain,domain) values('%s','%s')" % (sub_table_name,each,each.split("/")[-1])
                        execute_sql_in_db(sql,DB_NAME)
                        # write to config.ini
                        if not os.path.exists(LOG_FOLDER_PATH):
                            os.system("mkdir %s" % LOG_FOLDER_PATH)
                        if not os.path.exists("%s/sub" % LOG_FOLDER_PATH):
                            os.system("cd %s && mkdir sub" % LOG_FOLDER_PATH)
                        os.system(
                            "echo %s >> %s" %
                            (each.split("/")[-1], LOG_FOLDER_PATH + "/sub/" + sub_table_name + ".txt"))


        else:
            pass

        return item
