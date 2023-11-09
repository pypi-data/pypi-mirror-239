import pytest
from unittest.mock import patch
from my_module.functions import onewordperline, changepreset, gptchat, cowtalk, preset

# A mock response that mimics the OpenAI API response structure
mock_openai_response = {
    'choices': [
        {'message': {'content': 'mocked response'}}
    ]
}


# Mock the llm function
@pytest.fixture
def mock_llm(monkeypatch):
    def mock(*args, **kwargs):
        return 'mocked response'
    monkeypatch.setattr("my_module.functions.llm", mock)

# Tests for gptchat
@pytest.mark.parametrize("test_input, expected", [
    (("joke", "computers"), "mocked response"),
    (("joke", None), "mocked response"),
    (("haiku", "spring"), "mocked response"),
    (("haiku", None), "mocked response"),
    (("compliment", "music"), "mocked response"),
    (("compliment", None), "mocked response"),
    (("email", "project"), "mocked response"),
    (("email", None), "mocked response"),
    ((None, "a fact"), "mocked response"),
    ((None, None), "mocked response"),
])
def test_gptchat(mock_llm, test_input, expected):
    type_, subject_ = test_input
    response = gptchat(type=type_, subject=subject_)
    assert expected == response

@pytest.mark.parametrize("test_input, expected", [
    (("unknown_type", "anything"), "mocked response"),
    (("unknown_type", None), "mocked response"),
    (("", ""), "mocked response"),
    (("joke", ""), "mocked response"),
    (("", "space"), "mocked response"),
])
def test_gptchat_additional_cases(mock_llm, test_input, expected):
    type_, subject_ = test_input
    response = gptchat(type=type_, subject=subject_)
    assert expected == response


#cowtalk test
# Mock `gptchat` response as it's not directly called from `cowtalk`
@pytest.fixture
def mock_gptchat(monkeypatch):
    def mock(*args, **kwargs):
        # Return the input if provided, else a default string
        return args[0] if args else "This is a mocked response from gptchat function."
    monkeypatch.setattr("my_module.functions.gptchat", mock)

# Helper function to create the expected 'moo' pattern
def create_moo_pattern(sentence):
    words = sentence.split()
    moo_pattern = []
    for i in range(0, len(words), 3):
        moo_pattern.extend(words[i:i+3])
        moo_pattern.append("moo")
    return " ".join(moo_pattern).rstrip(' moo')

# Test for a regular sentence with multiples of three words
def test_cowtalk_regular_sentence(mock_gptchat):
    test_input = "This is a test sentence for the cowtalk function."
    expected_output = create_moo_pattern(test_input)
    result = cowtalk(test_input)
    assert result == expected_output

# Test for a sentence with a non-multiple of three words
def test_cowtalk_non_multiple_of_three(mock_gptchat):
    test_input = "One two three four five"
    expected_output = create_moo_pattern(test_input)
    result = cowtalk(test_input)
    assert result == expected_output

# Test for an empty string
def test_cowtalk_empty_string(mock_gptchat):
    test_input = ""
    expected_output = ""  # Assuming no "moo" added if there are no words
    result = cowtalk(test_input)
    assert result == expected_output



# test one wrod per line
# Test cases
def test_onewordperline_normal():
    input_string = "hello world"
    expected_output = "hello\nworld"
    assert onewordperline(input_string) == expected_output

def test_onewordperline_with_punctuation():
    input_string = "hello, world!"
    expected_output = "hello,\nworld!"
    assert onewordperline(input_string) == expected_output

def test_onewordperline_with_multiple_spaces():
    input_string = "hello   world"  # Multiple spaces between words
    expected_output = "hello\nworld"
    assert onewordperline(input_string) == expected_output


def test_changepreset_updates_global_preset(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "New Preset")
    result = changepreset()
    assert result == "New Preset"


def test_changepreset_empty_input(monkeypatch):
    global preset
    # Assume preset has a predefined value before the test
    original_preset = preset
    monkeypatch.setattr('builtins.input', lambda _: "")
    result = changepreset()
    assert result == original_preset  # Expecting the original preset after empty input

def test_changepreset_space_input(monkeypatch):
    global preset
    # Assume preset has a predefined value before the test
    original_preset = preset
    monkeypatch.setattr('builtins.input', lambda _: " ")
    result = changepreset()
    assert result == original_preset  # Expecting the original preset after space input

