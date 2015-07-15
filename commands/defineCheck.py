import urllib.request

def defineTranslate(message):
    place=message.find("define")
    message=message[place+7:]
    here=message.find(' ')
    if here==-1:
        return message
    else:
        return message[:here]

def basicCheck(word,printerQ):
    page = urllib.request.urlopen("http://www.dictionary.reference.com/browse/"+word)
    text = page.read().decode("utf8")
    if text.find('<div id="sph">No results found for <i>')==-1:
        printerQ.put("What you were searching for was unable to be found, please try again.")
    start=text.find('<!-- google_ad_section_start -->')
    end=text.find('<!-- google_ad_section_end -->')
    text=text[start+32:end]
    printerQ.put(recursiveAllDefinition(text[text.find('<div class="body"><div class="pbk"><span class="pg">')+52:]))
    
def recursiveAllDefinition(text):
    this=text.find('<div class="luna-Ent"><span class="dnindex">')
    if this ==-1:
        return ""
    else:
        text=text[this:]
        this=text.find('<div class="luna-Ent"><span class="dnindex">')
        here=text.find('</span>')
        number=text[this+44:here-1]
        definition=text[text.find('<div class="dndata">')+20:text.find('</div>')]
        definition=removeTags(definition)
        text=text[text.find('</div>')+2:]
        if number!='' and definition!='':
            return (" Definition "+number+', '+definition+recursiveAllDefinition(text))
        else:
            return (recursiveAllDefinition(text))

def removeTags(text):
    this=text.find('<')
    if this == -1:
        return text
    toBeReturned=""
    while True:
        this=text.find('<')
        if this == -1:
            toBeReturned+=text
            return toBeReturned
        else:
            toBeReturned+=text[:this]
            text=text[text.find('>')+1:]
            
class command():
    def __init__(self, text, allV):
        self.text=text
        self.allV=allV
        self.match=False
        self.repeat=False
        self.question=False
        if text.find("define")!=-1:
            self.match=True
    def run(self):
        basicCheck(defineTranslate(self.text),self.allV['printQ'])


def helpBasic():
    return 'dictionary'

def helpAdv(message):
    if message.find('dictionary')!=-1:
        return 'To search dictionary.com for a word, say "define" and then the word you want to search for'
    return None
