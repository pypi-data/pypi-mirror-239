from io import StringIO
import tempfile
import pytest
from src.sstgame import randomGame


def test_randomGameRuns(monkeypatch):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
        tmp_file.write("v")

    input_string = StringIO("0\n1\n2\n3\n4\n5\n6")
    monkeypatch.setattr("sys.stdin", input_string)

    value = randomGame.randomGame(0, 1, tmp_file.name, tmp_file.name, tmp_file.name)

    assert value >= 0


def test_randomGameExcludeAll():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
        tmp_file.write("v")

    value = randomGame.randomGame(
        0,
        1,
        tmp_file.name,
        tmp_file.name,
        madLibAssert=False,
        numberGuessAssert=False,
        wyrAssert=False,
        hangmanAssert=False,
        anagramAssert=False
    )

    assert value == -1


def test_randomGameExcludeNumberGuess(monkeypatch):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
        tmp_file.write("v")
    input_string = StringIO("0\n1\n2\n3\n4\n5\n6")
    monkeypatch.setattr("sys.stdin", input_string)

    value = randomGame.randomGame(0, 1, tmp_file.name, tmp_file.name,tmp_file.name,tmp_file.name, numberGuessAssert=False)

    assert value > 0


def test_randomGameExcludeMadLib(monkeypatch):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
        tmp_file.write("v")
    input_string = StringIO("0\n1\n2\n3\n4\n5\n6")
    monkeypatch.setattr("sys.stdin", input_string)

    value = randomGame.randomGame(0, 1, tmp_file.name, tmp_file.name,tmp_file.name,tmp_file.name, madLibAssert=False)

    assert value == 0 or value == 2 or value == 3 or value == 4


def test_randomGameExcludeWyr(monkeypatch):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
        tmp_file.write("v")
    input_string = StringIO("0\n1\n2\n3\n4\n5\n6")
    monkeypatch.setattr("sys.stdin", input_string)

    value = randomGame.randomGame(0, 1, tmp_file.name, tmp_file.name,tmp_file.name,tmp_file.name, wyrAssert=False)

    assert value == 0 or value == 1 or value == 3 or value == 4


def test_randomGameExcludeHangman(monkeypatch):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
        tmp_file.write("v")
    input_string = StringIO("0\n1\n2\n3\n4\n5\n6")
    monkeypatch.setattr("sys.stdin", input_string)

    value = randomGame.randomGame(0, 1, tmp_file.name, tmp_file.name,tmp_file.name,tmp_file.name, hangmanAssert=False)

    assert value == 0 or value == 1 or value == 2 or value == 4

def test_randomGameExcludeAnagram(monkeypatch):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
        tmp_file.write("v")
    input_string = StringIO("0\n1")
    monkeypatch.setattr("sys.stdin", input_string)

    value = randomGame.randomGame(0, 1, tmp_file.name, tmp_file.name,tmp_file.name,tmp_file.name,anagramAssert=False)

    assert value == 0 or value == 1 or value == 2 or value == 3

def test_randomGameOnlyMadLib(monkeypatch):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
        tmp_file.write("v")
    input_string = StringIO("0\n1")
    monkeypatch.setattr("sys.stdin", input_string)

    value = randomGame.randomGame(
        minValue = None,
        maxValue = None,
        madLibFile = tmp_file.name,
        numberGuessAssert=False,
        wyrAssert=False,
        hangmanAssert=False,
        anagramAssert=False
    )

    assert value == 1


def test_randomGameOnlyNumberGuess(monkeypatch):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
        tmp_file.write("v")
    input_string = StringIO("0\n1")
    monkeypatch.setattr("sys.stdin", input_string)

    value = randomGame.randomGame(
        minValue = 0,
        maxValue = 1,
        madLibAssert=False,
        wyrAssert=False,
        hangmanAssert=False,
        anagramAssert=False
    )

    assert value == 0


def test_randomGameOnlyWyr(monkeypatch):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
        tmp_file.write("v")
    input_string = StringIO("0\n1")
    monkeypatch.setattr("sys.stdin", input_string)

    value = randomGame.randomGame(
        minValue = None,
        maxValue = None,
        wyrFile = tmp_file.name,
        numberGuessAssert=False,
        madLibAssert=False,
        hangmanAssert=False,
        anagramAssert=False
    )

    assert value == 2


def test_randomGameOnlyHangman(monkeypatch):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
        tmp_file.write("hello,world")
    input_string = StringIO("a\nb\nc\nr\nz\nf\ng\n")
    monkeypatch.setattr("sys.stdin", input_string)

    value = randomGame.randomGame(
        minValue = None,
        maxValue = None,
        hangmanFile = tmp_file.name,
        numberGuessAssert=False,
        madLibAssert=False,
        wyrAssert=False,
        anagramAssert=False
    )

    assert value == 3

def test_randomGameOnlyAnagram(monkeypatch):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
        tmp_file.write("hello,world")
    input_string = StringIO("a\nb\nc\nr\nz\nf\ng\n")
    monkeypatch.setattr("sys.stdin", input_string)

    value = randomGame.randomGame(
        minValue = None,
        maxValue = None,
        anagramFile = tmp_file.name,
        numberGuessAssert=False,
        madLibAssert=False,
        wyrAssert=False,
        anagramAssert=True,
        hangmanAssert=False
    )

    assert value == 4
