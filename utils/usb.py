import re
import time
import psutil
import datetime
import subprocess
from utils.db import get_usb_information

def get_devices():
    device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
    df = subprocess.check_output("lsusb").decode()
    devices = []
    for i in df.split('\n'):
        if i:
            info = device_re.match(i)
            if info:
                dinfo = info.groupdict()
                dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                devices.append(dinfo)
    return devices

def get_input_device():
    process = subprocess.Popen(['ls', '/dev/input/by-id'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    return out.decode()

def detect_keyboard(data):
    if data[1] is not None:
        if "keyboard" in data[1].lower():
            print('[!] Potential keyboard attacks: '+str(data))

def live_logging_usb(DB_PATH, pid):
    print("[!] Live Logging activate")
    master_connected_devices = get_devices()
    live_device_arr = []
    filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
    
    with open(filename, "a+") as f:
        for dev in master_connected_devices:
            f.write(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ', ' + dev['id'] + ' ' + dev['tag'] + ' connected\n')
            live_device_arr.append(dev)
    
    main_thread_ps = psutil.Process(pid=pid)

    while True:
        try: 
            if main_thread_ps.status() in (psutil.STATUS_DEAD, psutil.STATUS_STOPPED):
                break
        except psutil.NoSuchProcess:
            break

        curr_connected_devices = get_devices()
        if len(curr_connected_devices) > len(live_device_arr):
            for dev in curr_connected_devices:
                if dev not in live_device_arr:
                    with open(filename, "a+") as f:
                        f.write(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ', ' + dev['id'] + ' ' + dev['tag'] + ' connected\n')
                    vid,pid = dev['id'].split(':')
                    db_data = get_usb_information(DB_PATH, vid, pid)
                    detect_keyboard(db_data)
        elif len(curr_connected_devices) < len(live_device_arr):
            for dev in live_device_arr:
                if dev not in curr_connected_devices:
                    with open(filename, "a+") as f:
                        f.write(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ', ' + dev['id'] + ' ' + dev['tag'] + ' disconnected\n')
                    break
        live_device_arr = curr_connected_devices