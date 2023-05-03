class evaluationClass:
    regex = ".*"
    name = "unnamedClass"
    wordDict = {}
    probabilityDict = {}
    documentCount = 0
    
    def totalWordNum(self):
        return len(self.wordDict.keys())
    
    def addWord(self, word):
        if (word in self.wordDict):
            self.wordDict[word] = self.wordDict[word] + 1
        else:
            self.wordDict[word] = 1

    def addProbability(self, word, probability):
        self.probabilityDict[word] = probability

    def setDocumentCount(self, count):
        self.documentCount = count

    def __init__(self, pName, pRegex):
        self.name = pName
        self.regex = pRegex

    def __str__(self):
        return self.name