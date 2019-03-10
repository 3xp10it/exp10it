```
def get_string_from_command(command):
    # 不能执行which nihao,这样不会有输出,可nihao得到输出
    # 执行成功的命令有正常输出,执行不成功的命令得不到输出,得到输出为"",eg.command=which nihao
    # 判断程序有没有已经安装可eg.get_string_from_command("sqlmap --help")
def get_system_bits():
    # return 64 or 32,type is int.
def module_exist(module_name):
    # 检测python模块是否已经安装
    # 有则返回True
    # 无则返回False
def get_module_path():
    # 得到当前文件的路径
def get_home_path():
    # python在os.path.exists("~")时不认识~目录,于是写出这个函数
    # open("~/.zshrc")函数也不认识~
    # 但是os.system认识~,可能只有os.system认识
    # 也即操作系统认识~,但是python不认识~
    # mac_o_s下的~是/var/root,ubuntu下的~是/root
    # 返回~目录的具体值,eg./var/root
    #a=get_string_from_command("cd ~ && pwd")
    # 后来发现os.path.expanduser函数可以认识~
def aes_dec(text,key):
    # 初始化加密器
def base64encode(string):
    # 得到base64的字符串
    # 输入为str类型
    # 返回为str类型
def base64decode(string):
    # 得到经过base64加密后字符串解密后的明文
    # 输入为str类型
    # 返回为str类型
def is_internal_ip(ip):
    # 判断ip是不是内网ip
def string2argv(string):
    # 将string转化成argv格式
    # 返回一个列表
    # eg:
    # -u 'http://1.php' --dbms=mysql -v 3将转化成:
    # ['-u','http://1.php','--dbms','mysql','-v','3']
    # 最后将--url转化成-u,因为sqlmap中需要
def param2argv(param_list):
    # 将形如['-u','http://a b1.php','--dbms=mysql','-v','3']转化成
    #['-u','http://a b1.php','--dbms','mysql','-v','3']
    # 最后将--url转化成-u,因为sqlmap中需要
def install_scrapy():
    # ubuntu 16.04下安装scrapy
def install_medusa():
    # linux mint下安装medusa
    # 下面用于支持ssh爆破
def file_outof_date(file, check_time=3):
    # 文件距离上次修改后到现在为止经过多久,如果超过check_time的天数则认为文件过期,返回True
    # 如果没有超过3天则认为文件没有过期,返回False
def tab_complete_file_path():
    # this is a function make system support Tab key complete file_path
    # works on linux,it seems windows not support readline module
def seconds2hms(seconds):
    # 将秒数转换成时分秒
    # 返回类型为str类型
def checkvpn():
    # 检测vpn是否连接成功
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
def get_cain_key(lst_file):
    # 参数为cain目录下的包含用户名口令的文件,eg.pop3.lst,imap.lst,smtp.lst,http.lst,ftp.lst...
    # 效果为在程序当前目录下生成一个xxx-cain_out_put.txt为整理后的文件
def get_all_abs_path_file_name(folder, ext_list):
    # ext_list为空时,得到目录下的所有绝对路径形式的文件名,不返回空文件夹名
    # ext_list为eg.['jpg','png']
    # eg.folder="~"时,当~目录下有一个文件夹a,一个文件2.txt,a中有一个文件1.txt
    # 得到的函数返回值为['a/1.txt','2.txt']
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
def post_request(url, data, verify=True):
    # 发出post请求
    # 第二个参数是要提交的数据,要求为字典格式
    # 返回值为post响应的html正文内容,返回内容为str类型
    # print("当前使用的data:")
    # print(data)
    # 这里的verify=False是为了防止https服务器证书无法通过校验导致无法完成https会话而设置的,并不一定有效,后期可能
    # 要改
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
def get_param_list_from_param_part(param_part):
    # eg. get ['a','b'] from 'a=1&b=2'
def test_speed(address):
    # test ping speed
def get_request(url, by="MechanicalSoup", proxy_url="", cookie="", delay_switcher=1):
    # 如果用在爬虫或其他需要页面执行js的场合,用by="selenium_phantom_js",此外用by="MechanicalSoup"
    # 因为by="selenium_phantom_js"无法得到http的响应的code(状态码)
    # 如果用selenium,用firefox打开可直接访问,要是用ie或chrome打开则要先安装相应浏览器驱动
    # 默认用MechanicalSoup方式访问url
    # 发出get请求,返回值为一个字典,有5个键值对
    # eg.{"code":200,"title":None,"content":"",'has_form_action',"",'form_action_value':""}
    # code是int类型
    # title如果没有则返回None,有则返回str类型
    # content如果没有则返回""
    # has_form_action的值为True或False,True代表url对应的html中有表单可提交
def check_start_time(want_time):
    # eg:a="11:59:59"
def send_http_packet(string, http_or_https, proxies={}):
    # 发http请求包封装函数,string可以是burpsuite等截包工具中拦截到的包
    # string要求是burpsuite中抓包抓到的字符串,也即已经经过urlencode
    # proxy_url为代理地址,eg."http://127.0.0.1:8080"
    # 返回的内容为一个字典,{'code':xxx,'html':'xxx'},其中code为int类型,html为str类型
def keep_session(url, cookie):
    # 保持服务器上的session长久有效
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
def get_url_has_csrf_token(url, cookie=""):
    # test if url has csrf token
    # return a dict
    # return dict['has_csrf_token']=True for has
    # return dict['has_csrf_token']=False for has not
    # return dict['csrf_token_name']="csrf token param name value" or ""
def get_user_and_pass_form_from_url(url):
    # 从url的get请求中获取所有form表单
    # 返回结果为一个字典,包含3个键值对
    #"user_form_name":"" 没有则相应返回值为None,不是返回""(空字符串)
    #"pass_form_name":"" 没有则相应返回值为None,不是返回""(空字符串)
    #"response_key_value":value 这个value的值是一个字典,也即get_request函数的返回结果
    # 之所以要每次在有访问url结果的函数里面返回url访问结果,这样是为了可以只访问一次url,这样就可以一直将访问的返\
    # 回结果传递下去,不用多访问,效率更高
def get_yanzhengma_form_and_src_from_url(url):
    # 得到url对应的html中的验证码的表单名和验证码src地址
def crack_ext_direct_webshell_url(url, pass_dict_file, ext):
    # 爆破php|asp|aspx|jsp的一句话类型的webshell
    # 表单形式爆破的webshell爆破起来方法一样,不用分类
    # 一句话形式的webshell爆破需要根据后缀对应的脚本的语法的不同来爆破
def jie_di_qi_crack_ext_direct_webshell_url(url, pass_dict_file, ext):
    # 爆破php|asp|aspx|jsp的一句话类型的webshell
    # 表单形式爆破的webshell爆破起来方法一样,不用分类
    # 一句话形式的webshell爆破需要根据后缀对应的脚本的语法的不同来爆破
def get_value_from_url(url):
    # 返回一个字典{'y1':y1,'y2':y2}
    # eg.从http://www.baidu.com/12/2/3.php?a=1&b=2中得到
    #'y1':"http://www.baidu.com/12/2/3.php"
    #'y2':"http://www.baidu.com/12/2"
def like_admin_login_content(html):
    # 根据html内容判断页面是否可能是管理员登录页面
def like_admin_login_url(url):
    # 判断url对应的html内容是否可能是管理员登录页面
def get_domain_key_value_from_url(url):
    # 从url中得到域名的关键值
    # eg.从http://www.baidu.com中得到baidu
def post_html_handler(html):
    # 处理爬虫遇到包含post数据的html(url)的情况
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
def get_input_intime1(default_choose, timeout=10):
    # http://www.cnblogs.com/jefferybest/archive/2011/10/09/2204050.html
    # 在一定时间内得到选择的值,如果没有选择则返回默认选择
    # 第一个参数为默认选择值
    # 第二个参数为设置超时后自动选择默认值的时间大小,单位为秒
    # 返回选择的值,返回值是选择的值或是默认选择值,选择的值为str类型,默认的选择值可为任意类型
def get_input_intime(default_choose, timeout=10):
    # http://www.cnblogs.com/jefferybest/archive/2011/10/09/2204050.html
    # 在一定时间内得到选择的值,如果没有选择则返回默认选择
    # 第一个参数为默认选择值
    # 第二个参数为设置超时后自动选择默认值的时间大小,单位为秒
    # 返回选择的值,返回值是选择的值或是默认选择值,选择的值为str类型,默认的选择值可为任意类型
    # 无法输入长字符串,适用于只输入1-2个字符长度的字符串,一般用于选项的选择
def able_connect_site(site):
    # 检测与site之间是否能成功连接
def search_key_words(key_words, by='bing'):
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
def get_ip(domain):
    # 从domain中获取ip
def get_pure_list(list):
    # this is a function to remove \r\n or \n from one sting
    # 得到域名列表
def save_url_to_file(url_list, name):
    # this is my write url to file function:
def get_ip_domains_list(ip):
    # 不再用bing接口查询旁站
def get_root_domain(domain):
    # 得到domain的根域名,eg.www.baidu.com得到baidu.com
    # domain可为http开头或纯domain,不能是非http://+domain的url
def get_root_domain_bak(domain):
    # 得到domain的根域名,eg.www.baidu.com得到baidu.com
    # domain可为http开头或纯domain,不能是非http://+domain的url
def get_target_script_type(target):
    # 得到target的脚本类型
    # target要是http(s)+domain格式
    # 此处不考虑html静态类型,如果没有找到,默认返回php
def static_sqli(url):
    # re.search("",url)
def get_server_type(url):
    # 得到url对应web服务器的类型,eg.apache,iis,nginx,lighttpd
    # phpstudy中试验上面4种的php默认post参数最大个数为1000个
def get_cms_entry_from_start_url(start_url):
    # eg.start_url="http://192.168.1.10/dvwa/index.php"
    # return:"http://192.168.1.10/dvwa/"
    # eg.start__url="http://192.168.1.10:8000"
    # return:"http://192.168.1.10:8000/"
def start_ipproxypool():
    # 默认在8000端口开服务
def start_web_server(host,port,rules):
    #eg.rules={'GET':get,'POST':post}
    #def get(self):
    #    from urllib.parse import parse_qs
    #    headers = str(self.headers)
    #    if self.path!='/favicon.ico':
    #        query_dict=parse_qs(self.path[2:])
    #        self._set_headers()
    #        self.wfile.write(bytes(str(query_dict), "utf-8"))
    #start_web_server(host='0.0.0.0',port=8888,rules=rules)
```
