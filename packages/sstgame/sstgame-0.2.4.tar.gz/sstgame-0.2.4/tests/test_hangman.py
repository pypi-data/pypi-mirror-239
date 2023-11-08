import pytest
import tempfile
from src.sstgame import hangman
from io import StringIO


def test_readTextEmptyFile():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
        tmp_file.write("")
    prompts = hangman.readText(tmp_file.name)
    assert len(prompts) == 0


def test_readNoTextFile():
    prompts = hangman.readText()
    assert len(prompts) > 0


def test_readTextFirstLine():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
        tmp_file.write("hello world")
    prompts = hangman.readText(tmp_file.name)
    assert len(prompts) == 1
    assert prompts[0] == "helloworld"


def test_readTextMultipleLines():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
        tmp_file.write("hello world \n apple")
    prompts = hangman.readText(tmp_file.name)
    assert len(prompts) == 2
    assert prompts[0] == "helloworld"
    assert prompts[1] == "apple"


def test_validWord():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
        tmp_file.write('"hello world" \n apple, taxi, \n pear, "laptop"')
    prompts = hangman.readText(tmp_file.name)
    assert prompts[0] == "helloworld"
    assert prompts[1] == "apple"
    assert prompts[2] == "taxi"
