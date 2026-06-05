from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'ladecima11'   # needed for flash messages

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/reserve', methods=['POST'])
def reserve():
    flash('Your table has been reserved! We look forward to serving you.', 'success')
    return redirect(url_for('home', _anchor='reserve'))

@app.route('/comment', methods=['POST'])
def comment():
    flash('Thank you for your comment! We appreciate your feedback.', 'success')
    return redirect(url_for('home', _anchor='reserve'))