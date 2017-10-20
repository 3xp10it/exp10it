import os
os.system("pcregrep -M '^def .*\(((.*)|(\n(.*,\n)*.*))\):\n((\s)*#.*\n){1,10}' exp10it.py > api.md")
