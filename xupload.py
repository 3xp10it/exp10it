import requests
import re
from exp10it import get_request
from exp10it import get_param_part_from_content
url="http://192.168.135.39/dvwa/vulnerabilities/upload/"
cookie="PHPSESSID=cl4u4quib5tebhico07nopn2o0;security=low"
rsp=get_request(url,cookie=cookie)
html=rsp['content']
if not re.search(r"<form\s+",html,re.I):
    print("Sorry,I can't find any form,you should supply a post packet file")
else:
    param_part=get_param_part_from_content(html)
    print(param_part)

