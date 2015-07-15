import urllib.request

def localWeather(printQ):
    condition=''
    page = urllib.request.urlopen("http://www.wunderground.com/")
    text = page.read().decode("utf8")
    position=text.find('<td class="nobr b vaT"><div class="textData">Current Location:</div></td>')
    text=text[position:]
    printQ.put("In "+weatherPlace(text)+" it is currently "+weatherTemperature(text)+" and "+weatherCondition(text)+'.')

def otherWeather(state, city, printQ):
    condition=''
    page=urllib.request.urlopen("http://www.wunderground.com/US/"+state+"/"+city+".html")
    text=page.read().decode("utf8")
    position=text.find('<a class="br10" id="stationselector_button" href="javascript:void(0);"><span>Station Select</span></a>')
    text=text[position:]
    printQ.put("In "+city+","+state+" it is currently "+weatherTemperature(text)+" and "+weatherCondition(text)+'.')

def weather(user, printQ):
    place=user.find(" in ") 
    if place==-1:
        localWeather(printQ)
    else:
        statefinder=user[place+1:]
        while True:
            place=statefinder.find(' ')
            if statefinder[place+3]==' ':
                state=statefinder[place+1:place+3]
                break
            elif place==-1:
                printQ.put("invalid entry")
                return 0
            else:
                statefinder=statefinder[place+1:]
        place=user.find(" in ")
        city=''
        for each in user[place+7:place+40]:
            if each!= ' ':
                city+=each
            else:
                break
        otherWeather(state, city, printQ)
        
def weatherPlace(text):
    position=text.find('<div class="textData">')
    text=text[position+3:]
    position=text.find('<div class="textData">')
    text=text[position+24:]
    position=text.find('>')
    text=text[position+1:]
    return text[:text.find('</a>')]

def weatherTemperature(text):
    position=text.find('<span class="nobr"><span class="b">')
    text=text[position+35:]
    position=text.find('</span>')
    temp=text[:position]
    text=text[position+2:]
    position=text.find('</span>')
    degree=text[position-1:position]
    if degree=='C':
        degree=' degrees Celsius'
    elif degree=='F':
        degree=' degrees Fahrenheit'
    return (str(temp) + str(degree))

def weatherCondition(text):
    position=text.find('<img src="')
    text=text[position:]
    position=text.find(' alt="')
    text=text[position+6:]
    position=text.find('"')
    return text[:position]




class command():
    def __init__(self, text, allV):
        self.text=text
        self.allV=allV
        self.repeat=False
        self.match=False
        self.question=False
        if text.find("weather")!=-1 and text.find('help')==-1:
            self.match=True
    def run(self):
        weather(self.text, self.allV['printQ'])


def helpBasic():
    return 'weather'

def helpAdv(message):
    if message.find('weather')!=-1:
        return 'To get the local weather, just use the world weather'
    return None
