import re
import sys
from exp10it import get_request
from exp10it import get_http_domain_from_url
# modulePath = __file__[:-len(__file__.split("/")[-1])]
return_string = ""
leakList = [".hg", ".git", ".svn", ".ds_store", ".bzr", "WEB-INF/database.propertiesl", "WEB-INF/web.xml"]
for each in leakList:
    http_domain = get_http_domain_from_url(sys.argv[1])
    leakedUrl = http_domain + "/" + each
    a = get_request(leakedUrl)
    if not re.search(r"页面不存在", a['content'], re.I) and a['code'] == 200:
        return_string += "%s exists!\n" % leakedUrl
if return_string != "":
    return_string += "visit http://www.hacksec.cn/Penetration-test/474.html to exploit it"
    with open("result.txt", "a+") as f:
        f.write(return_string)
