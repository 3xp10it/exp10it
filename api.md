def moduleExist(moduleName):
    # 检测python模块是否已经安装
    # 有则返回True
    # 无则返回False
def get_string_from_command(command):
    # 不能执行which nihao,这样不会有输出,可nihao得到输出
    # 执行成功的命令有正常输出,执行不成功的命令得不到输出,得到输出为"",eg.command=which nihao
    # 判断程序有没有已经安装可eg.get_string_from_command("sqlmap --help")
def getModulePath():
    # 得到当前文件的路径
def getHomePath():
    # python在os.path.exists("~")时不认识~目录,于是写出这个函数
    # open("~/.zshrc")函数也不认识~
    # 但是os.system认识~,可能只有os.system认识
    # 也即操作系统认识~,但是python不认识~
    # macOS下的~是/var/root,ubuntu下的~是/root
    # 返回~目录的具体值,eg./var/root
    #a=get_string_from_command("cd ~ && pwd")
    # 后来发现os.path.expanduser函数可以认识~
def string2argv(string):
    # 将string转化成argv格式
    # 返回一个列表
    # eg:
    # -u 'http://1.php' --dbms=mysql -v 3将转化成:
    # ['-u','http://1.php','--dbms','mysql','-v','3']
    # 最后将--url转化成-u,因为sqlmap中需要
def param2argv(paramList):
    # 将形如['-u','http://a b1.php','--dbms=mysql','-v','3']转化成
    #['-u','http://a b1.php','--dbms','mysql','-v','3']
    # 最后将--url转化成-u,因为sqlmap中需要
def install_scrapy():
    # ubuntu 16.04下安装scrapy
def install_medusa():
    # linux mint下安装medusa
    # 下面用于支持ssh爆破
def fileOutofDate(file, checkTime=3):
    # 文件距离上次修改后到现在为止经过多久,如果超过checkTime的天数则认为文件过期,返回True
    # 如果没有超过3天则认为文件没有过期,返回False
def tab_complete_file_path():
    # this is a function make system support Tab key complete file_path
    # works on linux,it seems windows not support readline module
def seconds2hms(seconds):
    # 将秒数转换成时分秒
    # 返回类型为str类型
def figlet2file(logo_str, file_abs_path, print_or_not):
    # 输出随机的logo文字到文件或屏幕,第二个参数为0时,只输出到屏幕
    # apt-get install figlet
    # man figlet
    # figure out which is the figlet's font directory
    # my figlet font directory is:
    # figlet -I 2,output:/usr/share/figlet
def oneline2nline(oneline, nline, file_abs_path):
    # 将文件中的一行字符串用多行字符串替换,调用时要将"多行字符串的参数(第二个参数)"中的换行符设置为\n
def lin2win(file_abs_path):
    # 将linux下的文件中的\n换行符换成win下的\r\n换行符
def getCainKey(lstFile):
    # 参数为cain目录下的包含用户名口令的文件,eg.pop3.lst,imap.lst,smtp.lst,http.lst,ftp.lst...
    # 效果为在程序当前目录下生成一个xxx-cainOutPut.txt为整理后的文件
def get_all_file_name(folder, ext_list):
    # ext_list为空时,得到目录下的所有文件名,不返回空文件夹名
    # ext_list为eg.['jpg','png']
    # 返回结果为文件名列表,不是完全绝对路径名
    # eg.folder="~"时,当~目录下有一个文件夹a,一个文件2.txt,a中有一个文件1.txt
    # 得到的函数返回值为['a/1.txt','2.txt']
def save2github(file_abs_path, repo_name, comment):
    # 将文件上传到github
    # arg1:文件绝对路经
    # arg2:远程仓库名
    # 提交的commit注释
def get_os_type():
    # 获取操作系统类型,返回结果为"Windows"或"Linux"
def post_request(url, data):
    # 发出post请求
    # 第二个参数是要提交的数据,要求为字典格式
    # 返回值为post响应的html正文内容,返回内容为str类型
    # print("当前使用的data:")
    # print(data)
