import random
import string
import os
import re


def readText(fileString=None):
    if fileString is None:
        package_dir = os.path.dirname(__file__)
        fileString = os.path.join(package_dir, "hangman.txt")

    with open(fileString, "r") as file:
        prompts = []
        for line in file:
            prompt = line.strip()
            prompt = re.sub(r"[^\w,]+", "", prompt)
            prompt = prompt.split(",")
            if len(prompt) > 0:
                for p in prompt:
                    if p != "":
                        prompts.append(p)
    return prompts


def valid_word(fileString=None):
    if fileString is None:
        package_dir = os.path.dirname(__file__)
        fileString = os.path.join(package_dir, "hangman.txt")

    all_words = readText(fileString)
    word = random.choice(all_words)
    while "-" in word or " " in word:
        word = random.choice(fileString)
    return word.upper()


def hangman(fileString=None):
    if fileString is None:
        package_dir = os.path.dirname(__file__)
        fileString = os.path.join(package_dir, "hangman.txt")
    else:
        package_dir = os.path.dirname(__file__)
        fileString = os.path.join(package_dir, fileString)

    word = valid_word(fileString)
    word_letters = set(word)  # letters in the word
    alphabet = set(string.ascii_uppercase)
    used_letters = set()  # what the user has guessed

    tries = 6

    # getting user input
    while len(word_letters) > 0 and tries > 0:
        print(
            "You have",
            tries,
            "lives left.\nYou have used the letters:",
            " ".join(used_letters),
        )

        # word process
        word_list = [letter if letter in used_letters else "-" for letter in word]
        print("Current word: ", " ".join(word_list))

        user_letter = input("Guess a letter: ").upper()
        print("\n")
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            # correct guess
            if user_letter in word_letters:
                word_letters.remove(user_letter)
            else:
                tries = tries - 1
                print(user_letter, "is not in word")
        elif user_letter in used_letters:
            print("You have already used that letter. Please try again.")
        else:
            tries = 0
            print("Invalid character. You lost all of your lives")

    if tries == 0:
        print("\nNo more tries left. The word was", word)
    else:
        print("You guessed the word ", word, "correctly.")
