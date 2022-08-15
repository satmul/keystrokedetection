import pythoncom as pc, pyHook as ph
from time import time
import string
import threading


def OnKeyboardEvent(event):
  # block only the letter A, lower and uppercase
  strz = [(i) for i in range(0,256)]
  return (event.Ascii not in (strz)) #if kena baru masuk pumpmessage

hm = ph.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()

pc.PumpMessages()