def get_random_ua():
    # 得到随机user-agent值
def get_random_x_forwarded_for():
    # 得到随机x-forwarded-for值
def get_list_page(listurl="http://www.xicidaili.com/nt/"):
    # 获取列表页数
def check_banned(url):
    # 检测当前ip是否被拉黑
def get_proxy_list():
    # 尝试一直获取并初步验证代理,直到得到10个代理
def get_one_useful_proxy():
    # 相比get_one_proxy函数,这个函数得到的是经过验证的有效的代理
def get_request(url, by="MechanicalSoup", proxyUrl="", cookie="", delaySwitcher=1):
    # 如果用selenium,用firefox打开可直接访问,要是用ie或chrome打开则要先安装相应浏览器驱动
    # 默认用MechanicalSoup方式访问url
    # 发出get请求,返回值为一个字典,有三个键值对:eg.{"code":200,"title":None,"content":""}
    # code是int类型
    # title如果没有则返回None,有则返回str类型
    # content如果没有则返回""
    # by是使用方法,有两种:MechanicalSoup|chromedriver
    # https://github.com/hickford/MechanicalSoup
    # selenium+chromedriver,chromedriver不能得到code,默认用MechanicalSoup方法
    # delaySwitcher用于设置当前调用get_request函数时是否要按照延时设置来延时,如果设置为0则不需要延时,这种情况用于
def keepSession(url, cookie):
    # 保持服务器上的session长久有效
def get_response_key_value_from_url(url):
    # 得到url响应的关键参数的值
    # 包括:响应状态码,url的title,响应的html内容
    # 发出get请求,返回值为一个字典,有三个键值对:eg.{"code":200,"title":None,"content":content}
    # code是int类型
    # title如果没有则返回None,有则返回str类型
    # content如果没有则返回""
def get_urls_from_file(file):
    # 从文件中获取所有url
def get_title_from_file(file):
    # 等到文件中的所有url对应的title
def newscript():
    # 快速写脚本,加logo,写完后可选上传到github
def blog():
    # 便捷写博客(jekyll+github)函数
def get_remain_time(
        start_time,
        biaoji_time,
        remain_time,
        jiange_num,
        changing_var,
        total_num):
    # 显示完成一件事所需时间
    # start_time是开始进行时的时间变量
    # biaoji_time是用来标记每次经过jiange_num次数后的时间标记,biaoji_time是个"对当前函数全局"变量
    # remain_time是每隔jiange_num次后计算出的当前剩余完成时间
    # jiange_num是每间隔多少次计算处理速度
    # changing_var是会变化(从0到total_num)的变量
    # total_num是一件事的所有的次数
    # eg.show_remain_time(start[0],biaoji[0],temp_remain_time[0],20,current_num,230000)
def hunxiao(folder_path):
    # 改变md5函数,简单的cmd命令达到混淆效果,可用于上传百度网盘
    # 只适用于windows平台
def check_string_is_ip(string):
    # 检测输入的字符串是否是ip值,如果是则返回True,不是则返回False
def check_string_is_domain(string):
    # 检测输入的字符串是否是域名格式,如果是则返回True,不是则返回False
def config_file_has_key_value(file, section, key_name):
    # 检测配置文件中的节点中的键有没有具体值
    # 节点中没有键或键的值为空返回False
    # 否则返回True
def update_file_key_value(file, key_name, sep, key_value):
    # 更新文件中的关键字的值
    # key_name中没有单双引号
    # sep为=或:
def update_config_file_key_value(file, section, key_name, key_value):
    # 通过configparser模块的调用更新配置文件
    # section是[]里面的值
def get_key_value_from_file(key, separator, file_abs_path):
    # 从文件中获取指定关键字的值,第一个参数为关键字,第二个参数为分隔符,第三个参数为文件绝对路径
    # 默认设置分隔符为":"和"="和" "和"    ",如果使用默认分隔符需要将第二个参数设置为'',也即无字符
    # 如果不使用默认分隔符,需要设置第二个参数为string类型如"="
    # 如果不存在对应的关键字则返回0
