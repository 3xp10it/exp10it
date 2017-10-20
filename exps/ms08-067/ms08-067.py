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
figlet2file("test ms08-067 for %s" % target, 0, True)
a = get_string_from_command(
    "nmap --script=smb-vuln-ms08-067 %s 2>&1 | tee /tmp/result.txt" % (modulePath, target))
if re.search(r"VULNERABLE", a, re.I):
    os.system("mv /tmp/result.txt %s" % modulePath)
    CLIOutput().good_print("Congratulations! MS10-010 exists on %s" % target)
else:
    os.system("rm /tmp/result.txt")
