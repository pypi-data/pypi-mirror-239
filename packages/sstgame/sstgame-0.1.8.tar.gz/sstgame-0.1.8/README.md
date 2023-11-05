![example workflow](https://github.com/github/docs/actions/workflows/main.yml/badge.svg)

### Installing

Please use pip to install.
To install run pip install sstgame

### Importing

Please add import sstgame at the top of your file to import the module
If you would like to import individual games please follow the instructions below

## Import Madlibs game

Please add from sstgame import madlib to import the madlib module

## Import Would You Rather game

Please add from sstgame import wyr to import the would you rather module

## Import Random Number game

Please add from sstgame import randomGuess to import the random number game module

## Import Random Number game

Please add from sstgame import randomGame to import the random game module

### madlibs Function

To use the madlibs function you may pass in your own madlib text file if you would like to use your own custom madlibs.
Please ensure that each madlib is on a seperate line in the text file. If you would like to use the default text file please
do not enter anything.

### numberGuess Function

To use the numberGuess function you may pass in a minimum value which will be the lower bound of the number you have to guess and
a max value which will be the upper bound of what you will have to guess. If you do not want to pass in any arguments the default
will be from 0-100 inclusive.

### wouldYouRather Function

To use the wouldYouRather function you may pass in a txt file containing your own custom would you rathers. Please make sure that
each entry is on a seperate line. If you do not enter an argument, the function will use the default txt file.

### randomGame Function

To use the randomGame function you may pass in arguments for minValue, maxValue, madLibFile, wyrFile, numberGuessAssert, madLibAssert, wyrAssert
The minValue and maxValue will be the inputs for the numberGuess game, the madLibFile will be the txt file for the madlib function, the wyrFile will be the txt for the wouldYouRather function. If you choose to not provide an arguments the default arguments will be used, please refer to each functions section in the README.md for more information.
To include a game to be chosen at random please pass in True for the game you would like to include. Please pass in False to exclude it. By default all games are included and set to True.

### How To Contribute

In order to contribute please clone https://github.com/software-students-fall2023/3-python-package-exercise-sst3.git and create a branch with your contributions. Please install pipenv and use pipenv shell to set up your virtual enviornment. For testing please upload the package with your changes to TestPyPi and install them into your virtual enviornment to run your tests. Please make sure to write test codes using pytest for any created functions.

### Contributors

[Richard Li](https://github.com/Silver1793)
[Ryan Zhang](https://github.com/CouriersRyan)
