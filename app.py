import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "your_secret_key"

DATABASE = "Project1.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Create the table if it doesn't exist
def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS project3_DB (
            First_Name TEXT NOT NULL,
            Last_Name TEXT NOT NULL,
            Email TEXT PRIMARY KEY NOT NULL,
            Password TEXT NOT NULL,
            Phone_Number TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_table()

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM project3_DB WHERE Email = ? AND Password = ?",
            (email, password)
        ).fetchone()
        conn.close()
        if user:
            return 'Login successful!'
        else:
            flash('Invalid credentials. Please try again.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

# Signup page route
@app.route('/signup')
def signup():
    return render_template('signup.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        phone_number = request.form["phone_number"]

        try:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO project3_DB (First_Name, Last_Name, Email, Password, Phone_Number) VALUES (?, ?, ?, ?, ?)",
                (first_name, last_name, email, password, phone_number)
            )
            conn.commit()
            conn.close()
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Error: Email already exists.", "error")
            return redirect(url_for("signup"))

    return render_template("signup.html")

if __name__ == '__main__':
    app.run(debug=True)