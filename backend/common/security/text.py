import string


def find_not_allowed_symbols(text: str) -> list[str]:
    allowed = string.printable \
              + 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' \
                'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ' \
                'ґєіїҐЄІЇ'
    return [x for x in text if x not in allowed]
