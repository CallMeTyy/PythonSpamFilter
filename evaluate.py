import argparse
import glob
import re
import math
import sys
import time
from lib.pythonClassEvaluator import cutils, EvaluationClass

parser = argparse.ArgumentParser(description='Naive Bayes Classifier')

parser.add_argument('--folder', type=str, help='Test Folder', required=True)
parser.add_argument('--checkpoint', type=str, help='The checkpoint to compare to (trained dataset)', required=True)
parser.add_argument('--checkhamspam', type=bool, help='Whether to check for ham or spam and print performance (hardcoded check)', default=False,required=False)

args = parser.parse_args()

# Global Variables
guessDictionary = {} # Stores a predicted class for a path to a file. 
# ================


# Retrieve all files and open the checkpoint file
files = glob.glob(args.folder + "/**/*.txt", recursive=True)
checkpointFile = open(args.checkpoint, "r")
rawData = checkpointFile.read()
checkpointFile.close()

# Decode the data from the checkpoint file
classList = cutils.decodeData(rawData)

# Loop over all the files and check which class is most likely
for documentpath in files:
    words = cutils.getWordsForDocument(documentpath)
    highestChance = -1000000
    predictedClass = ""
    probabilities = []

    for index in range(len(classList)):
        probabilities.append(math.log10(EvaluationClass.getClassProbability(classList[index])))
        for word in words:
            probabilities[index] += EvaluationClass.getLogProbabilityForWord(classList[index], word)

    # The highest chance has the largest likelyhood
    for probability in probabilities:
        print(probability)
        if probability > highestChance:
            highestChance = probability
            className = classList[probabilities.index(probability)]
            predictedClass = EvaluationClass.getName(className)

    print("Predicted Class for ",documentpath, predictedClass, highestChance)
    guessDictionary[documentpath] = predictedClass


# A small file is generated with results
returnText = "<p>"
for path, c in guessDictionary.items():
    returnText += path+" - "+c+"<br>"
returnText += "</p>"
returnFile = open("./data/output.txt", "w")
returnFile.write(returnText)
returnFile.close()

if not args.checkhamspam:
    sys.exit(0)

def GetClassName():
    for index in range(20):
        if guessDictionary:
            returnText = "<p>"
            for path, c in guessDictionary.items():
                returnText += path+" - "+c+"<br>"
            returnText += "</p>"
            return returnText
        else:
            time.sleep(0.25)
    return '''<!doctype html>
    <title>Upload new File</title>
    <h1>File upload timed out/h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
            


# ======= Correct check ==========

correctGuessHam = 0
correctGuessSpam = 0
falseGuessHam = 0
falseGuessSpam = 0

# Loop over all guesses and check whether the guess was correct
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

    

