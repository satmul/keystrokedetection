#import pyautogui as keyboard 
import string
import random
import keyboard
from time import sleep

def rand_key():
    keys = string.ascii_lowercase+'1234567890'
    for x in range(0,10000):
        random_choice = random.choice(keys)
        keyboard.write(str(random_choice))
        sleep(random.uniform(0.3,0.8))

rand_key()