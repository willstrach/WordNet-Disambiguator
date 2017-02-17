from memory import *
from corpusAnalyser import *
from nltk.corpus import semcor
from nltk.corpus import wordnet as wn
from semcorReader import *
from tqdm import tqdm
import models


# The following values are stated here as constants to ease experimentation
# STM
STM_MAXSIZE = 5
STM_FORGETTHRESHHOLD = 0
STM_ACTIVATIONCONSTANTBOOST = 2
STM_FORGETCONSTANT = 0.5


#initialise memory structures
episodicBuffer = EpisodicBuffer()
stm = Stm(STM_MAXSIZE, STM_FORGETTHRESHHOLD, STM_ACTIVATIONCONSTANTBOOST, STM_FORGETCONSTANT)
memoryController = MemoryController(stm, episodicBuffer)

# Clear screen
if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")

# format testing data as a list of documents
allFiles = semcor.fileids()
noToTest = 4
increment = int((len(allFiles) - 1)/noToTest) + 1
testFiles = []
for i in range(0, len(allFiles) - 1, increment):
    testFiles.append(allFiles[i])


testCorpus = []
print "\n"
print "### Preparing Corpus! ###"
for f in tqdm(testFiles):
    testCorpus.append(semcorConverter(f))

# Process a section of the corpus
count = 0
print "\n"
print "### Disambiguating Text! ###"
for corpus in testCorpus:
    count += 1
    print ("File " + str(count) + "/" + str(noToTest))
    memoryController.stm.empty()
    memoryController.episodicBuffer.empty()
    corpusAnalyser(corpus, memoryController)

print "\n"
print "### Evaluating Results! ###"
correct = 0.0
wordCount = 0.0
directlySeen = 0
for corpus in tqdm(testCorpus):
    for sentence in corpus:
        for word in sentence:
            wordCount += 1
            if word.getDirectlySeen() == True:
                directlySeen += 1
            if word.getOutputSynset() is not None:
                for lemma in word.getOutputSynset().lemmas():
                    if str(lemma) == str(word.getCorrectSynset()):
                        correct += 1
                        break

percentCorrect = int((correct/wordCount) * 100)
percentDirectlySeen = int((directlySeen/wordCount) * 100)


# Empty the output text file
f = open("OutputDataFile.txt", "w")
f.close()

# Write the output of the program to file
f = open("OutputDataFile.txt", "a")
f.write("Percent Correct: " + str(percentCorrect) + "%\n")
f.write("Synset Directly Seen: " + str(percentDirectlySeen) + "%\n")
print "\n"
print ("Percent Correct: " + str(percentCorrect) + "%")
print ("Percent Synset Directly Seen: " + str(percentDirectlySeen) + "%\n")
print "\n"

f.close()
