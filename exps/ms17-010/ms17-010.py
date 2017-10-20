import sys
import re
import os
from urllib.parse import urlparse
from exp10it import get_string_from_command
from exp10it import figlet2file
from exp10it import CLIOutput
target = sys.argv[1]
modulePath = __file__[:-len(__file__.split("/")[-1])]
if target[:4] == "http":
    target = urlparse(target).hostname
figlet2file("test ms17-010 for %s" % target, 0, True)
if not os.path.exists("%ssmb-vuln-ms17-010.nse"):
    os.system("cd %s && wget https://raw.githubusercontent.com/cldrn/nmap-nse-scripts/master/scripts/smb-vuln-ms17-010.nse" %
              modulePath)
a = get_string_from_command(
    "nmap --script=%ssmb-vuln-ms17-010.nse %s 2>&1 | tee /tmp/result.txt" % (modulePath, target))
if re.search(r"VULNERABLE", a, re.I):
    os.system("mv /tmp/result.txt %s" % modulePath)
    CLIOutput().good_print("Congratulations! MS10-010 exists on %s" % target)
else:
    os.system("rm /tmp/result.txt")
