import pytest
from unittest.mock import patch
from src.pyprankerror import generate_hacked_message

# Define the mock_random_choice fixture in the test module
@pytest.fixture
def mock_random_choice():
    with patch('random.choice') as mock:
        yield mock

def test_default_arguments(mock_random_choice):
    messages = generate_hacked_message()
    for message in messages:
        assert "Your computer has been hacked by" in message

def test_is_silly_true(mock_random_choice):
    messages = generate_hacked_message(is_silly=True)
    for message in messages:
        assert "Your" in message
        assert "has been" in message
        assert "by a" in message

def test_is_long_and_is_silly_true(mock_random_choice):
    messages = generate_hacked_message(is_long=True, is_silly=True)
    assert len(messages) == 5
    for message in messages:
        assert "Your" in message
        assert "has been" in message
        assert "by a" in message

def test_is_long_and_is_silly_false(mock_random_choice):
    messages = generate_hacked_message(is_long=False, is_silly=False)
    assert len(messages) == 1
    for message in messages:
        assert "Your computer has been hacked by an anonymous hacker" in message
        assert "Hacker ID:" in message
        assert "Hacking Timestamp:" in message