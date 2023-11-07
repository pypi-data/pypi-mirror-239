# tests for one_word_per_line
import pytest
import sys

sys.path.append('my_module')

# Now you can import your module
from functions import onewordperline, changepreset



def test_onewordperline_default_type(capsys):
    onewordperline(type='joke')
    captured = capsys.readouterr()
    assert captured.out.strip() == "T h i s   i s   a   t e s t   j o k e"

def test_onewordperline_custom_type(capsys):
    onewordperline(type='haiku')
    captured = capsys.readouterr()
    assert captured.out.strip() == "T h i s   i s   a   t e s t   s t o r y"

def test_onewordperline_empty_response(capsys):
    onewordperline(type=None)
    captured = capsys.readouterr()
    assert captured.out.strip() == ""


# print(test_onewordperline_empty_input())

preset = None

def test_changepreset_input(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'NewPreset')
    changepreset()
    assert preset == 'NewPreset'

def test_changepreset_multiple_inputs(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'AnotherPreset')
    changepreset()
    assert preset == 'AnotherPreset'

def test_changepreset_empty_input(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')
    changepreset()
    assert preset == ''

if __name__ == '__main__':
    pytest.main()
