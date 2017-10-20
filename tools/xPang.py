from exp10it import bing_search
from exp10it import logFolderPath
from exp10it import figlet2file
from exp10it import getIp
from exp10it import save_url_to_file
import re
from exp10it import Xcdn

def get_pang_domains(target):
    # 得到target的旁站列表
    # target为如http://www.baidu.com的域名,含http
    if target[:4] == "http":
        domain = target.split("/")[-1]
    else:
        print("please make sure param has scheme http or https")
        return
    figlet2file("geting pang domains", 0, True)
    print(target)

    import os
    if False == os.path.exists(logFolderPath):
        os.system("mkdir %s" % logFolderPath)
    if False == os.path.exists("%s/pang" % logFolderPath):
        os.system("cd %s && mkdir pang" % logFolderPath)
    domain_pang_file = "%s/pang/%s_pang.txt" % (logFolderPath,domain.replace(".", "_"))
    import os
    import socket
    if os.path.exists(domain_pang_file):
        # 文件存在说明上次已经获取过旁站结果
        print("you have got the pang domains last time")
        with open(domain_pang_file,"r+") as f:
            result=f.read()
        return result
        # 如果数据库中存在对应表,但没有内容,说明数据库中表被删除,
        # 后来由于database_init函数在auto_attack重新运行时被执行,又有了旁站表
        # 此时旁站表为空将文件中的旁站写入数据库中

    else:
        domain_list = []
        http_domain_list = []
        origin_http_domain_url_list = []
        #ip = getIp(domain)
        xcdnObj=Xcdn(domain)
        ip = xcdnObj.return_value
        if ip==0:
            #此时有cdn但是没有找到真实ip,这种情况不获取旁站,退出当前处理过程
            returnString="Sorry,since I can not find the actual ip behind the cdn,I will not get pang domains."
            print(returnString)
            return returnString
        print(domain)
        all_nics_ip = socket.gethostbyname_ex(domain)[2]
        query = "ip:%s" % ip
        for piece in bing_search(query, 'Web'):
            if "https://" in piece['Url']:
                each_domain = piece['Url'][8:-1].split('/')[0]
                if each_domain not in domain_list and getIp(
                        each_domain) in all_nics_ip:
                    domain_list.append(each_domain)
                    http_domain_list.append("https://" + each_domain)
                    origin_http_domain_url_list.append(piece['Url'])
            else:
                each_domain = piece['Url'][7:-1].split('/')[0]
                if each_domain not in domain_list and getIp(
                        each_domain) in all_nics_ip:
                    domain_list.append(each_domain)
                    http_domain_list.append("http://" + each_domain)
                    origin_http_domain_url_list.append(piece['Url'])
        print(http_domain_list)
        import os
        save_url_to_file(http_domain_list, domain_pang_file)
        f = open(domain_pang_file, "r+")
        all = f.read()
        f.close()
        find_http_domain = re.search(r"(http(s)?://%s)" % re.sub(r"\.", "\.", domain), all)
        http_domain = ""
        if find_http_domain:
            http_domain = find_http_domain.group(1)
        else:
            print("can not find http_domain in %s" % domain_pang_file)
        pang_domains = ""
        for each in http_domain_list:
            if re.sub(r"(\s)$", "", each) != target:
                pang_domains += (each + '\n')
        #这里返回的是string结果
        return pang_domains

if __name__=='__main__':
    import sys
    result=get_pang_domains(sys.argv[1])
    print(result)

