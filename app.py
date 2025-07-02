import sqlite3
from flask import Flask, render_template, request, redirect, url_for

conn = sqlite3.connect("Project1.db")#name of the database
cursor = conn.cursor()
conn.execute('''CREATE TABLE IF NOT EXISTS project3_DB (
First_Name TEXT NOT NULL,
Last_Name TEXT NOT NULL,
Email TEXT PRIMARY KEY NOT NULL,
Password TEXT NOT NULL,
Phone_Number TEXT
)
''')
conn.commit()
print('''
    ***********************************************

    you have succcessfully created a database table.

    ***********************************************
    ''')

app = Flask(__name__)

# Home route (login page)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Here, you can add real authentication logic
        if email == 'test@example.com' and password == 'password':
            return 'Login successful!'
        else:
            return 'Invalid credentials. Please try again.'
    return render_template('login.html')

# Signup page route
@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)