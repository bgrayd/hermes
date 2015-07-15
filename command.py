from datetime import *
import os
import webbrowser
import sys
import time

def runMode(allV):
    activeCommands=[]
    commandQ=allV['commandQ']
    commands=loadCommand()
    name=allV['settings']['system']['program_name']
    responseTime=5
    if allV['settings']['system']['recoengine']=='none':
        responseTime=0
    while allV['run']:
        element=commandQ.get()
        element=element.split("~")
        if element[0]=="stop":
            on=False
            stop(allV['allQ'])
            allV['run']=False
        element[1]=element[1].lower()
        if element[1].find(name)!=-1:
            build=True
            message=element[1][element[1].find(name)+6:]
            while build:
                try:
                    temp=commandQ.get(True,responseTime)
                    message+=temp.split("~")[1]
                except Exception as ex:
                    build=False

            temp1=[]
            for each in activeCommands:
                if each.repeat:
                    temp1.append(each)
            activeCommands=temp1
            if activeCommands!=[]:
                worked=False
                for each in activeCommands:
                     if each.add(message):
                         worked=True
                if worked==False:
                    allV['printQ'].put("no active commands worked.  would you like to check other commands?")
                    time.sleep(10)
                    answer=""
                    build=True
                    while build:
                        try:
                            temp=commandQ.get(True,responseTime)
                            answer+=temp.split("~")[1]
                        except Exception as ex:
                            build=False
                    if answer.find("yes")!=-1:
                        command=commandType(message, allV, commands)
                        if command.match:
                            command.run()
                        else:
                            allV['printQ'].put("unable to match phrase with a command")
            else:
                command=commandType(message, allV, commands)
                if command.match:
                    command.run()
                else:
                    allV['printQ'].put("unable to match phrase with a command"+" "+message)
            while command.question:
                time.sleep(15)
                answer=""
                build=True
                while build:
                    try:
                        temp=commandQ.get(True,responseTime)
                        answer+=temp.split("~")[1]
                    except Exception as ex:
                        build=False
                if answer!="" or answer.find(" escape ")!=-1:
                    try:
                        command.add(answer)
                    except Exception as ex:
                        break
                    print(answer)
            if command.repeat:
                activeCommands.append(command)

def commandType(message, allV, commands):
    printQ=allV['printQ']
    command=baseCommand()
    command.match=True
    if message.find("remind")!=-1:
        this=(dateTranslate(message)+":"+message)
        todoAdd(this, allV['allQ'][2])
    elif message.find("shutdown")!=-1 or message.find("shut down")!=-1:
        stop(allV['allQ'])
    elif message.find("play pandora")!=-1:
        webbrowser.open("www.pandora.com")
    else:
        command.match=False
        for each in commands:
            foo=each.command(message,allV)
            if foo.match==True:
                command=foo
                break
    if command.match==False and message.find("help")!=-1:
        command.match=True
        for each in commands:
            foo=each.helpAdv(message)
            if foo!=None:
                printQ.put(foo)
                return command
        printQ.put('There are three built in commands for this version.')
        printQ.put('For a command to be recognized say '+str(allV['settings']['system']['program_name'])+' before the command')
        printQ.put('To safely close this program, say "shutdown"')
        printQ.put('Pandora will open if you say "play pandora"')
        printQ.put('If you want be to remind you of something, use "remind" in a sentance that includes when you want to be reminded, still in development')
        printQ.put('For more information on the following commands, say help and the command name.')
        for each in commands:
            foo=each.helpBasic()
            if foo!=None:
                printQ.put(foo)
    return command

class baseCommand():
    def __init__(self):
        self.repeat=False
        self.match=False
        self.question=False
    def run(self):
        pass
        
def loadCommand():
    commands=os.listdir("commands")
    command=[]
    for each in commands:
        if each.find('.py')!=-1:
            foo=each[:len(each)-3]
            command.append(__import__(str(foo)))
    return command
        










def stop(allQ):
    for each in allQ:
        each.put("stop~")

def todoAdd(command,todoQ):
    todoQ.put("new todo~"+command)
            
def dateTranslate(message):
    date=datetime.now()
    if message.find("tomorrow")!=-1:
        date=date.replace(day=date.day+1,hour=12,minute=0)
    elif message.find("today")!=-1:
        date=date
    elif message.find("days")!=1:
        index=message.find("days")
        user=message[:index]
        if user.find("two")!=-1:
            date=date.replace(day=today.day+2,hour=12,minute=0)
        elif user.find("three")!=-1:
            date=date.replace(day=today.day+3,hour=12,minute=0)
        elif user.find("four")!=-1:
            date=date.replace(day=today.day+4,hour=12,minute=0)
        elif user.find("five")!=-1:
            date=date.replace(day=today.day+5,hour=12,minute=0)
        elif user.find("six")!=-1:
            date=date.replace(day=today.day+6,hour=12,minute=0)
        elif user.find("seven")!=-1:
            date=date.replace(day=today.day+7,hour=12,minute=0)
    else:
        date=datetime.strftime(message[:message.find("20")+4],"%B %d, %Y")
    if message.find(" at ")!=-1:
        atLocation=message.find(" at ")
        remindLocation=message.find(" remind ")
        if atLocation<remindLocation:
            user=message[atLocation+4:remindLocation-1]
        else:
            user=message[message.find("at")+3:]
        if user.find(":")!=-1:
            user=user.strip(" ")
            user=user.split(":")
            hour=int(user[0])
            minute=int(user[1])
        else:
            tempTime=time.strftime(user,"%H %M")
        date=date.replace(hour=hour, minute=minute)
    return str("("+str(date.year)+","+str(date.month)+","+str(date.day)+","+str(date.hour)+","+str(date.minute)+")"+message)



sys.path.append('commands\\')
