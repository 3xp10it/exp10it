import os
import sys
exp10it_module_path = os.path.expanduser("~") + "/mypypi"
sys.path.insert(0, exp10it_module_path)
import re
import time
from urllib.parse import urlparse
from exp10it import get_string_from_command
from exp10it import CLIOutput
target = sys.argv[1]
print("checking ms08-067 vul for "+target)
current_dir = os.path.split(os.path.realpath(__file__))[0]
current_log_file = "/tmp/commix_" + str(time.time())
if target[:4] == "http":
    target = urlparse(target).hostname
cmd = "nmap --script=smb-vuln-ms08-067 %s 2>&1 | tee %s" % (
    target, current_log_file)
a = get_string_from_command(cmd)
if re.search(r"VULNERABLE", a, re.I):
    os.system("mv %s %s/result.txt" % (current_log_file, current_dir))
    CLIOutput().good_print("Congratulations! MS10-010 exists on %s" % target)
else:
    os.system("rm %s" % current_log_file)
