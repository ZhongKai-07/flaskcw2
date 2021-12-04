from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError
import email_validator

from model import User


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Regexp('^[a-zA-Z0-9]*$',
                                                          message='*The username should contain only a-z, A-Z and 0-9.')])
    email = StringField('Email', validators=[DataRequired(), Length(1, 254),Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128), EqualTo('repassword',
                                                                                             message='*The two password should is not same')])
    repassword = PasswordField('confirm password', validators=[DataRequired()])
    submit = SubmitField('Sign in')


    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('*The email is already in use.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('*The username is already in use.')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign up')


class EditForm(FlaskForm):
    old_password = StringField('Old Password', validators=[DataRequired(), Length(8, 128)])
    new_password = StringField('New Password', validators=[DataRequired(), Length(8, 128)])
    submit = SubmitField('change')


class SelectForm(FlaskForm):
    module = StringField('course module', validators=[DataRequired(), Regexp('^[a-zA-z][a-zA-z][a-zA-z][a-zA-z]\d{4}$',
                                            message='The module code is invalid.')])
    submit = SubmitField('submit')


class MessageForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(1, 50)])
    text = TextAreaField('Message', validators=[DataRequired(), Length(1, 500)])
    submit = SubmitField('send')


class CommentForm(FlaskForm):
    text = TextAreaField('write your comment here', validators=[DataRequired(),Length(1, 500)])
    submit = SubmitField('Send')


