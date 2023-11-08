import random
import os

def readText(fileString):
    prompts = []
    with open(fileString, "r") as file:
        for line in file:
            prompt = line.strip()
            prompts.append(prompt)
        return prompts

def wouldYouRather(fileName = None):
    if fileName is None:
        package_dir = os.path.dirname(__file__)
        fileName = os.path.join(package_dir, "wyr.txt")
    result = readText(fileName)
    prompt = random.choice(result)
    print(prompt)
    input("Please enter 1 for choice 1 or 2 for choice 2: ")
    return 1
