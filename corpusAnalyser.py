from memory import *
import models
from semcorReader import *
from nltk.corpus import wordnet as wn
from tqdm import tqdm

# The following functions deal with the analysis of the input corpus.
# They are divided into corpus, paragraph, sentence and word instead
# of just using nested loops for clarity, and so that
# the contents of the memory can be altered at each of these levels

def corpusAnalyser(inputCorpus, memoryController):
    # Takes input of a corpus, which is a list of sentences
    # and loops through all sentences
    # for paragraph in inputCorpus:
    for sentence in tqdm(inputCorpus):
        sentenceAnalyser(sentence, memoryController)
    return

# def paragraphAnalyser(inputParagraph, memoryController):
#     # Takes input of a paragraph, which is a list of sentences
#     # and loops through all sentences
#     outputList = []
#     for sentence in inputParagraph:
#         outputList.append(sentenceAnalyser(sentence, memoryController))
#         memoryController.stm.forgetAll()
#     return outputList

def sentenceAnalyser(inputSentence, memoryController):
    # Takes input of a sentence, which is a list of words
    # and loops through all nouns
    for word in inputSentence:
        if word.getPosTag() == "NN":
            wordAnalyser(word.getWordForm()[0], memoryController)
    for word in inputSentence:
        if word.getPosTag() == "NN":
            word.setOutputSynset(models.disambiguate(wn.synsets(word.getWordForm()[0]), memoryController))
            # if (len(wn.synsets(word[0])) > 0):
            #     outputList.append((word[0], models.disambiguate(wn.synsets(word[0]), memoryController)))
    return

def wordAnalyser(inputWord, memoryController):
    # Takes input of a word, each with a set of senses
    # and loops through all senses
    wordSenses = wn.synsets(inputWord)
    for sense in wordSenses:
        models.variableHypernym(sense, 0, memoryController)
