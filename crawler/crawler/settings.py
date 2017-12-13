# -*- coding: utf-8 -*-

# Scrapy settings for crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import os,sys
import requests
exp10it_module_path = os.path.expanduser("~")+"/mypypi"
sys.path.insert(0, exp10it_module_path)

from scrapy.spiders import Spider
from exp10it import CONFIG_INI_PATH
from exp10it import get_key_value_from_config_file
from exp10it import update_config_file_key_value

try:
    SPLASH_URL = eval(get_key_value_from_config_file(
        CONFIG_INI_PATH, 'default', 'splash_url'))
except:
    print("make sure you have start your scrapy_splash service,if not,do it now")
    SPLASH_SERVER=input("Please input your scrapy_splash server ip address\n:>")
    SPLASH_URL="http://"+SPLASH_SERVER+":8050"
    rsp=requests.get(SPLASH_URL)
    if rsp.status_code!=200:
        input("Attention! "+SPLASH_URL+" seems doesn't online,check it and press any key to continue...")
    update_config_file_key_value(CONFIG_INI_PATH, 'default', 'SPLASH_URL', "'" +SPLASH_URL+"'")


try:
    IPProxyPoolUrl= eval(get_key_value_from_config_file(
        CONFIG_INI_PATH, 'default', 'ipproxypoolurl'))
except:
    print("make sure you have start your IPProxyPool service,if not,do it now")
    IPProxyPoolServer=input("Please input your IPProxyPool server ip address\n:>")

    IPProxyPoolUrl="http://"+IPProxyPoolServer+":8000/?types=0&count=50"
    rsp=requests.get(IPProxyPoolUrl)
    if rsp.status_code!=200:
        input("Attention! "+IPProxyPoolUrl+" seems doesn't online,check it and press any key to continue...")
    update_config_file_key_value(CONFIG_INI_PATH, 'default', 'IPProxyPoolURL', "'" +IPProxyPoolUrl+"'")


BOT_NAME = 'crawler'

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    #'crawler.middlewares.ProxyMiddleware': 843,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'crawler.middlewares.CrawlerSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'crawler.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'crawler.pipelines.CrawlerPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
