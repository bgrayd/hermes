def save(fileName, dictionary):
    if fileName.find(".wgd")==-1:
        fileName+=".wgd"
    file=open(fileName,"w")
    temp5=recursiveBuilder(dictionary,"")
    file.write(temp5[1:])
    file.close()

def recursiveBuilder(passed,bar):
    if isinstance(passed, dict):
        foo=""
        for each in passed:
            temp=(recursiveBuilder(passed[each],bar+'\t'))
            tags=tagFormat(each)
            foo+='\n'+str(bar+str(tags[0])+'\n'+bar+'\t'+str(temp)+'\n'+bar+str(tags[1]))
        return foo
    else:
        return passed

def tagFormat(key):
    return(str("<"+key+">"),str("</"+key+">"))

def read(fileName):
    if fileName.find(".wgd")==-1:
        fileName+=".wgd"
    file=open(fileName,"r")
    foo={}
    bol=""
    for each in file:
        temp=each.strip('\n')
        bol+=temp.strip('\t')
    foo=recursiveReader(bol)
    file.close()
    return foo

def recursiveReader(passed):
    if passed.find("<")==-1:
        return passed
    working={}
    while True:
        place1=passed.find("<")
        place2=passed.find(">")
        if place2<place1:
            passed=passed[place1:]
            place1=0
            place2=passed.find(">")
        foo=passed[place1+1:place2]
        boo=closeTagMaker(passed[place1:place2+1])
        temp=passed.split(boo)
        working[foo]=recursiveReader(temp[0][place2+1:])
        try:
            passed=temp[1]
        except:
            passed=""
            print("none")
        if passed.find("<")==-1:
            return working
        

def closeTagMaker(opener):
    opener=opener[1:]
    return str("</"+opener)
