import argparse
from os import path, getcwd
import glob
import sys
import re
import numpy
from evaluationClass import evaluationClass

# Argument Parser > Allows for command input

parser = argparse.ArgumentParser(description='Naive Bayes Email Classifier Trainer')

parser.add_argument('--folder', type=str, help='Input Folder', required=True)
parser.add_argument('--c', type=int, help='The Amount of Classes', default=2, required=False)
parser.add_argument('--v', type=int, help='Words in vocabulary', default=200, required=False)

args = parser.parse_args()


# Global Variables
classlist = [] # All the different classes with the class name as key and the regex to find each class as value
totaldict = {}
totalNum = 0 # Total number of files
chiList = {} # List of all chisquare values for all words

# Check whether input folder exists, and glob all the filepaths into an array
if (path.exists(args.folder)):
    print("Folder Found")
else:
    sys.exit("Folder not found")
files = glob.glob(args.folder + "/**/*.txt", recursive=True)

for i in range(args.c):
    print("Enter Class Name")
    className = input()
    print("Enter regex for search name")
    classRegex = input()
    classlist.append(evaluationClass(className, classRegex))

def getTrimmedNamesFromFilesWithRegex(files, regex):
    filesInClass = []
    for pathToFile in files:
        nameWithoutSpaces = str.replace(pathToFile, " ", "")
        name = re.findall("([0-9a-zA-Z\-\(\)]+\.txt)$", nameWithoutSpaces)
        if (len(name) > 0):
            found = re.search(regex, name[0])
            if found:
                filesInClass.append(pathToFile)
    return filesInClass

def addWordToEvaluationClass(evalClass, currentList, word):
    if word not in currentList:
        evaluationClass.addWord(evalClass, word)
        if word in totaldict:
            totaldict[w] = totaldict[w] + 1
        else:
            totaldict[w] = 0
        list.append(currentList, word)

def getWordsForDocument(filePath):
    doc = open(filePath, "r")
    docstr = doc.read().lower()
    return re.findall("[a-z]+", docstr)


for ec in classlist:
    print("Creating list for class" + ec.name + "...")
    fileNames = getTrimmedNamesFromFilesWithRegex(files, ec.regex)        
    ec.setDocumentCount(len(fileNames))
    totalNum += ec.totalWordNum()
    
    print("Found ", ec.documentCount, " Files")
    print("Adding words to dictionary...")
    for filePath in fileNames:
        words = getWordsForDocument(filePath)
        currentlist = []
        for w in words:
            addWordToEvaluationClass(ec, currentlist, w)

    print("Words added for "+ec.name+": ",ec.totalWordNum())
                
print("Total Number of Files:", totalNum)
print("Total Number of Words: ",len(totaldict))

def calculateChiForWord(word):
    chi = 0.0
    n = len(files)
    for ec in classlist:
        for i in range(2):
            c = ec.documentCount
            w = (n * i - count) * numpy.sign(-0.5+i)
            e = (w*c)/n
            wordCount = 0
            if word in ec.wordDict:
                wordCount = ec.wordDict[word]
            m = (ec.documentCount * i - wordCount) * numpy.sign(-0.5+i)
            if (e != 0):
                chi += pow(m-e,2)/e
    return chi

for word, count in totaldict.items():
    chi = calculateChiForWord(word)
    chiList[word] = round(chi, 2)

sortedList = sorted(chiList.items(), key=lambda item: item[1])
wordCountWithHighChi = 0

for index in range(len(sortedList)-1):
    if (index > len(sortedList)-2 - args.v):
        wordCountWithHighChi+=1
        word = sortedList[index][0]
        for ec in classlist:
            if word in ec.wordDict:
                ec.addProbability(word, (ec.wordDict[word] + 1) / (ec.totalWordNum() + 2)) 

print("Amount of words in vocabulary", wordCountWithHighChi)
model = open("./data/data.model", "w")
for ec in classlist:
    model.write(ec.name+","+str(ec.documentCount/len(files))+";")
model.write("|")
for ec in classlist:
    for word, probability in ec.probabilityDict.items():
        model.write(ec.name+","+word+","+str(probability)+";")
model.close()
print("Done training model. Output path is ./data/data.model")
        


