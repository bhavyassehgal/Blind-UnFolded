import os
import sys
import time
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from datetime import datetime
from pydub import AudioSegment
from cryptography.fernet import Fernet
import beepy
import threading

def startup():
    '''function to check at startup if the program is run for the first time or not'''

    files=os.listdir("C:\\ProgramData\\")
    if "Blind Unfolded" not in files:
        os.mkdir("C:\\ProgramData\\Blind Unfolded")
    
    files=os.listdir("C:\\ProgramData\\Blind Unfolded")
    
    if 'data0.bin' not in files:
        f = open("C:\\ProgramData\\Blind Unfolded\\data0.bin",'w')
        key = Fernet.generate_key()
        key = key.decode('utf-8')
        key = key[::-1].swapcase()
        key = key[1:] + key[0]
        f.writelines([key,'\n '])
        f.close()
    
    if 'log.txt' not in files:
        f= open("C:\\ProgramData\\Blind Unfolded\\log.txt",'w')
        f.write("NO ENTRIES FOUND! Please try to print something first!\n")
        f.close()

def speech2text_active():
    ''' function to convert audio to text by realtime recording '''

    r= sr.Recognizer()
    mic= sr.Microphone(device_index=2)
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=1)
            time.sleep(1)
            update_text("Listening...")
            beepy.beep(sound=1)
            audio = r.listen(source, timeout=10)
    except:
        speak("Sorry, but I am unable to understand what you said!")
        return None
    else:
        try:
            txt=r.recognize_google(audio)
        except Exception as e:
            if e == "":
                speak("Sorry, but I am unable to understand what you said!")
                return None
            else:
                speak("It seems like there is a problem with your internet connection!")
                return None
        else:
            return txt

def speech2text_passive(file="C:\\braille\\tmp.wav"):
    ''' function to convert pre-recorded audio to text '''
    
    r=sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio=r.record(source)
    
    try:
        txt=r.recognize_google(audio)
        return txt
    except:
        return None

def get_key():
    '''Function to retrieve and decrypt the decryption key'''
    
    f = open("C:\\ProgramData\\Blind Unfolded\\data0.bin",'r')
    x = f.read()
    x = x.split("\n")
    key = x[0][::-1].swapcase()
    key = key[1:] + key[0]
    f.close()
    key = bytes(key, 'utf-8')
    return key,x[1]
    
def encrypt():
    '''Function to encrypt files with security key'''
    
    key,x = get_key()
    if x == ' ':
        with open('C:\\ProgramData\\Blind Unfolded\\log.txt', 'rb') as f:
            data = f.read()
        f.close()
        
        with open('C:\\ProgramData\\Blind Unfolded\\log.txt', 'wb') as f:
            f.write(Fernet(key).encrypt(data))
        f.close()
        
        with open("C:\\ProgramData\\Blind Unfolded\\data0.bin",'rb') as f:
            x = f.read()
            x = x[0:len(x)-1:]
        f.close()
        
        with open("C:\\ProgramData\\Blind Unfolded\\data0.bin",'wb') as f:
            f.write(x)
        f.close()
            
    
def decrypt():
    '''Function to decrypt files with security key'''
    
    key,x = get_key()
    if x == '':
        with open('C:\\ProgramData\\Blind Unfolded\\log.txt', 'rb') as f:
            data = f.read()
        f.close()
        
        with open('C:\\ProgramData\\Blind Unfolded\\log.txt', 'wb') as f:
            f.write(Fernet(key).decrypt(data))
        f.close()
        
        with open("C:\\ProgramData\\Blind Unfolded\\data0.bin",'rb') as f:
            x = f.read()
            x = x + bytes(' ', 'utf-8')
        f.close()
        
        with open("C:\\ProgramData\\Blind Unfolded\\data0.bin",'wb') as f:
            f.write(x)
        f.close()

def txt2braille(txt):
    '''Function to convert text into braille by unicodes'''

    b=""
    text_dict= {"a":u"\u2801",
                "b":u"\u2803",
                "c":u"\u2809",
                "d":u"\u2819",
                "e":u"\u2811",
                "f":u"\u280b",
                "g":u"\u281b",
                "h":u"\u2813",
                "i":u"\u280a",
                "j":u"\u281a",
                "k":u"\u2805",
                "l":u"\u2807",
                "m":u"\u280d",
                "n":u"\u281d",
                "o":u"\u2815",
                "p":u"\u280f",
                "q":u"\u281f",
                "r":u"\u2817",
                "s":u"\u280e",
                "t":u"\u281e",
                "u":u"\u2825",
                "v":u"\u2827",
                "w":u"\u283a",
                "x":u"\u282d",
                "y":u"\u283d",
                "z":u"\u2835",
                "1":u"\u2802",
                "2":u"\u2806",
                "3":u"\u2812",
                "4":u"\u2832",
                "5":u"\u2822",
                "6":u"\u2816",
                "7":u"\u2836",
                "8":u"\u2826",
                "9":u"\u2814",
                "0":u"\u2834",
                " ":u"\u2800",
                "\n":"\n"}

    if txt==None:
        return None

    txt=txt.lower()

    for i in txt:
        try:
            b+=text_dict[i]
        except:
            b+=i
    return b

