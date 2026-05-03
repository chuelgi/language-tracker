
from dotenv import load_dotenv
import os

load_dotenv()
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask import Flask, render_template, request, redirect
from models import Topic, Log, User
from db import db
from forms import TopicForm, LogForm
app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    #all topics

    topics = Topic.query.all()

    return render_template("dashboard.html", topics=topics)


@app.route("/add-language", methods=["GET", "POST"])
def add_language():
    form =TopicForm()
    if form.validate_on_submit():
        subject = Topic(name = form.name.data)
        db.session.add(subject)
        db.session.commit()
       #flash("Topic Registered")
        return redirect("/")

    return render_template("add_language.html", form = form)

@app.route("/add-log", methods=["GET", "POST"])
def add_log():

    form = LogForm()

    form.topic.choices = [(t.id, t.name) for t in Topic.query.all()]

    if form.validate_on_submit():
        if form.new_topic.data:
            topic = Topic(name=form.new_topic.data)
            db.session.add(topic)
            db.session.commit()
        else:
            topic = Topic.query.get(form.topic.data)

        new_log = Log(
            hours=form.hours.data,
            context=form.context.data,
            user_id=1,
            topic_id=1)

        db.session.add(new_log)
        db.session.commit()
        return redirect("/")

    return render_template("add_log.html", form=form)


@app.route("/logs")
def show_logs():
    logs = Log.query.all()

    return render_template("logs.html", logs=logs)

@app.route("/delete-log/<int:log_id>", methods=["GET", "POST"])
def delete_log(log_id):

    return redirect("/")

@app.route("/lang/<int:lang_id>")
def lang(lang_id):
    topic = Topic.query.get(lang_id)
    logs = Log.query.filter(Log.topic_id == topic.id).all()

    return render_template("lang.html", topic = topic, logs=logs)


if __name__ == '__main__':
    app.run(debug=True)