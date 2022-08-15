import os
import re
import sys
import keyboard
from time import sleep
from tkinter import Tk, messagebox
from utils.models import Device
from utils.log import write_date
from utils.windows_detect import *
logs_temp = ""
blacklisted_word = [] # load from config path
BANNED_DEVICE = [] # load from config path



def create_banned_device_usb(vendor_id, device_id):
    return """ACTION=="add", ATTR{idVendor}=="VENDOR_ID", ATTR{idProduct}=="DEVICE_ID", RUN=\"/bin/sh -c 'echo 0 >/sys/\$devpath/authorized'\"""".replace("VENDOR_ID",vendor_id).replace("DEVICE_ID",device_id)

def get_xinput_data_to_vid_pid(device):
    cmd = 'cat /proc/bus/input/devices'
    process = os.popen(cmd)
    data = process.read().split("\n\n")
    process.close()
    
    bus_data = ""
    FOUND_STATUS = False
    for d in data:
        if device in d:
            bus_data = d
            FOUND_STATUS = True
            break
    
    if FOUND_STATUS == False:
        print("Data not found")
        return None
    else:
        result = re.findall("Vendor=(\w+)\ Product=(\w+)\ ", bus_data)
        if len(result) == 0:
            print("Data not found")
            exit(1)
        vendor_id, product_id = result[0][0], result[0][1]
        return vendor_id, product_id

def check_banned_device(data, config):
    for device in config['BANNED_DEVICE']:
        if device in data.lower():
            return True
    return False

def check_whitelist_device(vendor_id, device_id, config):
    for device in config['WHITELIST_DEVICE']:
        if device['vendor_id'] == vendor_id and device['device_id'] == device_id:
            return False
    return True

def get_virtual_core_keyboard_data(config):
    get_data = False
    possible_attack_device = []
    check_keyboard = os.popen("xinput list").readlines()
    for line in check_keyboard:
        if "Virtual core keyboard" in line:
            get_data = True
            continue
        elif get_data == False:
            continue
        elif check_banned_device(line, config):
            continue
        check_keyboard = line.replace('↳',"")
        device_id, slave_id = re.findall('id=([0-9]+)\s+\[slave  keyboard \(([0-9]+)\)\]',check_keyboard)[0]
        name = re.findall('([\w\s]+)id=', check_keyboard)[0]
        possible_attack_device.append(Device(device_id, slave_id, name))
    return possible_attack_device

def banned(key, config):
    global logs_temp,blacklist 
    ##Blacklist filter
    logs_temp += str(key)
    blacklist = ""

    for logs_filter in logs_temp: 
        blacklist_replace = logs_filter.replace("'","")
        blacklist += blacklist_replace
    
    for x in range(len(config['BLACKLIST_WORD'])):
        if blacklist.lower().find(config['BLACKLIST_WORD'][x]) != -1:   
            return config['BLACKLIST_WORD'][x]#Banned Keystroke
       

    return 0 #No Banned keystroke 

def create_banned_device_rules(data, config):
    try:
        with open("/etc/udev/rules.d/keystroke-prevention.rules", "w") as f:
            f.write("# Disable USB with malicious vendor and device id\n")
            # data = [('16d0','0753'), ('16c0','27db')]
            for d in data:
                temp = get_xinput_data_to_vid_pid(d.name)
                if temp == None:
                    continue
                elif check_whitelist_device(temp[0], temp[1], config):
                    f.write(create_banned_device_usb(temp[0], temp[1])+"\n")

            os.popen("sudo udevadm control --reload")
    except PermissionError:
        print('[!] Permission denied on /etc/udev/rules.d/, run using sudo')
    except Exception as e:
        print('[!] Exception : ' + e)

def show_alert():
    window = Tk()
    window.geometry('0x0')
    messagebox.showwarning("WARNING","Keystroke Injection Detected! Blocking Keyboard... Press OK to re-enable your keyboard")
    window.destroy()
   

def block_keystroke(type_alert, config):
    #Checking keyboard with xinput
    write_date()
    if sys.platform == "win32" or sys.platform == "win64":
        from ctypes import windll
        print("Blocking Keyboard & Removing USB")
        check_device_windows("after.txt") #Creating USB signature differences
        print("[+] Adding malicious device signature")
        if str(get_device_difference()) != "None":
            add_known_device(get_device_difference()[0])
        

        #### deprecated
        # for i in range(150):
        #     keyboard.block_key(i)
        #windll.user32.BlockInput(True)
        #sleep(3)
        #windll.user32.BlockInput(False)
        
   
        pid = subprocess.Popen(['python3','utils/ban_keyboard_win.py'],shell=False)
        if type_alert == "gui":
            show_alert()
        sleep(5)
        #close_win()
        pid.kill()

        


    elif sys.platform == "linux" or sys.platform == "linux2":
        data = get_virtual_core_keyboard_data(config)
        print("[*] Blocking Keystroke for 5 Seconds")
        for d in data:
            keyboard_id = d.device_id
            keyboard_master = d.slave_id

            #Disabling Keyboard Input
            disable_keyboard = os.system('xinput float {}'.format(keyboard_id))

        if type_alert == "gui":
            messagebox.showwarning("WARNING","Keystroke Injection Detected! Blocking Keyboard... Press OK to re-enable your keyboard")

        sleep(5)

        for d in data:
            keyboard_id = d.device_id
            keyboard_master = d.slave_id

            #Reenable Keyboard Input in 5 seconds
            reenable_keyboard = os.system('xinput reattach {} {}'.format(keyboard_id,keyboard_master))

        print("[!] Creating banned rules for keyboard devices")
        create_banned_device_rules(data, config)