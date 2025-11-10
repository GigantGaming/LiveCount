from flask import Flask, render_template, request
import sqlite3
import os
import traceback
import sys

app = Flask(__name__)

# Use absolute path inside project so it's consistent on Render
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_NAME = os.path.join(BASE_DIR, "views.db")

def init_db():
    """Create DB and the page_views table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS page_views (
                id INTEGER PRIMARY KEY,
                views INTEGER
            )
        """)
        # ensure row with id=1 exists
        cur.execute("SELECT COUNT(*) FROM page_views WHERE id = 1")
        r = cur.fetchone()
        if not r or r[0] == 0:
            cur.execute("INSERT INTO page_views (id, views) VALUES (1, 0)")
        conn.commit()
    except Exception as e:
        # Print full traceback to stdout so Render logs will show it
        print("ERROR initializing DB:", file=sys.stderr)
        traceback.print_exc()
    finally:
        try:
            conn.close()
        except:
            pass

# Run DB init at import time so Gunicorn workers get DB ready
init_db()

def get_views():
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT views FROM page_views WHERE id=1")
        result = cur.fetchone()
        return result[0] if result else 0
    finally:
        try:
            conn.close()
        except:
            pass

def add_view():
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("UPDATE page_views SET views = views + 1 WHERE id=1")
        conn.commit()
    finally:
        try:
            conn.close()
        except:
            pass

@app.route("/")
def home():
    try:
        add_view()
        views = get_views()
        return render_template("index.html", views=views)
    except Exception as e:
        # Log and return a simple fallback page so you can see the site up
        print("ERROR in / route:", file=sys.stderr)
        traceback.print_exc()
        # show helpful info for debugging (non-sensitive)
        return (
            "<h3>There was an internal error</h3>"
            "<p>Check Render logs for full traceback.</p>"
            "<pre>{}</pre>".format(str(e)),
            500
        )

# Optional health-check route so you can test quickly
@app.route("/_health")
def health():
    return "OK"

if __name__ == "__main__":
    # local dev run
    app.run(host="0.0.0.0", port=5000, debug=True)    cur = conn.cursor()
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
