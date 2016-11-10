class memItem:
    def __init__(self, synset, activation):
        self.synset = synset
        self.activation = activation

    def activate(self):
        # This increases the activation of a synset according to a model
        # This method is subject to change
        self.activate += 1
    def forget(self):
        # This decreases the activation of a synset according to a model
        # This method is subject to change
        self.activate -= 1

    def getSynset(self):
        return self.synset
    def getActivation(self):
        return self.activation


#####################################################################################
#####################################################################################


class stm:
    def __init__(self, maxSize, forgetThreshold):
        self.contents = []
        self.size = 0
        self.maxSize = maxSize #This value can be set, so that it can be adjusted in experimentation
        self.forgetThreshold = forgetThreshold #This value can be set, so that it can be adjusted in experimentation

    def getLowestActivation(self):
        self.minItem = self.contents[0]
        for self.item in self.contents:
            if self.item.getActivation() < self.minItem.getActivation():
                self.minItem = self.item
        return minItem

    def swapLowestItem(self, newItem):
        if self.size < self.maxSize:
            # if the stm isn't full, just append
            self.contents.append(newItem)
        else:
            # first, find the synset with the lowest activation
            self.minItem = self.getLowestActivation()
            # should the new item get into stm?
            if newItem.getActivation() > self.minItem.getActivation():
                # remove item with lowest activation from stm
                self.contents.remove(self.minItem)
                # add new item to stm
                self.contents.append(newItem)
                # return old item
                return self.minItem
            else:
                return newItem
                # return item which failed to enter stm

    def forgetAll(self):
        for self.item in self.contents:
            self.item.forget()
            if self.item.getActivation() < self.forgetThreshold:
                self.contents.remove(self.item)

    def empty(self):
        for self.item in self.contents:
            self.contents.remove(self.item)


#####################################################################################
#####################################################################################


class episodicBuffer:
    def __init__(self):
        self.contents = []

    def addItem(self, newItemSS):
        self.newItem = memItem(newItemSS, 1) # Create a new memItem object, with an activation of 1 (subject to change)
        self.contents.append(newItem)

    def sendToStm(self, sendItem, stm):
        self.contents.remove(sendItem) # remove item being sent to the stm
        self.returnedItem = stm.swapLowestItem(sendItem) # send item to stm, old item from stm, or the sent item is rejected
        self.contents.append(self.returnedItem) # old stm item,or rejected sent item, re-added to episodic buffer

    def activateItem(self, newItemSS):
        for self.item in self.contents:
            if self.item.getSynset == self.newItemSS:
                self.item.activate()
                self.sendToStm(self.item)
                return
        self.addItem(newItemSS)

    def empty(self):
        for self.item in self.contents:
            self.contents.remove(self.item)
