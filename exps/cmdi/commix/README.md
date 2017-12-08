[![Logo](https://camo.githubusercontent.com/41258687d868cf76951a37f6be7961c4c862dfb3/687474703a2f2f692e696d6775722e636f6d2f6c4b6762336c712e706e67)](http://commixproject.com)

[![Build Status](https://api.travis-ci.org/commixproject/commix.svg?branch=master)](https://api.travis-ci.org/commixproject/commix) 
[![Version 2.1](https://img.shields.io/badge/Version-2.1-green.svg)](https://github.com/commixproject/commix/releases/tag/v2.1-20171003
)
[![Python 2.6-2.7](https://img.shields.io/badge/Python-2.6--2.7-yellow.svg)](http://www.python.org/download/)
[![GPLv3 License](https://img.shields.io/badge/License-GPLv3-red.svg)](https://github.com/commixproject/commix/blob/master/readme/COPYING)
[![Twitter](https://img.shields.io/badge/Twitter-@commixproject-blue.svg)](http://www.twitter.com/commixproject)


This is a commix 'API' tool forked from the original commix,check command injection tool,used for command injection vulnerability scan.

Usage:
    eg:
    `py2 commix.py -u "http://192.168.93.139/dvwa/vulnerabilities/exec/#" -d "ip=1&Submit=Submit" --cookie "PHPSESSID=frselcstsnts1lsbddpee8du74;security=low" -p ip -v 3 --ignore-session --batch`

The usage is the same as original commix,if there exists a vul,commix will stop and print "The parameter 'xx' seems injectable",we can use regexp to match it to check whether there exist a vul,eg:

```
import re
if re.search(r"The parameter.*seems injectable",commix_output_string,re.I):
    print("vul exists")
```
