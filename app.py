import os
import psycopg2
from contextlib import closing
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
 
app = Flask(__name__)
csrf = CSRFProtect(app)
 
# SECRET_KEY must be set in Vercel environment variables — no fallback for security
app.secret_key = os.environ['SECRET_KEY']
app.debug = os.environ.get('FLASK_DEBUG', '0') == '1'
 
# ---------- Database helpers ----------
# DATABASE_URL is set in Vercel environment variables (your Neon connection string)
DATABASE_URL = os.environ['DATABASE_URL']
 
def get_db():
    """Return a new PostgreSQL database connection."""
    conn = psycopg2.connect(DATABASE_URL)
    return conn
 
def init_db():
    """Create tables if they don't exist."""
    with closing(get_db()) as conn:
        with conn.cursor() as c:
            c.execute('''CREATE TABLE IF NOT EXISTS reservations (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                guests TEXT NOT NULL,
                created_at TEXT NOT NULL
            )''')
            c.execute('''CREATE TABLE IF NOT EXISTS comments (
                id SERIAL PRIMARY KEY,
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
    name    = request.form.get('name', '').strip()[:100]
    phone   = request.form.get('phone', '').strip()[:30]
    date    = request.form.get('date', '')[:20]
    time    = request.form.get('time', '')[:10]
    guests  = request.form.get('guests', '')[:10]
 
    if not all([name, phone, date, time]):
        flash('Please fill in all reservation fields.', 'error')
        return redirect(url_for('home', _anchor='reserve'))
 
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with closing(get_db()) as conn:
            with conn.cursor() as c:
                c.execute(
                    'INSERT INTO reservations (name, phone, date, time, guests, created_at) VALUES (%s, %s, %s, %s, %s, %s)',
                    (name, phone, date, time, guests, now)
                )
            conn.commit()
        flash('Your table has been reserved! We look forward to serving you.', 'success')
    except Exception as e:
        app.logger.error(f'Reservation failed: {e}')
        flash('Something went wrong. Please try again later.', 'error')
 
    return redirect(url_for('home', _anchor='reserve'))
 
@app.route('/comment', methods=['POST'])
def comment():
    name    = request.form.get('name', '').strip()[:100]
    message = request.form.get('message', '').strip()[:1000]
 
    if not name or not message:
        flash('Please provide both your name and a comment.', 'error')
        return redirect(url_for('home', _anchor='reserve'))
 
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with closing(get_db()) as conn:
            with conn.cursor() as c:
                c.execute(
                    'INSERT INTO comments (name, message, created_at) VALUES (%s, %s, %s)',
                    (name, message, now)
                )
            conn.commit()
        flash('Thank you for your comment! We appreciate your feedback.', 'success')
    except Exception as e:
        app.logger.error(f'Comment failed: {e}')
        flash('Oops! Could not save your comment. Please try again.', 'error')
 
    return redirect(url_for('home', _anchor='reserve'))
 