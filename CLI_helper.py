
from HiLinkAPI import webui

import logging
import sys
from time import sleep, time
from datetime import datetime


def logout(webUI):
    print("= Log out")
    webUI.stop()
    while(not webUI.isStopped()):
         webUI.stop()
         print(f"= Waiting for stop")
         sleep(1)

def dump(webUI):
    print("= dump:")
    webUI.queryDeviceInfo()
    webUI.queryWANIP()
    webUI.queryNetwork()
    webUI.queryDataConnection()

    deviceInfo = webUI.getDeviceInfo()
    for key in deviceInfo.keys():
        print(f"{key}\t:{deviceInfo[key]}")

    print(f"WAN_IP\t:{webUI.getWANIP()}")
    print(f"CELLOP\t:{webUI.getNetwork()}")

def usage():
    print(sys.argv[0] +" IP LOGIN PW <noop|dump|list_sms|reboot|data_on|data_off|reset_ip|mode_auto|mode_4g")
    sys.exit(1)

def main():

    try:    ip=sys.argv[1]
    except: usage()
    try:    login=sys.argv[2]
    except: usage()
    try:    password=sys.argv[3]
    except: usage()
    try:    action=sys.argv[4]
    except: usage()


    allowed_actions=[ "noop", "dump", "list_sms", "reboot", "data_on", "data_off", "reset_ip", "mode_auto", "mode_4g" ]

    if not action in allowed_actions:
        usage()

    logging.basicConfig(filename="hilinkapitest.log", format='%(asctime)s --  %(message)s', level=logging.DEBUG, datefmt="%Y-%m-%d %I:%M:%S %p:%Z")
    #webUI=webui("mymodem", "192.168.10.18", "admin",  'Labuga21!!!!'  , logger=logging, scheme='https')
    webUI=webui("mymodem", ip , login , password , logger=logging, scheme='https')
    webUI.start()
    max_attempts=2
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
            logout(webUI)
            sys.exit(1)

    print("= Logged in")

    if  action == "dump"         : dump(ctx)
    elif action == "noop"   : pass 
    elif action == "list_sms"   : list_sms(ctx)
    elif action == "reboot"     : reboot(ctx)
    elif action == "data_on"    : data_on(ctx)
    elif action == "data_off"   : data_off(ctx)
    elif action == "reset_ip"   : reset_ip(ctx)
    elif action == "mode_auto"   : mode_auto(ctx)
    elif action == "mode_4g"   : mode_4g(ctx)
    else:
        usage()

    logout(webUI)

main()
