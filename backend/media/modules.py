import io

from PIL import Image


def validate_image(image_data: bytes) -> bool:
    """Returns True, if image_data is a valid image, else - False."""
    try:
        image = Image.open(io.BytesIO(image_data))
        image.verify()
        image = Image.open(io.BytesIO(image_data))  # .verify() has side-effects, we have to reload data
        image.transpose(Image.FLIP_LEFT_RIGHT)
        return True
    except:
        return False