def convert(p):
    '''Copies and converts the given file to ".wav" format if needed'''
    
    d="C:\\ProgramData\\Blind Unfolded\\"
    files=os.listdir(d)
        
    if "tmp.wav" in files:
        os.remove("C:\\ProgramData\\Blind Unfolded\\tmp.wav")

    if p[-3::1]=="mp3":
        sound = AudioSegment.from_mp3(p)
        sound.export("C:\\ProgramData\\Blind Unfolded\\tmp.wav", format="wav")
    else:
        cmd="copy \""+p+"\" \""+d+"\""
        cmd=cmd.replace("/","\\")
        os.system('cmd /c "{}"'.format(cmd))
        p=p.replace("/","\\")
        p=p.split("\\")
        p=p[-1]
        p=d+p
        d=d+"tmp.wav"
        os.rename(p,d)
    
    return "C:\\ProgramData\\Blind Unfolded\\tmp.wav"

def log(out):
    '''Function to log all entries of the user (upto 100 lines)'''
    
    decrypt()
    x= open("C:\\ProgramData\\Blind Unfolded\\log.txt",'r')
    data=x.read()
    x.close()
    if data == "NO ENTRIES FOUND! Please try to print something first!\n":
        data = ""

    dt=str(datetime.now())
    dt=dt[:19:]
    data= dt + '\n' + out + '\n\n' + data
    x=''
    data= data.split('\n')
    data= data[:100:]
    for i in range(len(data)-1):
        x=x+data[i]+'\n'
    x+=data[i+1]
    data= x
    x= open("C:\\ProgramData\\Blind Unfolded\\log.txt",'w')
    x.write(data)
    x.close()
    encrypt()

def update_text(s=""):
    textBox.config(state= "normal")
    textBox.insert('end', s+"\n")
    textBox.config(state= "disabled")

def take_input():
    textBox.config(state= "normal")
    textBox.delete('1.0', END)
    textBox.focus_set()
    speak("Please type in the text that you want to convert into Braille. Say continue to let me know when you are done with your typing",False)
    while(True):
        cmd = listen(False)
        if "done" in cmd or "complete" in cmd or "continue" in cmd:
            i = textBox.get("1.0",END)
            break
        time.sleep(2)
    textBox.insert('end', "\n")
    return i

def speak(txt,alter_text = True):
    global beep
    beep = True
    engine.say(txt)
    if alter_text:
        update_text("Speaking...")
    engine.runAndWait()
    

def listen(alter_text = True):
    global beep
    r= sr.Recognizer()
    mic= sr.Microphone(device_index=2)
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=1)
            if beep:
                if alter_text:
                    update_text("Listening...")
                beepy.beep(sound=1)
                beep = False
            audio = r.listen(source, timeout=5)
            print(".")
    except:
        return ""
    else:
        try:
            txt=r.recognize_google(audio)
            print(txt)
        except:
            return ""
        else:
            return txt