def execute_sql_in_db(sql, db_name="mysql"):
    # 执行数据库命令
    # 返回值为fetchone()的返回值
def write_string_to_sql(
        string,
        db_name,
        table_name,
        column_name,
        table_primary_key,
        table_primary_key_value):
    # eg.write_string_to_sql("lll","exp10itdb","targets","scan_result","http_domain","https://www.baidu.com")
    # eg.write_string_to_sql(1,"exp10itdb","urls","cracked_admin_login_url","url",current_url)
    # 将string写入数据库
    # argv[1]:要写入的string
    # argv[2]:操作的数据库名
    # argv[3]:操作的表名
    # argv[4]:操作的列名
    # argv[5]:表的主键,默认为''(空)
    # argv[6]:表的主键值,默认为''(空)
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
def get_http_domain_pattern_from_url(url):
    # eg.从http://www.baidu.com/1/2.php中得到http://www.baidu.com的正则匹配类型
    # 也即将其中的.替换成\.
def check_webshell_url(url):
    # 检测url是否为webshell,并检测是webshell需要用html中搜索到的表单爆破还是用一句话类型爆破方式爆破
    # 返回结果为一个字典,有3个键值对
    # 第一个键为是否是webshell,用y1表示,y1为True或者False
    # 第二个键为webshell爆破方式,用y2表示
    # y2的值可能是
    # 1>"biaodan_bao"(根据搜到的表单爆)
    # 2>"direct_bao"(直接爆)
    # 3>""(空字符串,对应url不是webshell)
    # 4>"bypass"(对应url是一个webshll,且该webshell不用输入密码即可控制)
    # 第三个键为在http_get请求url所得的三个关键元素:code,title,content
def get_webshell_suffix_type(url):
    # 获取url所在的webshell的真实后缀类型,结果为asp|php|aspx|jsp
def get_http_domain_from_url(url):
    # eg.http://www.baidu.com/1/2/3.jsp==>http://www.baidu.com
def get_http_netloc_from_url(url):
    # eg.http://www.baidu.com:8080/1/2/3.jsp==>http://www.baidu.com:8080
    # eg.http://www.baidu.com:80/1/2/3.jsp==>http://www.baidu.com
def get_user_and_pass_form_from_html(html):
    # 从html内容(管理员登录的html)中获取所有的form表单
    # 返回结果为一个字典,包含3个键值对
    #"user_form_name":"" 没有则相应返回值为"None",不是返回""(空字符串)
    #"pass_form_name":"" 没有则相应返回值为"None",不是返回""(空字符串)
    #"form_action_url":"" 没有则相应返回值为"None",不是返回""(空字符串)
def get_user_and_pass_form_from_url(url):
    # 从url的get请求中获取所有form表单
    # 返回结果为一个字典,包含3个键值对
    #"user_form_name":"" 没有则相应返回值为None,不是返回""(空字符串)
    #"pass_form_name":"" 没有则相应返回值为None,不是返回""(空字符串)
    #"response_key_value":value 这个value的值是一个字典,也即get_response_key_value_from_url函数的返回结果
    # 之所以要每次在有访问url结果的函数里面返回url访问结果,这样是为了可以只访问一次url,这样就可以一直将访问的返\
    # 回结果传递下去,不用多访问,效率更高
def get_yanzhengma_form_and_src_from_url(url):
    # 得到url对应的html中的验证码的表单名和验证码src地址
def crack_ext_direct_webshell_url(url, pass_dict_file, ext):
    # 爆破php|asp|aspx|jsp的一句话类型的webshell
    # 表单形式爆破的webshell爆破起来方法一样,不用分类
    # 一句话形式的webshell爆破需要根据后缀对应的脚本的语法的不同来爆破
def jieDiQi_crack_ext_direct_webshell_url(url, pass_dict_file, ext):
    # 爆破php|asp|aspx|jsp的一句话类型的webshell
    # 表单形式爆破的webshell爆破起来方法一样,不用分类
    # 一句话形式的webshell爆破需要根据后缀对应的脚本的语法的不同来爆破
