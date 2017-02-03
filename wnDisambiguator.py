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
STM_FORGETCONSTANT = 1
# Episodic Buffer


#initialise memory structures
episodicBuffer = EpisodicBuffer()
stm = Stm(STM_MAXSIZE, STM_FORGETTHRESHHOLD, STM_ACTIVATIONCONSTANTBOOST, STM_FORGETCONSTANT)
memoryController = MemoryController(stm, episodicBuffer)

# format testing data as a list of documents
test_files = corpus.fileids()
total_corpus = []
for f in test_files:
    total_corpus.append(corpus.tagged_paras(f))

# Process a section of the corpus
disambiguatedCorpus = corpusAnalyser(total_corpus[0], memoryController)

# Empty the output text file
outputFile = open("output.txt", "w")
outputFile.close()

# Write the output of the program to file
outputFile = open("output.txt", "a")
for paragraph in disambiguatedCorpus:
    for sentence in paragraph:
        for word in sentence:
            outputFile.write(str(word[0])+" - "+str(word[1])+"\n")
outputFile.close()
