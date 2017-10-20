from exp10it import logFolderPath
from exp10it import ModulePath
from exp10it import cms_identify
from exp10it import figlet2file
import re

def single_cms_scan(target):
    # 对target根据target的cms类型进行cms识别及相应第三方工具扫描,target可以是主要目标或者是旁站或是子站
    # target要求为http+domain格式
    figlet2file("cms scaning...", 0, True)
    print(target)
    import os
    cms_value = cms_identify(target)
    if cms_value == "unknown":
        return ""

    # 下面相当于cms_scan过程
    if False == os.path.exists(logFolderPath):
        os.system("mkdir %s" % logFolderPath)
    if False == os.path.exists(logFolderPath + "/cms_scan_log"):
        os.system("cd %s && mkdir cms_scan_log" % logFolderPath)

    if False == os.path.exists(ModulePath + "cms_scan"):
        os.system("mkdir %s" % ModulePath + "cms_scan")

    if cms_value == 'discuz':
        if False == os.path.exists(ModulePath + "log/cms_scan_log/dzscan"):
            os.system("cd %slog/cms_scan_log && mkdir dzscan" % ModulePath)
        cms_scaner_list = os.listdir(ModulePath + "cms_scan")
        if "dzscan" not in cms_scaner_list:
            os.system(
                "cd %scms_scan && git clone https://github.com/code-scan/dzscan.git" % ModulePath)
        log_file = target.split("/")[-1].replace(".","_") + ".log"

        if os.path.exists(ModulePath + "log/cms_scan_log/dzscan/" + log_file):
            pass
        else:
            os.system(
                "cd %scms_scan/dzscan && python dzscan.py --update && python dzscan.py -u %s --log" %
                (ModulePath, target))

        os.system("mv %scms_scan/dzscan/%s %slog/cms_scan_log/dzscan/" %
                  (ModulePath, log_file, ModulePath))

        cms_scan_result=""
        if os.path.exists(ModulePath+"log/cms_scan_log/dzscan/"+log_file)==True:
            with open(ModulePath + "log/cms_scan_log/dzscan/" + log_file, "r+") as f:
                cms_scan_result=f.read()

    if cms_value == 'joomla':
        if False == os.path.exists(ModulePath + "log/cms_scan_log/joomscan"):
            os.system("cd %slog/cms_scan_log && mkdir joomscan" % ModulePath)
        cms_scaner_list=os.listdir(ModulePath + "cms_scan")
        if "joomscan" not in cms_scaner_list:
            os.system("cd %scms_scan && wget \
http://jaist.dl.sourceforge.net/project/joomscan/joomscan/2012-03-10/joomscan-latest.zip \
&& unzip joomscan-latest.zip -d joomscan && rm joomscan-latest.zip" % ModulePath)
        result=get_string_from_command(
            "perl %scms_scan/joomscan/joomscan.pl" % ModulePath)
        if re.search(
            r'you may need to install the Switch module',
                result):
            os.system(
                "sudo apt-get install libswitch-perl && perl -MCPAN -e 'install WWW::Mechanize'")
        log_file="report/%s-joexploit.txt" % target.split("/")[-1]
        if os.path.exists(ModulePath + "log/cms_scan_log/joomscan/" + log_file):
            pass
        else:
            os.system(
                "cd %scms_scan/joomscan && perl joomscan.pl update && perl joomscan.pl -u %s -ot" % (ModulePath, target))

        os.system(
            "mv %scms_scan/joomscan/%s log/cms_scan_log/joomscan/ " % (ModulePath, log_file))
        with open(ModulePath + "log/cms_scan_log/joomscan/" + log_file[7:], "r+") as f:
            cms_scan_result=f.read()

    if cms_value == 'wordpress':
        if False == os.path.exists(ModulePath + "log/cms_scan_log/wpscan"):
            os.system("cd %slog/cms_scan_log && mkdir wpscan" % ModulePath)
        cms_scaner_list=os.listdir(ModulePath + "cms_scan")
        if "wpscan" not in cms_scaner_list:
            os.system(
                "cd %scms_scan && git clone https://github.com/wpscanteam/wpscan.git && cd wpscan && echo y | unzip data.zip" % ModulePath)
        result=get_string_from_command(
            "ruby %scms_scan/wpscan/wpscan.rb" % ModulePath)
        if re.search(r'ERROR', result):
            os.system("sudo apt-get install libcurl4-openssl-dev libxml2 libxml2-dev libxslt1-dev \
ruby-dev build-essential libgmp-dev zlib1g-dev")
            os.system("gem install bundler && bundle install")
        log_file="%s.txt" % target.split("/")[-1]
        if os.path.exists(ModulePath + "log/cms_scan_log/wpscan/" + log_file):
            pass
        else:
            os.system(
                "cd %scms_scan/wpscan && ruby wpscan.rb --update && ruby wpscan.rb %s | tee %s" %
                (ModulePath, target, log_file))
            os.system(
                "mv %scms_scan/wpscan/%s %slog/cms_scan_log/wpscan/" % (ModulePath, log_file, ModulePath))
        with open(ModulePath + "log/cms_scan_log/wpscan/" + log_file, "r+") as f:
            cms_scan_result=f.read()

    print(cms_scan_result)
    return cms_scan_result

if __name__=="__main__":
    import sys
    target=sys.argv[1]
    single_cms_scan(target)


