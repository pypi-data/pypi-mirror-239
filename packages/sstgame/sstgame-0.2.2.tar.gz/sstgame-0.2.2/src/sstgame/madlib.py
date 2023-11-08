import re
import random
import os

def readText(fileString):
    prompts = []
    with open(fileString, "r") as file:
        for line in file:
            prompt = line.strip()
            prompts.append(prompt)
        return prompts

def extractWords(madlib):
    pattern = r'\[(.*?)\]'
    matches = re.findall(pattern, madlib)
    
    return matches

def userWords(replaceArray):
    usersChoice = []

    for word in replaceArray:
        temp = input("Please enter a " + word + ": ")
        usersChoice.append(temp)

    return usersChoice

def replace(originalPrompt, replacementWords):
    pattern = r'\[(.*?)\]'
    
    def replace_match(match):
        return replacementWords.pop(0)
    
    newPrompt = re.sub(pattern, replace_match, originalPrompt)
    
    return newPrompt

def madlib(fileString = None):
    if fileString is None:
        package_dir = os.path.dirname(__file__)
        fileString = os.path.join(package_dir, "madlib.txt")

    prompts = readText(fileString)
    randomPrompt = random.choice(prompts)
    extractedWords = extractWords(randomPrompt)
    usersWords = userWords(extractedWords)
    return replace(randomPrompt, usersWords)