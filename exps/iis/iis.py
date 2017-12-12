import re
import os
import sys
exp10it_module_path = os.path.expanduser("~") + "/mypypi"
sys.path.insert(0, exp10it_module_path)
from exp10it import getServerType
from exp10it import get_string_from_command
from exp10it import CLIOutput
import sys
from exp10it import COMMON_NOT_WEB_PORT_LIST
from exp10it import get_target_open_port_list

current_dir = os.path.split(os.path.realpath(__file__))[0]
target = sys.argv[1]
print("checking iis vul for "+target)
domain = target.split("/")[-1]

open_port_list = get_target_open_port_list(target)
for eachPort in open_port_list:
    if eachPort not in COMMON_NOT_WEB_PORT_LIST:
        serverType = getServerType(target)
        if not re.search(r"iis/6", serverType, re.I):
            continue
        a = get_string_from_command(
            "cd %s && python2 iis6.py %s %s" % (current_dir, domain, eachPort))
        if re.search(r"HHIT CVE-2017-7269 Success", a, re.I):
            string_to_write = "Congratulations! 存在iis6.0远程溢出漏洞:\n%s:%s" % (
                domain, eachPort)

            CLIOutput.good_print(string_to_write)
            with open("%s/result.txt" % current_dir, "a+") as f:
                f.write(string_to_write)

        else:
            print("coz I found no nmap scan result from database,I will test only on the default port but not test on all open ports")
