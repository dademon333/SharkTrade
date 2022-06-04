import string

from common.security.text import find_not_allowed_symbols


def test_english_alphabet():
    text = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = find_not_allowed_symbols(text)
    expected = []
    assert result == expected


def test_numbers():
    text = '0123456789'
    result = find_not_allowed_symbols(text)
    expected = []
    assert result == expected


def test_cyrillic():
    text = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    result = find_not_allowed_symbols(text)
    expected = []
    assert result == expected


def test_ukrainian():
    text = 'ґєіїҐЄІЇ'
    result = find_not_allowed_symbols(text)
    expected = []
    assert result == expected


def test_punctuation():
    text = string.punctuation
    result = find_not_allowed_symbols(text)
    expected = []
    assert result == expected


def test_whitespace():
    text = string.whitespace
    result = find_not_allowed_symbols(text)
    expected = []
    assert result == expected


def test_allowed_mix():
    text = 'абвгд abcdef 123 ґєі ({})'
    result = find_not_allowed_symbols(text)
    expected = []
    assert result == expected


def test_not_allowed_symbols():
    symbols = [chr(x) for x in range(10000, 10050)]
    result = find_not_allowed_symbols(''.join(symbols))
    assert sorted(result) == sorted(symbols)


def test_allowed_and_not_allowed_mix():
    allowed_symbols = 'abcdef'.split()
    not_allowed_symbols = [chr(x) for x in range(10000, 10050)]
    text = ''.join(allowed_symbols + not_allowed_symbols)
    result = find_not_allowed_symbols(text)
    assert sorted(result) == sorted(not_allowed_symbols)
