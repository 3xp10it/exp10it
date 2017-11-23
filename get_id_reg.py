import requests
import chardet
import re
import threading
from concurrent import futures

mutex=threading.Lock()

def get_id_reg(id):
    id=id[:18]
    api_url="http://qq.ip138.com/idsearch/index.asp?action=idcard&userid="+id+"&B1=%B2%E9+%D1%AF"
    res=requests.get(api_url)
    bytes_encoding=chardet.detect(res.content)['encoding']
    content=res.content.decode(encoding=bytes_encoding,errors="ignore")
    reg=re.search(r'''tdc2"\>([^\<]+)\<br/\>\<''',content,re.I).group(1)
    mutex.acquire()
    with open("get_id_reg_output.txt","a+") as f:
        f.write(id+"    "+reg+"\n")
    mutex.release()



with open("id_region.txt","r+") as f:
    lines=f.readlines()


with futures.ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(get_id_reg,lines)
