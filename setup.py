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

VERSION = "2.7.72"
LICENSE = "MIT"
#beepy在linux下可能会安装失败,有需要的情况下要手动安装
require_package_list=['mechanicalsoup', 'bs4', 'selenium', 'colorama', 'requests', 'configparser', 'chardet', 'wget', 'pymysql','pyperclip','html2text']
platform=platform.platform()
if re.search(r"windows",platform,re.I) or re.search(r"darwin",platform,re.I):
    require_package_list.append("beepy")
if not re.search(r"windows",platform,re.I):
    require_package_list=['mechanicalsoup', 'bs4', 'selenium', 'colorama', 'requests', 'configparser', 'chardet', 'wget', 'pycrypto', 'pymysql','pyperclip','html2text']
    if re.search(r"(centos)|(redhat)|(fedora)",platform,re.I):
        os.system("echo y | yum install readline")
    if re.search(r"(kali)|(debain)|(ubuntu)", platform, re.I):
        content=get_string_from_command("apt search libncurses5-dev")
        if "libncurses5-dev" not in content:
            os.system("apt-get update && (echo y | apt-get install libncurses5-dev) && pip3 install readline")
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
