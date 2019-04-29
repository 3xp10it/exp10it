#coding=utf-8
import codecs
import platform
import os
import re

try:
    from setuptools import setup
except:
    from distutils.core import setup

def get_string_from_command(command):
    import subprocess
    return subprocess.getstatusoutput(command)[1]

def read(fname):
    """
    定义一个read方法，用来读取目录下的长描述
    我们一般是将README文件中的内容读取出来作为长描述，这个会在PyPI中你这个包的页面上展现出来，
    你也可以不用这个方法，自己手动写内容即可，
    PyPI上支持.rst格式的文件。暂不支持.md格式的文件，<BR>.rst文件PyPI会自动把它转为HTML形式显示在你包的信息页面上。
    """
    return codecs.open(os.path.join(os.path.dirname(__file__), fname),encoding='utf-8').read()


NAME = "exp10it"
#PACKAGES = ['cms_identify', 'dicts', 'tools']
DESCRIPTION = "This is a package about network security"
LONG_DESCRIPTION = read("README.md")
KEYWORDS = "network security package"
AUTHOR = "quanyechavshuo"
AUTHOR_EMAIL = "quanyechavshuo@gmail.com"
URL = "http://3xp10it.cc"

VERSION = "2.7.19"
LICENSE = "MIT"
require_package_list=['mechanicalsoup', 'bs4', 'selenium', 'colorama', 'requests', 'configparser', 'chardet', 'wget', 'pymysql']
system=platform.system()
if system!='Windows':
    require_package_list=['mechanicalsoup', 'bs4', 'selenium','readline', 'colorama', 'requests', 'configparser', 'chardet', 'wget', 'pycrypto', 'pymysql']
    os.system("uname -a > /tmp/exp10it_setup")
    with open("/tmp/exp10it_setup", "r+") as f:
        sysinfo = f.read()
    os.system("rm /tmp/exp10it_setup")
    if re.search(r"(kali)|(debain)|(ubuntu)", sysinfo, re.I):
        content=get_string_from_command("apt search libncurses5-dev")
        if "libncurses5-dev" not in content:
            os.system("apt-get update && (echo y | apt-get install libncurses5-dev)")
setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            ],
        keywords=KEYWORDS,
        install_requires=require_package_list,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        url=URL,
        license=LICENSE,
        # packages=PACKAGES,
        include_package_data=True,
        zip_safe=True,
        py_modules=['exp10it', 'updateapi'],
        )
