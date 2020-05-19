from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, RadioField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from flask_login import current_user
from flask_babel import lazy_gettext as _l


class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators = [DataRequired()])
    password = PasswordField(_l('Password'), validators = [DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))

class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators = [DataRequired()])
    email = StringField(_l('Email'), validators = [DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators = [DataRequired()])
    password2 = PasswordField(_l('Password'), validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        u = User.query.filter_by(username = username.data).first()
        if u is not None:
            raise ValidationError(_l('Select differnet username dog'))

    def validate_email(self, email):
        u = User.query.filter_by(email = email.data).first()
        if u is not None:
            raise ValidationError(_l('Select differnet email dog'))

class PasswordReset(FlaskForm):

    email = StringField(_l('email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('submit'))

class PasswordResetting(FlaskForm):

    password = PasswordField(_l('new password'), validators=[DataRequired()])
    password_confirm = PasswordField(_l('confirm password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('submit'))