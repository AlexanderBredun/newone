from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, RadioField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from flask_login import current_user
from flask_babel import lazy_gettext as _l
from flask import request



class SimpleForm(FlaskForm):
    example = RadioField('Label', choices=[('default',_l('default')),('black',_l('black')),('red',_l('red'))])


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def validate_username(self, username):
        u = User.query.filter_by(username = username.data).first()
        if u is not None and u != current_user:
            
            raise ValidationError(_l('Select differnet username dog'))

class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something'), validators= [ DataRequired(), Length(min=0, max = 140) ] )
    submit = SubmitField(_l('Submit'))



class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


    
       