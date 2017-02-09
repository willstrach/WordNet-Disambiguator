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
STM_FORGETCONSTANT = 1
# Episodic Buffer


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
test_files = semcor.fileids()
total_corpus = []
print "\n"
print "### Preparing Corpus! ###"
for f in tqdm(test_files):
    total_corpus.append(semcorConverter(f))

# Process a section of the corpus
print "\n"
print "### Disambiguating Text! ###"
corpusAnalyser(total_corpus[0], memoryController)

print "\n"
print "### Evaluating Results! ###"
correct = 0.0
wordCount = 0.0
for sentence in tqdm(total_corpus[0]):
    for word in sentence:
        wordCount += 1
        if word.getOutputSynset() is not None:
            for lemma in word.getOutputSynset().lemmas():
                if str(lemma) == str(word.getCorrectSynset()):
                    correct += 1
                    break

percentCorrect = int((correct/wordCount) * 100)

# Empty the output text file
f = open("semcorTestOutput.txt", "w")
f.close()

# Write the output of the program to file
f = open("semcorTestOutput.txt", "a")
f.write("---------------------\n")
f.write("---------------------\n")
f.write("        " + str(percentCorrect) + "% Correct!\n")
f.write("---------------------\n")
f.write("---------------------\n")

# for sentence in total_corpus[0]:
#     for word in sentence:
#         if word.getOutputSynset() is not None:
#             f.write(str(word.getOutputSynset().lemmas()) + " - " + str(word.getCorrectSynset()) + "\n")
f.close()
