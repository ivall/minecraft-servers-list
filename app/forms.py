from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, validators


# Dodawanie serwerów
class AddServerForm(FlaskForm):
    ip = StringField('ip', [validators.DataRequired])


# Oddanie głosu na serwer
class AddVote(FlaskForm):
    recaptcha = RecaptchaField()
