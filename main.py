import time
import load
import os
if os.name == 'nt': # Only if we are running on Windows
    from ctypes import windll
    k = windll.kernel32
    k.SetConsoleMode(k.GetStdHandle(-11), 7)

    
def tOut(text):
    print(text)
    time.sleep((len(text)/50)*3)


def readStory(storyFileLocation):
    global story
    f = open(storyFileLocation,'r', encoding="utf8")
    story = f.readlines()
    f.close()

def loadChecks():
    storyIndex = 0
    global checkArray
    checkArray = []
    while storyIndex < len(story):
        block = story[storyIndex]
        c = 0
        while c < len(block):
            if block[c] == "/":
                break
            c = c + 1
        command = block[0:c]
        content = (block[(c+1):len(block)]).rstrip('\r\n')
        if command == 'check':
            checkArray.append([content,storyIndex])
        else:
            pass
        storyIndex = storyIndex + 1

def pushOG(flag):
    global storyIndex
    c = 0
    while c < len(story):
        if (story[c]).rstrip('\r\n') == ("check/" + flag):
            break
        c = c + 1
    storyIndex = c

def push(flag):
    global storyIndex
    global checkArray
    c = 0
    while c < len(checkArray):
        item = checkArray[c]
        if item[0] == flag:
            storyIndex = item[1]
            break
        c = c + 1
        
def save(loc,val):
    f = open("values.txt",'r', encoding="utf8")
    values = f.readlines()
    f.close()
    
    found = False
    c = 0
    while c < len(values):
        entry = values[c]
        
        c2 = 0
        while c2 < len(entry):
            if entry[c2] == ",":
                break
            c2 = c2 + 1
        newEntry = [entry[0:c2],(entry[(c2+1):len(entry)]).rstrip('\r\n')]
        
        if newEntry[0] == loc:
            newEntry[1] = val
            values[c] = newEntry[0] + "," + newEntry[1] + "\n"
            found = True
        else:
            pass
        c = c + 1
    
    if found == False:
        values.append(loc + "," + val + "\n")
    
    stringformat = ''
    for x in values:
        stringformat = stringformat + x
    f = open("values.txt","w", encoding="utf8")
    f.write(stringformat)
    f.close()
    
def varRead(loc):
    f = open("values.txt","r", encoding="utf8")
    values = f.readlines()
    f.close()
    
    for entry in values:
        c2 = 0
        while c2 < len(entry):
            if entry[c2] == ",":
                break
            c2 = c2 + 1
        
        if entry[0:c2] == loc:
            return ((entry[(c2+1):len(entry)]).rstrip('\r\n'))
    return None

story = []
checkArray = []
storyIndex = 0;

def play(storyFileLocation):
    storyFileLocation = "data/" + storyFileLocation + ".txt"
    
    global story
    global checkArray
    global storyIndex
        
    readStory(storyFileLocation)
    loadChecks()
    push('start')

    while storyIndex < len(story):
        block = story[storyIndex]
        c = 0
        while c < len(block):
            if block[c] == "/":
                break
            c = c + 1
        command = block[0:c]
        content = (block[(c+1):len(block)]).rstrip('\r\n')
        
        f = open("values.txt","r", encoding="utf8")
        values = f.readlines()
        f.close()
        
        for entry in values:
            c2 = 0
            while c2 < len(entry):
                if entry[c2] == ",":
                    break
                c2 = c2 + 1
            newEntry = [entry[0:c2],(entry[(c2+1):len(entry)]).rstrip('\r\n')]
            
            if ("{" + newEntry[0] + "}") in content:
                content = content.replace(("{" + newEntry[0] + "}"),newEntry[1])

        if command == 'say':
            tOut(content)
        elif command == 'pause':
            time.sleep(float(content))
        elif command == 'dec':
            c = 0
            while c < len(content):
                if content[c] == '#':
                    break
                c = c + 1
            ques = content[0:c]
            options = content[c:len(content)]

            optionsArr = []
            options = options.split("#")
            for x in options:
                optionsArr.append(x.split("="))

            gotAnswer = False
            while gotAnswer == False:
                inny = str(input(ques + " "))
                for x in optionsArr:
                    if inny == x[0]:
                        gotAnswer = True
                        push(x[1])
                        
        elif command == 'check':
            pass
        elif command == 'push':
            push(content)
        elif command == 'expush':
            play(content)
        elif command == 'end':
            break
        elif command == 'mancom':
            eval(content)
        elif command == 'gap':
            tOut('')
        elif command == 'save':
            loc = (content.split('='))[0]
            val = (content.split('='))[1]
            
            save(loc,val)
        elif command == "":
            #comment definition or a blank space
            pass
        elif command == 'stringin':
            inny = str(input(content + " "))
            save('temp',inny)
        elif command == 'if':
            contentParts = content.split("=")
            comparison1 = contentParts[0]
            contentParts = (contentParts[1]).split("#")
            comparison2 = contentParts[0]
            targetCheck = contentParts[1]
            
            if comparison1 == comparison2:
                push(targetCheck)

        storyIndex = storyIndex + 1

play("start")
