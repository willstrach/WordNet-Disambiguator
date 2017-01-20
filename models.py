from memory import *
from corpusAnalyser import *
from nltk.corpus import brown as corpus
from nltk.corpus import wordnet as wn

# All models to be varied will exist in this module. This makes it easier to vary
# them during experimentation

def basicActivation(activation, constant):
    # Increments activation, and returns the result
    # constant is taken as input, only to prevent no. of argument errors
    # during experimentation

    return (activation + 1)
def basicForget(activation, constant):
    # Decrements activation (bounded at zero), and returns the result
    # constant is taken as input, only to prevent no. of argument errors
    # during experimentation
    if activation > constant:
        return (activation - 1)
    else:
        return 0

def basicHypernym(synset, depth, memoryController):
    memoryController.activateSynset(synset)
    if depth > 0:
        for hypernym in synset.hypernyms():
            basicHypernym(hypernym, depth-1, memoryController)
        return
    else:
        return
