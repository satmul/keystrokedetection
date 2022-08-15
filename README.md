# Keystroke Injection Detection

## Installation

- `git clone https://github.com/satmul/keystrokedetection`
or
- `wget https://github.com/satmul/keystrokedetection -r`
- `cd keystrokedetection`
- `pip3 install -r requirements.txt`

- `apt-get install xinput` for Linux

## Usage

For Windows, open the Command Prompt with Run As Administrator.

```
GUI:
1. Run the gui.py via CLI -> python3 gui.py
2. Input the Word Per Minute (WPM) threshold
3. Choose if you want to enable the blacklist keyword feature or not, enable the random keystroke or enable the remove device feature (Currently for Windows Only).
4. Search attack keyword from Log Files
5. Open Log file
```

```
CLI:
usage: cli.py [-h] -t THRESHOLD [-b BAN] [-r REMOVE] [-rk RAND] [--gui-alert]

Keystroke Injection Detection

optional arguments:
  -h, --help            show this help message and exit
  -b BAN, --ban BAN     Ban Keywords (default: ON) | -b 0 to turn it off
  -r REMOVE, --remove REMOVE
                        Remove device based on signature [0/1] (Windows only)
  -rk RAND, --rand RAND
                        Random keystroke [0/1]
  --gui-alert           Alert Keystroke Detection with GUI

required named arguments:
  -t THRESHOLD, --threshold THRESHOLD
                        Threshold for Keystroke Injection Detection
                      
```

Every keystroke will be logged at the logs folder with file name format [date]_[time]_log.txt
