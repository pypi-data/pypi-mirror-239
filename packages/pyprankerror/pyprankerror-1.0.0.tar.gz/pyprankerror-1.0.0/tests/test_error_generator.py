import pytest
from unittest.mock import patch
import sys
import os


from src.pyprankerror import generate_crash_report, silly_long, silly_short, long, short

# --------------- Crash Report Test Code ---------------------
@pytest.fixture
def mock_random_randint():
    with patch('random.randint') as mock:
        yield mock

def test_default_arguments(mock_random_randint, capsys):
    mock_random_randint.return_value = 2
    generate_crash_report()
    captured = capsys.readouterr()
    assert captured.out.strip() == short[2]

def test_is_long_true(mock_random_randint, capsys):
    mock_random_randint.return_value = 3
    generate_crash_report(is_long=True)
    captured = capsys.readouterr()
    assert captured.out.strip() == long[3]

def test_is_silly_true(mock_random_randint, capsys):
    mock_random_randint.return_value = 1
    generate_crash_report(is_silly=True)
    captured = capsys.readouterr()
    assert captured.out.strip() == silly_short

def test_is_long_and_silly_true(mock_random_randint, capsys):
    mock_random_randint.return_value = 0
    generate_crash_report(is_long=True, is_silly=True)
    captured = capsys.readouterr()
    assert captured.out.strip() == silly_long
# --------------- End of Crash Report Test Code ---------------------

