# PythonSpamFilter

A simple e-mail classifier made in Python to learn the language.
It can train with a given input of classes and return a data document, which can be used to evaluate and classify emails.
It uses Regular Expressions to sort the different files, so make sure training data has specific naming conventions (e.g. Spam e-mails starting with s would use the expression ^s).

## Prerequisits

- Python 3 (3.11.3 was used to create the program)
- Numpy

## Usage (Windows)

1. Download/clone the repository and place the data samples in /data/
2. Open the train.bat file and follow the instructions - A data.model file will be generated which can be used for the evaluation
3. Place the e-mails to evaluate inside the /evaluate/ folder
4. Run evaluate.bat and follow the instructions, it will return the guesses for each e-mail.

## Usage (Other)

1. Download/clone the repository and place the data samples in /data/
2. Open a terminal and change the directory to the install location of the classifier
3. Run `python3 train.py --folder <training data folder (e.g. /data/train)> --c <The number of classes you want to train> --v <the vocabulary size (precision)>  - A data.model file will be generated which can be used for the evaluation
4. Place the e-mails to evaluate inside the /evaluate/ folder
5. Run `python3 evaluate.py --folder <evaluation data folder (e.g. /evaluate/test)> --checkpoint <The path to the data.model file> --checkhamspam <An optional argument to check whether something is "Ham" or "Spam" when using a spam e-mail classifier>
