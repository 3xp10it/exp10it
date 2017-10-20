import os
from exp10it import logFolderPath
from exp10it import ModulePath
from exp10it import get_root_domain
from exp10it import figlet2file

def get_sub_domains(target, use_tool="Sublist3r"):
    # target为http开头+domain
    # 注意target(http://www.baidu.com)要换成如baidu.com的结果,然后再当作参数传入下面可能用的工具中
    # www.baidu.com--->baidu.com,baidu.com是下面工具的参数
    # use_tool为子站获取工具选择
    # Sublist3r工具详情如下
    # 获取子站列表,domain为域名格式,不含http
    # https://github.com/aboul3la/Sublist3r
    # works in python2,use os.system get the execute output
    if target[:4] == "http":
        domain = target.split("/")[-1]
    else:
        print("make sure your para in get_sub_domains func has scheme like http or https")
        return
    figlet2file("geting sub domains", 0, True)

    root_domain = get_root_domain(domain)
    if os.path.exists(logFolderPath) == False:
        os.system("mkdir %s" % logFolderPath)
    if os.path.exists("%s/sub" % logFolderPath) == False:
        os.system("cd %s && mkdir sub" % logFolderPath)
    store_file = logFolderPath + "/sub/" + domain.replace(".", "_") + "_sub.txt"
    Sublist3r_store_file = "Sublist3r.out.txt"
    subDomainsBrute_store_file = "subDomainsBrute.out.txt"

    def Sublist3r(domain):
        # 用Sublist3r方式获取子站
        if os.path.exists(ModulePath + "Sublist3r") == False:
            os.system("git clone https://github.com/aboul3la/Sublist3r.git %sSublist3r" % ModulePath)
            # 下面的cd到一个目录只在一句代码中有效,执行完就不在Sublist3r目录里了
            os.system("cd %sSublist3r && pip install -r requirements.txt" % ModulePath)
            # 下面的命令执行不受上面的cd到一个目录影响
            os.system("cd %sSublist3r && python sublist3r.py -v -d %s -o %s" %
                      (ModulePath, root_domain, Sublist3r_store_file))
        else:
            os.system("cd %sSublist3r && python sublist3r.py -v -d %s -o %s" %
                      (ModulePath, root_domain, Sublist3r_store_file))

    def subDomainsBrute(domain):
        # 用subDomainsBrute方式获取子站
        # https://github.com/lijiejie/subDomainsBrute.git
        if os.path.exists(ModulePath + "subDomainsBrute") == False:
            os.system("git clone https://github.com/lijiejie/subDomainsBrute.git %ssubDomainsBrute" % ModulePath)
            os.system("pip install dnspython")
            os.system(
                "cd %ssubDomainsBrute && python subDomainsBrute.py -i -o %s %s" %
                (ModulePath, subDomainsBrute_store_file, root_domain))
        else:
            os.system(
                "cd %ssubDomainsBrute && python subDomainsBrute.py -i -o %s %s" %
                (ModulePath, subDomainsBrute_store_file, root_domain))

    if os.path.exists(store_file) == False:

        if use_tool == "all":
            Sublist3r(root_domain)
            os.system(
                "cat %sSublist3r/%s >> %s" %
                (ModulePath, Sublist3r_store_file, store_file))
            os.system("rm %sSublist3r/%s" % (ModulePath, Sublist3r_store_file))
            subDomainsBrute(root_domain)
            with open("%ssubDomainsBrute/%s" % (ModulePath, subDomainsBrute_store_file), "r+") as f:
                with open(store_file, "a+") as outfile:
                    for each in f:
                        if each not in outfile.readlines():
                            outfile.write(each)
            os.system("rm %ssubDomainsBrute/%s" % (ModulePath, subDomainsBrute_store_file))
        if use_tool == "Sublist3r":
            Sublist3r(domain)
            os.system(
                "cat %sSublist3r/%s >> %s" %
                (ModulePath, Sublist3r_store_file, store_file))
            os.system("rm %sSublist3r/%s" % (ModulePath, Sublist3r_store_file))
        if use_tool == "subDomainsBrute":
            subDomainsBrute(domain)
            os.system("cat %ssubDomainsBrute/%s >> %s" %
                      (ModulePath, subDomainsBrute_store_file, store_file))
            os.system("rm %ssubDomainsBrute/%s" % (ModulePath, subDomainsBrute_store_file))

    else:
        # 文件存在说明上次已经获取sub domains
        print("you have got the sub domains last time")

    with open(store_file, "r+") as f:
        string=f.read()

    return string


if __name__=='__main__':
    import sys
    get_sub_domains(sys.argv[1])
