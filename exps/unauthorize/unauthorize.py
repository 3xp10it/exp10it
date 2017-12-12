import os
import sys
import re
exp10it_module_path = os.path.expanduser("~") + "/mypypi"
sys.path.insert(0, exp10it_module_path)
import requests
from exp10it import CLIOutput
from exp10it import get_target_urls_from_db
from exp10it import get_url_cookie
current_dir = os.path.split(os.path.realpath(__file__))[0]
target = sys.argv[1]
print("checking unauthorize vul for "+target)
urls = get_target_urls_from_db(target, "exp10itdb")
urls.append(target)
cookie = get_url_cookie(target)
check_url_list = []
for url in urls:
    param_value_list = re.findall(
        r"([^?\^&=]+)=([^&\s]*\d+)(?:&|$)", url, re.I)
    if param_value_list != []:
        check_url_list.append(url)


def check(url):
    param_value_list = re.findall(r"([^?\^&=]+)=([^&\s]*\d+)(?:&|$)", url, re.I)
    for param_value in param_value_list:
        param = param_value[0]
        value = param_value[1]
        if value[-1] != '9':
            newvalue = value[:-1] + str(int(value[-1]) + 1)
        else:
            newvalue = value[:-1] + '0'
        newurl = url.replace(param + '=' + value, param + '=' + newvalue)
        if "^" not in url:
            # get request
            rsp = requests.get(newurl)
        else:
            # post request
            post_url = newurl.split("^")[0]
            data = newurl.split("^")[1]
            rsp = requests.post(post_url, data=data.encode(
                "utf-8"), verify=False, timeout=10)

        if rsp.status_code == 200 and not rsp.history:
            string_to_write = ("Congratulations! unauthorize vul may exist:" +
                               url + "the vul param is:" + param + "\n")
            CLIOutput().good_print(string_to_write)
            with open("%s/result.txt" % current_dir, "a+") as f:
                f.write(string_to_write)


from concurrent import futures
with futures.ThreadPoolExecutor(max_workers=15) as executor:
    executor.map(check, check_url_list)
