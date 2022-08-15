from asyncore import read
from cmath import pi
import sys
import os
from tkinter import *
from tkinter import messagebox,ttk
import threading
import subprocess
import signal
from tkinter import filedialog
from gui_script import start_rand_keystroke


get_status_ban = 0
get_status_remove = 0
get_status_randkey = 0
get_status_run = 0
### GUI SETTINGS

window=Tk()

window.title("Keystroke Injection Detection")
window.geometry('800x400')
# window.configure(bg="blue")
window.resizable(width=False, height=False) #maintain positions (fixed)


tabControl = ttk.Notebook(window)
  
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text ='Detection')
tabControl.add(tab2, text ='Logging')
tabControl.pack(expand = 1, fill ="both")


# Title tab 1
def title(name,xpos,ypos,pos):
    title_var = StringVar()
    title_var.set(name)
    title_var_final = Label(tab1,textvariable = title_var)
    title_var_final.place(x = xpos, y = ypos, anchor = pos)

def title2(name,xpos,ypos,pos):
    title_var = StringVar()
    title_var.set(name)
    title_var_final = Label(tab2,textvariable = title_var)
    title_var_final.place(x = xpos, y = ypos, anchor = pos)

def title_usage(name,xpos,ypos,pos):
    title_var = StringVar()
    title_var.set(name)
    title_var_final = Label(tab1,textvariable = title_var,font=("Arial", 12))
    title_var_final.place(x = xpos, y = ypos, anchor = pos)

def title2_usage(name,xpos,ypos,pos):
    title_var = StringVar()
    title_var.set(name)
    title_var_final = Label(tab2,textvariable = title_var,font=("Arial", 12))
    title_var_final.place(x = xpos, y = ypos, anchor = pos)

title_usage('Usage:',0.0,10,'nw')

if (sys.platform == "win32" or sys.platform == "win64"):
    title_usage('1. Input Threshold: Detect WPM from keystroke (Required)',0.0,35,'nw')
    title_usage('2. Ban Keywords: Ban keywords from keystroke',0.0,55,'nw')
    title_usage('3. Remove USB: Remove malicious usb',0.0,75,'nw')
    title_usage('4. Random Keystroke: Input random keystroke with random time',0.0,95,'nw')
    title_usage('5. Always Run: Always run detection',0.0,115,'nw')
    
if sys.platform == "linux" or sys.platform == "linux2":
    title_usage('1. Input Threshold: Detect WPM from keystroke (Required)',0.0,35,'nw')
    title_usage('2. Ban Keywords: Ban keywords from keystroke',0.0,55,'nw')
    title_usage('3. Random Keystroke: Input random keystroke with random time',0.0,95,'nw')




title2_usage('Usage:',400,10,'nw')
title2_usage('1. Open Log: see attack log history',380,35,'nw')
title2_usage('2. Log Search: search attack keyword from log file',380,65,'nw')



#get Threshold
#inputtxt = Text(window,height = 1,width = 5)
#inputtxt.place(x = 150,y = 100,anchor='nw') 

# Ban keywords title    
title('Set WPM Threshold',0.0,140,'nw')
title('Ban Keywords',0.0,170,'nw')

slider_value = DoubleVar()

def get_current_value():
    return '{:.0f}'.format(slider_value.get())

def slider_changed(event):
    value_label.configure(text=get_current_value())

slider = ttk.Scale(
    tab1,
    from_=50,
    to=150,
    orient='horizontal',
    command=slider_changed,
    variable=slider_value
)

slider.place(x=150,y=140)
value_label = ttk.Label(tab1,text=get_current_value())
value_label.place(x=260,y=140)

#Log filename text box
title2('Log Filename: ',10,0,'nw')
file_name_label = Entry(tab2)
file_name_label.insert(END,"No file opened")
file_name_label.config(state=DISABLED)
file_name_label.place(x=10,y=20)

def open_log():
    files = filedialog.askopenfilename(initialdir="", title="Open Log",filetypes=(("Text Files","*.txt"),))
    file_name_label.config(state=NORMAL)
    file_name_label.delete(0,'end')
    file_name_label.insert(END,os.path.basename(files))
    file_name_label.config(state=DISABLED)
    files = open(files,'r')
    log = files.read()
    read_log_area.config(state=NORMAL)
    read_log_area.delete('1.0', END)
    read_log_area.insert(END,log)
    files.close()
    read_log_area.config(state=DISABLED)


#Log preview scrollbar
scroll = Scrollbar(tab2)
scroll.pack(side=RIGHT,fill=Y,padx=390,pady=100)



#Log Preview text box
title2('Log Preview',10,90,'nw')
read_log_area = Text(tab2, width= 47, height=10,yscrollcommand=scroll.set)
read_log_area.insert(END,"No File opened")
read_log_area.config(state=DISABLED)
read_log_area.pack(side=LEFT)
read_log_area.place(x=10,y=110)
openfile_button = Button(tab2, text="Choose Log File",command=open_log)
openfile_button.place(x=10,y=50)
scroll.config(command=read_log_area.yview)





#Log search text box
title2('Log Search: ',150,0,'nw')
log_search_label = Entry(tab2,width=25)
log_search_label.place(x=150,y=20)

