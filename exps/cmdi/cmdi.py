import os,sys
import re
exp10it_module_path = os.path.expanduser("~")+"/mypypi"
sys.path.insert(0, exp10it_module_path)
from exp10it import get_param_list_from_param_part
current_dir=os.path.split(os.path.realpath(__file__))[0]
if not os.path.exists(current_dir+"/commix"):
    os.system("cd %s && git clone https://github.com/3xp10it/commix.git" % current_dir)
target=sys.argv[1]
urls=get_target_urls_from_db(target,"exp10itdb")
urls.append(target)
cookie=get_url_cookie(target)
for url in urls:
    match1=re.search(r"(([^\?&\^]*ip[^=]*=[^&]*)|([^\?&\^]*host[^=]=[^&]*)|([^\?&\^]*addr[^=]=[^&]*)|([^\?&\^]*cmd[^=]=[^&]*)|([^\?&\^]command[^=]=[^&]*))",url,re.I)
    if match1:
        vul_str=match1.group(1)

