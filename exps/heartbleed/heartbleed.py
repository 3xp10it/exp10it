import re
import sys
from urllib.parse import urlparse
from exp10it import get_string_from_command
from exp10it import CLIOutput
from exp10it import figlet2file
from exp10it import get_target_table_name_list
from exp10it import execute_sql_in_db
from exp10it import commonNotWebPortList

modulePath = __file__[:-len(__file__.split("/")[-1])]
target = sys.argv[1]
if target[:4] == "http":
    target = urlparse(target).hostname
figlet2file("test heartbleed vul for %s" % target, 0, True)
target_table_name = get_target_table_name_list(target)[0]
result = execute_sql_in_db("select port_scan_info from %s where http_domain='%s'" %
                           (target_table_name, target), "exp10itdb")
if len(result) > 0:
    nmap_result_string = result[0][0]
    a = re.findall(r"(\d+)/(tcp)|(udp)\s+open", nmap_result_string, re.I)
    openPortList = []
    for each in a:
        if each[0] not in openPortList and each[0] not in commonNotWebPortList:
            openPortList.append(each[0])
    for each in openPortList:
        a = get_string_from_command("cd %s && python2 ssltest.py -p %s %s " % (modulePath, each, target))
        if re.search(r"server is vulnerable", a, re.I):
            string_to_write = "Congratulations! heartbleed vul exists on %s:%s" % (target, each)
            CLIOutput().good_print(string_to_write)
            with open("%sresult.txt" % modulePath, "a+") as f:
                f.write(string_to_write)
else:
    print("coz I found no nmap scan result from database,I will not run heartbleed vul check module")
