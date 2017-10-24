import os
os.system("echo '```' > api.md")
os.system("pcregrep -M '^def .*\(((.*)|(\n(.*,\n)*.*))\):\n((\s)*#.*\n){1,10}' exp10it.py >> api.md")
os.system("echo '```' >> api.md")
