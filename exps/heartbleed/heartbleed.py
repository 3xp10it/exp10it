import re
import os
import sys
from urllib.parse import urlparse
from exp10it import get_string_from_command
from exp10it import CLIOutput
from exp10it import figlet2file
from exp10it import get_target_table_name_list
from exp10it import COMMON_NOT_WEB_PORT_LIST
from exp10it import get_http_domain_from_url
from exp10it import get_target_open_port_list


current_dir = os.path.split(os.path.realpath(__file__))[0]
target = sys.argv[1]
open_port_list = get_target_open_port_list(target)
http_domain = get_http_domain_from_url(target)
hostname = urlparse(target).hostname
figlet2file("test heartbleed vul for %s" % target, 0, True)
target_table_name = get_target_table_name_list(target)[0]
parsed = urlparse(target)
open_port_list = get_target_open_port_list(target)
if ":" in parsed.netloc:
    open_port_list.append(parsed.netloc.split(":")[1])

for each in open_port_list:
    if each not in COMMON_NOT_WEB_PORT_LIST:
        a = get_string_from_command(
            "cd %s && python2 ssltest.py -p %s %s " % (current_dir, each, hostname))
        if re.search(r"server is vulnerable", a, re.I):
            string_to_write = "Congratulations! heartbleed vul exists on %s:%s" % (
                hostname, each)
            CLIOutput().good_print(string_to_write)
            with open("%s/result.txt" % current_dir, "a+") as f:
                f.write(string_to_write)
        else:
            print("coz I found no nmap scan result from database,I will not run heartbleed vul check module on other ports")
