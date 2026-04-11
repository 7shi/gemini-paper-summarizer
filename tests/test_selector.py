import pytest
from gp_summarize.lang import selector

# Expected: (input, expected module name)
full_name_cases = [
    ("chinese",   "Chinese"),
    ("english",   "English"),
    ("esperanto", "Esperanto"),
    ("french",    "French"),
    ("german",    "German"),
    ("japanese",  "Japanese"),
    ("korean",    "Korean"),
    ("spanish",   "Spanish"),
]

code_cases = [
    ("de", "German"),
    ("en", "English"),
    ("eo", "Esperanto"),
    ("es", "Spanish"),
    ("fr", "French"),
    ("ja", "Japanese"),
    ("ko", "Korean"),
    ("zh", "Chinese"),
]

locale_cases = [
    ("de_DE", "German"),
    ("en_US", "English"),
    ("eo_001", "Esperanto"),
    ("es_ES", "Spanish"),
    ("fr_FR", "French"),
    ("ja_JP", "Japanese"),
    ("ko_KR", "Korean"),
    ("zh_CN", "Chinese"),
]

@pytest.mark.parametrize("language,expected", full_name_cases)
def test_full_name(language, expected):
    assert selector.init(language).name == expected

@pytest.mark.parametrize("language,expected", code_cases)
def test_code(language, expected):
    assert selector.init(language).name == expected

@pytest.mark.parametrize("language,expected", locale_cases)
def test_locale(language, expected):
    assert selector.init(language).name == expected
