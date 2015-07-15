from repeater import *
from command import *
from queue import *
from tkinter import *
import sys, threading, time, customfiletype, imaplib
import subprocess

def printer(printQ,allV):
    args=['notts']#[allV['settings']['system']['tts']]
    if args==['notts']:
        while allV['run']:
            element=printQ.get()
            element=element.split("~")
            if element[0]=='stop':
                print('stopping')
            elif element[0]=='command~':
                print(element[1])
            else:
                print(element[0])
    else:
        p=subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        allV['printer']=p
        while allV['run']:
            element=printQ.get()
            element=element.split("~")
            if element[0]=="stop":
                print("stopping")
                p.stdin.write(str('stopping').encode('utf-8'))
                time.sleep(1)
            elif element[0]=="command~":
                print(element[1])
                element[1]+="\n"
                p.stdin.write(element[1].encode('utf-8'))
            else:
                print(element[0])
                element[0]+="\n"
                p.stdin.write(element[0].encode('utf-8'))
        p.terminate()


def listen(allV):
    args=[allV['settings']['system']['recoengine']]
    if args==['none']:
         while allV['run']:
             allV['commandQ'].put("command~"+input())
    else:
        p=subprocess.Popen(args, stdout=subprocess.PIPE)
        allV['listener']=p
        listnQ=allV['listenQ']
        time.sleep(0)
        while allV['run']:
            ln=str(p.stdout.readline())
            allV['commandQ'].put("command~"+ln[2:len(ln)-5])
        p.terminate()
    
def createSettings():
    def approved():
        temp={}
        temp['program_name']=str(programName.get()).lower()
        temp['username']=str(userName.get()).lower()
        if reco.get()=='one that is just used for this':
            temp['recoengine']='cppinprocReco'
        elif reco.get()=='one that is used by all windows':
            temp['recoengine']='cppsharedreco'
        else:
            temp['recoengine']='none'

        if tts.get()=='Windows TTS':
            temp['tts']='cpptts'
        else:
            temp['tts']='notts'
        settings['system']=temp
        
    settings={'system':{},'gmail':{}}
    app=Tk()
    app.title('Customize the program for you!')
    reco=StringVar()
    tts=StringVar()
    reco.set(None)
    tts.set(None)
    Label(app,text='Name to refer to this program with').pack()
    programName=Entry(app)
    programName.pack()
    programName.insert(0,'Hermes')
    Label(app,text='').pack()
    Label(app,text='What is your name?').pack()
    userName=Entry(app)
    userName.pack()
    Label(app,text='').pack()
    Label(app,text='Which speech recognizer do you want to use?').pack()
    recoOptions=['one that is just used for this','one that is used by all windows','no speech recognition']
    OptionMenu(app,reco,*recoOptions).pack()
    Label(app,text='').pack()
    Label(app,text='Which Text to Speech engine do you want to use?').pack()
    ttsOptions=['Windows TTS','no TTS']
    OptionMenu(app,tts,*ttsOptions).pack()
    Label(app,text='').pack()
    Label(app,text='click ok then close this window when completed.').pack()
    Button(app,text='Okay',command=approved).pack()
    app.mainloop()
    return settings



commandQ=Queue(5)
printQ=Queue(10)
repeaterQ=Queue(5)
mainQ=Queue(5)
listenQ=Queue(5)
allV={}
allV['commandQ']=commandQ
allV['printQ']=printQ
allV['repeaterQ']=repeaterQ
allV['mainQ']=mainQ
allV['listenQ']=listenQ
try:
    allV['settings']=customfiletype.read("settings")
except Exception as ex:
    allV['settings']=createSettings()
    printQ.put('To hear a list of commands, say '+allV['settings']['system']['program_name']+' help')

allV['run']=True
allQ=[]
allQ.append(commandQ)
allQ.append(printQ)
allQ.append(repeaterQ)
allQ.append(mainQ)
allV['allQ']=allQ
#allV['settings']={'system':{'recoengine':'cppinprocReco','program_name':'hermes'}}

Printer=threading.Thread(target=printer, args=(printQ,allV))
Command=threading.Thread(target=runMode, args=(allV,))
repeater=threading.Thread(target=repeaterMain, args=(repeaterQ, printQ, allV))
listen=threading.Thread(target=listen, args=(allV,))
Printer.start()
Command.start()
repeater.start()
listen.start()

while allV['run']:
    time.sleep(10)
    
customfiletype.save('settings',allV['settings'])
