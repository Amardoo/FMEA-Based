# Main Flask app for blood risk evaluation system
# Handles login, donor/request sections, FMEA risk assessment, and dashboard
# Run with: python app.py
# Access at: http://127.0.0.1:5000/

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure key

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS donors 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, blood_type TEXT, medical_history TEXT, last_donation TEXT, risk_log TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS requests 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, hospital TEXT, blood_type TEXT, quantity INTEGER, risk_assessment TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS fmea 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, process_step TEXT, failure_mode TEXT, cause TEXT, effect TEXT, severity INTEGER, occurrence INTEGER, detection INTEGER, rpn INTEGER)''')
    # Add default admin user
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('admin', hashlib.md5('admin'.encode()).hexdigest()))
    conn.commit()
    conn.close()

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.process_step['username']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM donors")
    donors = c.fetchall()
    c.execute("SELECT * FROM requests")
    requests = c.fetchall()
    c.execute("SELECT * FROM fmea WHERE rpn > 60")
    high_risks = c.fetchall()
    conn.close()
    return render_template('dashboard.html', donors=donors, requests=requests, high_risks=high_risks)

# Donor section
@app.route('/donor', methods=['GET', 'POST'])
def donor():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        blood_type = request.form['blood_type']
        medical_history = request.form['medical_history']
        last_donation = request.form['last_donation']
        # Simple risk check (example: anemia if last donation < 2 months)
        risk_log = "High risk (anemia)" if last_donation and (2025 - int(last_donation.split('-')[0])) < 2 else "No risk"
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO donors (name, blood_type, medical_history, last_donation, risk_log) VALUES (?, ?, ?, ?, ?)",
                  (name, blood_type, medical_history, last_donation, risk_log))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('add_failure.html', section='donor')

# Request section
@app.route('/request', methods=['GET', 'POST'])
def request():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        hospital = request.form['hospital']
        blood_type = request.form['blood_type']
        quantity = int(request.form['quantity'])
        # Simple risk assessment (example: high risk if quantity > 5 or incompatible blood type)
        risk_assessment = "High risk (quantity/compatibility)" if quantity > 5 else "Low risk"
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO requests (hospital, blood_type, quantity, risk_assessment) VALUES (?, ?, ?, ?)",
                  (hospital, blood_type, quantity, risk_assessment))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('add_failure.html', section='request')

# FMEA route
@app.route('/fmea', methods=['GET', 'POST'])
def fmea():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        process_step = request.form['process_step']
        failure_mode = request.form['failure_mode']
        cause = request.form['cause']
        effect = request.form['effect']
        severity = int(request.form['severity'])
        occurrence = int(request.form['occurrence'])
        detection = int(request.form['detection'])
        rpn = severity * occurrence * detection
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO fmea (process_step, failure_mode, cause, effect, severity, occurrence, detection, rpn) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (process_step, failure_mode, cause, effect, severity, occurrence, detection, rpn))
        conn.commit()
        conn.close()
        if rpn > 60:
            # Simple alert (can be extended to email/notification)
            print(f"High Risk Alert: {failure_mode} with RPN {rpn}")
    return render_template('add_failure.html', section='fmea')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
