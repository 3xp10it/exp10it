#/usr/bin/env python3
#字典去重工具
#usage:py3 xrepeat.py file
import sys
import os
import re
if len(sys.argv)!=2:
    print("usage:python3 xrepeat.py")
file=sys.argv[1]
if not os.path.exists(file):
    print("%s file not exists" % file)
with open(file,"r+") as f:
    all_lines=f.readlines()
print("老文件共%s个word" % str(len(all_lines)))
new_list=[]
for each_line in all_lines:    
    each_word=re.sub(r"\s$","",each_line)
    if each_word not in new_list and each_word!="":
        new_list.append(each_word)
print("新文件共%s个word" % str(len(new_list)))
for each_word in new_list:
    with open("newfile","a+") as f:
        f.write(each_word+"\n")
