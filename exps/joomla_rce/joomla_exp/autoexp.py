import os
def check(url):
    cmd = 'python joomla_exp.py '+url+' >> PCLOK.txt'
    p = os.popen(cmd)
    print p.read()
if __name__ == '__main__':

    fp=open("url.txt", "r")
    alllines=fp.readlines()
    fp.close()
    for eachline in alllines:
            eachline=eachline.strip('\n')
            eachline=eachline.strip(' ')
            check(eachline)