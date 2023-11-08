import pytest
import tempfile
from src.sstgame import madlib
from io import StringIO


def test_readTextEmptyFile():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write('')
    prompts = madlib.readText(tmp_file.name)
    assert len(prompts) == 0

def test_extractWordsEmpty():
    matches = madlib.extractWords("This is something that has no extraction")
    assert len(matches) == 0

def test_extractWordsOne():
    matches = madlib.extractWords("There should be one extraction here [verb]")
    assert len(matches) == 1
    assert matches[0] == "verb"

def test_extractWordsMultiple():
    matches = madlib.extractWords("There should be [multiple] [extractions] here [verb]")
    assert len(matches) == 3
    assert matches[0] == "multiple"
    assert matches[1] == "extractions"
    assert matches[2] == "verb"

def test_readTextFirstLine():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write('hello worlds')
    prompts = madlib.readText(tmp_file.name)
    assert len(prompts) == 1
    assert prompts[0] == "hello worlds"

def test_readTextMultipleLines():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write('hello worlds \n pineapple')
    prompts = madlib.readText(tmp_file.name)
    assert len(prompts) == 2
    assert prompts[0] == "hello worlds"
    assert prompts[1] == "pineapple"

def test_userWordsSingle(capfd, monkeypatch):

    input_string = StringIO("run")

    monkeypatch.setattr('sys.stdin', input_string)

    result = madlib.userWords(["verb"])

    captured = capfd.readouterr()

    expected_prompt = "Please enter a verb: "

    assert captured.out == expected_prompt
    assert len(result) == 1
    assert result[0] == "run"

def test_userWordsEmpty(capfd, monkeypatch):

    input_string = StringIO("run")

    monkeypatch.setattr('sys.stdin', input_string)

    result = madlib.userWords([])

    captured = capfd.readouterr()

    assert captured.out == ""
    assert len(result) == 0

def test_userWordsMultiple(capfd, monkeypatch):

    input_string = StringIO("run\npineapple")

    monkeypatch.setattr('sys.stdin', input_string)

    result = madlib.userWords(["verb", "noun"])

    captured = capfd.readouterr()

    assert captured.out == "Please enter a verb: Please enter a noun: "
    assert len(result) == 2
    assert result[0] == "run"
    assert result[1] == "pineapple"

def test_replaceMultiple():
    result = madlib.replace("This is a [verb] [verb] [adj] [adj] [noun]", ["quick", "running", "blue", "red", "pineapple"])

    assert len(result) == len("This is a quick running blue red pineapple")
    assert result == "This is a quick running blue red pineapple"

def test_replaceSingle():
    result = madlib.replace("This is a [noun]", ["pineapple"])

    assert len(result) == len("This is a pineapple")
    assert result == "This is a pineapple"

def test_replaceNone():
    result = madlib.replace("This is a strawberry", ["pineapple"])
    
    assert len(result) == len("This is a strawberry")
    assert result == "This is a strawberry"

def test_madlibSingle(monkeypatch):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write("Once upon a time in a [adjective] kingdom")
    input_string = StringIO("blue")
    monkeypatch.setattr('sys.stdin', input_string)


    result = madlib.madlib(tmp_file.name)

    assert len(result) == len("Once upon a time in a blue kingdom")
    assert result == "Once upon a time in a blue kingdom"

def test_madlibMultiple(monkeypatch):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write("Once upon a time in a [adjective] [noun]")
    input_string = StringIO("blue\npineapple")
    monkeypatch.setattr('sys.stdin', input_string)


    result = madlib.madlib(tmp_file.name)

    assert len(result) == len("Once upon a time in a blue pineapple")
    assert result == "Once upon a time in a blue pineapple"

def test_madlibNone(monkeypatch):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write("Once upon a time in a purple strawberry")
    input_string = StringIO("blue\npineapple")
    monkeypatch.setattr('sys.stdin', input_string)


    result = madlib.madlib(tmp_file.name)

    assert len(result) == len("Once upon a time in a purple strawberry")
    assert result == "Once upon a time in a purple strawberry"

