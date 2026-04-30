from flask import Flask, render_template, request, redirect
from flask_login import LoginManager
import secrets

import sqlite3

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)




@app.route("/")
def index():
    conn = sqlite3.connect('logs.db')
    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    cur.execute("""
                SELECT languages.id, languages.name, SUM(logs.hours) AS total_hours
                FROM logs
                         JOIN languages ON logs.lang_id = languages.id
                GROUP BY logs.lang_id
                """)

    totals = cur.fetchall()

    labels = [row["name"] for row in totals]
    values = [row["total_hours"] or 0 for row in totals]


    conn.close()

    return render_template(
        "dashboard.html",
        totals=totals,
        labels=labels,
        values=values,
        goal=50
    )
@app.route("/add-language", methods=["GET", "POST"])
def add_language():
    if request.method == "POST":
        language = request.form["language"]

        conn = sqlite3.connect('logs.db')
        cur = conn.cursor()

        cur.execute('INSERT INTO languages (name) VALUES (?)', (language,))

        conn.commit()
        conn.close()

        return redirect('/')


    return render_template("add_language.html")

@app.route("/add-log", methods=["GET", "POST"])
def add_log():

    conn = sqlite3.connect('logs.db')
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    if request.method == "POST":
        lang_id = request.form["lang_id"]
        hours= request.form["hours"]
        date = request.form["date"]
        notes = request.form["notes"]

        cur.execute('''
                    INSERT INTO logs (lang_id, hours, date, notes)
                    VALUES (?, ?, ?, ?)
                    ''', (lang_id, hours, date, notes))

        conn.commit()
        conn.close()

        return redirect('/')
    cur.execute('SELECT * FROM languages')
    languages = cur.fetchall()
    conn.close()
    return render_template("add_log.html", languages=languages)

@app.route("/delete-log/<int:log_id>", methods=["GET", "POST"])
def delete_log(log_id):
    conn = sqlite3.connect('logs.db')
    cur = conn.cursor()

    cur.execute("DELETE FROM logs WHERE id = ?", (log_id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/lang/<int:lang_id>")
def lang(lang_id):
    conn = sqlite3.connect('logs.db')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    cur.execute("SELECT * FROM languages WHERE id = ?", (lang_id,))
    language = cur.fetchone()

    #list logs

    cur.execute("SELECT * FROM logs WHERE lang_id = ?", (lang_id,))
    logs = cur.fetchall()

    conn.close()
    return render_template("lang.html", language=language, logs=logs)


if __name__ == '__main__':
    app.run(debug=True)