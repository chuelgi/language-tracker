import os
from datetime import date

from werkzeug.security import generate_password_hash

from app import app
from db import db
from models import Topic, Log, User

def seed_data():
    print("running seed...")
    with app.app_context():

        db.drop_all()
        db.create_all()

        #topic
        t1 = Topic(name="Spanish")
        t2 =Topic(name = "Japanese")
        t3 = Topic(name="Python")
        t4 = Topic(name="Java")

        #users
        u1 = User(username = "user1", password=generate_password_hash("pass1"))
        u2 = User(username="caleb", password=generate_password_hash("pass2"))
        u3 = User(username="user3", password=generate_password_hash("pass3"))

        #logs

        l1 = Log(duration=36000, title= "New book" ,context="Read a book",time_stamp = date.today(), user = u1, topic = t1)
        l12 = Log(duration=4570,title="1st chapter", context="Read a book",time_stamp = date.today(), user = u1, topic = t2)
        l13 = Log(duration=6000, title="last chapter", context="Read a book",time_stamp = date.today(), user = u1, topic = t3)

        l2 = Log(duration=4000, title= "Java documentary", context="Watched a movie",time_stamp = date.today(), user=u2, topic=t4)
        l3 = Log(duration=5000, context="Practiced",time_stamp = date.today(), user_id=1, topic_id=1)
        db.create_all()

        db.session.add_all([t1, t2, t3, u1, u2, u3, l1, l2, l3, l12, l13])
        db.session.commit()

        print("ending seed...")


if __name__ == "__main__":
    seed_data()