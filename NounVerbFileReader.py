import os

def keyReader(inLine):
    returnString = inLine.split("*")[2]
    return returnString.split("\n")[0]

def listItemReader(inLine):
    returnString = inLine.split("+")[2]
    returnString = returnString[1:-2]
    returnString = returnString.split("\n")[0]
    synset, distance = returnString.split(", ")
    distance = float(distance)
    return [synset, distance]

def fileReader(fileName):
    returnDict = {}
    currentKey = ""
    currentList = []
    with open(fileName) as f:
        for line in f:
            if line[0] == "*":
                if currentKey != "":
                    returnDict[currentKey] = currentList
                currentKey = keyReader(line)
                currentList = []
            else:
                currentList.append(listItemReader(line))
    f.close()
    return returnDict

def relationDictGen():
    if (not (os.path.isfile("NounFile.txt"))) or (not (os.path.isfile("VerbFile.txt"))):
        os.system("python nounVerbDistanceAnalyser.py")
    nounDict = fileReader("NounFile.txt")
    verbDict = fileReader("VerbFile.txt")
    return nounDict, verbDict
