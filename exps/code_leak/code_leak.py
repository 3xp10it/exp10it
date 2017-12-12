import re
import os
import sys
exp10it_module_path = os.path.expanduser("~") + "/mypypi"
sys.path.insert(0, exp10it_module_path)
import sys
from exp10it import get_request
from exp10it import get_http_domain_from_url
target=sys.argv[1]
print("checking code leak vul for "+target)
current_dir = os.path.split(os.path.realpath(__file__))[0]
return_string = ""
leakList = [".hg", ".git", ".svn", ".ds_store", ".bzr",
            "WEB-INF/database.propertiesl", "WEB-INF/web.xml"]
for each in leakList:
    http_domain = get_http_domain_from_url(target)
    leakedUrl = http_domain + "/" + each
    a = get_request(leakedUrl)
    if not re.search(r"页面不存在", a['content'], re.I) and a['code'] == 200:
        return_string += "%s exists!\n" % leakedUrl
if return_string != "":
    return_string += "visit http://www.hacksec.cn/Penetration-test/474.html to exploit it"
    with open("%s/result.txt" % current_dir, "a+") as f:
        f.write(return_string)
