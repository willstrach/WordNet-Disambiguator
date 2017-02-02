from memory import *
from corpusAnalyser import *
from nltk.corpus import brown as corpus
from nltk.corpus import wordnet as wn
import models
from sys import stdout

# The following values are stated here as constants to ease experimentation
# STM
STM_MAXSIZE = 5
STM_FORGETTHRESHHOLD = 0
STM_ACTIVATIONCONSTANTBOOST = 2
STM_FORGETCONSTANT = 0.5
# Episodic Buffer
EB_ACTIVATIONCONSTANT = 1
EB_FORGETCONSTANT = 0.5

#initialise memory structures
episodicBuffer = episodicBuffer(EB_ACTIVATIONCONSTANT, EB_FORGETCONSTANT)
stm = stm(STM_MAXSIZE, STM_FORGETTHRESHHOLD, STM_ACTIVATIONCONSTANTBOOST, STM_FORGETCONSTANT)
memoryController = memoryController(stm, episodicBuffer)

# format testing data as a list of documents
test_files = corpus.fileids()
total_corpus = []
for f in test_files:
    total_corpus.append(corpus.tagged_paras(f))


disambiguatedCorpus = corpusAnalyser(total_corpus[0], memoryController)

# Write the output of the program to file
outputFile = open("output.txt", "a")
for paragraph in disambiguatedCorpus:
    for sentence in paragraph:
        for word in sentence:
            outputFile.write(str(word[0])+" - "+str(word[1])+"\n")
outputFile.close()
