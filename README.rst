#### 数据库设置相关:

eg.主要目标为http://www.freebuf.com

1.targets或first_targets表中存放有http_domain="http://www.freebuf.com"的项,且表中的sub_domains和pang_domains中
  没有www.freebuf.com

2.www_freebuf_com_pang和www_freebuf_com_sub表中没有http_domain="http://www.freebuf.com"的项

3.本地文件pang/www_freebuf_com_pang.txt和sub/www_freebuf_com_sub.txt中都有www.freebuf.com的条目,其中
  www_freebuf_com_pang.txt中为http+domain形式,www_freebuf_com_sub.txt中没有http,只有纯domain,因为sub domains是由
  第三方工具获得的,如果需要可后期添加

#### 工具框架流程方案

1>pang_get(获取旁站模块)
2>sub_get(获取子站模块)
3>crawl(爬虫模块)
4>risk_scan(高危漏洞扫描模块)
5>sqli_scan(sql注入扫描模块)
6>dirb_scan(目录扫描模块)
7>cms_scan(cms信息相关模块)
8>crack_scan(爆破模块)


#### 输出文件

get_pang_domains:
	log/pang
get_sub_domains:
	log/sub
dirb:
	log/dirsearch_log/www.freebuf.com_log.txt

cms_scan
	dzscan
		log/cms_scan_log_/dzscan/www.freebuf.com.log
	joomscan
		log/cms_scan_log/joomscan/www.freebuf.com-joexploit.txt
	wpscan
		log/cms_scan_log/wpscan/www.freebuf.com.txt

