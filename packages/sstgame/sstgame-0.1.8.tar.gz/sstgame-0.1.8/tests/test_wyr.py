import pytest
import tempfile
from src.sstgame import wyr
from io import StringIO

def test_wouldYouRatherWithFile(capfd, monkeypatch):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write('Would you rather eat food or drink water')

    inputString = StringIO("drink water")
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