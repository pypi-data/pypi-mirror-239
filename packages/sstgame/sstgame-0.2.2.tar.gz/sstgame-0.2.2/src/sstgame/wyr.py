from src.sstgame.madlib import readText
import random
import os


def wouldYouRather(fileName = None):
    if fileName is None:
        package_dir = os.path.dirname(__file__)
        fileName = os.path.join(package_dir, "wyr.txt")
    result = readText(fileName)
    prompt = random.choice(result)
    print(prompt)
    input("Please enter 1 for choice 1 or 2 for choice 2: ")
    return 1
