from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, FileField, SelectField,SelectMultipleField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class LoginForm(FlaskForm):
    username = StringField('USERNAME:', validators=[DataRequired()])
    password = PasswordField('PASSWORD:', validators=[DataRequired()])
    submit = SubmitField('LOGIN')


class ContentForm(FlaskForm):
    type = SelectField(choices=['Article', 'Project'] , validators=[DataRequired()])
    subjects = SelectMultipleField(validators=[DataRequired()], choices=['JavaScript', 'Flask', 'Python', 'CSS3', 'HTML5', 'Bootstrap'])
    title = StringField('TITLE:', validators=[DataRequired()])
    content = TextAreaField('CONTENT:', validators=[DataRequired()])
    image = FileField()
    submit = SubmitField('SAVE')