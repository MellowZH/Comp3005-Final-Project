import psycopg2
from postgresConfig import *

# Open a connection to the postgres database using parameters from config file
conn = psycopg2.connect(database = DATABASE_NAME, 
                        user = USER_NAME, 
                        host= HOST,
                        password = PASSWORD,
                        port = PORT)

# Open a cursor to perform database operations
cur = conn.cursor()

try:
    # Execute a command: create roles table
    cur.execute("""CREATE TABLE roles(
                role_id SERIAL PRIMARY KEY,
                role_name TEXT NOT NULL)""")
                
    # Execute a command: create users table
    cur.execute("""CREATE TABLE users(
                user_id SERIAL PRIMARY KEY,
                password TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                DOB DATE,
                role INT references roles(role_id))""")
                
    # Execute a command: create members table
    cur.execute("""CREATE TABLE members(
                user_id PRIMARY KEY references users(user_id),
                loyalty_points INT,
                join_date DATE)""")
    
    # Execute a command: create trainers table
    cur.execute("""CREATE TABLE trainers(
                user_id PRIMARY KEY references users(user_id),
                start_date DATE)""")
                
    # Execute a command: create profiles table
    cur.execute("""CREATE TABLE profiles(
                profile_id SERIAL PRIMARY KEY,
                HRV TEXT NOT NULL,
                SPO2 TEXT NOT NULL,
                RHR TEXT NOT NULL,
                5k_goal TEXT NOT NULL,
                pushup_goal TEXT NOT NULL,
                5k_best TEXT NOT NULL,
                pushup_best TEXT NOT NULL,
                member INT references members(user_id))""")
                
    # Execute a command: create rooms table
    cur.execute("""CREATE TABLE rooms(
                room_id SERIAL PRIMARY KEY references users(user_id),
                location TEXT NOT NULL)""")
                
    # Execute a command: create personal sessions table
    cur.execute("""CREATE TABLE personal_sessions(
                ps_id SERIAL PRIMARY KEY,
                date DATE,
                trainer INT references trainers(user_id),
                member INT references members(user_id),
                room INT references rooms(room_id))""")
                
    # Execute a command: create group sessions table
    cur.execute("""CREATE TABLE group_sessions(
                gs_id SERIAL PRIMARY KEY,
                date DATE,
                trainer INT references trainers(user_id),
                room INT references rooms(room_id))""")
    
    # Execute a command: create group session attendees table
    cur.execute("""CREATE TABLE group_session_attendees(
                gs_id INT PRIMARY KEY references group_sessions(gs_id),
                member INT PRIMARY KEY references members(user_id))""")
    
    # Execute a command: create progress notes table
    cur.execute("""CREATE TABLE progress_notes(
                note_id INT SERIAL PRIMARY KEY,
                note TEXT NOT NULL,
                profile INT references profiles(profile_id))""")
    
    # Make the changes to the database persistent
    conn.commit()
    print('All tables created successfully!')

    # Execute a command: insert initial data into all tables
    cur.execute("""INSERT INTO roles(role_name) VALUES
    ('Member'),
    ('Trainer');""")

    # Make the changes to the database persistent
    conn.commit()
    print("Student table populated successfully!")

except Exception as error:
    print("ERROR:", error)

# Close cursor and communication with the database
cur.close()
conn.close()