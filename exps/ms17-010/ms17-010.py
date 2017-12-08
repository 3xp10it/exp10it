import sys
import re
import os
import time
from urllib.parse import urlparse
from exp10it import figlet2file
from exp10it import CLIOutput
target = sys.argv[1]
current_dir = os.path.split(os.path.realpath(__file__))[0]
current_log_file = "/tmp/commix_" + str(time.time())
if target[:4] == "http":
    target = urlparse(target).hostname
figlet2file("test ms17-010 for %s" % target, 0, True)
if not os.path.exists("%s/smb-vuln-ms17-010.nse" % current_dir):
    os.system("cd %s && wget https://raw.githubusercontent.com/cldrn/nmap-nse-scripts/master/scripts/smb-vuln-ms17-010.nse" %
              current_dir)
cmd = "nmap --script=%s/smb-vuln-ms17-010.nse %s 2>&1 | tee %s" % (
    current_dir, target, current_log_file)
a = os.system(cmd)
with open(current_log_file, "r+") as f:
    log_str = f.read()
if re.search(r"VULNERABLE", log_str, re.I):
    os.system("mv %s %s/result.txt" % (current_log_file, current_dir))
    CLIOutput().good_print("Congratulations! MS10-010 exists on %s" % target)
else:
    os.system("rm %s" % current_log_file)