def crack_admin_login_url(
        url,
        user_dict_file=ModulePath + "dicts/user.txt",
        pass_dict_file=ModulePath + "dicts/pass.txt",
        yanzhengma_len=0):
    # 这里的yanzhengma_len是要求的验证码长度,默认不设置,自动获得,根据不同情况人为设置不同值效果更好
    # 爆破管理员后台登录url,尝试自动识别验证码,如果管理员登录页面没有验证码,加了任意验证码数据也可通过验证
def crack_allext_biaodan_webshell_url(url, user_dict_file, pass_dict_file):
    # 爆破表单类型的webshell
    # 表单类型的webshell爆破方法一样,不用分不同脚本类型分别爆破
def crack_webshell(url, anyway=0):
    # webshll爆破,第二个参数默认为0,如果设置不为0,则不考虑判断是否是webshll,如果设置为1,直接按direct_bao方式爆破
    # 如果设置为2,直接按biaodan_bao方式爆破
def exist_database(db_name):
    # 检测db_name名字的数据库是否存在
    # 存在返回True,否则返回False
def exist_table_in_db(table_name, db_name):
    # 检测数据库中存在表,存在返回True,否则返回False
def database_init():
    # 本地数据库初始化,完成数据库配置和建立数据(数据库和targets+first_targets表),以及目标导入
    # 完成这一步后需要从数据库中按优先级取出没有完成的任务
    # eg.一个目标为http://www.freebuf.com,将它加入到targets表中,targets表中的sqli_scaned等各项标记扫描完成列代
    # 表该目标及其所有旁站对应项的扫描全部完成,在www_freebuf_com_pang表中也有http_domain为
    # http://www.freebuf.com的记录,该表中对应的sqli_scaned等各项标记代表目标
    # http://www.freebuf.com这一个网站的扫描完成情况
def get_value_from_url(url):
    # 返回一个字典{'y1':y1,'y2':y2}
    # eg.从http://www.baidu.com/12/2/3.php?a=1&b=2中得到
    #'y1':"http://www.baidu.com/12/2/3.php"
    #'y2':"http://www.baidu.com/12/2"
def collect_urls_from_url(url):
    # 从url所在的html内容中收集url到url队列
    # 返回值是一个字典,{'y1':y1,'y2':y2}
    # y1是根据参数url得到的html页面中的所有url,是个列表类型
    # y2是参数url对应的三个关键元素,y2是个字典类型,eg.{"code":200,"title":None,"content":""}
    # 包括收集没有http_domain前缀的uri,src属性中的uri等
    # 整理uri,暂时不做带参数的uri变成不带参数的页面
    # eg.http://www.baidu.com/nihao?a=1&b=2为http://www.baidu.com/nihao
    # 后期可将带参数的uri根据参数fuzz,用于爆路径,发现0day等
def like_admin_login_content(html):
    # 根据html内容判断页面是否可能是管理员登录页面
def like_admin_login_url(url):
    # 判断url对应的html内容是否可能是管理员登录页面
def get_domain_key_value_from_url(url):
    # 从url中得到域名的关键值
    # eg.从http://www.baidu.com中得到baidu
def crawl_url(url):
    # 爬虫,可获取url对应网站的所有可抓取的url和所有网页三元素:code,title,content
def crawl_scan(target):
    # target是主要目标
    # 对target目标的爬虫扫描,称为爬虫扫描而不是爬虫是因为这里不只是对一个eg.http://www.freebuf.com的扫描
    # 而是根据scan_way来对目标以及目标的旁站或子站的爬虫
    # target要求是http格式
def get_yanzhengma_from_pic(img, cleanup=True, plus=''):
    # 调用系统安装的tesseract来识别验证码
    # cleanup为True则识别完成后删除生成的文本文件
    # plus参数为给tesseract的附加高级参数
    # print get_string_from_yanzhengma('2.jpg')  # 打印识别出的文本,删除txt文件
    # print get_string_from_yanzhengma('2.jpg', False)  # 打印识别出的文本,不删除txt文件
    # print get_string_from_yanzhengma('2.jpg', False, '-l eng')  #
    # 打印识别出的文本,不删除txt文件,同时提供高级参数
