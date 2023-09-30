from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, URL, Email
import email_validator


##WTForm
class CreateRegisterForm(FlaskForm):
    login = StringField(name="Login:", validators=[DataRequired()])
    e_mail = EmailField(name="E-mail:", validators=[DataRequired(), Email()])
    password = StringField(name="Password:", validators=[DataRequired()])
    submit = SubmitField(name="Register", render_kw={'class': 'submit-custom'})


class CreateLoginForm(FlaskForm):
    e_mail = EmailField(name="E-mail:", validators=[DataRequired(), Email()])
    password = StringField(name="Password:", validators=[DataRequired()])
    submit = SubmitField(name="Login", render_kw={'class': 'submit-custom'})
