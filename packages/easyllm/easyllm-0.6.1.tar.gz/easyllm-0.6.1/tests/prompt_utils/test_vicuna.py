# test_build_vicuna_prompt.py

import pytest

from easyllm.prompt_utils.vicuna import build_vicuna_prompt


def test_build_vicuna_prompt_single_message():
    message = "Hello!"
    expected_output = f"\n\nUSER: {message}\nASSISTANT: "
    result = build_vicuna_prompt(message)
    assert result == expected_output


def test_build_vicuna_prompt_multiple_messages():
    messages = [
        {"content":"You are a chat bot.", "role":"system"},
        {"content":"Hello!", "role": "user"},
    ]
    expected_output = "You are a chat bot.\n\nUSER: Hello!\nASSISTANT: "
    result = build_vicuna_prompt(messages)
    assert result == expected_output


def test_build_vicuna_prompt_function_call():
    messages = [
        {"content":"You are a chat bot.", "role":"system"},
        {"content":"some_function()", "role": "function"},
    ]
    with pytest.raises(ValueError, match="Vicuna does not support function calls."):
        build_vicuna_prompt(messages)
