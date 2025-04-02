# from flask import Flask, render_template, request, redirect, url_for
# from database import save_user, login_user

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template("GettingStarted.html")

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         confirm_password = request.form['confirm_password']
#         skills = request.form.getlist('skills')  # Get selected skills as a list

#         if password != confirm_password:
#             return "Passwords do not match!"

#         # Save user to database
#         save_user(username, email, password, skills)
#         return redirect('/login')

#     return render_template('register.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         # Call login_user from the database to verify the login details
#         result = login_user(email, password)

#         if result['status'] == 'success':
#             # Redirect to profile page with user data
#             return render_template('profile.html', 
#                                    name=result['username'], 
#                                    skills=result['skills'],  # Passed the skills as a list
#                                    rating=result['rating'])
#         else:
#             return result['message']  # Display error message if login fails

#     return render_template('login.html')  # Show login form if GET request

# if __name__ == '__main__':
#     app.run(debug=True)
