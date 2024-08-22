import os
import secrets
from PIL import Image
import requests,base64
from flask import url_for, current_app

url = "https://api.imgbb.com/1/upload"

def save_picture_post(form_picture):
    random_hax = secrets.token_hex(8)
    _ , file_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hax + file_ext

    i = Image.open(form_picture)
    i.save(picture_fn)
    with open(picture_fn,'rb') as image_file:
        params = {
            "key" : os.getenv("API_KEY_IMGBB"),
            "image" : base64.b64encode(image_file.read()).decode('utf-8'),
        }
        response = requests.post(url, data=params)
        response.raise_for_status()
        response = response.json()
        
    os.remove(picture_fn)
    return response['data']['image']['url']
