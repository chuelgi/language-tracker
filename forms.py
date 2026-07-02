from flask_wtf import FlaskForm
from sqlalchemy import Integer, String
from wtforms import IntegerField, StringField, SubmitField, SelectField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Optional, NumberRange


class LogForm(FlaskForm):
    topic = SelectField("Topic", coerce=int)
    title = StringField("Title")

    hours = IntegerField("Hours", validators=[Optional(), NumberRange(min=0)])
    minutes = IntegerField("Minutes", validators=[Optional(), NumberRange(min=0, max=59)])

    context = StringField("Description")
    new_topic = StringField("Or create new topic")
    submit = SubmitField("Add Log")

class EditLogForm(FlaskForm):
    title = StringField("Title")
    hours = IntegerField("Hours", validators=[Optional(), NumberRange(min=0)])
    minutes = IntegerField("Minutes", validators=[Optional(), NumberRange(min=0, max=59)])

    context  =StringField("Description")
    submit = SubmitField("Save Log")

class DeleteLogForm(FlaskForm):
    submit = SubmitField("Delete Log")

class TopicForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Add Topic")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
