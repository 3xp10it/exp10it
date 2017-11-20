import os
from exp10it import get_all_abs_path_file_name
from exp10it import get_all_file_name

import sys

bakdir = os.path.expanduser("~") + "/Local"
if not os.path.exists(bakdir):
    os.system("mkdir %s" % bakdir)


def get_current_all_abs_file_name_list():
    all_file_name_list = []
    for path in sys.argv[1:]:
        file_name_list = get_all_abs_path_file_name(path, [])
        all_file_name_list += file_name_list
    return all_file_name_list


original_abs_file_name_list = get_current_all_abs_file_name_list()
print("第1次读完所有文件名列表了,共有%d个文件,现在进入监控中..." % len(original_abs_file_name_list))
while True:
    tmp = get_current_all_abs_file_name_list()
    if tmp != original_abs_file_name_list:
        print("注意,有变化")
    for each in tmp:
        if each not in original_abs_file_name_list:
            print("注意,新增了一个文件:\n" + each)
            os.system("cp %s ~/Local/ && rm %s" % (each,each))
            print("已将%s文件删除,且备份在~/Local目录下" % each)