#### Log search function
def find_str():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'
    LOG_DIR = ROOT_DIR + 'log'
    strings = str(log_search_label.get())
    file_name_label.config(state=NORMAL)
    file_name_label.delete(0,'end')
    file_name_label.insert(END,"No file opened")
    file_name_label.config(state=DISABLED)
    if len(strings) > 0:
        read_log_area.config(state=NORMAL)
        read_log_area.delete('1.0', END)
        #read_log_area.tag_remove('found', '1.0', END)
        for files in os.listdir(LOG_DIR):
            cur_path = os.path.join(LOG_DIR, files)
            if os.path.isfile(cur_path):  
                with open(cur_path, 'r') as file:
                    contents = files + ":\n" + file.read() + '\n\n'
            if strings in contents:
                read_log_area.config(state=NORMAL)
                read_log_area.tag_config('found', foreground='black',background='blue')    
                read_log_area.insert(END,contents)
                #read_log_area.config(state=DISABLED)        
                read_log_area.tag_remove('found', '1.0', END)
        
                
                if strings:
                    start_idx = '1.0'
                    while 1:
                        start_idx = read_log_area.search(strings, start_idx, nocase=1,
                                        stopindex=END)
                        if not start_idx: break
                        lastidx = '%s+%dc' % (start_idx, len(strings))
                        read_log_area.tag_add('found', start_idx, lastidx)
                        start_idx = lastidx
                    
                    #mark located string as red
                    read_log_area.tag_config('found', foreground='white')
    else:
        messagebox.showerror("ERROR","Fill the box.")




#Log Search button
log_search_button = Button(tab2,text="Search text",command=find_str)
log_search_button.place(x=150,y=50)


# Ban Keywords checkbox 
def get_options():
    global get_status_ban
    if v1.get() == 1:
        get_status_ban = 1
        if get_status_ban == 1:
            print("Ban Keywords Feature Enabled")

    if v1.get() == 0:
        get_status_ban = 0
        if get_status_ban == 0:
            print("Ban Keywords Feature Disabled")

    return get_status_ban

def remove_options():
    global get_status_remove
    if v2.get() == 1:
        get_status_remove = 1 
        if get_status_remove == 1:
            print("Remove Device Feature Enabled")
    if v2.get() == 0:
        get_status_remove = 0
        if get_status_remove == 0:
            print("Remove Device Feature Disabled")
    return get_status_remove

# Random keystroke checkbox 
def random_key_options():
    global get_status_randkey 
    if v3.get() == 1:
        get_status_randkey = 1
        if get_status_randkey == 1:
            print("Random keystroke Feature Enabled")

    if v3.get() == 0:
        get_status_randkey = 0
        if get_status_randkey == 0:
            print("Random keystroke Feature Disabled")

    return get_status_randkey

def always_run():
    global get_status_run
    if v4.get() == 1:
        get_status_run = 1
        if get_status_run == 1:
            print("Always Run Enabled")

    if v4.get() == 0:
        get_status_run = 0
        if get_status_run == 0:
            print("Always Run Disabled")

    return get_status_run

v1 = IntVar()
v2 = IntVar()
v3 = IntVar()
v4 = IntVar()
ban_cb = Checkbutton(tab1, text='Enable',variable=v1, onvalue=1, offvalue=0, command=get_options)
ban_cb.place(x = 180, y = 180,anchor = 'nw')

if (sys.platform == "win32" or sys.platform == "win64"):
    title('Remove Device (Windows Only)',0.0,200,'nw')
    remove_cb = Checkbutton(tab1, text='Enable',variable=v2, onvalue=1, offvalue=0, command=remove_options)
    remove_cb.place(x = 180, y = 210,anchor = 'nw')

    
title('Random Keystroke',0.0,230,'nw')
rand_cb = Checkbutton(tab1, text='Enable',variable=v3, onvalue=1, offvalue=0, command=random_key_options)
rand_cb.place(x = 180, y = 240,anchor = 'nw')

title('Always Run Script',0.0,260,'nw')
run_cb = Checkbutton(tab1, text='Enable',variable=v4, onvalue=1, offvalue=0, command=always_run)
run_cb.place(x = 180, y = 270,anchor = 'nw')



#Run Script with GUI
def run():
    global threshold_args,banned_args,pid,get_status_ban,get_status_randkey,get_status_run

    try:
        threshold_args = int(get_current_value())
        banned_args = get_status_ban

        if threshold_args > 0:
            pid = subprocess.Popen(['python3', 'gui_script.py','-t',str(threshold_args),'-b',str(banned_args),'-r',str(get_status_remove),"--gui-alert","-rk",str(get_status_randkey),"--run",str(get_status_run)], shell=False)
            messagebox.showinfo("Info","Script is running")
        else:
            messagebox.showerror("Error", "Please input threshold more than 0")

    except ValueError:
        messagebox.showerror("Error", "Please input number only.")
   
        

def threading_process():
    threading.Thread(target=run).start()

def stop():
    global pid
    try:
        pid.terminate() #Terminate Keystroke Script
        
        messagebox.showinfo("Info","Stopping script, press OK to continue")
    
    except NameError:
        pass
    

start_btn = Button(tab1, text = "Run Script", bg = "black", fg = "white",command = threading_process)
start_btn.place(x = 200, y = 300, anchor = 'n')


stop_btn = Button(tab1, text = "Stop Script", bg = "black", fg = "white",command = stop)
stop_btn.place(x = 200, y = 330, anchor = 'n')

window.mainloop()