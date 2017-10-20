#### 数据库设置相关

```
eg.主要目标为http://www.freebuf.com

将生成如下表:
tarets,first_targets,www_freebuf_com_pang,www_freebuf_com_sub
默认主要目标存放在targets表中,first_targets为优先级高的表
也即targets或first_targets表中存放有start_url="http://www.freebuf.com"的项

www_freebuf_com_pang存放www.freebuf.com的旁站列表
www_freebuf_com_sub存放www.freebuf.com的子站列表
www_freebuf_com_pang和www_freebuf_com_sub表中没有http_domain="http://www.freebuf.com"的项

本地文件log/pang/www_freebuf_com_pang.txt和log/sub/www_freebuf_com_sub.txt中都有www.freebuf.com的条目,这两个txt文件的内容为http+domain格式的列表文件

```

#### 相关输出文件

```
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

```
