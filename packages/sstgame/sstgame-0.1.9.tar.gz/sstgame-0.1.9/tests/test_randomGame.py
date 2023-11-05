from io import StringIO
import tempfile
import pytest
from src.sstgame import randomGame
def test_randomGameRuns(monkeypatch):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write('v')
    
    input_string = StringIO("0\n1")
    monkeypatch.setattr('sys.stdin', input_string)

    value = randomGame.randomGame(0, 1, tmp_file.name, tmp_file.name)

    assert value >= 0

def test_randomGameExcludeAll():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write('v')
    
    value = randomGame.randomGame(0, 1, tmp_file.name, tmp_file.name, madLibAssert=False, numberGuessAssert=False, wyrAssert=False)

    assert value == -1

def test_randomGameExcludeNumberGuess(monkeypatch):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write('v')
    input_string = StringIO("0\n1")
    monkeypatch.setattr('sys.stdin', input_string)

    value = randomGame.randomGame(0, 1, tmp_file.name, tmp_file.name, numberGuessAssert=False)

    assert value > 0

def test_randomGameExcludeMadLib(monkeypatch):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write('v')
    input_string = StringIO("0\n1")
    monkeypatch.setattr('sys.stdin', input_string)

    value = randomGame.randomGame(0, 1, tmp_file.name, tmp_file.name, madLibAssert=False)

    assert value == 0 or value == 2

def test_randomGameExcludeWyr(monkeypatch):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write('v')
    input_string = StringIO("0\n1")
    monkeypatch.setattr('sys.stdin', input_string)

    value = randomGame.randomGame(0, 1, tmp_file.name, tmp_file.name, wyrAssert=False)

    assert value == 0 or value == 1

def test_randomGameOnlyMadLib(monkeypatch):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write('v')
    input_string = StringIO("0\n1")
    monkeypatch.setattr('sys.stdin', input_string)

    value = randomGame.randomGame(0, 1, tmp_file.name, tmp_file.name, numberGuessAssert=False, wyrAssert=False)

    assert value == 1

def test_randomGameOnlyNumberGuess(monkeypatch):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write('v')
    input_string = StringIO("0\n1")
    monkeypatch.setattr('sys.stdin', input_string)

    value = randomGame.randomGame(0, 1, tmp_file.name, tmp_file.name, madLibAssert=False, wyrAssert=False)

    assert value == 0

def test_randomGameOnlyWyr(monkeypatch):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write('v')
    input_string = StringIO("0\n1")
    monkeypatch.setattr('sys.stdin', input_string)

    value = randomGame.randomGame(0, 1, tmp_file.name, tmp_file.name, numberGuessAssert=False, madLibAssert=False)

    assert value == 2