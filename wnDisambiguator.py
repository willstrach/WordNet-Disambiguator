from memory import *
from nltk.corpus import brown as corpus
from nltk.corpus import wordnet as wn
from sys import stdout


#initialise memory structures
episodicBuffer = episodicBuffer(1, 1)
stm = stm(5, 0, 1, 1)
memoryController = memoryController(stm, episodicBuffer)

# format testing data as a list of documents
test_files = corpus.fileids()
total_corpus = []
for f in test_files:
    total_corpus.append(corpus.sents(f))


def corpus_analyser(input_corpus):
    counter = 0
    for sentence in input_corpus:
        counter = counter + 1
        print counter
        for word in sentence:
            word_analyser(word)

    for item in stm.getContents():
        print str(item.getSynset()) + ", " + str(item.getActivation)

def word_analyser(input_word):
    word_senses = wn.synsets(input_word)
    for sense in word_senses:
        memoryController.activateSynset(sense)

corpus_analyser(total_corpus[0])
