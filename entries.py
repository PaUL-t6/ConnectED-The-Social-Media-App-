# import sqlite3
# import pandas as pd

# # Connect to the SQLite database
# conn = sqlite3.connect('your_database.db')
# cursor = conn.cursor()

# # Read data from Excel file
# excel_file = 'database_data.xlsx'
# user_info_df = pd.read_excel(excel_file, sheet_name='user_info')
# user_skills_df = pd.read_excel(excel_file, sheet_name='user_skills')
# club_info_df = pd.read_excel(excel_file, sheet_name='club_info')
# hackathon_info_df = pd.read_excel(excel_file, sheet_name='hackathon_info')
# hackathon_skills_df = pd.read_excel(excel_file, sheet_name='hackathon_skills')
# project_info_df = pd.read_excel(excel_file, sheet_name='project_info')
# teams_df = pd.read_excel(excel_file, sheet_name='teams')
# team_members_df = pd.read_excel(excel_file, sheet_name='team_members')
# user_hackathons_df = pd.read_excel(excel_file, sheet_name='user_hackathons')
# user_projects_df = pd.read_excel(excel_file, sheet_name='user_projects')
# hackathon_team_rankings_df = pd.read_excel(excel_file, sheet_name='hackathon_team_rankings')
# hackathon_team_leaders_df = pd.read_excel(excel_file, sheet_name='hackathon_team_leaders')
# requests_df = pd.read_excel(excel_file, sheet_name='requests')

# # Function to insert data into a table
# def insert_data(table_name, df):
#     for _, row in df.iterrows():
#         columns = ', '.join(row.index)
#         placeholders = ', '.join(['?'] * len(row))
#         query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
#         cursor.execute(query, tuple(row))

# # Insert data into each table
# insert_data('user_info', user_info_df)
# insert_data('user_skills', user_skills_df)
# insert_data('club_info', club_info_df)
# insert_data('hackathon_info', hackathon_info_df)
# insert_data('hackathon_skills', hackathon_skills_df)
# insert_data('project_info', project_info_df)
# insert_data('teams', teams_df)
# insert_data('team_members', team_members_df)
# insert_data('user_hackathons', user_hackathons_df)
# insert_data('user_projects', user_projects_df)
# insert_data('hackathon_team_rankings', hackathon_team_rankings_df)
# insert_data('hackathon_team_leaders', hackathon_team_leaders_df)
# insert_data('requests', requests_df)

# # Commit changes and close the connection
# conn.commit()
# conn.close()

# print("Database populated successfully!")