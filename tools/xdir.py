from exp10it import ModulePath
from exp10it import logFolderPath
from exp10it import get_target_script_type
import re
def single_dirb_scan(target):
    # 对一个target进行dirb扫描
    target=re.sub(r"/+","",target)
    import os

    if False == os.path.exists(ModulePath + "dirsearch"):
        os.system("git clone https://github.com/maurosoria/dirsearch.git %sdirsearch" % ModulePath)

    if False == os.path.exists(logFolderPath):
        os.system("mkdir %s" % logFolderPath)

    if False == os.path.exists(logFolderPath + "/dirsearch_log"):
        os.system("cd %s && mkdir dirsearch_log" % logFolderPath)
    log_file = logFolderPath + "/dirsearch_log/%s_log.txt" % target.split("/")[-1]
    if os.path.exists(log_file):
        pass
    else:
        script_type=get_target_script_type(target)
        if len(script_type)>1:
            for each in script_type:
                tmp=each+","
            script_type_value=tmp[:-1]
        elif len(script_type)==1:
            script_type_value=script_type[0]
        else:
            return "get script type wrong in %stools/xdir.py" % ModulePath

        ext=script_type_value

        origin_log_dir = ModulePath + "dirsearch/reports/%s" % target.split("/")[-1]
        if False == os.path.exists(log_file):
            if (True == os.path.exists(origin_log_dir) and True == os.path.exists(origin_log_dir) and len(
                    os.listdir(origin_log_dir)) == 0) or False == os.path.exists(origin_log_dir):
                os.system(
                    "cd %sdirsearch && python3 dirsearch.py -u %s -t 200 -e %s --random-agents -x 301,302,500 -r" %
                    (ModulePath, target, ext))

            if False == os.path.exists(origin_log_dir):

                from colorama import init, Fore
                init(autoreset=True)
                print(Fore.YELLOW + target)

                print(
                    Fore.YELLOW +
                    "single_dirb_scan may be banned coz too much request to the target server")
                return ""
            else:
                origin_log_name_list = os.listdir(origin_log_dir)
                if len(origin_log_name_list) > 0:
                    os.system("mv %s/%s %s" %
                              (origin_log_dir, origin_log_name_list[0], log_file))
        else:
            pass

    strings = ""
    urls_list = []
    if os.path.exists(log_file) == True:
        # 如果dirbsearch失败则不会产生log文件
        with open(log_file, "r+") as f:
            for each_line in f:
                # 每行最后一个字符是\n
                if each_line[:3] == '200':
                    url = re.search(r"(http.*)", each_line).group(1)
                    if url not in urls_list and url[0:-(1 + len(url.split(".")[-1]))] + url.split(
                            ".")[-1].upper() not in urls_list and '.' in url[-6:]:
                        urls_list.append(url)
                        strings += (url + "\n")
        strings_to_write = strings
    else:
        strings_to_write = ""

    return strings_to_write

if __name__=='__main__':
    import sys
    target=sys.argv[1]
    single_dirb_scan(target)
