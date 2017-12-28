import sys
#from exp10it import get_all_abs_path_file_name
from exp10it import get_all_file_name
folder_path=input("请输入待识别的文件夹:\n > ")
files_list=get_all_file_name(folder_path,['txt'])
print(files_list)

