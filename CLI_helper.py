
from HiLinkAPI import webui

import logging
import sys
from time import sleep, time
from datetime import datetime

logging.basicConfig(filename="hilinkapitest.log", format='%(asctime)s --  %(message)s', level=logging.DEBUG, datefmt="%Y-%m-%d %I:%M:%S %p:%Z")

webUI=webui("mymodem", "192.168.10.18", "admin",  'Labuga21!!!!'  , logger=logging, scheme='https')

webUI.start()

max_attempts=5
i=0

while not webUI.getValidSession():
    sleep(1)
    i+=1
    print(f"= logging in, attempt {i}/{max_attempts}")
    # check for active errors
    if webUI.getActiveError() is not None:
           error = webUI.getActiveError()
           print(f"= {error}")
           sleep(1)
    else:
        pass
    # check for login wait time
    if webUI.getLoginWaitTime() > 0:
           print(f"= Login wait time available = {webUI.getLoginWaitTime()} minutes")
           sleep(1)
    else:
        pass
    if i  == max_attempts :
        print(f"= max attempts reached")
        webUI.stop()
        while(not webUI.isStopped()):
             webUI.stop()
             print(f"= Waiting for stop")
             sleep(1)
        sys.exit(1)

print("= got session")

if True:

            webUI.queryDeviceInfo()
            webUI.queryWANIP()
            webUI.queryNetwork()
            webUI.queryDataConnection()

            deviceInfo = webUI.getDeviceInfo()
            for key in deviceInfo.keys():
                print(f"{key}\t:{deviceInfo[key]}")

            print(f"WAN_IP\t:{webUI.getWANIP()}")
            print(f"CELLOP\t:{webUI.getNetwork()}")
            print("")

webUI.stop()
while(not webUI.isStopped()):
     webUI.stop()
     print(f"= Waiting for stop")
     sleep(1)

