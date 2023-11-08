# test_generate_error.py

import pytest
from src.pyprankerror import generate_error

# Test Case 1: isSilly defaults to False if the arg is not included
def test_isSilly_default():
    result = generate_error("syntax")
    assert result == "SyntaxError: unexpected EOF while parsing"

# Test Case 2: Test that err_type flags return the right outputs
def test_err_type_flags():
    result_syntax = generate_error("syntax")
    assert result_syntax == "SyntaxError: unexpected EOF while parsing"

    result_runtime = generate_error("runtime")
    assert result_runtime == "NameError: name 'undefined_variable' is not defined"

    result_logical = generate_error("logical")
    assert result_logical == "In JavaScript 0+1 == True"

# Test Case 3: Test isSilly flag with err_type
def test_err_type_and_isSilly():
    result_syntax_silly = generate_error("syntax", isSilly=True)
    assert result_syntax_silly == "SINNNNNtaxError: unexpected EOF while parsing HEHE"

    result_runtime_silly = generate_error("runtime", isSilly=True)
    assert result_runtime_silly == "NAMEMEMEMEError: HEHEHAHA name 'undefined_variable' is not defined"

    result_logical_silly = generate_error("logical", isSilly=True)
    assert result_logical_silly == "THE LOGIC IS NOT RIGHT"