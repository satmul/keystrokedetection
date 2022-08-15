import re
import requests

def read_file_information(path):
    with open(path) as f:
        content = f.readlines()
    return content

def get_txt_information(DB_PATH):
    db = requests.get('http://www.linux-usb.org/usb.ids', timeout=10).text
    with open(DB_PATH, "w") as f:
        f.write(db)


def get_usb_information(DB_PATH,vid,pid):
    content = read_file_information(DB_PATH)
    re_vid = re.compile(rf'^{vid}  (.*?$)')
    re_pid = re.compile(rf'^\t{pid}  (.*?$)')
    vid_source = None
    pid_source = None

    for num,line in enumerate(content):
        vid_match = re_vid.match(line)
        if vid_match:
            vid_source = vid_match.group(1)
            for subnum,subline in enumerate(content[num+1:]):
                if subline[0] == '\t':
                    pid_match = re_pid.match(subline)
                    if pid_match:
                        pid_source = pid_match.group(1)
                        break
            return (vid_source, pid_source)
    return (vid_source, pid_source)