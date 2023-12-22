#!/usr/bin/python3

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

def data_on(webUI):
    print(f"= Data ON\n{webUI.switchConnection(True)}")
    wait_data(webUI)

def data_off(webUI):
    print(f"= Data OFF\n{webUI.switchConnection(False)}")

def wait_data(webUI):
    print("=> Wait data")
    max_attempts=20
    i=0
    while True:
        i+=1
        webUI.queryWANIP()
        print("= attempt "+str(i) )
        ip=webUI.getWANIP()
        #print(ip)
        if ip:
            print("= got Data "+ip)
            return True
        else:
            sleep(1)
    print("= no data, give up")
    return False

def mode_auto(webUI):
    print("=>Auto")
    ret = webUI.setNetwokModes("AUTO", "WCDMA")
    print(f"Network mode setting = {ret}")
    ret = webUI.switchNetworMode(True)
    print(f"Switching = {ret}")

def mode_4g(webUI):
    print("=>4g")
    ret = webUI.setNetwokModes("LTE", "WCDMA")
    print(f"Network mode setting = {ret}")
    ret = webUI.switchNetworMode(True)
    print(f"Switching = {ret}")

def reset_ip(webUI):
    print("=>Reset IP")
    mode_4g(webUI)
    mode_auto(webUI)
    wait_data(webUI)

def reboot(webUI):
    print("=>Reboot")
    ret=webUI.reboot()
    print(ret)

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

    ret=HiLinkGET(webUI, "/api/monitoring/status")
    print(ret)

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
    max_attempts=6
    i=0

    while not webUI.getValidSession():
        sleep(1)
        i+=1
        print(f"= logging in, attempt {i} of max_attempts {max_attempts}")
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

    if  action == "dump"        : dump(webUI)
    elif action == "noop"       : pass 
    elif action == "list_sms"   : list_sms(webUI)
    elif action == "reboot"     : reboot(webUI)
    elif action == "data_on"    : data_on(webUI)
    elif action == "data_off"   : data_off(webUI)
    elif action == "reset_ip"   : reset_ip(webUI)
    elif action == "mode_auto"  : mode_auto(webUI)
    elif action == "mode_4g"    : mode_4g(webUI)
    else:
        usage()

    logout(webUI)

main()

# H112-370
