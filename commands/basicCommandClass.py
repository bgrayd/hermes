class command():
    def __init__(self, text, allV):
        #text is the string from the user
        #allV is a dictionary and holds all of the whole program variables
        self.allV=allV
        self.text=text
        
        #self.repeat is wether or not this command class should be added to the
        #   active commands list and can have more strings passed to it
        self.repeat=False

        #self.match is if this command type is started from some of the text
        #   in the string
        self.match=False

        self.question=False

    def run(self):
        #this is where it actually runs whatever the command is for
        return

    def add(self, message):
        #this is for if the command can have stuff added to it
        return

def helpBasic():
    #this is for the basic help question, please return a string or None
    return None

def helpAdv(message):
    #this is for help about this specific command, have a breif if to check if
    #applicable, it if is, return a single string, otherwise return None
    return None
