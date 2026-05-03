from db import db

class Log(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    hours = db.Column(db.Integer)
    context = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"), nullable = False)

    user = db.relationship("User", back_populates="logs")
    topic = db.relationship("Topic", back_populates="logs")