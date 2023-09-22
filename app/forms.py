from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Optional
from flask_wtf.file import FileField, FileAllowed, FileRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class UploadForm(FlaskForm):
    files = FileField('Music Files', validators=[
        FileRequired(),
        FileAllowed(['mp3', 'wav', 'flac'], 'Music files only.')
    ])
    submit = SubmitField('Upload')

class EditMetadataForm(FlaskForm):
    title = StringField('Title', validators=[Optional()])
    artist_name = StringField('Artist', validators=[Optional()])
    album = StringField('Album', validators=[Optional()])
    genre = StringField('Genre', validators=[Optional()])
    submit = SubmitField('Update Metadata')

