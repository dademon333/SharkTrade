from pathlib import Path

from media.modules import validate_image


def _read_file(name: str) -> bytes:
    path = Path(
        Path(__file__).parent,
        name
    )
    return path.read_bytes()


def test_png():
    data = _read_file('logo.png')
    result = validate_image(data)
    assert result is True


def test_jpg():
    data = _read_file('logo.jpg')
    result = validate_image(data)
    assert result is True


def test_corrupted_png():
    data = _read_file('corrupted.png')
    result = validate_image(data)
    assert result is False


def test_corrupted_jpg():
    data = _read_file('corrupted.jpg')
    result = validate_image(data)
    assert result is False


def test_py_file():
    # Lmao let's try to feed it py file
    data = _read_file('hello_world.py')
    result = validate_image(data)
    assert result is False
