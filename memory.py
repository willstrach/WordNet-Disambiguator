import random

class memItem:
    def __init__(self, synset, activation):
        self.synset = synset
        self.activation = activation

    def activate(self, increase):
        # This increases the activation of a synset according to a model
        # This method is subject to change
        self.activation += increase
    
    def forget(self):
        # This decreases the activation of a synset according to a model
        # This method is subject to change    
        if self.activation > decrease:
            self.activation -= decrease
        else:
            self.activation = 0

    def getSynset(self):
        return self.synset
    
    def getActivation(self):
        return self.activation

###############################################################################
###############################################################################

class stm:
    def __init__(self, maxSize, forgetThreshold, activationConstant, forgetConstant):
        self.contents = []
        self.size = 0
        # The following values can be set, so that they can be adjusted in experimentation
        self.maxSize = maxSize
        self.forgetThreshold = forgetThreshold
        self.activationConstant = activationConstant
        self.forgetConstant = forgetConstant

    def getContents(self):
        return self.contents

    def getSize(self):
        return self.size

    def inContents(self, inputSynset):
        # Takes an input of a synset, and returns boolean value, depending upon whether synset is in stm
        for item in self.getContents():
            if item.getSynset() == inputSynset:
                return True
        return False

    def addItem(self, newItem):
        # Takes input of type memItem, and adds it to the stm
        if self.getSize() < self.maxSize:
            if isinstance(newItem, memItem):
                self.contents.append(newItem)
                self.size += 1
                return
            else:
                raise TypeError("Argument is not of memItem type")
        else:
            raise Exception("stm is full")

    def removeSynset(self, removedSynset):
        # Takes input of a synset, and removes its corresponding memItem from the stm
        for item in self.contents:
            if item.getSynset() == removedSynset:
                self.contents.remove(item)
                self.size -= 1
                return
        raise LookupError("Item not in STM")

    def getLowestActivation(self):
        # Returns the memItem in the stm with the lowest activation
        minItem = self.contents[0]
        for item in self.getContents():
            if item.getActivation() < minItem.getActivation():
                minItem = item
            elif item.getActivation() == minItem.getActivation():
                minItem = random.choice([minItem, item])
        return minItem

    def swapLowestItem(self, newItem):
        # Takes memItem input, and either, swaps it for the lowest activation
        # item in the stm (returning the old stm item), or it rejects (and returns)
        # the input memItem object
        if self.getSize() < self.maxSize:
            self.addItem(newItem)
            return None
        else:
            self.lowestItem = self.getLowestActivation()
            if newItem.getActivation() < self.lowestItem.getActivation():
                return newItem
            else:
                self.removeSynset(self.lowestItem.getSynset())
                self.addItem(newItem)
                return self.lowestItem

    def forgetAll(self):
        # forgets all items in the stm
        for item in self.contents:
            item.forget()

    def activateItem(self, synset):
        # actiivates the memItem corresponding to the input synset
        if self.inContents(synset):
            for item in self.contents:
                if item.getSynset() == synset:
                    item.activate(self.activationConstant)
                    return
        else:
            raise LookupError("Item not in stm")

###############################################################################
###############################################################################

class episodicBuffer:
    def __init__(self, activationConstant, forgetConstant):
        self.contents = []
        # The following values can be set, so that they can be adjusted in experimentation
        self.activationConstant = activationConstant
        self.forgetConstant = forgetConstant

    def getContents(self):
        return self.contents

    def inContents(self, inputSynset):
        for item in self.getContents():
            if item.getSynset() == inputSynset:
                return True
        return False

    def addSynset(self, newSynset):
        if self.inContents(newSynset):
            raise Exception("Synset already in episodicBuffer")
        else:
            newItem = memItem(newSynset, self.activationConstant)
            self.contents.append(newItem)

    def addItem(self, newItem):
        if newItem == None:
            return
        if isinstance(newItem, memItem):
            if self.inContents(newItem.getSynset()):
                raise Exception("Synset already in episodicBuffer")
            else:
                self.contents.append(newItem)
        else:
            raise TypeError("Argument is not of memItem type")


    def removeSynset(self, removedSynset):
        for item in self.contents:
            if item.getSynset() == removedSynset:
                self.contents.remove(item)
                return
        raise LookupError("Item not in episodic buffer")

    def activateItem(self, synset):
        if self.inContents(synset):
            for item in self.contents:
                if item.getSynset() == synset:
                    item.activate(self.activationConstant)
                    return
        else:
            raise LookupError("Item not in episodic Buffer")

    def forgetAll(self):
        for item in self.contents:
            item.forget()

###############################################################################
###############################################################################

class memoryController:
    def __init__(self, stm, episodicBuffer):
        self.stm = stm
        self.episodicBuffer = episodicBuffer

    def sendToStm(self, inputSynset):
        for item in self.episodicBuffer.getContents():
            if item.getSynset() == inputSynset:
                inputItem = item
                break
        self.episodicBuffer.removeSynset(inputSynset)
        returnedItem = self.stm.swapLowestItem(inputItem)
        self.episodicBuffer.addItem(returnedItem)



    def activateSynset(self, synset):
        if self.stm.inContents(synset):
            self.stm.activateItem(synset)
        elif self.episodicBuffer.inContents(synset):
            self.episodicBuffer.activateItem(synset)
            self.sendToStm(synset)
        else:
            self.episodicBuffer.addSynset(synset)
            self.sendToStm(synset)
