def tab_complete_file_path():
    # this is a function make system support Tab key complete file_path
    # works on linux,it seems windows not support readline module
def figlet2file(logo_str, file_abs_path, print_or_not):
    # 输出随机的logo文字到文件或屏幕,第二个参数为任意非文件的参数时(eg.0,1,2),只输出到屏幕
    # apt-get install figlet
    # man figlet
    # figure out which is the figlet's font directory
    # my figlet font directory is:
    # figlet -I 2,output:/usr/share/figlet
def oneline2nline(oneline, nline, file_abs_path):
    # 将文件中的一行字符串用多行字符串替换,调用时要将"多行字符串的参数(第二个参数)"中的换行符设置为\n
def lin2win(file_abs_path):
    # 将linux下的文件中的\n换行符换成win下的\n\n换行符
def get_all_file_name(folder, ext_list):
    # exp_list为空时,得到目录下的所有文件名,不返回空文件夹名
    # 返回结果为文件名列表,不是完全绝对路径名
    # eg.folder="/root"时,当/root目录下有一个文件夹a,一个文件2.txt,a中有一个文件1.txt
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
    # 返回值为post响应的html正文内容
def get_random_ua():
    # 得到随机user-agent值
def get_random_x_forwarded_for():
    # 得到随机x-forwarded-for值
def get_request(url):
    # 发出get请求,返回值为一个字典,有三个键值对:eg.{"code":200,"title":None,"content":""}
    # code是int类型
    # title如果没有则返回None,有则返回str类型
    # content如果没有则返回""
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
def get_key_value_from_file(key, separator, file_abs_path):
    # 从文件中获取指定关键字的值,第一个参数为关键字,第二个参数为分隔符,第三个参数为文件绝对路径
    # 默认设置分隔符为":"和"="和" "和"    ",如果使用默认分隔符需要将第二个参数设置为'',也即无字符
    # 如果不使用默认分隔符,需要设置第二个参数为string类型如"="
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
    # eg.write_string_to_sql("lll","h4cktool","targets","scan_result","http_domain","https://www.baidu.com")
    # eg.write_string_to_sql(1,"h4cktool","urls","is_admin_login_url","url",current_url)
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
def get_user_and_pass_form_from_html(html):
    # 从html内容(管理员登录的html)中获取所有的form表单
    # 返回结果为一个字典,包含2个键值对
    #"user_form_name":"" 没有则相应返回值为"None",不是返回""(空字符串)
    #"pass_form_name":"" 没有则相应返回值为"None",不是返回""(空字符串)
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
def crack_admin_login_url(
        url,
        user_dict_file="dicts/user.txt",
        pass_dict_file="dicts/pass.txt"):
    # 爆破管理员后台登录url,尝试自动识别验证码,如果管理员登录页面没有验证码,加了任意验证码数据也可通过验证
def crack_allext_biaodan_webshell_url(url, user_dict_file, pass_dict_file):
    # 爆破表单类型的webshell
    # 表单类型的webshell爆破方法一样,不用分不同脚本类型分别爆破
def crack_webshell(url, anyway=0):
    # webshll爆破,第二个参数默认为0,如果设置不为0,则不考虑判断是否是webshll,如果设置为1,直接按direct_bao方式爆破
    # 如果设置为2,直接按biaodan_bao方式爆破
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
def get_string_from_command(command):
    # 执行命令并得到命令执行打印出的字符串,不会显示执行命令中的输出
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
def mail_msg_to(msg, mailto, subject, user, password, format='plain'):
    # 使用163的邮箱发送邮件
    # msg是要发送的string
    # mailto是发送的目标邮箱地址
    # subject是主题名
    # user,password是用户名密码,其中user要带上邮箱地址后缀
def get_input_intime(default_choose, timeout=5):
    # 在一定时间内得到选择的值,如果没有选择则返回默认选择
    # 第一个参数为默认选择值
    # 第二个参数为设置超时后自动选择默认值的时间大小,单位为秒
    # 返回选择的值,返回值是选择的值或是默认选择值,选择的值为str类型,默认的选择值可为任意类型
def checkvpn():
    # 检测vpn是否连接成功
def get_source_domain_of_target_sqli_urls(url):
    # 得到旁站所属的doamin
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
def get_one_target_from_db(db, target_table):
    # 从数据库db中的target表中按优先级取出目标
def risk_scan(target):
    # 高危exp遍历模块
def dirb_scan(target):
    # 扫目录模块
def sqli_scan(target):
    # sqli扫描模块,sqli.py相当于对目标target及它的旁站的sqli模块的扫描,也可以不用MyToolKit,而每个目标分别单独扫描sqli
def cms_scan(target):
    # cms类型检测及对应第三方扫描工具扫描模块
def crack_scan(target):
    # 爆破模块
def auto_attack(target):
    # 自动化检测target流程
