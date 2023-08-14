import os,time
while True:
    os.system("screen python3 main.py")
    time.sleep(1)
    os.system("killall screen")
