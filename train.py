import argparse
from os import path
import glob
import sys
from lib.pythonClassEvaluator import EvaluationClass, cutils

# Argument Parser > Allows for command input

parser = argparse.ArgumentParser(description='Naive Bayes Email Classifier Trainer')

parser.add_argument('--folder', type=str, help='Input Folder', required=True)
parser.add_argument('--c', type=int, help='The Amount of Classes', default=2, required=False)
parser.add_argument('--v', type=int, help='Words in vocabulary', default=200, required=False)
parser.add_argument('--cs', type=int, help='All class names in csv', default="", required=False)
parser.add_argument('--rs', type=int, help='All class regex in csv', default="", required=False)

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

# Create the classes with an input name and a regular expression
if args.cs and args.rs:
    clist = args.cs.split(',')
    rlist = args.cs.split(',')
    for i in range(args.c):
        if clist[i] and rlist[i]:
            classlist.append(EvaluationClass(clist[i], rlist[i]))
else:
    for i in range(args.c):
        print("Enter Class Name")
        className = input()
        print("Enter regex for search name")
        classRegex = input()
        classlist.append(EvaluationClass(className, classRegex))


# Loop over all the documents and add the words to the dictionaries using custom made cutils (important functions)
for ec in classlist:
    print("Creating list for class " + ec.name + "...")
    fileNames = cutils.getTrimmedNamesFromFilesWithRegex(files, ec.regex)        
    ec.setDocumentCount(len(fileNames))
    totalNum += EvaluationClass.GetDocumentCount(ec)
    print("Found ", ec.documentCount, " Files")
    print("Adding words to dictionary...")
    for filePath in fileNames:
        words = cutils.getWordsForDocument(filePath)
        currentlist = []
        for word in words:
            if word not in currentlist:
                ec.addWord(word)
                currentlist.append(word)
                if word in totaldict:
                    totaldict[word] += 1
                else:
                    totaldict[word] = 1 
    print("Amount of words added for "+ec.name+": ",EvaluationClass.getTotalWordNum(ec))
           
print("Total Number of Files:", totalNum)
print("Total Number of Words: ",len(totaldict))

# Loop over all the words and calculate the X2 values
for word, count in totaldict.items():
    chi = cutils.calculateChiForWord(word, classlist,totaldict[word])
    chiList[word] = round(chi, 2)

# Sort the list from low to high
sortedList = sorted(chiList.items(), key=lambda item: item[1])
wordCountWithHighChi = 0
#min(args.v, len(sortedList))
# Go over all the highest X2 words and calculate their probabilities
for index in range(max(0,len(sortedList)-args.v), len(sortedList)):
    if (index >= 0):
        wordCountWithHighChi+=1
        word = sortedList[index][0]
        for ec in classlist:
            if word in ec.wordDict:
                probability = (EvaluationClass.getOccuranceForWord(ec, word)+1) / (EvaluationClass.GetDocumentCount(ec) + 2)
                EvaluationClass.addProbability(ec, word, probability)
                print(ec.name, word, probability) 

print("Amount of words in vocabulary", wordCountWithHighChi)
cutils.encodeData(classlist)
print("Done training model. Output path is ./evaluate/data.model")
        


