import re
import os
import sys
exp10it_module_path = os.path.expanduser("~") + "/mypypi"
sys.path.insert(0, exp10it_module_path)
import time
from exp10it import CLIOutput
from exp10it import get_target_urls_from_db
from exp10it import get_url_cookie
current_dir = os.path.split(os.path.realpath(__file__))[0]
if not os.path.exists(current_dir + "/commix"):
    os.system(
        "cd %s && git clone https://github.com/3xp10it/commix.git" % current_dir)
target = sys.argv[1]
print("checking command injection vul for "+target)
urls = get_target_urls_from_db(target, "exp10itdb")
urls.append(target)
cookie = get_url_cookie(target)
check_url_list = []
for url in urls:
    match = re.search(
        r"(([^\?&\^]*ip[^=]*=[^&]*)|([^\?&\^]*host[^=]=[^&]*)|([^\?&\^]*addr[^=]=[^&]*)|([^\?&\^]*cmd[^=]=[^&]*)|([^\?&\^]command[^=]=[^&]*))", url, re.I)
    if match:
        vul_str = match.group(1)
        param = vul_str.split("=")[0]
        url = url.replace(vul_str, param + "=xxxxxxxxxx")
        check_url_list.append(url)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Cookie': '%s' % cookie,
           'Content-Type': 'text/xml;charset=UTF-8'
           }


def check(url):
    url = url.replace("xxxxxxxxxx", "*")
    current_log_file = "/tmp/commix_" + str(time.time())
    if "^" in url:
        url_list = url.split("^")
        url = url_list[0]
        data = url_list[1]
        if cookie != "":
            cmd = '''cd %s && python2 commix.py -u "%s" --data "%s" --cookie "%s" -v 3 --batch | tee %s''' % (
                current_dir + "/commix", url, data, cookie, current_log_file)
            os.system(cmd)
        else:
            cmd = '''cd %s && python2 commix.py -u "%s" --data "%s" -v 3 --batch | tee %s''' % (
                current_dir + "/commix", url, data, current_log_file)
            os.system(cmd)
    else:
        if cookie != "":
            cmd = '''cd %s && python2 commix.py -u "%s" --cookie "%s" -v 3 --batch | tee %s''' % (
                current_dir + "/commix", url, cookie, current_log_file)
            os.system(cmd)
        else:
            cmd = '''cd %s && python2 commix.py -u "%s" -v 3 --batch | tee %s''' % (
                current_dir + "/commix", url, current_log_file)
            os.system(cmd)

    with open(current_log_file, "r+") as f:
        log_str = f.read()
    os.system("rm %s" % current_log_file)
    if re.search(r"The parameter.*seems injectable", log_str, re.I):
        string_to_write = "Congratulations! command injection vul exists:" + url + "\n"
        CLIOutput().good_print(string_to_write)
        with open("%s/result.txt" % current_dir, "a+") as f:
            f.write(string_to_write)
    else:
        print("no cmdi vul")


from concurrent import futures
with futures.ThreadPoolExecutor(max_workers=15) as executor:
    executor.map(check, check_url_list)
