import codecs
import os
import re
from exp10it import get_string_from_command

try:
    from setuptools import setup
except:
    from distutils.core import setup


def read(fname):
    """
    定义一个read方法，用来读取目录下的长描述
    我们一般是将README文件中的内容读取出来作为长描述，这个会在PyPI中你这个包的页面上展现出来，
    你也可以不用这个方法，自己手动写内容即可，
    PyPI上支持.rst格式的文件。暂不支持.md格式的文件，<BR>.rst文件PyPI会自动把它转为HTML形式显示在你包的信息页面上。
    """
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


NAME = "exp10it"
#PACKAGES = ['cms_identify', 'dicts', 'tools']
DESCRIPTION = "This is a package about web security"
LONG_DESCRIPTION = read("README.md")
KEYWORDS = "web security package"
AUTHOR = "quanyechavshuo"
AUTHOR_EMAIL = "quanyechavshuo@gmail.com"
URL = "http://3xp10it.cc"

VERSION = "2.6.78"
LICENSE = "MIT"
print(6666666666666)
sysinfo = get_string_from_command("uname -a")
print(7777777777777777777)
if re.search(r"kali", sysinfo, re.I):
    os.system("sudo apt-get update && apt-get install libncurses5-dev")
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
    install_requires=['mechanicalsoup', 'bs4', 'selenium', 'readline',
                      'colorama', 'requests', 'configparser', 'chardet', 'wget'],
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    # packages=PACKAGES,
    include_package_data=True,
    zip_safe=True,
    py_modules=['exp10it', 'updateapi'],
)
