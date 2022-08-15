#! /usr/bin/python3
import os, sys, subprocess
import argparse
import threading
import ctypes
from utils.main import run_detection,final_wpm
from utils.db import get_txt_information
from utils.usb import live_logging_usb
from utils.windows_detect import check_device_windows,remove_usb_windows,read_known_device,check_malicious_device
from time import sleep

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'
DB_PATH = ROOT_DIR + "db.txt"


flag = 0

def start_rand_keystroke():
    pid_rand = subprocess.Popen(['python3','utils/random_keystroke.py'],shell = False)
    return pid_rand

if __name__ == "__main__":
    program_parser = argparse.ArgumentParser(description='Keystroke Injection Detection')
    requiredNamed = program_parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-t', '--threshold',help='Threshold for Keystroke Injection Detection', required=True)
    requiredNamed.add_argument('-run', '--run',help='Always Run', required=True,type=int)
    program_parser.add_argument('-b','--ban', help='Ban Keywords (default: ON) | -b 0 to turn it off',type=int)
    program_parser.add_argument('-r','--remove', help='Remove device based on signature [0/1] (Windows only)',type=int)
    program_parser.add_argument('-rk','--rand', help='Random keystroke [0/1]')
    program_parser.add_argument('--gui-alert', default=False, action="store_true", help='Alert Keystroke Detection with GUI')
    args = program_parser.parse_args()

    if not args.threshold.isnumeric():
        print('Use -h to see help message')
        
    if int(args.threshold) <= 0:
        print('Threshold must be above 0')
        flag = 1

    if not os.path.exists(DB_PATH):
        get_txt_information(DB_PATH)
    
    try:
        if int(args.rand) == 1:
            pid_rand = start_rand_keystroke()
    except TypeError:
        pass

    if (sys.platform == "win32" or sys.platform == "win64"):
        if args.remove != None:
            if args.remove > 1 or args.remove < 0 :
                flag = 1
                print("[!] ERROR Remove argument must be 0 or 1")
        if ctypes.windll.shell32.IsUserAnAdmin() != 1:
            print("[X] Please run script as Administrator")
            exit()
               
        if args.remove == 1: ##Removing device based on signature
            try:
                check_malicious_device()
                if remove_usb_windows(read_known_device()).find('No devices were removed.'):
                    flag = 0
                
                else: exit()
            except:
                pass


    if sys.platform == "linux" or sys.platform == "linux2":
        pid = os.getpid()
        x = threading.Thread(target=live_logging_usb, args=(DB_PATH,pid), daemon=True)
        x.start()
    elif flag == 1 and (sys.platform == "win32" or sys.platform == "win64"):
        os.system('del init.txt')
        #exit()
    
    print(args.ban)
    # live_logging_usb(DB_PATH)
    run_detection(int(args.threshold), args.ban, "gui", ROOT_DIR + '/config.yaml',args.run) if args.gui_alert else run_detection(int(args.threshold), args.ban, "cli", ROOT_DIR + '/config.yaml',args.run)
    
    if (sys.platform == "win32" or sys.platform == "win64"):
        os.system('del init.txt after.txt')
    
    try:
        pid_rand.kill()
    except NameError: 
        pass
    print("Main Thread Closed & USB Signature Removed")
   