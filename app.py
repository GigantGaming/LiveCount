from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Database file path
DB_PATH = os.path.join(os.getcwd(), "database.db")

# Create table if not exists
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            comment TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()  # Initialize database

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        comment = request.form.get("comment")

        # Validation (avoid blank)
        if name.strip() and comment.strip():
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("INSERT INTO comments (name, comment) VALUES (?, ?)", (name, comment))
            conn.commit()
            conn.close()

        return redirect("/")  # refresh page

    # Show all comments
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, comment, created_at FROM comments ORDER BY id DESC")
    all_comments = c.fetchall()
    conn.close()

    return render_template("index.html", comments=all_comments)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
