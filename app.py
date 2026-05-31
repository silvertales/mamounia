import os
import sqlite3
from contextlib import closing
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
csrf = CSRFProtect(app) 

# Load configuration from environment variables
app.secret_key = os.environ.get('SECRET_KEY', 'ladecima11')
app.debug = os.environ.get('FLASK_DEBUG', '0') == '1'

# ---------- Database helpers ----------
DATABASE = 'restaurant.db'

def get_db():
    """Return a new database connection. Use with closing()."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  
    return conn

def init_db():
    """Create tables if they don't exist."""
    with closing(get_db()) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            guests TEXT NOT NULL,
            created_at TEXT NOT NULL
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )''')
        conn.commit()

init_db()

# ---------- Routes ----------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/reserve', methods=['POST'])
def reserve():
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    date = request.form.get('date', '')
    time = request.form.get('time', '')
    guests = request.form.get('guests', '')

    if not all([name, phone, date, time]):
        flash('Please fill in all reservation fields.', 'error')
        return redirect(url_for('home', _anchor='reserve'))

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with closing(get_db()) as conn:
            conn.execute(
                'INSERT INTO reservations (name, phone, date, time, guests, created_at) VALUES (?, ?, ?, ?, ?, ?)',
                (name, phone, date, time, guests, now)
            )
            conn.commit()
        flash('Your table has been reserved! We look forward to serving you.', 'success')
    except sqlite3.Error as e:
        app.logger.error(f'Reservation failed: {e}')
        flash('Something went wrong. Please try again later.', 'error')

    return redirect(url_for('home', _anchor='reserve'))

@app.route('/comment', methods=['POST'])
def comment():
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not message:
        flash('Please provide both your name and a comment.', 'error')
        return redirect(url_for('home', _anchor='reserve'))

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with closing(get_db()) as conn:
            conn.execute(
                'INSERT INTO comments (name, message, created_at) VALUES (?, ?, ?)',
                (name, message, now)
            )
            conn.commit()
        flash('Thank you for your comment! We appreciate your feedback.', 'success')
    except sqlite3.Error as e:
        app.logger.error(f'Comment failed: {e}')
        flash('Oops! Could not save your comment. Please try again.', 'error')

    return redirect(url_for('home', _anchor='reserve'))

# Future improvement: Add CSRF protection with Flask-WTF

if __name__ == '__main__':
    app.run(debug=app.debug, host='0.0.0.0')