def get_string_from_url_or_picfile(url_or_picfile):
    # 从url或图片文件中得到验证码,不支持jpeg,支持png
def mail_msg_to(msg, mailto='config', subject='test', user='config', password='config', format='plain'):
    # 使用163的邮箱发送邮件
    # msg是要发送的string
    # mailto是发送的目标邮箱地址
    # subject是主题名
    # user,password是用户名密码,其中user要带上邮箱地址后缀
def get_input_intime(default_choose, timeout=10):
    # http://www.cnblogs.com/jefferybest/archive/2011/10/09/2204050.html
    # 在一定时间内得到选择的值,如果没有选择则返回默认选择
    # 第一个参数为默认选择值
    # 第二个参数为设置超时后自动选择默认值的时间大小,单位为秒
    # 返回选择的值,返回值是选择的值或是默认选择值,选择的值为str类型,默认的选择值可为任意类型
    # 无法输入长字符串,适用于只输入1-2个字符长度的字符串,一般用于选项的选择
def checkvpn():
    # 检测vpn是否连接成功
def ableConnectSite(site):
    # 检测与site之间是否能成功连接
def get_source_main_target_domain_of_pang_url(url):
    # 得到旁站所属的doamin
def get_source_main_target_domain_of_sub_url(url):
    # 得到子站url对应的主要目标的域名
    # eg.得到http://wit.freebuf.com/1.php对应的结果为数据库中的www.freebuf.com
    # 返回一个字典,eg.{'domain':'www.freebuf.com','http_domain':'http_domain':'http://www.freebuf.com'}
def get_url_belong_main_target_domain(url):
    # 结合get_source_main_target_domain_of_pang_url和get_source_main_target_domain_of_sub_url函数得到当前url所属
    # 的主目标的域名,如得到http://wit.freebuf.com/1.php的所属主目标为www.freebuf.com
def get_sqlmap_result_and_save_result(url):
    # 得到sqlmap对url对应target的扫描结果,并将相关结果存入数据库
    # url可以是包含http形式的url，也可以是纯domain形式
    # py3
    # 这个import有可能会因为最开始有过import相同文件的动作而两次的文件不同,导致自己的罗辑错误
    # 这里的import要求是有配置参数的config
def get_scan_finished(scaned_column_name, db, table, http_domain_value):
    # 检测扫描是否完成,返回结果为0或1,0代表没有扫描完,1代表扫描完成
    # scaned_column_name代表对应是否扫描完的字段
    # http_domain_value为表的主键值,http_domain列对应的值
def set_scan_finished(scaned_column_name, db, table, http_domain_value):
    # 设置相应的扫描完成列值为1代表扫描完成,参数意义同上一个函数
def set_scan_unfinished(scaned_column_name, db, table, http_domain_value):
    # 设置相应的扫描完成列值为1代表扫描完成,参数意义同上一个函数
def get_one_target_from_db(db, target_table):
    # 从数据库db中的target表中按优先级取出目标
def searchKeyWords(keyWords, by='bing'):
    # 通过搜索引擎搜索关键字
    # 返回搜索得到的html页面
    # 默认用bing搜索引擎
def get_http_or_https_from_search_engine(domain):
    # 从搜索引擎中得到domain是http还是https
