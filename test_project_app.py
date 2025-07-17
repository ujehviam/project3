import unittest
import tempfile
import os
import sqlite3
from app import ProjectApp  # Ensure your main script is named project_app.py
from flask import Flask

class ProjectAppTestCase(unittest.TestCase):
    def setUp(self):
        # Setup a test instance of the app
        self.app_instance = ProjectApp()
        self.app = self.app_instance.app
        self.app.config['TESTING'] = True
        self.app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
        self.db_fd, self.temp_db = tempfile.mkstemp()
        self.app_instance.DATABASE = self.temp_db

        # Create test client
        self.client = self.app.test_client()

        # Re-create table in test DB
        with self.app.app_context():
            self.app_instance.create_table()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.temp_db)

    def test_signup_page_loads(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign Up', response.data)  # Adjust based on your HTML content

    def test_register_user(self):
        response = self.client.post('/register', data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'password123',
            'phone_number': '1234567890'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data.lower())  # Adjust if needed

        # Confirm user is in the DB
        conn = sqlite3.connect(self.app_instance.DATABASE)
        user = conn.execute("SELECT * FROM project3_DB WHERE Email = ?", ('john@example.com',)).fetchone()
        conn.close()
        self.assertIsNotNone(user)

    def test_duplicate_email_registration(self):
        # First registration
        self.client.post('/register', data={
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane@example.com',
            'password': 'password123',
            'phone_number': '9876543210'
        })

        # Duplicate registration
        response = self.client.post('/register', data={
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@example.com',
            'password': 'anotherpassword',
            'phone_number': '5555555555'
        }, follow_redirects=True)

        self.assertIn(b'Email already exists', response.data)

    def test_successful_login(self):
        # Register first
        self.client.post('/register', data={
            'first_name': 'Alice',
            'last_name': 'Wonder',
            'email': 'alice@example.com',
            'password': 'wonder123',
            'phone_number': '0001112222'
        })

        # Login
        response = self.client.post('/', data={
            'email': 'alice@example.com',
            'password': 'wonder123'
        }, follow_redirects=True)

        self.assertIn(b'Login successful', response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post('/', data={
            'email': 'nonexistent@example.com',
            'password': 'wrongpass'
        }, follow_redirects=True)

        self.assertIn(b'Invalid credentials', response.data)


if __name__ == '__main__':
    unittest.main()