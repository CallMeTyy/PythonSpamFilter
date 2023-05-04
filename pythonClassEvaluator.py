import re
import numpy

class EvaluationClass:
    """A class containing the data for evaluation"""
    regex = ".*"
    name = "unnamedClass"
    wordDict = {}
    probabilityDict = {}
    documentCount = 0
    
    def getTotalWordNum(self):
        """Returns  the total amount of words. {}"""
        return len(self.wordDict.keys())
    
    def addWord(self, word):
        """Adds a word to the word dictionary. Counts the amount of times called for a word. {word}"""
        if (word in self.wordDict):
            self.wordDict[word] = self.wordDict[word] + 1
        else:
            self.wordDict[word] = 1

    def addProbability(self, word, probability):
        """Adds a probability to the probability dictionary. {word, probability}"""
        self.probabilityDict[word] = probability

    def setDocumentCount(self, count):
        """Sets the document count for this class. {count}"""
        self.documentCount = count

    def __init__(self, pName, pRegex):
        self.name = pName
        self.regex = pRegex

    def __str__(self):
        return self.name
    
class cutils:
    """A class with the required functions to create the class evaluator and trainer"""

    def getTrimmedNamesFromFilesWithRegex(files, regex):
        """Returns an array with all file paths that follow from a given regex. {rawFilePathArray, classRegex}"""
        filesInClass = []
        for pathToFile in files:
            nameWithoutSpaces = str.replace(pathToFile, " ", "")
            name = re.findall("([0-9a-zA-Z\-\(\)]+\.txt)$", nameWithoutSpaces)
            if (len(name) > 0):
                found = re.search(regex, name[0])
                if found:
                    filesInClass.append(pathToFile)
        return filesInClass

    def getWordsForDocument(filePath):
        """Returns an array with all words in a document from the given filepath. {filepath}"""
        doc = open(filePath, "r")
        docstr = doc.read().lower()
        doc.close()
        return re.findall("[a-z]+", docstr)
    
    def calculateTotalFileCount(classlist):
        """Helper function to calculate file count for all classes. {classlist}"""
        count = 0
        for ec in classlist:
            count += ec.documentCount
        return count
    
    def calculateChiForWord(word, classlist):
        """Returns an Chi Squared value for a given word. Requires the classlist. {word, classlist}"""
        chi = 0.0
        n = cutils.calculateTotalFileCount(classlist)
        for ec in classlist:
            for i in range(2):
                c = ec.documentCount
                count = classlist[i].wordDict[word]
                w = (n * i - count) * numpy.sign(-0.5+i)
                e = (w*c)/n
                wordCount = 0
                if word in ec.wordDict:
                    wordCount = ec.wordDict[word]
                m = (ec.documentCount * i - wordCount) * numpy.sign(-0.5+i)
                if (e != 0):
                    chi += pow(m-e,2)/e
        return chi
    
    def encodeData(classlist):
        """Encodes the data of a given classlist to a document file (output at ./data/data.model). {classlist}"""
        totalFileCount = cutils.calculateTotalFileCount(classlist)
        model = open("./data/data.model", "w")
        for ec in classlist:
            model.write(ec.name+","+str(ec.documentCount/totalFileCount)+";")
        model.write("|")
        for ec in classlist:
            for word, probability in ec.probabilityDict.items():
                model.write(ec.name+","+word+","+str(probability)+";")
        model.close()