def blind_main():
    speak("Hello and welcome to Blind Unfolded! Would you like me to tell you the available options?")
    cmd = listen()
    if "yes" in cmd:
        speak("Option 1. Audio based services. Option 2. Text based services. Option 3. Show log. Option 4. Delete old records from log. Option 5. Exit")
    else:
        speak("I will be right by your side. Feel free to ask for my assistance")
    while (True):        
        startup()
        encrypt()
        cmd = listen()
        if "exit" in cmd or "quit" in cmd or "five" in cmd:
            speak("Goodbye! I will be back in service as soon as you need me!")
            root.destroy()
            sys.exit()
        
        elif "one" in cmd or "audio" in cmd or "voice" in cmd or "speech" in cmd:
            speak("These are the options for the audio services. Option 1. Convert voice to Braille as you speak. Option 2. Convert an audio file to Braille. Option 3. Return to main menu.")
            while (True):
                cmd = listen()
                if "one" in cmd or "speech" in cmd or "speak" in cmd or "voice" in cmd:
                    txt=speech2text_active()
                    out=txt2braille(txt)
                    if out!=None:
                        update_text(out)
                        log(txt)
                        speak("Voice converted into Braille and logged successfully!")
                    break
                elif "two" in cmd or "audio" in cmd or "file" in cmd or "open" in cmd:
                    tk.Tk().withdraw()
                    p=fd.askopenfilename(title = "Select the audio file",filetypes = (("mp3 files","*.mp3"),("wav files","*.wav")),parent=root)
                    if (p!=''):
                        file=convert(p)
                        txt=speech2text_passive(file)
                        out=txt2braille(txt)
                        if out==None:
                            speak("Sorry but I am unable to extract speech from the audio file!")
                        else:
                            speak("Audio converted into Braille, and logged successfully!")
                            update_text(out)
                            log(txt)
                    else:
                        speak("No file was selected!")
                    break
                elif "three" in cmd or "back" in cmd or "return" in cmd or "main" in cmd:
                    speak("Waiting for furthur instructions in the main menu.")
                    break
        
        elif "two" in cmd or "text" in cmd or "type" in cmd:
            speak("These are the options for the text services. Option 1. Convert text to Braille by typing. Option 2. Convert an existing text file to Braille. Option 3. Return to main menu.")
            while (True):
                cmd = listen()
                if "one" in cmd or "type" in cmd:
                    #speak("Please type in the text that you want to convert into Braille. Say 'done' to let me know when you are done with your typing")
                    txt = take_input()
                    if len(txt)<1:
                        speak("It seems that you didn't type anything.")
                    else:
                        out=txt2braille(txt)
                        update_text(out)
                        log(txt)
                        speak("Text converted into Braille, and logged successfully!")
                elif "two" in cmd or "file" in cmd or "open" in cmd:
                    tk.Tk().withdraw()
                    p=fd.askopenfilename(title = "Select the text file (only txt files supported)",filetypes = (("txt Files","*.txt"),),parent=root)
                    if (p!=''):
                        x=open(p,'r')
                        txt= x.read()
                        x.close()
                        if len(txt)<1:
                            speak("The selected file is empty.")
                        else:
                            out=txt2braille(txt)
                            update_text(out)
                            log(txt)
                            speak("Text file converted into Braille, and logged successfully!")
                    else:
                        speak("No File was Selected!")
                    break
                elif "three" in cmd or "back" in cmd or "return" in cmd or "main" in cmd:
                    speak("Waiting for furthur instructions in the main menu.")
                    break
        
        elif "three" in cmd or "show" in cmd or "log" in cmd:
            decrypt()
            x=open("C:\\ProgramData\\Blind Unfolded\\log.txt",'r')
            data=x.read()
            x.close()
            encrypt()
            update_text(data)
            speak("Log file loaded successfully. Waiting for furthur instructions")
        
        elif "four" in cmd or "delete" in cmd or "remove" in cmd:
            speak("Are you sure you want to delete all the previous records?")
            while (True):
                cmd = listen()
                if "yes" in cmd:
                    os.remove("C:\\ProgramData\\Blind Unfolded\\log.txt")
                    os.remove("C:\\ProgramData\\Blind Unfolded\\data0.bin")
                    speak("All old logs and records have been deleted successfully.")
                    break
                elif "no" in cmd or "cancel" in cmd or "back" in cmd or "return" in cmd:
                    speak("Waiting for furthur instructions in the main menu.")
                    break
        
        elif "option" in cmd or "options" in cmd or "services" in cmd or "help" in cmd:
            speak("Option 1. Audio based services. Option 2. Text based services. Option 3. Show log. Option 4. Delete old records from log. Option 5. Exit")
        time.sleep(2)

#__main__

beep = False
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[1].id)

root = Tk()
root.title("Blind UnFolded")
root.geometry("1250x625")
root.minsize(1250, 625)
root.maxsize(1250, 625)
root.wm_attributes('-topmost', 1)

icon = PhotoImage(file = 'ok.png')
root.iconphoto(False, icon)

logo = PhotoImage(file='logo.png')
logolabel = tk.Label(image=logo)
logolabel.grid(column=0,row=0)

i = tk.Label(root, text="Vision without sight is now a reality", font=("Lucida Handwriting",28))
i.grid(columnspan=10, column=0, row=1)

frame = Frame(root)
frame.grid(columnspan=10, column=1, row=0)
textBox = tk.Text(frame, font= ('Consolas 20'), height= 15, width= 45, wrap=WORD)
textBox.insert('end', "")
textBox.config(state= "normal")
textBox.focus_set()
textBox.pack()

backend = threading.Thread(target=blind_main)
backend.daemon = True
backend.start()
root.mainloop()