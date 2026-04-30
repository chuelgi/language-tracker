from flask import Flask, render_template, request, redirect
from flask_login import LoginManager
import secrets

import sqlite3

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


#used to reload user obj from userid stored in session
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('study_tracker.db')
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("SELECT username FROM users WHERE ?", (user_id,))
    row = cur.fetchone()

    conn.close()

    print(row['username'])
