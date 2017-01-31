from memory import *
from corpusAnalyser import *
from nltk.corpus import brown as corpus
from nltk.corpus import wordnet as wn
import random

# All models to be varied will exist in this module. This makes it easier to vary
# them during experimentation


### ACTIVATION MODELS ###
def basicActivation(activation, constant):
    # Increments activation, and returns the result
    # constant is taken as input, only to prevent no. of argument errors
    # during experimentation
    return (activation + 1)

def variableActivation(activation, constant):
    # Adds constant to activation, and returns the result
    return (activation + constant)



### FORGETTING MODELS ###
def basicForget(activation, constant):
    # Decrements activation (bounded at zero), and returns the result
    # constant is taken as input, only to prevent no. of argument errors
    # during experimentation
    if activation > constant:
        return (activation - 1)
    else:
        return 0

def variableForget(activation, constant):
    # Subtracts constant from activation, and returns the result
    return (activation - constant)



### HYPERNYM MODELS ###
def basicHypernym(synset, depth, memoryController, constant):
    memoryController.activateSynset(synset, constant)
    if depth > 0:
        for hypernym in synset.hypernyms():
            basicHypernym(hypernym, depth-1, memoryController, constant)
        return
    else:
        return

def linearHypernym(synset, depth, memoryController, constant):
    constant *= 0.25
    if constant < 0.05:
        return
    memoryController.activateSynset(synset, constant)
    if depth > 0:
        for hypernym in synset.hypernyms():
            basicHypernym(hypernym, depth-1, memoryController, constant)
        return
    else:
        return



### DISABIGUATION MODELS ###
def hyponymSearch(synsetList, searchItem):
    hyponymList = searchItem.hyponyms()
    if len(hyponymList) == 0:
        return None
    for item in hyponymList:
        if item in synsetList:
            return item
    for item in hyponymList:
        returnedItem = hyponymSearch(synsetList, item)
        if returnedItem != None:
            return returnedItem
    return None



def disambiguate(synsetList, memoryController):
    for item in memoryController.stm.getContents():
        if item in synsetList:
            return item
    for item in memoryController.stm.getContents():
        returnedSynset = hyponymSearch(synsetList, item)
        if returnedSynset != None:
            return returnedSynset
        else:
            return random.choice(synsetList)