def get_http_or_https(domain):
    # 获取domain对应的scheme,如获取www.baidu.com对应的scheme为https,此功能待完善
    # 如果首先请求http成功,则认为是http,不再去看https,因为https有可能是cdn强加的,而它本身是http
    # 不连接vpn访问http://{domain}无法访问,访问https://{domian}却可以访问,这样的情况下可能是这个domain被GFW拦截了
    #.这样的话用exp10it.py模块中的get_http_or_https会得到是https
    # 连接vpn访问http://{domain}可以正常访问,访问https://{domain}也可以正常访问,这样的情况下可能是cdn强制给
    # domain加的https[eg.cloudflare].这样的话用exp10it.py模块中的get_http_or_https会得到http
    # 因此,在尝试获取domain的cdn背后的真实ip时,exp10it.py模块中的get_http_or_https可能因此而受干扰[GFW+cdn]
    # 因此,修改exp10it.py模块中的get_http_or_https函数,先用baidu[site:{domain}]这样查一下对方是http还是https,如果
    # 得不到再用原来get_http_or_https的方法继续

    # 首先由搜索引擎尝试获取
def getIp(domain):
    # 从domain中获取ip
def get_pure_list(list):
    # this is a function to remove \r\n or \n from one sting
    # 得到域名列表
def save_url_to_file(url_list, name):
    # this is my write url to file function:
def bing_search(query, search_type):
    # the main function to search use bing api
    # search_type: Web, Image, News, Video
def get_ip_domains_list(ip):
    # 不再用bing接口查询旁站
def get_pang_domains(target):
    # 得到target的旁站列表
    # target为如http://www.baidu.com的域名,含http
def get_root_domain(domain):
    # 得到domain的根域名,eg.www.baidu.com得到baidu.com
    # domain可为http开头或纯domain,不能是非http://+domain的url
def get_sub_domains(target, use_tool="Sublist3r"):
    # target为http开头+domain
    # 注意target(http://www.baidu.com)要换成如baidu.com的结果,然后再当作参数传入下面可能用的工具中
    # www.baidu.com--->baidu.com,baidu.com是下面工具的参数
    # use_tool为子站获取工具选择
    # Sublist3r工具详情如下
    # 获取子站列表,domain为域名格式,不含http
    # https://github.com/aboul3la/Sublist3r
    # works in python2,use os.system get the execute output
def get_main_target_table_name(target):
    # 返回targets或first_targets
    # 得到主要目标的数据库中所在表的名字,结果为eval(get_key_value_from_config_file(configIniPath,'default','targets_table_name'))或eval(get_key_value_from_config_file(configIniPath,'default','first_targets_table_name'))
    # 由于主要目标存放在eval(get_key_value_from_config_file(configIniPath,'default','targets_table_name'))或eval(get_key_value_from_config_file(configIniPath,'default','first_targets_table_name'))当中,所以这样检测
    # target可为domain或http domain格式
def get_target_table_name_list(target):
    # 得到target所在的表名,检索的表包括targets,first_targets,xxx_pang,xxx_sub
    # 返回一个列表,如果target是主要目标,则该列表中只有一个表名,targets或是first_targets
    # 如果target是子站或旁站且该子站如wit.freebuf.com既是子站又是旁站值,则返回的列表中有两个表名,xxx_pang和
    # xxx_sub
def get_target_table_name_info(target):
    # 得到target是主要目标还是旁站或子站
    # 返回值如下
    #'target_is_main_and_table_is_targets':target_is_main_and_table_is_targets,
    #'target_is_main_and_table_is_first_targets':target_is_main_and_table_is_first_targets,
    #'target_is_pang_and_sub':target_is_pang_and_sub,
    #'target_is_only_pang':target_is_only_pang,
    #'target_is_only_sub':target_is_only_sub
def get_target_urls_from_db(target, db):
    # 从数据库中得到一个目标爬完虫后的的urls,返回结果是个列表
    # tareget可以是主要目标或者主要目标的旁站或子站
def single_cdn_scan(target):
    # 扫描cdn情况,如果有cdn则尝试获取真实ip
    # target可以是主要目标或是主要目标的旁站或子站,但是扫描器中第1次运行single_cdn_scan并没有运行到找旁站和
    # 子站的模块,这时target只可能是主要目标,扫描器中第2次运行single_cdn_scan时在获取子站之后,此时主要实际用于针
    # 对子站进行cdn识别
