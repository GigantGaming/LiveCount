from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

DB_NAME = "views.db"

# --------------------------
# Create DB automatically
# --------------------------
def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS page_views (id INTEGER PRIMARY KEY, views INTEGER)")
        cur.execute("INSERT INTO page_views (id, views) VALUES (1, 0)")
        conn.commit()
        conn.close()

# --------------------------
# Get current views
# --------------------------
def get_views():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT views FROM page_views WHERE id=1")
    result = cur.fetchone()
    conn.close()
    return result[0]

# --------------------------
# Increase view count
# --------------------------
def add_view():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE page_views SET views = views + 1 WHERE id=1")
    conn.commit()
    conn.close()

# --------------------------
# PAGE ROUTE
# --------------------------
@app.route("/")
def home():
    add_view()
    views = get_views()
    return render_template("index.html", views=views)

# --------------------------
if __name__ == "__main__":
    init_db()
