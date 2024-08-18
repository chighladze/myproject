import os
import secrets
from flask import current_app
from PIL import Image

"""save user avatar"""


def save_avatar(avatar):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(avatar.filename)
    avatar_filename = random_hex + file_extension
    avatar_path = os.path.join(current_app.config['SERVER_PATH'], avatar_filename)
    output_size = (125, 125)
    img = Image.open(avatar)
    img.thumbnail(output_size)
    img.save(avatar_path)
    return avatar_filename
