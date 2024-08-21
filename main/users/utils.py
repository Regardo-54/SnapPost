from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from dotenv import load_dotenv
import os
import secrets
from PIL import Image
from flask import url_for, current_app
import smtplib
from email.message import EmailMessage

load_dotenv()

my_email = os.getenv('MY_EMAIL')
password = os.getenv('EMAIL_PASSWORD')

def save_picture(form_picture):
    random_hax = secrets.token_hex(8)
    _ , file_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hax + file_ext
    picture_path = os.path.join(current_app.root_path,'static/profile_pic',picture_fn)

    output = (118,118)
    i = Image.open(form_picture)
    i.thumbnail(output)
    i.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = EmailMessage()
    msg["Subject"] = "Password Reset Request"
    msg["From"] = my_email
    msg["To"] = user.email
    msg_body = f'''To reset your password, visit the following link:
{url_for('users.reset_token',token=token,_external=True)}

If you did not make this request then simply ignore this email and no change will be made.
'''
    msg.set_content(msg_body)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
        connection.ehlo()
        connection.login(user=my_email, password=password)
        connection.send_message(msg)


class Hash:
    secret_password = "738881f14ead291d25de0b782f920558"
    def pass_encrypt(self,password):
       salt = get_random_bytes(16)
       Key = PBKDF2(self.secret_password, salt, dkLen=32)
       password = bytes(password, 'utf-8')
       cipher = AES.new(Key, AES.MODE_CBC)
       ciphered_data = cipher.encrypt(pad(password, AES.block_size))
       final_password_hash = salt+cipher.iv+ciphered_data
       
       return final_password_hash
           
    def pass_decrypt(self,encrypted_pass):
        salt=encrypted_pass[:16]
        iv = encrypted_pass[16:32]
        decrypt_data = encrypted_pass[32:] 
        Key = PBKDF2(self.secret_password, salt, dkLen=32)
        cipher = AES.new(Key, AES.MODE_CBC, iv=iv)
        original = unpad(cipher.decrypt(decrypt_data), AES.block_size).decode('utf-8')
        
        return original