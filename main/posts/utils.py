import os
import secrets
from PIL import Image
from flask import url_for, current_app
import cloudinary
import cloudinary.uploader
import cloudinary.api

url = "https://api.imgbb.com/1/upload"

def save_picture_post(form_picture):
    random_hax = secrets.token_hex(8)
    _ , file_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hax + file_ext

    i = Image.open(form_picture)
    i.save(picture_fn)
    with open(picture_fn,'rb') as image_file:
        cloudinary.config(
            cloud_name = os.getenv("CLOUD_NAME") ,
            api_key = os.getenv("API_KEY_COLUDINARY"),
            api_secret = os.getenv("SECRET_KEY_COLUDINARY")
        )
        response = cloudinary.uploader.upload(picture_fn)
    os.remove(picture_fn)
    return response['secure_url']
