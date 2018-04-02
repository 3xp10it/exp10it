a=1
def b():
    global a
    a=2
while 1:
    import time
    time.sleep(0.5)
    print(a)
