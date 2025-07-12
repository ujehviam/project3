import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

class ProjectApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = "your_secret_key"

        self.DATABASE = "Project1.db"
        self.UPLOAD_FOLDER = 'static/uploads'
        os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)
        self.app.config['UPLOAD_FOLDER'] = self.UPLOAD_FOLDER

        self.create_table()
        self.setup_routes()

    def get_db_connection(self):
        conn = sqlite3.connect(self.DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    def create_table(self):
        conn = self.get_db_connection()
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

    def setup_routes(self):
        @self.app.route('/', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                email = request.form.get('email')
                password = request.form.get('password')
                conn = self.get_db_connection()
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

        @self.app.route('/signup')
        def signup():
            return render_template('signup.html')

        @self.app.route('/register', methods=['GET', 'POST'])
        def register():
            if request.method == "POST":
                first_name = request.form["first_name"]
                last_name = request.form["last_name"]
                email = request.form["email"]
                password = request.form["password"]
                phone_number = request.form["phone_number"]
                profile_picture = request.files.get("profile_picture")

                if profile_picture:
                    filename = secure_filename(profile_picture.filename)
                    picture_path = os.path.join(self.app.config['UPLOAD_FOLDER'], filename)
                    profile_picture.save(picture_path)
                else:
                    filename = None

                try:
                    conn = self.get_db_connection()
                    conn.execute(
                        "INSERT INTO project3_DB (First_Name, Last_Name, Email, Password, Phone_Number) VALUES (?, ?, ?, ?, ?)",
                        (first_name, last_name, email, password, phone_number)
                    )
                    conn.commit()
                    conn.close()
                    return render_template("success.html", filename=filename)
                except sqlite3.IntegrityError:
                    flash("Error: Email already exists.", "error")
                    return redirect(url_for("signup"))

            return render_template("signup.html")

    def run(self, **kwargs):
        self.app.run(**kwargs)

if __name__ == '__main__':
    app_instance = ProjectApp()
    app_instance.run(debug=True)