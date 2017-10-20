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
    allLines=f.readlines()
print("老文件共%s个word" % str(len(allLines)))
newList=[]
for eachLine in allLines:    
    eachWord=re.sub(r"\s$","",eachLine)
    if eachWord not in newList and eachWord!="":
        newList.append(eachWord)
print("新文件共%s个word" % str(len(newList)))
for eachWord in newList:
    with open("newfile","a+") as f:
        f.write(eachWord+"\n")
