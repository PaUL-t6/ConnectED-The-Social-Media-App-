# import sqlite3
# from flask import Flask, render_template, request, redirect
# import pandas as pd
# import os

# DB_NAME = 'users.db'
# EXCEL_EXPORT_FILE = 'users_data.xlsx'

# app = Flask(__name__)

# # Initialize the database
# def init_db():
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute('''CREATE TABLE IF NOT EXISTS users (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         username TEXT NOT NULL,
#                         email TEXT NOT NULL UNIQUE,
#                         password TEXT NOT NULL,
#                         skill TEXT DEFAULT 'None',
#                         rating REAL DEFAULT 0
#                     )''')
#     conn.commit()
#     conn.close()

# # Check if the table exists
# def check_table_exists():
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
#     table_exists = cursor.fetchone()
#     conn.close()

#     if table_exists:
#         print("Table 'users' exists.")
#     else:
#         print("Table 'users' does NOT exist.")

# # Routes
# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/register', methods=['POST'])
# def register():
#     username = request.form['username']
#     email = request.form['email']
#     password = request.form['password']
    
#     try:
#         save_user(username, email, password)
#         export_to_excel()
#         return "Registration successful! You can now log in."
#     except sqlite3.IntegrityError:
#         return "Email already exists! Please use a different email."

# @app.route('/login', methods=['POST'])
# def login():
#     email = request.form['email']
#     password = request.form['password']
#     result = login_user(email, password)

#     if result['status'] == 'success':
#         return render_template('profile.html', 
#                                name=result['username'], 
#                                skill=result['skill'], 
#                                rating=result['rating'])
#     else:
#         return result['message']

# # Run the app
# if __name__ == '__main__':
#     # Delete database file if exists (run once)
#     if os.path.exists(DB_NAME):
#         os.remove(DB_NAME)
#         print(f"Database file '{DB_NAME}' deleted. Reinitializing...")

#     init_db()  # Initialize the database
#     check_table_exists()  # Check if the table exists
#     app.run(debug=True)
