import re
from concurrent import futures
from exp10it import send_http_package
from urllib.parse import urlparse
import sys
package_file=sys.argv[1]
targets_file=sys.argv[2]
pattern=sys.argv[3]
pattern=re.compile("("+pattern+")",re.I)
with open(package_file,"r+") as f:
    package=f.read()
with open(targets_file,"r+") as f:
    targets=f.readlines()

match_string_list=[]

def send_single_package(each):
    global package
    each=each[:-1]
    parsed=urlparse(each)
    host=parsed.netloc
    each_package=re.sub(r"(?<=Host: )(.+)",host,package,re.I)
    each_package=re.sub(r"(?<=Referer: )(.+)",each,each_package,re.I)
    a=send_http_package(each_package,each.split(":")[0])
    print("%s return:\n%s\n\n" % (each,a))
    each_match_str=pattern.search(a).group(1)
    match_string_list.append(each_match_str)

with futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(send_single_package,targets)

print(match_string_list)
