# PythonSpamFilter

A simple e-mail classifier made in Python to learn the language.
It can train with a given input of classes and return a data document, which can be used to evaluate and classify emails.
It uses Regular Expressions to sort the different files, so make sure training data has specific naming conventions (e.g. Spam e-mails starting with s would use the expression ^s).

## Docker
Please note that this program has a simple to use docker with a web interface. To learn more, please visit [this repository](https://github.com/callmetyy/pythonspamfilter_docker)

## Prerequisits

- Python 3 (3.11.3 was used to create the program)
- Numpy

## Usage

### Usage - Training

1. Download/clone the repository and place the data samples in /data/
2. Open a terminal and change the directory to the install location of the classifier (e.g. `cd C:/git/PythonSpamFilter`)
3. Run `python3 train.py --folder <training data folder (e.g. /data/train)> --c <The number of classes you want to train> --v <the vocabulary size (precision)>` 
A data.model file will be generated which can be used for the evaluation

To run a training for example run: `python3 train.py --folder ./data --c 2 --v 200`

### Usage - Evaluation
Usage of the Evaluation script requires a model. Either first follow the Training steps to generate a model or look under the latest tags to find a pre-trained model for spam and ham (not-spam).

1. Download/clone the repository
1. Open a terminal and change the directory to the install location of the classifier (e.g. `cd C:/git/PythonSpamFilter`)
2. Place the e-mails to evaluate inside the /evaluate/ folder
3. Run `python3 evaluate.py --folder <evaluation data folder (e.g. /evaluate/test)> --checkpoint <The path to the data.model file> --checkhamspam <An optional argument to check whether something is "Ham" or "Spam" when using a spam e-mail classifier>`

To run an evaluation for example run: `python3 evaluate.py --folder ./evaluate --checkpoint ./data.model`

### Usage - Regular Expressions

When training the system, you will have to enter the regular expressions for the files you have as data. If you are training for ham-spam and are using the corpus (University assignment), you can use `^[0-9]` for ham and `^s` for spam. 

These expressions are indicators for the program to recognize file names. If other file name structures are used, please create a suitable regular expression before usage. In general, the easiest way to recognize a filename is by using the starts with symbol `^`

### Extra Flags
- For both scrips the argument `--debug True` can be added to generate more extensive print lines. This does decrease performance by a lot.
- To speed up the input of training hidden flags `--cs` and `--rs` were added. Both must be used to bypass the custom input.
  - Usage --cs: `--cs "<classNames in csv"` (e.g. `--cs "ham,spam"`)
  - Usage --rs: `--rs "<regex in csv>"` (e.g. `--rs "^[0-9],^s"`)
