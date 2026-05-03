from db import db

class Topic(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100),unique = True, nullable = False)

    logs = db.relationship("Log", back_populates="topic")