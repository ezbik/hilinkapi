
from HiLinkAPI import webui

import logging
from time import sleep, time
from datetime import datetime

logging.basicConfig(filename="hilinkapitest.log", format='%(asctime)s --  %(message)s', level=logging.DEBUG, datefmt="%Y-%m-%d %I:%M:%S %p:%Z")


webUI=webui("E", "192.168.10.14", "admin",  'Labuga21!!!!'  , logger=logging)

webUI.start()

while not webUI.getValidSession():
                # check for active errors
                if webUI.getActiveError() is not None:
                    error = webUI.getActiveError()
                    print(error)
                    sleep(5)
                # check for login wait time
                if webUI.getLoginWaitTime() > 0:
                    print(f"Login wait time available = {webUI.getLoginWaitTime()} minutes")
                    sleep(5)


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
     print(f"Waiting for stop")
     sleep(1)

