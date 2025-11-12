from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Database path
DB_PATH = os.path.join(os.getcwd(), "database.db")

# Function to create table if not exists
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS ip_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            user_agent TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Call init_db when app starts
init_db()

@app.route("/")
def home():
    return "Welcome to IP Logger Flask App!"

@app.route("/log-ip", methods=["GET", "POST"])
def log_ip():
    # Get client IP (Render proxy ke liye X-Forwarded-For check)
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent", "Unknown")

    # Insert IP into SQLite
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO ip_logs (ip_address, user_agent) VALUES (?, ?)", (ip, user_agent))
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "ip": ip,
        "message": "IP stored successfully!"
    })

@app.route("/show-ips")
def show_ips():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM ip_logs ORDER BY id DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()

    return jsonify(rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
