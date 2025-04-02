from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flashing messages

DB_NAME = 'connected.db'

# Initialize the database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create user_info table
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_info (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    achievements TEXT,
                    social_links TEXT,
                    rating INTEGER
                )''')

    # Create user_skills table
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_skills (
                    user_skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    skill TEXT NOT NULL,
                    rating INTEGER,
                    FOREIGN KEY (user_id) REFERENCES user_info (user_id)
                )''')

    # Create club_info table
    cursor.execute('''CREATE TABLE IF NOT EXISTS club_info (
                    club_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    club_name TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    announcements TEXT
                )''')

    # Create hackathon_info table
    cursor.execute('''CREATE TABLE IF NOT EXISTS hackathon_info (
                    hackathon_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL
                )''')

    # Create hackathon_skills table
    cursor.execute('''CREATE TABLE IF NOT EXISTS hackathon_skills (
                    hackathon_skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hackathon_id INTEGER,
                    skill TEXT NOT NULL,
                    FOREIGN KEY (hackathon_id) REFERENCES hackathon_info (hackathon_id)
                )''')

    # Create project_info table
    cursor.execute('''CREATE TABLE IF NOT EXISTS project_info (
                    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    project_head INTEGER REFERENCES user_info (user_id)
                )''')

    # Create teams table
    cursor.execute('''CREATE TABLE IF NOT EXISTS teams (
                    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    project_id INTEGER,
                    hackathon_id INTEGER,
                    rankings TEXT,
                    FOREIGN KEY (project_id) REFERENCES project_info (project_id),
                    FOREIGN KEY (hackathon_id) REFERENCES hackathon_info (hackathon_id)
                )''')

    # Create team_members table
    cursor.execute('''CREATE TABLE IF NOT EXISTS team_members (
                    team_member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    team_id INTEGER,
                    user_id INTEGER,
                    FOREIGN KEY (team_id) REFERENCES teams (team_id),
                    FOREIGN KEY (user_id) REFERENCES user_info (user_id)
                )''')

    # Create user_hackathons table
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_hackathons (
                    user_id INTEGER,
                    hackathon_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES user_info (user_id),
                    FOREIGN KEY (hackathon_id) REFERENCES hackathon_info (hackathon_id)
                )''')

    # Create user_projects table
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_projects (
                    user_id INTEGER,
                    project_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES user_info (user_id),
                    FOREIGN KEY (project_id) REFERENCES project_info (project_id)
                )''')

    # Create hackathon_team_rankings table
    cursor.execute('''CREATE TABLE IF NOT EXISTS hackathon_team_rankings (
                    hackathon_id INTEGER,
                    team_id INTEGER,
                    rank INTEGER,
                    FOREIGN KEY (hackathon_id) REFERENCES hackathon_info (hackathon_id),
                    FOREIGN KEY (team_id) REFERENCES teams (team_id)
                )''')

    # Create hackathon_team_leaders table
    cursor.execute('''CREATE TABLE IF NOT EXISTS hackathon_team_leaders (
                    hackathon_id INTEGER,
                    team_id INTEGER,
                    team_leader_id INTEGER,
                    FOREIGN KEY (hackathon_id) REFERENCES hackathon_info (hackathon_id),
                    FOREIGN KEY (team_id) REFERENCES teams (team_id),
                    FOREIGN KEY (team_leader_id) REFERENCES user_info (user_id)
                )''')
    
    #Create Request Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS requests (
                        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        hackathon_id INTEGER,
                        team_id INTEGER,
                        team_leader_id INTEGER,
                        user_id INTEGER,
                        FOREIGN KEY (hackathon_id) REFERENCES hackathon_info (hackathon_id),
                        FOREIGN KEY (team_id) REFERENCES teams (team_id),
                        FOREIGN KEY (team_leader_id) REFERENCES user_info (user_id),
                        FOREIGN KEY (user_id) REFERENCES user_info (user_id)
                    )  ''')

    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Generate next available user_id
def get_next_user_id():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT MAX(user_id) FROM user_info')
    last_id = cursor.fetchone()[0]

    conn.close()
    return 1 if last_id is None else last_id + 1  # Start from 1

# Save a new user
def save_user(username, email, password, skills=None, rating=400):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Insert into user_info table
    cursor.execute('INSERT INTO user_info (username, email, password, rating) VALUES (?, ?, ?, ?)', 
                   (username, email, password, rating))
    user_id = cursor.lastrowid  # Get the auto-generated user_id

    # Insert skills into user_skills table
    if skills:
        for skill in skills:
            cursor.execute('INSERT INTO user_skills (user_id, skill, rating) VALUES (?, ?, ?)', 
                           (user_id, skill, rating))

    conn.commit()
    conn.close()

# Validate user login
def login_user(email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Fetch user details
    cursor.execute('SELECT user_id, username, password, rating FROM user_info WHERE email = ?', (email,))
    result = cursor.fetchone()

    if result:
        user_id, username, stored_password, rating = result
        if stored_password == password:
            # Fetch skills from user_skills table
            cursor.execute('SELECT skill, rating FROM user_skills WHERE user_id = ?', (user_id,))
            skills = cursor.fetchall()
            conn.close()
            return {'status': 'success', 'user_id': user_id, 'username': username, 'skills': skills, 'rating': rating}
        else:
            conn.close()
            return {'status': 'error', 'message': 'Incorrect password!'}
    else:
        conn.close()
        return {'status': 'error', 'message': 'Email not found. Please create an account.'}

# Save a new club
def save_club(club_name, email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('INSERT INTO club_info (club_name, email, password) VALUES (?, ?, ?)', 
                   (club_name, email, password))

    conn.commit()
    conn.close()

# Validate club login
def login_club(club_name, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT club_id, club_name, password FROM club_info WHERE club_name = ?', (club_name,))
    result = cursor.fetchone()

    conn.close()

    if result:
        club_id, club_name, stored_password = result
        if stored_password == password:
            return {'status': 'success', 'club_id': club_id, 'club_name': club_name}
        else:
            return {'status': 'error', 'message': 'Incorrect password!'}
    else:
        return {'status': 'error', 'message': 'Club not found. Please register.'}

# Route for getting started page
@app.route('/')
def getting_started():
    return render_template("GettingStarted.html")

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        skills = request.form['skills']  # This is a comma-separated string

        # Split the skills string into a list of individual skills
        skills_list = skills.split(',')

        # Save the user and their skills to the database
        save_user(username, email, password, skills_list)

        return redirect(url_for('login'))  # Redirect to login page after registration

    # If it's a GET request, render the registration page
    return render_template('register.html')

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        result = login_user(email, password)

        if result['status'] == 'success':
            return redirect(url_for('home', username=result['username']))  # Redirecting to /home/{username}
        else:
            flash(result['message'])
            return redirect(url_for('login'))

    return render_template('login.html')

# Home route (after login)
@app.route('/home/<string:username>', methods=['GET', 'POST'])
def home(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if request.method == 'POST':
        # Fetch applicant_username and team_id from query string
        applicant_username = request.args.get('applicant_username')
        team_id = request.args.get('team_id')

        if not applicant_username or not team_id:
            flash('Invalid request: Missing applicant_username or team_id', 'error')
            return redirect(url_for('home', username=username))

        # Fetch user_id for the applicant_username
        cursor.execute('SELECT user_id FROM user_info WHERE username = ?', (applicant_username,))
        user_result = cursor.fetchone()

        if not user_result:
            flash('Applicant not found', 'error')
            return redirect(url_for('home', username=username))

        user_id = user_result[0]  # Access by index

        try:
            # Add user_id to team_members table
            cursor.execute('''
                INSERT INTO team_members (team_id, user_id)
                VALUES (?, ?)
            ''', (team_id, user_id))
            print("Inserted into team_members table")  # Debugging line

            # Delete the request from the requests table
            cursor.execute('''
                DELETE FROM requests
                WHERE user_id = ? AND team_id = ?
            ''', (user_id, team_id))
            print("Deleted from requests table")  # Debugging line

            conn.commit()
            flash('User added to team successfully!', 'success')
        except Exception as e:
            conn.rollback()
            print(f"Error: {str(e)}")  # Debugging line
            flash(f'An error occurred: {str(e)}', 'error')
        finally:
            conn.close()

        return redirect(url_for('home', username=username))

    else:
        # Fetch user details
        cursor.execute('SELECT user_id, rating FROM user_info WHERE username = ?', (username,))
        user_result = cursor.fetchone()

        if not user_result:
            flash("User not found!")
            return redirect(url_for('login'))

        user_id, rating = user_result

        # Fetch clubs and their announcements
        cursor.execute('SELECT club_id, announcements FROM club_info')
        clubs = cursor.fetchall()

        # Fetch hackathon titles
        cursor.execute('SELECT name FROM hackathon_info')
        hackathons = cursor.fetchall()

        # Fetch project titles
        cursor.execute('SELECT name FROM project_info')
        projects = cursor.fetchall()

        # Fetch requests where the team leader is the logged-in user
        cursor.execute('''
            SELECT r.user_id, r.team_id, r.hackathon_id, u.username AS applicant_username, h.name AS hackathon_name, t.name AS team_name
            FROM requests r
            JOIN user_info u ON r.user_id = u.user_id
            JOIN hackathon_info h ON r.hackathon_id = h.hackathon_id
            JOIN teams t ON r.team_id = t.team_id
            JOIN hackathon_team_leaders htl ON t.team_id = htl.team_id
            JOIN user_info ul ON htl.team_leader_id = ul.user_id
            WHERE ul.username = ?
        ''', (username,))
        requests = cursor.fetchall()

        conn.close()

        # Convert clubs to a list of dictionaries for easier access in the template
        clubs_list = [{'club_id': club[0], 'announcements': club[1] or "No announcements"} for club in clubs]

        # Convert hackathons to a list of titles
        hackathon_titles = [hackathon[0] for hackathon in hackathons]

        # Convert projects to a list of titles
        project_titles = [project[0] for project in projects]

        print("Clubs data:", clubs_list)  # Debugging line
        print("Hackathon titles:", hackathon_titles)  # Debugging line
        print("Project titles:", project_titles)  # Debugging line
        print("Requests data:", requests)  # Debugging line

        return render_template(
            "home.html",
            username=username,
            rating=rating,
            user_id=user_id,
            clubs=clubs_list,
            hackathons=hackathon_titles,
            projects=project_titles,
            requests=requests  # Pass requests to the template
        )


# Profile route
@app.route('/profile/<string:username>')
def profile(username):
    try:
        # Connect to the database
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Fetch user details
        cursor.execute('SELECT user_id, rating FROM user_info WHERE username = ?', (username,))
        user_result = cursor.fetchone()

        if user_result:
            user_id, rating = user_result

            # Fetch skills from user_skills table
            cursor.execute('SELECT skill, rating FROM user_skills WHERE user_id = ?', (user_id,))
            skills = [{"skill": skill[0], "rating": skill[1]} for skill in cursor.fetchall()]

            # Fetch projects from project_info table
            cursor.execute('SELECT name, description FROM project_info WHERE project_head = ?', (user_id,))
            projects = [{"name": project[0], "description": project[1]} for project in cursor.fetchall()]

            # Fetch hackathons where the user is part of a team
            cursor.execute('''
                SELECT h.name, h.description, h.start_date, h.end_date 
                FROM hackathon_info h
                JOIN teams t ON h.hackathon_id = t.hackathon_id
                JOIN team_members tm ON t.team_id = tm.team_id
                WHERE tm.user_id = ?
            ''', (user_id,))
            hackathons = [{
                "name": hackathon[0],
                "description": hackathon[1],
                "start_date": hackathon[2],
                "end_date": hackathon[3]
            } for hackathon in cursor.fetchall()]

            # Close the database connection
            conn.close()

            # Render the profile template with the fetched data
            return render_template(
                'profile.html',
                username=username,
                rating=rating,
                skills=skills,  # Pass skills as a list of dictionaries
                projects=projects,
                hackathons=hackathons
            )
        else:
            conn.close()
            flash("User not found!")
            return redirect(url_for('login'))

    except sqlite3.OperationalError as e:
        conn.close()
        flash(f"Database error: {str(e)}")
        return redirect(url_for('login'))

    except Exception as e:
        conn.close()
        flash(f"An unexpected error occurred: {str(e)}")
        return redirect(url_for('login'))
        

# Club registration route
@app.route('/club/register', methods=['GET', 'POST'])
def club_register():
    if request.method == 'POST':
        club_name = request.form['club_name']
        email = request.form['email']
        password = request.form['password']
        
        save_club(club_name, email, password)
        flash("Club registered successfully!")
        return redirect('/club/login')

    return render_template('club_register.html')

# Club login route
@app.route('/club/login', methods=['GET', 'POST'])
def club_login():
    if request.method == 'POST':
        club_name = request.form['club_name']
        password = request.form['password']
        
        result = login_club(club_name, password)

        if result['status'] == 'success':
            flash("Club login successful!")
            return redirect(url_for('club_home', club_name=club_name))
        else:
            flash(result['message'])
            return redirect(url_for('club_login'))

    return render_template('club_login.html')

# Club home route
@app.route('/club/home/<club_name>')
def club_home(club_name):
    # Render the club_home.html template and pass the club_name variable to it
    return render_template('club_home.html', club_name=club_name)

@app.route('/club/home/<club_name>/save_announcement', methods=['POST'])
def save_announcement(club_name):
    if request.method == 'POST':
        announcement = request.form['announcement']  # Get the announcement from the form

        # Save the announcement to the database
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        try:
            # Fetch the current announcements
            cursor.execute('SELECT announcements FROM club_info WHERE club_name = ?', (club_name,))
            result = cursor.fetchone()

            if result:
                current_announcements = result[0] or ""  # Handle case where announcements is NULL
                new_announcements = f"{current_announcements}\n{announcement}"  # Append the new announcement
            else:
                new_announcements = announcement

            # Update the database
            cursor.execute('UPDATE club_info SET announcements = ? WHERE club_name = ?', (new_announcements, club_name))
            conn.commit()
            flash("Announcement saved successfully!")
        except Exception as e:
            conn.rollback()
            flash(f"An error occurred: {e}")
        finally:
            conn.close()

    return redirect(url_for('club_home', club_name=club_name))

# Route to create a hackathon
@app.route('/createhack', methods=['GET', 'POST'])
def create_hackathon():
    if request.method == 'POST':
        # Get form data
        hackathon_name = request.form['hackathon_name']
        hackathon_description = request.form['hackathon_description']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        skills = request.form.getlist('skills[]')  # Get selected skills as a list

        # Store in SQLite database
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Insert into hackathon_info table
        cursor.execute('''
            INSERT INTO hackathon_info (name, description, start_date, end_date)
            VALUES (?, ?, ?, ?)
        ''', (hackathon_name, hackathon_description, start_date, end_date))
        hackathon_id = cursor.lastrowid  # Get the auto-generated hackathon_id

        # Insert skills into hackathon_skills table
        for skill in skills:
            cursor.execute('INSERT INTO hackathon_skills (hackathon_id, skill) VALUES (?, ?)', 
                           (hackathon_id, skill))

        conn.commit()
        conn.close()

        return redirect(request.referrer)  # Redirect to the same page

    return render_template('create_hackathon.html')

@app.route('/home/<username>/<hackathon_name>')
def hackathon_details(username, hackathon_name):
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Fetch hackathon details based on hackathon_name
    cursor.execute('SELECT * FROM hackathon_info WHERE name = ?', (hackathon_name,))
    hackathon = cursor.fetchone()

    # If hackathon is found, fetch associated skills and teams
    if hackathon:
        hackathon_id = hackathon[0]  # Assuming hackathon_id is the first column

        # Fetch skills for this hackathon from hackathon_skills table
        cursor.execute('SELECT skill FROM hackathon_skills WHERE hackathon_id = ?', (hackathon_id,))
        skills_data = cursor.fetchall()
        skills = [skill[0] for skill in skills_data]  # Extract skills from tuples

        # Fetch teams associated with this hackathon
        cursor.execute('''
            SELECT t.team_id, t.name, t.project_id, t.rankings
            FROM teams t
            WHERE t.hackathon_id = ?
        ''', (hackathon_id,))
        teams_data = cursor.fetchall()

        # Fetch team members and calculate average rating for each team
        teams = []
        for team in teams_data:
            team_id, team_name, project_id, rankings = team

            # Fetch team members and their ratings
            cursor.execute('''
                SELECT u.rating
                FROM team_members tm
                JOIN user_info u ON tm.user_id = u.user_id
                WHERE tm.team_id = ?
            ''', (team_id,))
            members_ratings = cursor.fetchall()

            # Calculate average rating
            if members_ratings:
                ratings = [rating[0] for rating in members_ratings if rating[0] is not None]
                average_rating = sum(ratings) / len(ratings) if ratings else None
            else:
                average_rating = None

            # Add team details to the teams list
            teams.append({
                'team_id': team_id,
                'name': team_name,
                'project_id': project_id,
                'rankings': rankings,
                'average_rating': average_rating
            })

        # Close the database connection
        conn.close()

        # Prepare hackathon details
        hackathon_details = {
            'name': hackathon[1],  # Assuming name is the second column
            'description': hackathon[2],
            'start_date': hackathon[3],
            'end_date': hackathon[4],
            'skills': skills  # Skills fetched from hackathon_skills table
        }

        return render_template('hack_detail.html', username=username, hackathon=hackathon_details, teams=teams)
    else:
        conn.close()
        return "Hackathon not found", 404

@app.route('/home/<username>/project/<project_name>')
def project_details(username, project_name):
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Fetch project details based on project_name
    cursor.execute('''
        SELECT p.name, p.description, u.username AS project_head
        FROM project_info p
        JOIN user_info u ON p.project_head = u.user_id
        WHERE p.name = ?
    ''', (project_name,))
    project = cursor.fetchone()

    # Close the database connection
    conn.close()

    # If project is found, pass details to the template
    if project:
        project_details = {
            'name': project[0],  # Project name
            'description': project[1],  # Project description
            'project_head': project[2]  # Project head's username
        }
        return render_template('project_detail.html', username=username, project=project_details)
    else:
        # If project is not found, return a 404 error
        return "Project not found", 404
    
@app.route('/home/<username>/<hackathon_name>/createteam', methods=['GET', 'POST'])
def create_team(username, hackathon_name):
    if request.method == 'POST':
        team_name = request.form['team_name']
        team_description = request.form['team_description']

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Fetch the hackathon_id
        cursor.execute('SELECT hackathon_id FROM hackathon_info WHERE name = ?', (hackathon_name,))
        result = cursor.fetchone()
        
        if result is None:
            flash("Hackathon not found!")
            return redirect(url_for('hackathon_details', username=username, hackathon_name=hackathon_name))

        hackathon_id = result[0]

        # Fetch the user_id of the logged-in user (team leader)
        cursor.execute('SELECT user_id FROM user_info WHERE username = ?', (username,))
        user_result = cursor.fetchone()

        if user_result is None:
            flash("User not found!")
            return redirect(url_for('hackathon_details', username=username, hackathon_name=hackathon_name))

        user_id = user_result[0]

        # Insert into teams table with NULL project_id and rankings
        cursor.execute('''
            INSERT INTO teams (name, description, project_id, hackathon_id, rankings)
            VALUES (?, ?, ?, ?, ?)
        ''', (team_name, team_description, None, hackathon_id, None))

        # Get the auto-generated team_id
        team_id = cursor.lastrowid

        # Insert the team leader into hackathon_team_leaders table
        cursor.execute('''
            INSERT INTO hackathon_team_leaders (hackathon_id, team_id, team_leader_id)
            VALUES (?, ?, ?)
        ''', (hackathon_id, team_id, user_id))

        # Insert the logged-in user as a team member into team_members table
        cursor.execute('''
            INSERT INTO team_members (team_id, user_id)
            VALUES (?, ?)
        ''', (team_id, user_id))

        conn.commit()
        conn.close()

        flash("Team created successfully!")
        return redirect(url_for('hackathon_details', username=username, hackathon_name=hackathon_name))

    return render_template('create_team.html', username=username, hackathon_name=hackathon_name)


@app.route('/home/<username>/<hackathon_name>/<int:team_id>', methods=['GET', 'POST'])
def team_details(username, hackathon_name, team_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if request.method == 'POST':
        # Fetch user_id from username
        cursor.execute('''
            SELECT user_id
            FROM user_info
            WHERE username = ?
        ''', (username,))
        user_result = cursor.fetchone()

        if not user_result:
            flash('User not found', 'error')
            return redirect(url_for('team_details', username=username, hackathon_name=hackathon_name, team_id=team_id))

        user_id = user_result[0]  # Access by index

        # Fetch hackathon_id and team_leader_id for the team
        cursor.execute('''
            SELECT t.hackathon_id, htl.team_leader_id
            FROM teams t
            LEFT JOIN hackathon_team_leaders htl ON t.team_id = htl.team_id
            WHERE t.team_id = ?
        ''', (team_id,))
        team_info = cursor.fetchone()

        if not team_info:
            flash('Team not found', 'error')
            return redirect(url_for('team_details', username=username, hackathon_name=hackathon_name, team_id=team_id))

        hackathon_id = team_info[0]  # Access by index
        team_leader_id = team_info[1]  # Access by index

        try:
            # Insert the request into the requests table
            cursor.execute('''
                INSERT INTO requests (hackathon_id, team_id, team_leader_id, user_id)
                VALUES (?, ?, ?, ?)
            ''', (hackathon_id, team_id, team_leader_id, user_id))

            conn.commit()
            flash('Applied successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'An error occurred: {str(e)}', 'error')
        finally:
            conn.close()

        return redirect(url_for('team_details', username=username, hackathon_name=hackathon_name, team_id=team_id))

    else:
        # Handle GET request (fetch team details, members, and hackathon info)
        # Fetch team details
        cursor.execute('''
            SELECT t.name, t.description, u.username AS team_leader, AVG(u.rating) AS average_rating, t.hackathon_id, htl.team_leader_id
            FROM teams t
            LEFT JOIN hackathon_team_leaders htl ON t.team_id = htl.team_id
            LEFT JOIN user_info u ON htl.team_leader_id = u.user_id
            WHERE t.team_id = ?
        ''', (team_id,))
        team = cursor.fetchone()

        # Fetch team members
        cursor.execute('''
            SELECT u.username
            FROM team_members tm
            JOIN user_info u ON tm.user_id = u.user_id
            WHERE tm.team_id = ?
        ''', (team_id,))
        members = cursor.fetchall()

        # Fetch hackathon details
        cursor.execute('''
            SELECT name, description, start_date, end_date
            FROM hackathon_info
            WHERE hackathon_id = ?
        ''', (team[4],))  # team[4] is the hackathon_id
        hackathon = cursor.fetchone()

        conn.close()

        if team and hackathon:
            team_details = {
                'name': team[0],  # Access by index
                'description': team[1],  # Access by index
                'team_leader': team[2],  # Access by index
                'average_rating': team[3],  # Access by index
                'hackathon_id': team[4],  # Access by index
                'team_leader_id': team[5]  # Access by index
            }
            hackathon_details = {
                'name': hackathon[0],  # Access by index
                'description': hackathon[1],  # Access by index
                'start_date': hackathon[2],  # Access by index
                'end_date': hackathon[3]  # Access by index
            }
            return render_template(
                'team_detail.html',
                username=username,
                hackathon_name=hackathon_name,
                team=team_details,
                members=members,
                team_id=team_id,
                hackathon=hackathon_details,
                current_user=username  # Pass the username as current_user
            )
        else:
            flash('Team or Hackathon not found', 'error')
            return redirect(url_for('team_details', username=username, hackathon_name=hackathon_name, team_id=team_id))

@app.route('/home/<username>/createproject', methods=['GET'])
def create_project(username):
    return render_template('create_project.html', username=username)

@app.route('/home/<username>/createproject', methods=['POST'])
def submit_project(username):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        # Connect to the database
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Insert the new project into the project_info table
        cursor.execute('''
            INSERT INTO project_info (name, description, project_head)
            VALUES (?, ?, (SELECT user_id FROM user_info WHERE username = ?))
        ''', (title, description, username))

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

        # Redirect to the home page or another appropriate page
        return redirect(url_for('home', username=username))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)