def single_risk_scan(target):
    # 单个target高危exp遍历模块
    # target要求为http(s)+domain格式
    # risk_scan模块对每个target,无论是主要目标的旁站还是子站,都进行详细的判断target是否是主要目标,并在对应的表
    # 中记录risk_scaned的完成状态
    # 这里的target不一定是主要目标,可以是旁站或子站
    # exps目录下的每个目录为不同中高危漏洞对应的检测脚本,需要python3,运行检测脚本后如果对应目录下有result.txt则代
    # 表有对应的漏洞,没有产生result.txt则代表没有对应的漏洞
def get_target_script_type(target):
    # 得到target的脚本类型
    # target要是http(s)+domain格式
    # 此处不考虑html静态类型,如果没有找到,默认返回php
def single_script_type_scan(target):
    # 对一个target进行脚本类型识别,这里的target可以为主要目标,也可以为主要目标的旁站或子站
def single_dirb_scan(target):
    # 对一个target进行dirb扫描,这里的target可以为主要目标,也可以为主要目标的旁站或子站
def cms_identify(target):
    # 对target进行cms识别
    # target可以是主要目标,也可以是主要目标的旁站或子站
def single_cms_scan(target):
    # 对target根据taret的cms类型进行cms识别及相应第三方工具扫描,target可以是主要目标或者是旁站或是子站
    # target要求为http+domain格式
def static_sqli(url):
    # re.search("",url)
def sqlmap_g_nohuman(http_url_or_file, tor_or_not, post_or_not):
    # this function use sqlmap's "-g" option to find sqli urls,but this "-g"
    # option can only get 100 results due to google api restriction,but in
    # this mode,there is no need for us human to handle any situation.
def sqlmap_crawl(origin_http_url_or_file, tor_or_not, post_or_not):
    # this function use sqlmap's "--crawl" option to find sqli urls.
def sqlmap_g_human(http_url_or_file, tor_or_not, post_or_not):
    # this function use myGoogleScraper to search google dork to get the full
    # urls,in this mode,we need input the yanzhengma by human,not robot,coz
    # sqlmap's -g option can only get the former 100 results,this function will
    # get almost the all results.
def sqli_scan(target):
    # 根据scan_way而采取相应的扫描sqli模式
    # target要求是http...格式,不能是纯domain
def getServerType(url):
    # 得到url对应web服务器的类型,eg.apache,iis,nginx,lighttpd
    # phpstudy中试验上面4种的php默认post参数最大个数为1000个
def single_crack_admin_page_scan(target):
    # 这里爆破所有可能是管理登录的页面,普通用户登录页面也爆破
    # target可以是主要目标或是主要目标的旁站或子站
    # dirb后缀扫描后与爬虫获得的url联合找出可疑登录页面,并进行爆破
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
def get_http_pang_domains_list_from_db(target, db):
    # 从数据库中获取主要目标的旁站列表
    # target要是主要目标
def get_http_sub_domains_list_from_db(target, db):
    # 从数据库中获取主要目标的子站列表
    # target要是主要目标
def get_domainUrl_cookie(domainUrl):
    # 得到domainUrl的cookie,目前为从config.ini文件中获取
    # eg.domainUrl=https://www.baidu.com:8080
    # 如果domainUrl在config.ini中没有cookie,则查找config.ini中是否有domainUrl对应的主站有cookie，如果有对应的主站
    # 有cookie,则用domainUrl对应的主站的cookie
    # 如果没有则返回""空字符串
def set_target_scan_finished(target):
    # 根据扫描模式设置扫描完成
def auto_attack(target):
    # 自动化检测target流程
    # 根据扫描模式进行cdn情况扫描,如果有cdn,尝试获取真实ip
    # cdn模块的结果影响端口扫描模块,也影响是否进行旁站获取,cdn模块在获取旁站模块前要运行一次,
    # 在获取子站模块后要再运行一次,第1次是为了给是否获取旁站提供指导,第2次是为了给子站获取真实ip,给端口扫描子站
    # 提供指导
def scanInit():
    # 这个函数用于配置exp10itScanner要用到的参数
def exp10itScanner():
    # 相当于扫描工具的main函数
