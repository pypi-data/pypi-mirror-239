import random

def chooseRandom(minValue, maxValue):
    return random.randint(minValue, maxValue)

def compare(answer, guess):
    guess = int(guess)
    answer = int(answer)
    if(guess == answer):
        return 0
    if(guess > answer):
        return 1
    return -1

def numberGuess(minValue = None, maxValue = None):
    if(minValue == None):
        minValue = 0
    if(maxValue == None):
        maxValue = 100
    answer = chooseRandom(minValue, maxValue)
    guess = int(input("Enter your guess: "))
    while(compare(guess, answer) != 0):
        compareResult = compare(answer, guess)
        if(compareResult == 1):
            print("Your guess was too high, please try again")
        elif(compareResult == -1):
            print("Your guess was too low, please try again")
        guess = int(input("Enter your guess: "))
    print("You guessed the correct number!")