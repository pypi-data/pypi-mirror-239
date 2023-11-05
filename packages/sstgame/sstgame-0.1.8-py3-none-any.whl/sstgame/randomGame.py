from src.sstgame import numberGuess
from src.sstgame import madlib
from src.sstgame import wyr
import random
import os

def randomGame(minValue = None, maxValue = None, madLibFile = None, wyrFile = None, numberGuessAssert = True, madLibAssert = True, wyrAssert = True):
    index = 0
    numberGuessIndex = -1
    madLibIndex = -1
    wyrIndex = -1

    # Check which games to include.
    if numberGuessAssert == True :
        numberGuessIndex = index
        index += 1

    if madLibAssert == True :
        madLibIndex = index
        index += 1

    if wyrAssert == True :
        wyrIndex = index
        index += 1

    if index == 0 :
        print("All games were excluded. No games were chosen!")
        return -1

    # Choose a random int and run a game associated with the int.
    randomInt = random.randint(0, index-1)

    if randomInt == numberGuessIndex:
        print("Running Guess the Number:\n")
        numberGuess.numberGuess(minValue, maxValue)
        return 0
    elif randomInt == madLibIndex:
        print("Running Mad Libs:\n")
        madlib.madlib(madLibFile)
        return 1
    elif randomInt == wyrIndex:
        print("Running Would You Rather?:\n")
        wyr.wouldYouRather(wyrFile)
        return 2
    else :
        # Program should never reach here.
        print("No game was found.")
        return -2