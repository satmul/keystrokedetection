import subprocess
import re
import difflib
import os


def get_device_difference():
    flag = 0
    try:
        find_device_regex = re.compile(r"(\+ HID\\\w+&)")
        with open("init.txt",'r') as before:
            device_init = before.readlines()
        with open("after.txt",'r') as after:
            device_after = after.readlines()
        d = difflib.Differ()
        diff = d.compare(device_init, device_after)
        device_diff = ''.join(diff)
        device_hwid = find_device_regex.findall(device_diff)[0].replace('+','').replace(' ','').replace('&','').replace('\\\\','\\')
        flag = 1
        
        return device_hwid,flag
    except IndexError:
        print("[!] No device changes detected (attack probably with your own physical keyboard)")
        
    

def check_device_windows(filename):
    device_list = subprocess.Popen(['devcon.exe', 'find', '*HID*'],stdout=subprocess.PIPE)
    output = device_list.stdout.read()
    find_usb = re.compile(r"(HID\\\w+&)")
    parsed = find_usb.findall(str(output.decode()))
    f = open(filename,'w+')
    f.write(str(output.decode()))
    f.close()

def remove_usb_windows(device_hwid):
    try:
        if len(read_known_device())>0: 
            remove = subprocess.run(['devcon.exe', 'remove', "*"+ device_hwid+"*"],stdout=subprocess.PIPE)
        #print(str(remove.stdout).replace("b",'').replace('\\r\\n',''))
        else: quit()
    except TypeError:
        print("Error Removing USB, Check Signature")

def add_known_device(device_hwid):
    f = open('known_HID.txt','w+')
    f.write(device_hwid)
    f.close()


def read_known_device():
    f = open('known_HID.txt','r')
    device = f.readline()
    f.close()
    return device

def check_malicious_device():
    hid = read_known_device()
    print(hid)
    list = os.popen('devcon.exe find *HID*').read()
    if hid in list:
        print("Malicious Signature Detected.. Blocking")
        remove_usb_windows(hid)
       
    else:
        print("No known device...")
        quit()
