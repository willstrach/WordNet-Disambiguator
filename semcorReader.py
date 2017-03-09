from nltk.corpus import semcor
from nltk.corpus import brown
from nltk.corpus import wordnet as wn
from nltk import Tree
import os

class corpusWord:
    def __init__(self, wordForm, posTag, correctSynset):
        self.wordForm = wordForm
        self.posTag = posTag
        self.correctSynset = correctSynset
        self.outputSynset = None
        self.directlySeen = False

    def __repr__(self):
        return (str(self.getWordForm()) + " - " + str(self.getPosTag()) + " - " + str(self.getCorrectSynset()) + " - " + str(self.getOutputSynset()))

    def __str__(self):
        return (str(self.getWordForm()) + " - " + str(self.getPosTag()) + " - " + str(self.getCorrectSynset()) + " - " + str(self.getOutputSynset()))


    def getWordForm(self):
        return self.wordForm

    def getPosTag(self):
        return self.posTag

    def getCorrectSynset(self):
        return self.correctSynset

    def getOutputSynset(self):
        return self.outputSynset

    def setOutputSynset(self, newSynset):
        self.outputSynset = newSynset

    def getDirectlySeen(self):
        return self.directlySeen

    def setDirectlySeen(self, seen):
        self.directlySeen = seen

def idConverter(inputId):
    return ("c" + inputId.split("-")[1][:-4])

def wordSplitter(inputWord):
        if isinstance(inputWord, Tree):
            wordForm = inputWord.leaves()
            posTag = inputWord.pos()[0][1]
            lemmaTag = inputWord.label()
            if (posTag == "NN") or (posTag == "VB"):
                return corpusWord(wordForm, posTag, lemmaTag)
        else:
            return None

def semcorConverter(fileId):
    sentenceList = []
    for sentence in semcor.tagged_sents(fileId, tag="both"):
        wordList = []
        for word in sentence:
            wordObj = wordSplitter(word)
            if wordObj is not None:
                wordList.append(wordObj)
        sentenceList.append(wordList)
    return sentenceList
