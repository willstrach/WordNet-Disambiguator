from memory import *
import models
from nltk.corpus import wordnet as wn

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
    for paragraph in inputCorpus:
        paragraphAnalyser(paragraph, memoryController)

def paragraphAnalyser(inputParagraph, memoryController):
    # Takes input of a paragraph, which is a list of sentences
    # and loops through all sentences
    for sentence in inputParagraph:
        print(memoryController)
        sentenceAnalyser(sentence, memoryController)
        memoryController.forgetAll()

def sentenceAnalyser(inputSentence, memoryController):
    # Takes input of a sentence, which is a list of words
    # and loops through all nouns
    for word in inputSentence:
        if (word[1][:1] == "N") and (word[1][:1] != "NP"):
            wordAnalyser(word[0], memoryController)

def wordAnalyser(inputWord, memoryController):
    # Takes input of a word, each with a set of senses
    # and loops through all senses
    word_senses = wn.synsets(inputWord)
    for sense in word_senses:
        models.linearHypernym(sense, 3, memoryController, 1)
