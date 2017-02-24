from nltk.corpus import semcor
from nltk.corpus import wordnet as wn
from tqdm import tqdm

nounDict = {}
verbDict = {}

def verbDistance(verb, sentence):
    outputList = []
    for i in range(0, len(sentence)):
        if sentence[i] == verb:
            verbLocation = i
    for i in range(0,len(sentence)):
        if sentence[i][1] == "N":
            outputList.append((sentence[i][0], 1/(abs(i - verbLocation))))
    return outputList

def nounDistance(noun, sentence):
    outputList = []
    for i in range(0, len(sentence)):
        if sentence[i] == noun:
            nounLocation = i
    for i in range(0,len(sentence)):
        if sentence[i][1] == "V":
            outputList.append((sentence[i][0], 1.0/(abs(i - nounLocation))))
    return outputList

def listUpdater(currentList, updateList):
    for currentItem in currentList:
        for updateItem in updateList:
            if currentItem[0] == updateItem[0]:
                currentItem = [currentItem[0], (currentItem[1]+updateItem[1])]
                currentItem[1] += updateItem[1]
                break
    return currentList

allFiles = semcor.fileids()
for fileId in tqdm(allFiles):
    for sentence in semcor.tagged_sents(fileId, tag="both"):
        sentenceList = []
        for word in sentence:
            if word.pos()[0][1] == "VB":
                try:
                    lemma = word.label()
                    sentenceList.append([lemma.synset(), "V"])
                except AttributeError:
                    pass
            if word.pos()[0][1] == "NN":
                try:
                    lemma = word.label()
                    sentenceList.append([lemma.synset(), "N"])
                except AttributeError:
                    pass
        for word in sentenceList:
            if word[1] == "V":
                distanceList = verbDistance(word, sentenceList)
                if word[0] in verbDict.keys():
                    verbDict[word[0]] = listUpdater(verbDict[word[0]], distanceList)
                else:
                    verbDict[word[0]] = distanceList
            if word[1] == "N":
                distanceList = nounDistance(word, sentenceList)
                if word[0] in nounDict.keys():
                    nounDict[word[0]] = listUpdater(nounDict[word[0]], distanceList)
                else:
                    nounDict[word[0]] = distanceList

nounFile = open("NounFile.txt", "w")
nounFile.close()
verbFile = open("VerbFile.txt", "w")
verbFile.close()

nounFile = open("NounFile.txt", "a")
for noun in nounDict.keys():
    nounFile.write("**" + str(noun) + "\n")
    for verb in nounDict[noun]:
        nounFile.write("    ++" + str(verb) + "\n")
nounFile.close()

verbFile = open("VerbFile.txt", "a")
for verb in verbDict.keys():
    verbFile.write("**" + str(verb) + "\n")
    for noun in verbDict[verb]:
        verbFile.write("    ++" + str(noun) + "\n")
verbFile.close()
