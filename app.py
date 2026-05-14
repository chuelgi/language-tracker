
from dotenv import load_dotenv
import os

from flask_login import LoginManager, login_user, logout_user, login_required
from flask_login import current_user
from jinja2.compiler import generate
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask import Flask, render_template, request, redirect, jsonify
from models import Topic, Log, User
from db import db
from forms import TopicForm, LogForm, RegistrationForm, LoginForm
from sqlalchemy import func
app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
db.init_app(app)



with app.app_context():
    db.create_all()

#flask login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()

        if user and check_password_hash(user.password,form.password.data):
            print("SUCCESS")
            login_user(user)
            return redirect("/")

    return render_template("login.html", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)

        user = User(
            username = form.username.data,
            password = hashed_pw
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/")
    return render_template("register.html", form = form)

@app.route("/")
def index():
    if current_user.is_authenticated:

        topics = (
            db.session.query(Topic)
            .join(Log)
            .filter(Log.user_id == current_user.id)
            .distinct()
            .all()
        )

        results = db.session.query(
            Topic.name,
            func.sum(Log.duration)
        ).join(Topic).filter(
            Log.user_id == current_user.id
        ).group_by(Topic.name).all()

    else:
        topics = Topic.query.all()
        results = []

    # 🔥 COMMUNITY STATS (always computed)
    community_results = db.session.query(
        Topic.name,
        func.sum(Log.duration)
    ).join(Topic).group_by(Topic.name).all()

    # convert to JSON-safe
    results = [(r[0], r[1]) for r in results]
    community_results = [(r[0], r[1]) for r in community_results]

    return render_template(
        "dashboard.html",
        topics=topics,
        results=results,
        community_results=community_results
    )
@app.route("/add-topic", methods=["GET", "POST"])
@login_required
def add_topic():
    form =TopicForm()
    if form.validate_on_submit():
        subject = Topic(name = form.name.data)
        db.session.add(subject)
        db.session.commit()
       #flash("Topic Registered")
        return redirect("/")

    return render_template("add_topic.html", form = form)

@app.route("/add-log", methods=["GET", "POST"])
@login_required
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
            duration=form.duration.data,
            context=form.context.data,
            user_id=current_user.id,
            topic_id=topic.id)

        db.session.add(new_log)
        db.session.commit()
        return redirect("/")

    return render_template("add_log.html", form=form)


@app.route("/logs")
def show_logs():

    logs = Log.query.filter_by(user_id = current_user.id)



    return render_template("logs.html", logs=logs)

@app.route("/delete-log/<int:log_id>", methods=["GET", "POST"])
def delete_log(log_id):

    return redirect("/")

@app.route("/topic/<int:topic_id>")
@login_required
def get_topic_logs(topic_id):
    topic = Topic.query.get_or_404(topic_id)

    logs = Log.query.filter_by(
        topic_id=topic_id,
        user_id=current_user.id
    ).all()

    for log in logs:
        log.hours = round(log.duration / 3600,2)

    return render_template("lang.html", topic = topic, logs=logs)
@app.route("/timer", methods=["GET"])
@login_required
def timer():
    topics = Topic.query.all()

    return render_template('timer.html', topics = topics)

@app.route("/save-session", methods=["POST"])
@login_required
def save_session():
    data = request.get_json()
    topic_id = data["topic_id"]
    duration = data["duration"]

    log = Log(user_id=current_user.id,topic_id=topic_id, duration=duration)
    db.session.add(log)
    db.session.commit()
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)