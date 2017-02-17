import random
import models

class MemItem:
    def __init__(self, synset, activation):
        self.synset = synset
        self.activation = activation

    def __str__(self):
        return (str(self.synset) + " - " + str(self.activation))

    def __repr__(self):
        return (str(self.synset) + " - " + str(self.activation))

    def activate(self, constant):
        # This increases the activation of a synset according to a model
        self.activation = models.variableActivation(self.activation, constant)

    def forget(self, constant):
        # This decreases the activation of a synset according to a model
        self.activation = models.variableForget(self.activation, constant)

    def getSynset(self):
        return self.synset

    def getActivation(self):
        return self.activation

###############################################################################
###############################################################################

class Stm:
    def __init__(self, maxSize, forgetThreshold, activationConstantBoost, forgetConstant):
        self.contents = []
        self.size = 0
        # The following values can be set, so that they can be adjusted in experimentation
        self.maxSize = maxSize
        self.forgetThreshold = forgetThreshold
        self.activationConstantBoost = activationConstantBoost
        self.forgetConstant = forgetConstant

    def __repr__(self):
        # Returns the contents of the stm, formatted nicely, used for debugging
        toReturn = "---------------------------------\n"
        for synset in self.getContents():
            toReturn += str(synset.getSynset()) + " - " + str(synset.getActivation()) + "\n"
        toReturn += "---------------------------------"
        return toReturn

    def __str__(self):
        # Returns the contents of the stm, formatted nicely, used for debugging
        toReturn = "---------------------------------\n"
        for synset in self.getContents():
            toReturn += str(synset.getSynset()) + " - " + str(synset.getActivation()) + "\n"
        toReturn += "---------------------------------"
        return toReturn

    def getContents(self):
        if not self.contents:
            return self.contents
        self.unorderedList = self.contents[:]
        self.orderedList = []
        while len(self.unorderedList) > 0:
            maxItem = self.unorderedList[0]
            for item in self.unorderedList:
                if item.getActivation() > maxItem.getActivation():
                    maxItem = item
            self.unorderedList.remove(maxItem)
            self.orderedList.append(maxItem)
        return self.orderedList


    def getSize(self):
        return self.size

    def inContents(self, inputSynset):
        # Takes an input of a synset, and returns boolean value, depending upon whether synset is in stm
        for item in self.getContents():
            if item.getSynset() == inputSynset:
                return True
        return False

    def getItem(self, inputSynset):
        for item in self.getContents():
            if item.getSynset() == inputSynset:
                return item

    def addItem(self, newItem):
        # Takes input of type memItem, and adds it to the stm
        if self.getSize() < self.maxSize:
            if isinstance(newItem, MemItem):
                self.contents.append(newItem)
                self.size += 1
                return
            else:
                raise TypeError("Argument is not of MemItem type")
        else:
            raise Exception("stm is full")

    def removeSynset(self, removedSynset):
        # Takes input of a synset, and removes its corresponding MemItem from the stm
        for item in self.getContents():
            if item.getSynset() == removedSynset:
                self.getContents().remove(item)
                self.size -= 1
                return
        raise LookupError("Item not in STM")

    def getLowestActivation(self):
        # Returns the MemItem in the stm with the lowest activation
        if self.getContents():
            return self.getContents()[-1]
        # minItem = self.getContents()[0]
        # for item in self.getContents():
        #     if item.getActivation() < minItem.getActivation():
        #         minItem = item
        #     elif item.getActivation() == minItem.getActivation():
        #         minItem = random.choice([minItem, item])
        # return minItem

    def swapLowestItem(self, newItem):
        # Takes MemItem input, and either, swaps it for the lowest activation
        # item in the stm (returning the old stm item), or it rejects (and returns)
        # the input MemItem object
        if self.getSize() < self.maxSize:
            self.addItem(newItem)
            return None
        else:
            self.lowestItem = self.getLowestActivation()
            if newItem.getActivation() < self.lowestItem.getActivation():
                return None
            else:
                self.removeSynset(self.lowestItem.getSynset())
                self.addItem(newItem)
                return self.lowestItem

    def forgetAll(self):
        # forgets all items in the stm
        for item in self.getContents():
            item.forget(self.forgetConstant)
            if item.getActivation() < self.forgetConstant:
                self.removeSynset(item.getSynset())

    def activateAll(self, activationModifier):
        # activates all items in the stm
        for item in self.getContents():
            item.activate(activationModifier)

    def activateItem(self, synset, constant):
        # actiivates the MemItem corresponding to the input synset
        constant *= self.activationConstantBoost
        if self.inContents(synset):
            for item in self.getContents():
                if item.getSynset() == synset:
                    item.activate(constant)
                    return
        else:
            raise LookupError("Item not in stm")

    def empty(self):
        # removes all items from stm
        for item in self.getContents():
            self.removeSynset(item.getSynset())


