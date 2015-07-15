from urllib.request import *
import webbrowser
def titleMaker(title):
    temp=''
    for each in title:
        if each==' ':
            temp+='+'
        else:
            temp+=each
    return temp


class result():
    def __init__(self, text):
        self.name=text[text.find("<media:title type='plain'>")+26:text.find("</media:title>")]
        self.desc=text[text.find("<media:description type='plain'>")+32:text.find("</media:description>")]
        temp=text.find("<media:player url='")+19
        self.link=text[temp:text[temp:].find("'/><media:")+temp]

    def play(self):
        webbrowser.open(self.link)

class command():
    def __init__(self, text, allV):
        #text is the string from the user
        #allV is a dictionary and holds all of the whole program variables
        self.allV=allV
        self.text=text
        
        #self.repeat is wether or not this command class should be added to the
        #   active commands list and can have more strings passed to it
        self.repeat=False
        self.question=False

        #self.match is if this command type is started from some of the text
        #   in the string
        self.match=False
        if text.find("search videos")!=-1:
            self.match=True

    def run(self):
        #this is where it actually runs whatever the command is for
        self.videos=[]
        self.start = self.text.find("search videos for ")+18
        self.allV['printQ'].put("Do you want to do a search of youtube for "+self.text[self.start:])
        self.repeat=True
        self.question=True
        self.position=0
        self.current=0
            
    def add(self, message):
        #this is for if the command can have stuff added to it
        if self.videos==[]:
            if message.find(" no ")!=-1 or message=='no':
                self.repeat=False
                self.question=False
            else:
                self.allV['printQ'].put("starting a search of youtube for "+self.text[self.start:])
                #webbrowser.open('http://gdata.youtube.com/feeds/api/videos?vq='+titleMaker(self.text[start:])+'&racy=include&orderby=relevance')
                page=urlopen('http://gdata.youtube.com/feeds/api/videos?vq='+titleMaker(self.text[self.start:])+'&racy=include&orderby=relevance')
                text=page.read().decode('utf8')
                while text.find("<entry>")!=-1:
                    temp=result(text[text.find("<entry>"):text.find("</entry>")])
                    self.videos.append(temp)
                    text=text[text.find("</entry>")+2:]
                if len(self.videos)==1:
                    self.allV['printQ'].put("only one video was found, it is "+str(self.videos[0].name))
                    self.choices=[self.videos[0]]
                elif len(self.videos)==2:
                    self.allV['printQ'].put("two videos were found, they are " +str(self.videos[0].name)+' and '+str(self.videos[1].name))
                    self.choices=[self.videos[0],self.videos[1]]
                else:
                    self.choices=[self.videos[0],self.videos[1],self.videos[2]]
                    self.allV['printQ'].put(str(len(self.videos))+" were found, the first few are "+str(self.videos[0].name)+', '+str(self.videos[1].name)+', and '+str(self.videos[2].name))

        elif message.find("next")!=-1:
            if self.position==len(self.videos)-1:
                self.allV['printQ'].put("you have reached the end of the list")
            elif self.position+6>=len(self.videos)-1:
                self.position=len(self.videos)-3
            else:
                self.position+=3
            self.allV['printQ'].put("the next three options are "+str(self.videos[self.position].name)+' '+str(self.videos[self.position+1].name)+' '+str(self.videos[self.position+2].name))

        else:
            if message.find(" first ")!=-1:
                self.current=self.position
            elif message.find("second ")!=-1:
                self.current=self.position+1
            elif message.find("third ")!=-1:
                self.current=self.position+2
            if message.find(" name ")!=-1:
                self.allV['printQ'].put("the name you requested is "+str(self.videos[self.current].name))
            elif message.find("description")!=-1:
                self.allV['printQ'].put("I think you just requested the description for "+str(self.videos[self.current].name)+" which is " +str(self.videos[self.current].desc))
            elif message.find("play")!=-1 or message.find("open it")!=-1:
                self.videos[self.current].play()
                self.repeat=False
                self.question=False


def helpBasic():
    return "video search"

def helpAdv(message):
    if message.find('video search')!=-1:
        return 'to search for videos on youtube, say "search videos" followed by what you want to search for.  You will be given a list of titles, in sets of three if possible.  Refer to them as "first", "second", and "third" for a repeat of the name, a description, or for it to be opened in your webbrowser'
    return None
