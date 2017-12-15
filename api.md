```
def scan_init():
    # 这个函数用于配置exp10itScanner要用到的参数
def get_start_url_urls_table(start_url):
    # eg.http://www.baidu.com --> www_baidu_com_urls
    # eg.http://www.baidu.com/ --> www_baidu_com_urls
    # eg.http://www.baidu.com/cms/ --> www_baidu_com_cms_urls
    # eg.http://www.baidu.com/1.php --> www_baidu_com_urls
    # eg.http://www.baidu.com/cms --> www_baidu_com_cms_urls
    # eg.http://www.baidu.com/cms/1.php --> www_baidu_com_cms_urls
    # eg.http://www.baidu.com:40711 --> www_baidu_com_40711_urls
    # eg.http://www.baidu.com:40711/cms/1.php --> www_baidu_com_40711_cms_urls
def set_column_name_scan_module_unfinished(column_name, scan_way):
    # set the scan module which has column_name to be unfinished
    # eg,column_name="cdn_scaned"
def database_init():
    # 本地数据库初始化,完成数据库配置和建立数据(数据库和targets+first_targets表),以及目标导入
    # 完成这一步后需要从数据库中按优先级取出没有完成的任务
    # eg.一个目标为http://www.freebuf.com,将它加入到targets表中,targets表中的sqli_scaned等各项标记扫描完成列代
    # 表该目标及其所有旁站对应项的扫描全部完成,在www_freebuf_com_pang表中也有http_domain为
    # http://www.freebuf.com的记录,该表中对应的sqli_scaned等各项标记代表目标
    # http://www.freebuf.com这一个网站的扫描完成情况
def get_one_target_from_db(db, target_table):
    # 从数据库db中的target表中按优先级取出目标
def set_scan_finished(scaned_column_name, db, table, column_name, column_value):
    # 设置相应的扫描完成列值为1代表扫描完成,参数意义同上一个函数
def set_scan_unfinished(scaned_column_name, db, table, column_name, column_value):
    # 设置相应的扫描完成列值为1代表扫描完成,参数意义同上一个函数
def get_main_target_table_name(target):
    # 返回targets或first_targets
    # 得到主要目标的数据库中所在表的名字,结果为eval(get_key_value_from_config_file(CONFIG_INI_PATH,'default','TARGETS_TABLE_NAME'))或eval(get_key_value_from_config_file(CONFIG_INI_PATH,'default','FIRST_TARGETS_TABLE_NAME'))
    # 由于主要目标存放在eval(get_key_value_from_config_file(CONFIG_INI_PATH,'default','TARGETS_TABLE_NAME'))或eval(get_key_value_from_config_file(CONFIG_INI_PATH,'default','FIRST_TARGETS_TABLE_NAME'))当中,所以这样检测
    # target可为domain或http domain格式
def get_source_main_target_domain_of_pang_url(url):
    # 得到旁站所属的doamin
def get_source_main_target_domain_of_sub_url(url):
    # 得到子站url对应的主要目标的域名
    # eg.得到http://wit.freebuf.com/1.php对应的结果为数据库中的www.freebuf.com
    # 返回一个字典,eg.{'domain':'www.freebuf.com','http_domain':'http_domain':'http://www.freebuf.com'}
def get_url_belong_main_target_domain(url):
    # 结合get_source_main_target_domain_of_pang_url和get_source_main_target_domain_of_sub_url函数得到当前url所属
    # 的主目标的域名,如得到http://wit.freebuf.com/1.php的所属主目标为www.freebuf.com
def get_target_table_name_list(start_url):
    # 得到target所在的表名,检索的表包括targets,first_targets,xxx_pang,xxx_sub
    # 返回一个列表,如果target是主要目标,则该列表中只有一个表名,targets或是first_targets
    # 如果target是子站或旁站且该子站如wit.freebuf.com既是子站又是旁站值,则返回的列表中有两个表名,xxx_pang和
    # xxx_sub
def get_target_table_name_info(target):
    # 得到target是主要目标还是旁站或子站
    # 返回值如下
    # 'target_is_main_and_table_is_targets':target_is_main_and_table_is_targets,
    # 'target_is_main_and_table_is_first_targets':target_is_main_and_table_is_first_targets,
    # 'target_is_pang_and_sub':target_is_pang_and_sub,
    # 'target_is_only_pang':target_is_only_pang,
    # 'target_is_only_sub':target_is_only_sub,
    # 'target_is_main':target_is_main_target,
    # 'target_is_pang_or_sub':target_is_pang_or_sub
def get_target_urls_from_db(target, db):
    # 从数据库中得到一个目标爬完虫后的的urls,返回结果是个列表
    # tareget可以是主要目标或者主要目标的旁站或子站
def get_scan_finished(scaned_column_name, db, table, column_name, column_value):
    # 检测扫描是否完成,返回结果为0或1,0代表没有扫描完,1代表扫描完成
    # scaned_column_name代表对应是否扫描完的字段
    # http_domain_value为表的主键值,http_domain列对应的值
def get_url_start_url(url):
    # eg. url=http://www.baidu.com/cms/laal.jsp
    # there are [http://www.baidu.com] and
    # [http://www.baidu.com/cms] in config.ini
    # in this case ,it should return http://www.baidu.com/cms
def single_cdn_scan(target):
    # 扫描cdn情况,如果有cdn则尝试获取真实ip
    # target可以是主要目标或是主要目标的旁站或子站,但是扫描器中第1次运行single_cdn_scan并没有运行到找旁站和
    # 子站的模块,这时target只可能是主要目标,扫描器中第2次运行single_cdn_scan时在获取子站之后,此时主要实际用于针
    # 对子站进行cdn识别
def single_port_scan(target):
    # 这里扫描开放端口与服务情况
    # target可以是主要目标或是主要目标的旁站或子站,但是端口扫描比较特殊,如果target为旁站domain,则不进行端口扫描
    # 因为旁站与主站是同一ip,如果target是子站domain,进行端口扫描
def single_portBruteCrack_scan(target):
    # 这里进行端口暴力破解的扫描
    # target可以是主要目标或是主要目标的旁站或子站,但是旁站不进行端口暴破,子站如果与主要目标ip不同再进行端口暴破

    # 对于主要目标,首先判断主要目标是否已经有开放了的端口信息21,22,3306,1433,3389,如果没有则不进行端口暴破
    # 对于子站目标,首先看ip是否是与主站相同,如果不是再进行21,22,3306,1433,3389端口暴破
def single_whois_scan(target):
    # 这里进行whois信息收集的扫描
    # target可以是主要目标或是主要目标的旁站或子站,但是子站不找whois,旁站找whois
def single_risk_scan(target):
    # 单个target高危exp遍历模块
    # target要求为http(s)+domain格式
    # risk_scan模块对每个target,无论是主要目标的旁站还是子站,都进行详细的判断target是否是主要目标,并在对应的表
    # 中记录risk_scaned的完成状态
    # 这里的target不一定是主要目标,可以是旁站或子站
    # exps目录下的每个目录为不同中高危漏洞对应的检测脚本,需要python3,运行检测脚本后如果对应目录下有result.txt则代
    # 表有对应的漏洞,没有产生result.txt则代表没有对应的漏洞
def get_url_cookie(url):
    # 得到url的cookie,目前为从config.ini文件中获取
    # eg.url=https://www.baidu.com:8080/dvwa/1.php
    # 如果url在config.ini中没有cookie,则查找config.ini中是否有url对应的主站有cookie，如果有对应的主站
    # 有cookie,则用url对应的start_url的cookie
    # 如果没有则返回""空字符串
def get_pang_domains(start_url):
    # 得到target的旁站列表
    # target为如http://www.baidu.com的域名,含http
def get_sub_domains(start_url, use_tool="Sublist3r"):
    # target为http开头+domain
    # 注意target(http://www.baidu.com)要换成如baidu.com的结果,然后再当作参数传入下面可能用的工具中
    # www.baidu.com--->baidu.com,baidu.com是下面工具的参数
    # use_tool为子站获取工具选择
    # Sublist3r工具详情如下
    # 获取子站列表,domain为域名格式,不含http
    # https://github.com/aboul3la/Sublist3r
    # works in python2,use os.system get the execute output
def scrapy_splash_crawl_url(url):
    # replace crawl_url method
def crawl_scan(start_url):
    # target是主要目标
    # 对target目标的爬虫扫描,称为爬虫扫描而不是爬虫是因为这里不只是对一个eg.http://www.freebuf.com的扫描
    # 而是根据SCAN_WAY来对目标以及目标的旁站或子站的爬虫
    # target要求是http格式
def sqli_scan(start_url):
    # 根据SCAN_WAY而采取相应的扫描sqli模式
    # target要求是http...格式,不能是纯domain
def single_xss_scan(start_url):
    # 这里进行xss漏洞检测
    # target可以是主要目标或是主要目标的旁站或子站
def single_script_type_scan(target):
    # 对一个target进行脚本类型识别,这里的target可以为主要目标,也可以为主要目标的旁站或子站
def single_dirb_scan(target):
    # 对一个target进行dirb扫描,这里的target可以为主要目标,也可以为主要目标的旁站或子站
def auto_write_string_to_sql(
        string,
        db_name,
        table_name,
        column_name,
        table_primary_key,
        table_primary_key_value):
    # 自动写内容到数据库中,相比write_string_to_sql函数多了其他相关写内容到数据库的动作
    # 会在将一个column内容写到数据库时将其他的与之相关的可以确定的其他column中的可以填
    # 写的数据填入数据库,eg.targets表中填写http_domain时顺便填写domain
    # eg.urls表中填写url时顺便填写urls表中的http_domain
    # 只多写相同表中的可写的column,不同表中的可写column暂时不写
def crack_webshell(url, anyway=0):
    # webshll爆破,第二个参数默认为0,如果设置不为0,则不考虑判断是否是webshll,如果设置为1,直接按direct_bao方式爆破
    # 如果设置为2,直接按biaodan_bao方式爆破
def single_cms_scan(start_url):
    # 对target根据target的cms类型进行cms识别及相应第三方工具扫描,target可以是主要目标或者是旁站或是子站
def crack_admin_login_url(
        url,
        user_dict_file=ModulePath + "dicts/user.txt",
        pass_dict_file=ModulePath + "dicts/pass.txt",
        yanzhengma_len=0):
    # 这里的yanzhengma_len是要求的验证码长度,默认不设置,自动获得,根据不同情况人为设置不同值效果更好
    # 爆破管理员后台登录url,尝试自动识别验证码,如果管理员登录页面没有验证码,加了任意验证码数据也可通过验证
def single_crack_admin_page_scan(target):
    # 这里爆破所有可能是管理登录的页面,普通用户登录页面也爆破
    # target可以是主要目标或是主要目标的旁站或子站
    # dirb后缀扫描后与爬虫获得的url联合找出可疑登录页面,并进行爆破
def get_http_pang_domains_list_from_db(target, db):
    # 从数据库中获取主要目标的旁站列表
    # target要是主要目标
def get_http_sub_domains_list_from_db(target, db):
    # 从数据库中获取主要目标的子站列表
    # target要是主要目标
def set_target_scan_finished(start_url):
    # 根据扫描模式设置扫描完成
def auto_attack(start_url):
    # 自动化检测target流程
    # 根据扫描模式进行cdn情况扫描,如果有cdn,尝试获取真实ip
    # cdn模块的结果影响端口扫描模块,也影响是否进行旁站获取,cdn模块在获取旁站模块前要运行一次,
    # 在获取子站模块后要再运行一次,第1次是为了给是否获取旁站提供指导,第2次是为了给子站获取真实ip,给端口扫描子站
    # 提供指导
def exp10itScanner():
    # 相当于扫描工具的main函数
```
