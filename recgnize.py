import os
import sys


def get_all_abs_path_file_name(folder, ext_list):
    # ext_list为空时,得到目录下的所有绝对路径形式的文件名,不返回空文件夹名
    # ext_list为eg.['jpg','png']
    # eg.folder="~"时,当~目录下有一个文件夹a,一个文件2.txt,a中有一个文件1.txt
    # 得到的函数返回值为['a/1.txt','2.txt']

    tmp_get_file_name_value = [0]
    tmp_all_file_name_list = []

    def get_all_abs_path_file_name_inside_func(f, e):
        folder = f
        ext_list = e
        import os
        tmp_get_file_name_value[0] += 1
        if tmp_get_file_name_value[0] == 1:
            if folder[-1] == '/':
                root_dir = folder[:-1]
            else:
                root_dir = folder

        allfile = os.listdir(folder)

        for each in allfile:
            each_abspath = os.path.join(folder, each)
            if os.path.isdir(each_abspath):
                get_all_abs_path_file_name_inside_func(each_abspath, ext_list)
            else:
                if len(ext_list) == 0:
                    tmp_all_file_name_list.append(each_abspath)
                else:
                    for each_ext in ext_list:
                        if(each_abspath.split('.')[-1] == each_ext):
                            # print filename
                            tmp_all_file_name_list.append(each_abspath)
        return tmp_all_file_name_list
    return get_all_abs_path_file_name_inside_func(folder, ext_list)


def get_key_word_line_num_from_file(key_word, abs_file_path):
    with open(abs_file_path, "r+") as f:
        lines = f.readlines()
    i = 0
    for line in lines:
        i += 1
        if key_word in line:
            break
        else:
            continue
    return i


folder_path = input("请输入待识别的文件夹(支持递归查找文件):\n > ")
key_word = input("请输入关键词,如果有多个需以空格符分开:\n > ")
key_word_list = key_word.split(" ")
file_list = get_all_abs_path_file_name(folder_path, ['txt'])
for abs_file_path in file_list:
    for key_word in key_word_list:
        with open(abs_file_path,"r+") as f:
            abs_file_path_content=f.read()
        if key_word in abs_file_path_content:
            line_num = get_key_word_line_num_from_file(key_word, abs_file_path)
            print("在%s文件的第%s行发现敏感词%s" %
                  (abs_file_path, str(line_num), key_word))
