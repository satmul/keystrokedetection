from time import time
from pynput.keyboard import Listener
from time import sleep
from utils.log import logging,text
from utils.ban import block_keystroke, banned
from pynput.keyboard import Key
from utils.windows_detect import check_device_windows
from utils.config import import_yaml
import os, sys

threshold_args = 0 #Threshold args variable
blacklist = ""
final_wpm = 0 #Initialize WPM
detected = 0 #Initialize injection value 
timestamp = [200] #Store Timestamp per Keystroke // prevent ms to block early
type_alert = "" #The type alert that will be shown on script
banned_args = 0 #Banned args variable 
repeat_args = 0
CONFIG = ""
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'
INIT_PATH = ROOT_DIR + "../init.txt"

COMBINATION = {Key.ctrl_l, Key.alt_l,Key.backspace}
current=set()

if sys.platform == "win32" or sys.platform == "win64":
    check_device_windows(INIT_PATH)

#Initialize Time when script is started
if sys.platform == "win32" or sys.platform == "win64":
    import keyboard
    while True:
        if keyboard.read_key():
            #print("Keystroke detected")
            break

t0 = time()
t2 = time()
final_wpm = 0
def on_press(key):
    global detected,banned_args,empty_argv,t0,type_alert,CONFIG,final_wpm,repeat_args

    logging(key) 
    t1 = time()
    delta_time = (t1 - t0)*1200
    delta_time_wpm = t1 - t2
    final_wpm = len(text) * 60 / (5*delta_time_wpm)

    timestamp.append(delta_time)
    avg = sum(timestamp[-20:]) /20 

    t0 = t1
    print("avg = ",avg)
    print("wpm = ",final_wpm)

    if key in COMBINATION:
        current.add(key)
        if all(k in current for k in COMBINATION):
            print('[!] Deactivating keyboard detection')
            return False

    if banned_args == 0 and (avg <= 20) or (final_wpm >= threshold_args):
        print("[!] Keystroke injection detected.")
        block_keystroke(type_alert, CONFIG)
        if repeat_args == 0:
            exit()
        detected = 1


    if key == Key.shift_l or key == Key.shift or key == Key.shift_r: #Avoid false ban when shift pressed
        key = str('SHIFT')
    
    if key == Key.cmd: #Avoid false ban when cmd pressed (windows key)
        key = str("Windows Key") 

    if banned_args == 1 and banned(key, CONFIG) != 0 and avg < 20 : #If return status = 0 , keystroke is safe from suspicious program && check if ban feature is not disabled
        print("[!] Keystroke injection detected.")
        print("\n[!!!] Banned Keystroke = " + banned(key, CONFIG)+"\n")
        block_keystroke(type_alert, CONFIG)
        exit()
    


    
def on_release(key):
    # Stop listener
    global current
    current = set()
    pass


def run_detection(threshold, ban, type, config_path,repeat):
    global banned_args,threshold_args,text,blacklisted_word,type_alert,CONFIG,repeat_args

    try:
        type_alert = type
        threshold_args += threshold
        CONFIG = import_yaml(config_path)
        if ban == 1: # checking if user turn off the ban feature
            banned_args = 1
        
        if repeat == 1:
            repeat_args = 1

        if sys.platform == "win32" or sys.platform == "win64":
            check_device_windows("after.txt")
        print("Keypress detected ! Running script with {} WPM threshold".format(threshold))
        
        
        # Collect events until released
        with Listener(on_press=on_press,on_release=on_release) as listener:
            listener.join()
        
    except Exception as e:
        print(e)


