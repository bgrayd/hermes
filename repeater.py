from datetime import *
import time
def startRepeater():
    file1=open("todolist.txt","r")
    for each in file1:
        index=each.find(')')
        date=each[1:index]
        event=each[index+1:]
        date=date.split(',')
        time=datetime(int(date[0]),int(date[1]),int(date[2]),int(date[3]),int(date[4]),0,0)
        todo[time]=event
    file1.close()        

def stoprepeater():
    file1=open("todo.txt","w")
    for each in todo:
        file1.write(each+todo[each])

def repeaterMain(repeaterQ, printQ,allV):
    todo={}
    startRepeater()
    on=allV['run']
    count=0
    while on:
        count+=1
        time.sleep(10)
        if count%6==0:
            for each in todo:
                now=datetime.now()
                if now>=each:
                    printQ.put("command~"+str(todo[each]))
        if repeaterQ.empty()==False:
            element=repeaterQ.get()
            element=element.split("~")
            if element[0]=="stop":
                on=False
            elif element[0]=="new todo":
                dictionary=element[1].split(":")
