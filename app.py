from flask import Flask, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
import sqlite3

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

def init_user_db():
    with sqlite3.connect('users.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

def init_booking_db():
    with sqlite3.connect('booking_detaiils.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                phone TEXT,
                age INTEGER,
                gender TEXT,
                departure TEXT,
                return_date TEXT,
                destination TEXT,
                package TEXT
            )
        ''')

@app.route('/')
def home_page():
    return send_from_directory('.', 'index.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')
    try:
        with sqlite3.connect('users.db') as conn:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        return send_from_directory('.', 'index.html')
    except sqlite3.IntegrityError:
        return "Username already exists"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    with sqlite3.connect('users.db') as conn:
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
        if user:
            return send_from_directory('.', 'home.html')
        return "Invalid credentials"

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    name = data.get('myname1')
    email = data.get('myemail')
    phone = data.get('myphone')
    age = data.get('myage')
    gender = data.get('mygender')
    departure = data.get('departuredate')
    return_date = data.get('returndate')
    destinations = request.form.getlist('td')
    destination_str = ', '.join(destinations)
    package = data.get('locations')

    with sqlite3.connect('booking_detaiils.db') as conn:
        conn.execute('''
            INSERT INTO registrations 
            (name, email, phone, age, gender, departure, return_date, destination, package)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, email, phone, age, gender, departure, return_date, destination_str, package))
        conn.commit()

    return "Registration successful"

@app.route('/delete', methods=['POST'])
def delete_user():
    name_to_delete = request.form.get('name')
    with sqlite3.connect('booking_detaiils.db') as conn:
        conn.execute("DELETE FROM registrations WHERE name = ?", (name_to_delete,))
        conn.commit()
    return f"User '{name_to_delete}' deleted successfully."

if __name__ == '__main__':
    init_user_db()
    init_booking_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
