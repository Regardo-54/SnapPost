from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField,FileField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

class Posts(FlaskForm):
    title = StringField("Title",validators=[DataRequired()])
    content = TextAreaField("Content",validators=[DataRequired()])
    image = FileField("Add a picture", validators=[FileAllowed(['png','jpg'])])
    submit = SubmitField("Post")