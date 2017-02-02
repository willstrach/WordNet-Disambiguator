from memory import *
import models
from nltk.corpus import wordnet as wn
from tqdm import tqdm

def printStm(memoryController):
    # Prints the contents of the stm, used for debugging
    print "---------------------------------"
    for synset in memoryController.stm.getContents():
        print str(synset.getSynset()) + " - " + str(synset.getActivation())
    print "---------------------------------"

# The following functions deal with the analysis of the input corpus.
# They are divided into corpus, paragraph, sentence and word instead
# of just using nested loops for clarity, and so that
# the contents of the memory can be altered at each of these levels

def corpusAnalyser(inputCorpus, memoryController):
    # Takes input of a corpus, which is a list of paragraphs
    # and loops through all paragraphs
    outputList = []
    for paragraph in tqdm(inputCorpus):
        outputList.append(paragraphAnalyser(paragraph, memoryController))
    return outputList

def paragraphAnalyser(inputParagraph, memoryController):
    # Takes input of a paragraph, which is a list of sentences
    # and loops through all sentences
    outputList = []
    for sentence in inputParagraph:
        outputList.append(sentenceAnalyser(sentence, memoryController))
        memoryController.forgetAll()
    return outputList

def sentenceAnalyser(inputSentence, memoryController):
    # Takes input of a sentence, which is a list of words
    # and loops through all nouns
    outputList = []
    for word in inputSentence:
        if (word[1][:1] == "N") and (word[1][:1] != "NP"):
            wordAnalyser(word[0], memoryController)
    # print(memoryController)
    for word in inputSentence:
        if (len(wn.synsets(word[0])) > 0):
            outputList.append((word[0], models.disambiguate(wn.synsets(word[0]), memoryController)))
    return outputList

def wordAnalyser(inputWord, memoryController):
    # Takes input of a word, each with a set of senses
    # and loops through all senses
    wordSenses = wn.synsets(inputWord)
    for sense in wordSenses:
        models.linearHypernym(sense, 3, memoryController, 1)
