from flask_wtf import FlaskForm
from sqlalchemy import Integer, String
from wtforms import IntegerField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class LogForm(FlaskForm):
    topic = SelectField("Topic", coerce=int)
    hours = IntegerField("Hours", validators=[DataRequired()])
    context = StringField("Description")
    new_topic = StringField("Or create new topic")
    submit = SubmitField("Add Log")

class TopicForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Add Topic")