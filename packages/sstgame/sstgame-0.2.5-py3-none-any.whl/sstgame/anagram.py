import random
import os

#Creates a set out of the provided list of words
def makeSet(fileString):
    words_set = set(line.strip() for line in open(fileString))
    return words_set

#Given a number of letters, provides a randomly generated list of letters for use and makes sure at least 1 vowel is provided
def generateLetters(letterCount):
    vowels = ['a', 'e', 'i', 'o', 'u']

    consonants = [chr(i) for i in range(ord('a'), ord('z')+1) if chr(i) not in vowels] #List of consonants

    letters = [random.choice(vowels)]

    for _ in range(letterCount-1):
        letters.append(random.choice(vowels + consonants))
    
    return letters

#Using the word inputted, will check if it is present in the set of words
#Should only be used if and only if the correct letters (and amount of) are used.
#I.E, can't use the worse 'Even' if only one 'e' is provided
def is_valid_answer(words_set, word, letters):
    letter_count = {} #A dictionary to track the amount of letters available.

    for letter in letters:
        if letter in letter_count:
            letter_count[letter] +=1
        else:
            letter_count[letter] = 1
    
    for char in word:
        if char in letter_count and letter_count[char] > 0:
            letter_count[char] -= 1
        else:
            return False #If a character is not in the dictionary, or if the user's word goes over the allowed number of a specific character
        
    #Checks if the word is in the large set of words    
    if word in words_set: 
        return True
    
    return False

#Using the word inputted, will calculate a score to add.
#Once again, this function should only be called if and only if the word is valid. In this case, it must also pass the search as well.
def calcScore(word, letters):
    score = len(word) * 10

    if set(word) == set(letters):
        score += 30
    return score


def anagram(fileString = None):
    if fileString is None:
        package_dir = os.path.dirname(__file__)
        fileString = os.path.join(package_dir, "anagram.txt")
    else:
        package_dir = os.path.dirname(__file__)
        fileString = os.path.join(package_dir, fileString)
        
    words_set = makeSet(fileString) #Makes the anagram.txt into a set for easy access later

    #Initiate all variables for tracking
    attempts = 3
    score = 0
    letters = generateLetters(7)

    print ("Using only the following letters and 3 attempts, make some words! \n" ,','.join(str(x) for x in letters))
    while(attempts > 0):
        answer = input("You've got " + str(attempts) + " attempt left. What word will you make? \n")

        if(is_valid_answer(words_set, answer, letters)):
            score += calcScore(answer, letters)
            print("That's a good answer!\nYour current score is: " + str(score))
        else:
            print("Sorry, your word is invalid or not present in the set.")
        attempts= attempts - 1
    
if __name__ == "__main__":
    anagram()
   
    
