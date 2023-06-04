import re
import numpy
import math

class EvaluationClass:
    """A class containing the data for evaluation"""
    regex = ".*"
    name = "unnamedClass"
    wordDict = {}
    probabilityDict = {}
    documentCount = 0
    classProbability = 0
    
    def getTotalWordNum(self):
        """Returns  the total amount of words. {}"""
        return len(self.wordDict.keys())
    
    def addWord(self, word):
        """Adds a word to the word dictionary. Counts the amount of times called for a word. {word}"""
        if (word in self.wordDict):
            self.wordDict[word] = self.wordDict[word] + 1
        else:
            self.wordDict[word] = 1

    def getOccuranceForWord(self, word):
        """Returns the occurances of a word. {word}"""
        if word in self.wordDict:
            return self.wordDict[word]
        return 0

    def addProbability(self, word, probability):
        """Adds a probability to the probability dictionary. {word, probability}"""
        self.probabilityDict[word] = float(probability)

    def setDocumentCount(self, count):
        """Sets the document count for this class. {count}"""
        self.documentCount = count

    def GetDocumentCount(self):
        return self.documentCount

    def getClassProbability(self):
        """Returns the overall probability of the class (document count / total document count). {}"""
        return self.classProbability

    def getName(self):
        """Returns the class name. {}"""
        return self.name
    
    def getLogProbabilityForWord(self, word):
        """Returns the probability for a given word. Returns 0 if non existent. {word}"""
        prob = 1.0 # log of 1 is 0
        if word in self.probabilityDict:
            prob = self.probabilityDict[word]
        return math.log10(prob)


    def __init__(self, pName, pRegex):
        self.name = pName
        self.regex = pRegex
        self.wordDict = dict()
        self.probabilityDict = dict()

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
    
    def calculateChiForWord(word, classlist, totalOccuranceCount):
        """Returns an Chi Squared value for a given word. Requires the classlist and the number of times a word occurred in total. {word, classlist, totalOccur}"""
        chi = 0.0
        n = cutils.calculateTotalFileCount(classlist)
        for ec in classlist:
            for i in range(2):
                c = ec.documentCount
                wordCount = 0
                if word in ec.wordDict:
                    wordCount = ec.wordDict[word]
                w = (n * i - totalOccuranceCount) * numpy.sign(-0.5+i)
                e = (w*c)/n                    
                m = (ec.documentCount * i - wordCount) * numpy.sign(-0.5+i)
                if (e != 0):
                    chi += pow(m-e,2)/e
        return chi
    
    def encodeData(classlist):
        """Encodes the data of a given classlist to a document file (output at ./data.model). {classlist}"""
        totalFileCount = cutils.calculateTotalFileCount(classlist)
        model = open("./data.model", "w")
        for ec in classlist:
            model.write(ec.name+","+str(ec.documentCount/totalFileCount)+";")
        model.write("|")
        for ec in classlist:
            for word, probability in ec.probabilityDict.items():
                model.write(ec.name+","+word+","+str(probability)+";")
        model.close()

    def decodeData(rawData):
        """Decodes the data of a raw encoded dataset to a list with classes. {rawdata}"""
        dataParts = re.split("\|", rawData)
        classProbabilities = re.split(";", dataParts[0])
        probabilityData = re.split(";", dataParts[1])
        classList = []
        for cpd in classProbabilities:
            values = re.split(",", cpd)
            if (len(values) == 2):
                evalClass = EvaluationClass(values[0],"")
                evalClass.classProbability = float(values[1])
                classList.append(evalClass)

        for d in probabilityData:
            value = re.split(",",d)
            if (len(value) == 3):
                classname = value[0]
                word = value[1]
                probability = value[2]
                for ec in classList:
                    if classname == EvaluationClass.getName(ec):
                        EvaluationClass.addProbability(ec, word, probability)

        return classList