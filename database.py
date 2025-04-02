# import sqlite3
# import pandas as pd  # For exporting the database to Excel

# DB_NAME = 'users.db'
# EXCEL_EXPORT_FILE = r'D:\College Projects\ConnectEd\users_data.xlsx'  # The Excel file name

# # Initialize the database
# def init_db():
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()

#     # Create users table
#     cursor.execute('''CREATE TABLE IF NOT EXISTS users (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         username TEXT NOT NULL,
#                         email TEXT NOT NULL UNIQUE,
#                         password TEXT NOT NULL,
#                         rating REAL DEFAULT 400
#                     )''')

#     # Create user_skills table to store multiple skills for a user
#     cursor.execute('''CREATE TABLE IF NOT EXISTS user_skills (
#                         user_id INTEGER,
#                         skill TEXT,
#                         FOREIGN KEY (user_id) REFERENCES users (id)
#                     )''')
    
#     conn.commit()
#     conn.close()

# # Initialize the database (This should be done when the app starts)
# init_db()

# # Save a new user
# def save_user(username, email, password, skills=None, rating=400):
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()

#     if skills is None:
#         skills = []

#     cursor.execute('INSERT INTO users (username, email, password, rating) VALUES (?, ?, ?, ?)', 
#                    (username, email, password, rating))

#     # Get the user ID of the newly inserted user
#     user_id = cursor.lastrowid

#     # Insert the skills into the user_skills table
#     for skill in skills:  # Corrected variable name here
#         cursor.execute('INSERT INTO user_skills (user_id, skill) VALUES (?, ?)', (user_id, skill))
    
#     conn.commit()
#     conn.close()

# # Validate login credentials
# def login_user(email, password):
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
    
#     cursor.execute('SELECT id, password, username, rating FROM users WHERE email = ?', (email,))
#     result = cursor.fetchone()

#     if result:
#         user_id, stored_password, username, rating = result
#         if stored_password == password:
#             # Fetch skills for the user
#             cursor.execute('SELECT skill FROM user_skills WHERE user_id = ?', (user_id,))
#             skills = [row[0] for row in cursor.fetchall()]
            
#             # Return user data for the profile page
#             return {'status': 'success', 'username': username, 'skills': skills, 'rating': rating}
#         else:
#             return {'status': 'error', 'message': 'Password is incorrect!'}
#     else:
#         return {'status': 'error', 'message': 'Email not found. Please create a new account.'}

# # Export database to Excel
# def export_to_excel():
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()

#     try:
#         cursor.execute("SELECT * FROM users")
#     except sqlite3.OperationalError:
#         return  # No table to export

#     df_users = pd.read_sql_query("SELECT * FROM users", conn)
#     df_skills = pd.read_sql_query("SELECT u.username, us.skill FROM users u JOIN user_skills us ON u.id = us.user_id", conn)
    
#     # Merge users with their skills
#     df = pd.merge(df_users, df_skills, left_on="id", right_on="user_id", how="left").drop(columns=["user_id"])
    
#     # Save to Excel
#     df.to_excel(EXCEL_EXPORT_FILE, index=False)
#     conn.close()
