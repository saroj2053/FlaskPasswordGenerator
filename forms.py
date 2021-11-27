from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, EmailField, TextAreaField

class ContactForm(FlaskForm):
    name = StringField("Your Name: ")
    email = EmailField("Email: ")
    queries = TextAreaField("Your Query: ")
    submit = SubmitField("Submit Form")
