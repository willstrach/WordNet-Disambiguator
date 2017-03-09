from memory import *
import models
from semcorReader import *
from nltk.corpus import wordnet as wn
from tqdm import tqdm

def writeStm(nounStmString, verbStmString, sentence, outputFile):
    # Writes the contents of the stm to an output file
    stmOutputFile = open(outputFile, "a")
    stmOutputFile.write("=====================")
    stmOutputFile.write("\n")
    stmOutputFile.write(nounStmString)
    stmOutputFile.write("\n")
    stmOutputFile.write(verbStmString)
    stmOutputFile.write("\n\n")
    for word in sentence:
        for wordForm in word.getWordForm():
            stmOutputFile.write((wordForm + " "))
    stmOutputFile.write("\n")
    stmOutputFile.write("=====================")
    stmOutputFile.close()

def listCompare(plausibleNouns, actualNouns):
    for noun in plausibleNouns:
        for compNoun in actualNouns:
            if str(noun[0]) == str(compNoun):
                return True
    return False

# def disambiguateSentence(sentence, nounMemoryController, verbMemoryController, nounDict, verbDict, blackList);

# The following functions deal with the analysis of the input corpus.
# They are divided into corpus, paragraph, sentence and word instead
# of just using nested loops for clarity, and so that
# the contents of the memory can be altered at each of these levels

def corpusAnalyser(inputCorpus, nounMemoryController, verbMemoryController, nounDict, verbDict):
    # Takes input of a corpus, which is a list of sentences
    # and loops through all sentences
    prevSentenceOne = None
    prevSentenceTwo = None

    stmOutputFile = open("stmOutputFile.txt", "w")
    stmOutputFile.close()

    for sentence in tqdm(inputCorpus):
        sentenceAnalyser(sentence, nounMemoryController, verbMemoryController, prevSentenceTwo, nounDict, verbDict)

        nounMemoryController.stm.forgetAll()
        verbMemoryController.stm.forgetAll()

        writeStm(str(nounMemoryController.stm), str(verbMemoryController.stm), sentence, "stmOutputFile.txt")

        prevSentenceTwo = prevSentenceOne
        prevSentenceOne = sentence

    sentenceAnalyser([], nounMemoryController, verbMemoryController, prevSentenceOne, nounDict, verbDict)
    sentenceAnalyser([], nounMemoryController, verbMemoryController, prevSentenceTwo, nounDict, verbDict)
    return


def sentenceAnalyser(inputSentence, nounMemoryController, verbMemoryController, prevSentenceTwo, nounDict, verbDict):
    # Takes input of a sentence, which is a list of words
    # and loops through all nouns and verbs

    # Activation of words and hypernyms in sentence
    for word in inputSentence:
        if word.getPosTag() == "NN":
            wordAnalyser(word.getWordForm()[0], "n", nounMemoryController)
        if word.getPosTag() == "VB":
            wordAnalyser(word.getWordForm()[0], "v",verbMemoryController)
            # memoryController.stm.activateAll(0.1)
    # Disambiguation of sentence
    if prevSentenceTwo is not None:
        for word in prevSentenceTwo:
            if word.getPosTag() == "NN":
                disambiguationOutput = models.disambiguate(wn.synsets(word.getWordForm()[0], pos="n"), nounMemoryController, [])
                word.setOutputSynset(disambiguationOutput[0])
                if disambiguationOutput[1] == True:
                    word.setDirectlySeen(True)
            if word.getPosTag() == "VB":
                disambiguationOutput = models.disambiguate(wn.synsets(word.getWordForm()[0], pos="v"), verbMemoryController, [])
                word.setOutputSynset(disambiguationOutput[0])
                if disambiguationOutput[1] == True:
                    word.setDirectlySeen(True)
        # Sanity check of words in sentence
        sane = False # initialise sane to ensure loop runs at least once
        blackList = []
        count = 0
        nounList = []
        verbList = []
        for word in prevSentenceTwo:
            if word.getPosTag() == "NN":
                nounList.append(word.getOutputSynset())
            elif word.getPosTag() == "VB":
                verbList.append(word.getOutputSynset())
        loopCount = 0
        while not sane:
            # count += 1
            # print count
            sane = True
            for verb in verbList:
                if str(verb) in verbDict.keys():
                    plausibleNouns =  verbDict[str(verb)]
                    listCompare(plausibleNouns, nounList)
                    if listCompare(plausibleNouns, nounList):
                        try:
                            verbList.remove(verb)
                            continue
                        except:
                            continue
                    else:
                        loopCount += 1
                        if loopCount < 10:
                            sane = False
                        blackList.append(verb)
                        try:
                            verbList.remove(verb)
                            continue
                        except:
                            continue
                        disambiguationOutput = models.disambiguate(wn.synsets(word.getWordForm()[0], pos="v"), verbMemoryController, blackList)
                        word.setOutputSynset(disambiguationOutput[0])
                        verbList.append(disambiguationOutput[0])
                        if disambiguationOutput[1] == True:
                            word.setDirectlySeen(True)
                        else:
                            word.setDirectlySeen(False)
    return

def wordAnalyser(inputWord, posTag, memoryController):
    # Takes input of a word, each with a set of senses
    # and loops through all senses
    wordSenses = wn.synsets(inputWord, pos=posTag)
    for sense in wordSenses:
        models.variableHypernym(sense, 0.0, memoryController)