###############################################################################
###############################################################################

class EpisodicBuffer:
    def __init__(self):
        self.contents = []

    def __repr__(self):
        # Prints the contents of the stm, used for debugging
        toReturn = "---------------------------------\n"
        for synset in self.getContents():
            toReturn += str(synset) + "\n"
        toReturn += "---------------------------------"
        return toReturn

    def getContents(self):
        return self.contents

    def inContents(self, inputSynset):
        # Takes an input of a synset, and returns boolean value,
        # depending upon whether synset is in episodicBuffer
        for item in self.getContents():
            if str(item) == str(inputSynset):
                return True
        return False

    def addSynset(self, inputSynset):
        # Takes input of Synset, and adds it to the episodicBuffer
        if self.inContents(inputSynset):
            raise Exception("Synset already in episodicBuffer")
        else:
            self.contents.append(inputSynset)

    def removeSynset(self, inputSynset):
        # Takes input of a synset, and removes its corresponding Item from the
        # EpisodicBuffer
        for item in self.getContents():
            if item == removedSynset:
                self.contents.remove(item)
                return
        raise LookupError("Item not in episodic buffer")

    def empty(self):
        # Removes all synsets from the episodicBuffer
        self.contents = []

###############################################################################
###############################################################################

class MemoryController:
    def __init__(self, stm, episodicBuffer):
        self.stm = stm
        self.episodicBuffer = episodicBuffer

    def __repr__(self):
        # Prints the contents of the stm and episodicBuffer, used for debugging
        toReturn = "##### STM ##### \n"
        toReturn += self.stm + "\n \n"
        toReturn += "##### EPISODIC BUFFER ##### \n"
        toReturn += self.episodicBuffer + "\n \n"

    def sendToStm(self, inputItem):
        # Take input of a synset, and swaps it's corresponding MemItem with one in the STM,
        # if its activation is high enough
        returnedItem = self.stm.swapLowestItem(inputItem)
        if returnedItem is None:
            return
        if not self.episodicBuffer.inContents(returnedItem.getSynset()):
            self.episodicBuffer.addSynset(returnedItem.getSynset())

    def activateSynset(self, synset, activationModifier):
        # Takes input of synset, and: if synset exists in the stm, activates it
        # if synset existsin episodicBuffer and not in stm, the synset is activated
        # with a boost
        # if synset isnot present in system, activates it and sends it to the stm
        if self.stm.inContents(synset):
            self.stm.getItem(synset).activate(activationModifier)
            return
        if self.episodicBuffer.inContents(synset):
            newMemItem = MemItem(synset, 0.5)
            newMemItem.activate(activationModifier)
            self.sendToStm(newMemItem)
            return
        newMemItem = MemItem(synset, 0.0)
        newMemItem.activate(activationModifier)
        self.sendToStm(newMemItem)

    def initialise(self):
        # initialises both memory structures
        self.stm.empty()
        self.episodicBuffer.empty()
