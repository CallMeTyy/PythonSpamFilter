import argparse
from os import path, getcwd
import glob
import sys
import re
import numpy

parser = argparse.ArgumentParser(description='Naive Bayes Email Classifier Trainer')

parser.add_argument('--folder', type=str, help='Input Folder', required=True)
parser.add_argument('--c', type=int, help='The Amount of Classes', default=2, required=False)
parser.add_argument('--v', type=int, help='Words in vocabulary', default=200, required=False)

args = parser.parse_args()

files = glob.glob(args.folder + "/**/*.txt", recursive=True)
if (path.exists(args.folder)):
    print("Folder Found")
else:
    sys.exit("Folder not found")

classdict = {}
regdict = {}
numdict = {}
for i in range(args.c):
    print("Enter Class Name")
    className = input()
    print("Enter regex for search name")
    classRegex = input()
    classdict[className] = dict()
    numdict[className] = 0
    regdict[className] = classRegex

totaldict = {}
totalNum = 0
for cname, wordict in classdict.items():
    filesInClass = []
    print("Creating list for class" + cname + "...")
    for s in files:
        trimmedName = str.replace(s, " ", "")
        name = re.findall("([0-9a-zA-Z\-\(\)]+\.txt)$", trimmedName)
        if (len(name) > 0):
            found = re.search(regdict[cname], name[0])
            if found:
                filesInClass.append(s)
    numdict[cname] = len(filesInClass)
    totalNum += numdict[cname]
    print("Found ", len(filesInClass), " Files")
    print("Adding words to dictionary...")
    for pathToFile in filesInClass:
        doc = open(pathToFile, "r")
        docstr = doc.read().lower()
        words = re.findall("[a-z]+", docstr)
        curlist = []
        for w in words:
            if (w in wordict and w not in curlist):
                totaldict[w] = totaldict[w] + 1
                wordict[w] = wordict[w] + 1
                curlist.append(w)
            elif (w not in wordict):
                wordict[w] = 1
                curlist.append(w)
                if w not in totaldict:
                    totaldict[w] = 1
                else:
                    totaldict[w] = totaldict[w] + 1
                

# sys.exit("done")
print("TotalNum ", totalNum)
for cname, wordict in classdict.items():
    print("Num for regex", cname, numdict[cname])
    print("Amount of words for class", cname, len(dict.values(wordict)))
    

chiList = {}
print("Totaldict Length: ",len(totaldict))
for word, count in totaldict.items():
    chi = 0
    n = len(files)
    for cname, wordict in classdict.items():
        for i in range(2):
            c = numdict[cname] 
            w = (n * i - count) * numpy.sign(-0.5+i)
            wordCount = 0
            if word in wordict:
                wordCount = wordict[word]
            m = (numdict[cname] * i - wordCount) * numpy.sign(-0.5+i)
            e = (w*c)/n
            if (e != 0):
                chi += pow(m-e,2)/e
    chiList[word] = round(chi, 2)

probabilitydict = {}

for cname, wordict in classdict.items():
    probabilitydict[cname] = dict()


sortedList = sorted(chiList.items(), key=lambda item: item[1])
wordCountWithHighChi = 0

for index in range(len(sortedList)-1):
    if (index > len(sortedList)-2 - args.v):
        wordCountWithHighChi+=1
        word = sortedList[index][0]
        for cname, wordict in classdict.items():
            if word in wordict:
                probabilitydict[cname][word] = (wordict[word] + 1) / (numdict[cname] + 2)

print("Amount of words in vocabulary", wordCountWithHighChi)
checkpoint = open("./data.model", "w")
for cname, probabilitydicts in probabilitydict.items():
    checkpoint.write(cname+","+str(numdict[cname]/len(files))+";")

checkpoint.write("|")

for cname, probabilitydicts in probabilitydict.items():
    for word, probability in dict.items(probabilitydicts):
        checkpoint.write(cname+","+word+","+str(probability)+";")
checkpoint.close()

        


