import os
import secrets
from PIL import Image
from flask import url_for, current_app


def save_picture_post(form_picture):
    random_hax = secrets.token_hex(8)
    _ , file_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hax + file_ext
    picture_path = os.path.join(current_app.root_path,'static/post_pic',picture_fn)

    i = Image.open(form_picture)
    i.save(picture_path)

    return picture_fn
