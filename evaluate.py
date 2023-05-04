import argparse
import glob
import re
import math
import sys
from pythonClassEvaluator import cutils

parser = argparse.ArgumentParser(description='Naive Bayes Classifier')

parser.add_argument('--folder', type=str, help='Test Folder', required=True)
parser.add_argument('--checkpoint', type=str, help='The checkpoint to compare to (trained dataset)', required=True)
parser.add_argument('--checkhamspam', type=bool, help='Whether to check for ham or spam and print performance (hardcoded check)', default=False,required=False)

args = parser.parse_args()

files = glob.glob(args.folder + "/**/*.txt", recursive=True)
checkpointFile = open(args.checkpoint, "r")
checkpoint = checkpointFile.read()
checkpointFile.close()

classdict = {}
prodict = {}
data = re.split("\|", checkpoint)
classprodata = re.split(";", data[0])
for cpd in classprodata:
    values = re.split(",", cpd)
    if (len(values) == 2):
        probability = values[1]
        prodict[values[0]] = values[1]
        classdict[values[0]] = dict()

probabilitydata = re.split(";", data[1])
for d in probabilitydata:
    value = re.split(",",d)
    if (len(value) == 3):
        classname = value[0]
        word = value[1]
        probability = value[2]
        classdict[classname][word] = probability
        
guessDictionary = {}
for documentpath in files:
    doc = open(documentpath, "r")
    text = doc.read().lower()
    words = re.findall("[a-z]+", text)
    probabilities = {}
    for cname, p in prodict.items():
        probabilities[cname] = math.log10(float(p))
        wordict = classdict[cname]
        for w in words:
            if w in wordict:
                probabilities[cname] = probabilities[cname] + math.log10(float(wordict[w]))
    highestChance = -1000000
    predictedClass = ""
    for cname, probability in probabilities.items():
        if float(probability) > highestChance:
            highestChance = float(probability)
            predictedClass = cname
    print(documentpath, predictedClass, highestChance)
    guessDictionary[documentpath] = predictedClass

if not args.checkhamspam:
    sys.exit("Done :)")

# ======= Correct check ==========

correctGuessHam = 0
correctGuessSpam = 0
falseGuessHam = 0
falseGuessSpam = 0
for path, guess in guessDictionary.items():
    name = re.findall("([0-9a-zA-Z\-\(\)]+\.txt)$", str.replace(path, " ", ""))
    actualclass = "ham"
    if name:
        spam = re.search("^s", name[0])
        if (spam):
            actualclass = "spam"

    if guess == actualclass:
        if (actualclass == "ham"):
            correctGuessHam += 1
        else:
            correctGuessSpam += 1
    else:
        if (actualclass == "ham"):
            falseGuessHam += 1
        else:
            falseGuessSpam += 1
totalCorrectGuesses = correctGuessHam + correctGuessSpam
totalFalseGuesses = falseGuessSpam + falseGuessHam
correctPercentage = totalCorrectGuesses / (totalCorrectGuesses + totalFalseGuesses)
print("Correct Guesses Total:")
print(correctGuessHam+correctGuessSpam)
print("Correct %:")
print(correctPercentage)
    

