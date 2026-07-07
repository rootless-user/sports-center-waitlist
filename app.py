import sqlite3
from pathlib import Path
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "waitlist.db"

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()

    with open(BASE_DIR / "schema.sql", encoding="utf-8") as file:
        connection.executescript(file.read())

    connection.commit()
    connection.close()


@app.route("/")
def index():
    return render_template("add_client.html")


@app.route("/add-client", methods=["GET", "POST"])
def add_client():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        social_contact = request.form["social_contact"]
        preferred_days = request.form["preferred_days"]
        preferred_time = request.form["preferred_time"]
        trainer_preference = request.form["trainer_preference"]
        comment = request.form["comment"]

        connection = get_db_connection()

        current_time = get_current_time()

        connection.execute(
            """
            INSERT INTO clients (
                name,
                phone,
                social_contact,
                preferred_days,
                preferred_time,
                trainer_preference,
                comment,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                phone,
                social_contact,
                preferred_days,
                preferred_time,
                trainer_preference,
                comment,
                current_time,
                current_time,
            ),
        )

        connection.commit()
        connection.close()

        return redirect(url_for("clients"))

    return render_template("add_client.html")


@app.route("/clients")
def clients():
    status_filter = request.args.get("status", "")

    connection = get_db_connection()

    if status_filter:
        clients_list = connection.execute(
            "SELECT * FROM clients WHERE status = ? ORDER BY created_at DESC",
            (status_filter,),
        ).fetchall()
    else:
        clients_list = connection.execute(
            "SELECT * FROM clients ORDER BY created_at DESC"
        ).fetchall()

    connection.close()

    return render_template(
        "clients.html",
        clients=clients_list,
        status_filter=status_filter,
    )


@app.route("/update-status/<int:client_id>", methods=["POST"])
def update_status(client_id):
    new_status = request.form["status"]
    current_time = get_current_time()

    connection = get_db_connection()

    connection.execute(
        """
        UPDATE clients
        SET status = ?, updated_at = ?
        WHERE id = ?
        """,
        (new_status, current_time, client_id),
    )

    connection.commit()
    connection.close()

    return redirect(url_for("clients"))

@app.route("/search")
def search_clients():
    day = request.args.get("day", "").strip()
    preferred_time = request.args.get("time", "").strip()
    trainer = request.args.get("trainer", "").strip()

    query = "SELECT * FROM clients WHERE status = ?"
    params = ["Ожидает"]

    if day:
        query += " AND preferred_days LIKE ?"
        params.append(f"%{day}%")

    if preferred_time:
        query += " AND preferred_time LIKE ?"
        params.append(f"%{preferred_time}%")

    if trainer:
        query += " AND trainer_preference LIKE ?"
        params.append(f"%{trainer}%")

    query += " ORDER BY created_at ASC"

    connection = get_db_connection()
    clients_list = connection.execute(query, params).fetchall()
    connection.close()

    return render_template(
        "search_clients.html",
        clients=clients_list,
        day=day,
        preferred_time=preferred_time,
        trainer=trainer,
    )

@app.route("/delete-client/<int:client_id>", methods=["POST"])
def delete_client(client_id):
    connection = get_db_connection()

    connection.execute(
        "DELETE FROM clients WHERE id = ?",
        (client_id,),
    )

    connection.commit()
    connection.close()

    return redirect(url_for("clients"))


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=False)