import pytest
import tempfile
from src.sstgame import wyr
from io import StringIO

def test_readTextFirstLine():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write('hello worlds')
    prompts = wyr.readText(tmp_file.name)
    assert len(prompts) == 1
    assert prompts[0] == "hello worlds"

def test_readTextMultipleLines():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write('hello worlds \n pineapple')
    prompts = wyr.readText(tmp_file.name)
    assert len(prompts) == 2
    assert prompts[0] == "hello worlds"
    assert prompts[1] == "pineapple"

def test_readTextEmptyFile():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write('')
    prompts = wyr.readText(tmp_file.name)
    assert len(prompts) == 0

def test_wouldYouRatherWithFileChoiceOne(capfd, monkeypatch):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write('Would you rather eat food or drink water')

    inputString = StringIO("1")
    monkeypatch.setattr('sys.stdin', inputString)

    result = wyr.wouldYouRather(tmp_file.name)

    captured = capfd.readouterr()

    assert "Would you rather eat food or drink water\nPlease enter 1 for choice 1 or 2 for choice 2: "==captured.out
    assert result == 1

def test_wouldYouRatherWithFileChoiceTwo(capfd, monkeypatch):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write('Would you rather eat food or drink water')

    inputString = StringIO("2")
    monkeypatch.setattr('sys.stdin', inputString)

    result = wyr.wouldYouRather(tmp_file.name)

    captured = capfd.readouterr()

    assert "Would you rather eat food or drink water\nPlease enter 1 for choice 1 or 2 for choice 2: "==captured.out
    assert result == 1

def test_wouldYouRatherWithOutFile(monkeypatch):
    inputString = StringIO("drink water")
    monkeypatch.setattr('sys.stdin', inputString)

    result = wyr.wouldYouRather()
    assert result == 1

