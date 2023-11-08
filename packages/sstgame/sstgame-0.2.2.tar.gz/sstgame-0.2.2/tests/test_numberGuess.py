import pytest
from src.sstgame import numberGuess
from io import StringIO


def test_chooseRandomPositive():
    result = numberGuess.chooseRandom(1, 3)
    assert result >= 1 and result <= 3

def test_chooseRandomNegative():
    result = numberGuess.chooseRandom(-3, -1)
    assert result >= -3 and result <= -1

def test_chooseRandomPositiveAndNeg():
    result = numberGuess.chooseRandom(-3, 3)
    assert result <= 3 and result >= -3

def test_compareGreaterThan():
    result = numberGuess.compare(0, 100)
    assert result == 1

def test_compareLessThan():
    result = numberGuess.compare(100, 0)
    assert result == -1

def test_compareEqualTo():
    result = numberGuess.compare(0, 0)
    assert result == 0

def test_numberGuessHigher(capfd, monkeypatch):
    input_string = StringIO("10\n3")
    monkeypatch.setattr('sys.stdin', input_string)

    numberGuess.numberGuess(3,3)

    captured = capfd.readouterr()

    assert 'Please enter a guess between 3 and 3\nEnter your guess: Your guess was too high, please try again\nEnter your guess: You guessed the correct number!\n' == captured.out

def test_numberGuessLower(capfd, monkeypatch):
    input_string = StringIO("0\n3")
    monkeypatch.setattr('sys.stdin', input_string)

    numberGuess.numberGuess(3,3)

    captured = capfd.readouterr()

    assert 'Please enter a guess between 3 and 3\nEnter your guess: Your guess was too low, please try again\nEnter your guess: You guessed the correct number!\n' == captured.out

def test_numberGuessExact(capfd, monkeypatch):
    input_string = StringIO("3")
    monkeypatch.setattr('sys.stdin', input_string)

    numberGuess.numberGuess(3,3)

    captured = capfd.readouterr()

    assert 'Please enter a guess between 3 and 3\nEnter your guess: You guessed the correct number!\n' == captured.out

