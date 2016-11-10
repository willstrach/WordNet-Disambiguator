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



class stm:
    def __init__(self, maxSize):
        self.contents = []
        self.size = 0
        self.maxSize = maxSize #This value can be set, so that it can be adjusted in experimentation

    def getLowestActivation(self):
        self.minItem = self.contents[0]
        for item in self.contents:
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
