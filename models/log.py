from datetime import datetime

from db import db

class Log(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    duration = db.Column(db.Integer) #seconds
    context = db.Column(db.String(255))
    time_stamp = db.Column(db.Date,default = datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"), nullable = False)

    user = db.relationship("User", back_populates="logs")
    topic = db.relationship("Topic", back_populates="logs")