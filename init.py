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
                role INT NOT NULL REFERENCES roles(role_id))""")
                
    # Execute a command: create members table
    cur.execute("""CREATE TABLE members(
                user_id INT PRIMARY KEY REFERENCES users(user_id),
                loyalty_points INT,
                join_date DATE)""")
    
    # Execute a command: create trainers table
    cur.execute("""CREATE TABLE trainers(
                user_id INT PRIMARY KEY REFERENCES users(user_id),
                start_date DATE)""")
    
    # Execute a command: create admins table
    cur.execute("""CREATE TABLE admins(
                user_id INT PRIMARY KEY REFERENCES users(user_id))""")
                
    # Execute a command: create profiles table
    cur.execute("""CREATE TABLE profiles(
                profile_id SERIAL PRIMARY KEY,
                HRV TEXT,
                SPO2 TEXT,
                RHR TEXT,
                "5k_goal" TEXT,
                pushup_goal TEXT,
                "5k_best" TEXT,
                pushup_best TEXT,
                member INT NOT NULL REFERENCES members(user_id))""")
                
    # Execute a command: create rooms table
    cur.execute("""CREATE TABLE rooms(
                room_id SERIAL PRIMARY KEY REFERENCES users(user_id),
                location TEXT NOT NULL)""")
                
    # Execute a command: create personal sessions table
    cur.execute("""CREATE TABLE personal_sessions(
                ps_id SERIAL PRIMARY KEY,
                date TIMESTAMP,
                trainer INT NOT NULL REFERENCES trainers(user_id),
                member INT REFERENCES members(user_id),
                room INT NOT NULL REFERENCES rooms(room_id))""")
                
    # Execute a command: create group sessions table
    cur.execute("""CREATE TABLE group_sessions(
                gs_id SERIAL PRIMARY KEY,
                date TIMESTAMP,
                trainer INT NOT NULL REFERENCES trainers(user_id),
                room INT NOT NULL REFERENCES rooms(room_id))""")
    
    # Execute a command: create group session attendees table
    cur.execute("""CREATE TABLE group_session_attendees(
                gs_id INT REFERENCES group_sessions(gs_id),
                member INT REFERENCES members(user_id),
                PRIMARY KEY(gs_id, member))""")
    
    # Execute a command: create progress notes table
    cur.execute("""CREATE TABLE progress_notes(
                note_id SERIAL PRIMARY KEY,
                note TEXT NOT NULL,
                trainer INT NOT NULL REFERENCES trainers(user_id),
                profile INT NOT NULL REFERENCES profiles(profile_id))""")
    
    # Make the changes to the database persistent
    conn.commit()
    print('All tables created successfully!')

    # Execute a command: insert initial data into roles table
    cur.execute("""INSERT INTO roles(role_name) VALUES
    ('Member'),
    ('Trainer'),
    ('Admin')""")
    
    # Execute a command: insert initial data into users table
    cur.execute("""INSERT INTO users(password, first_name, last_name, email, phone, DOB, role) VALUES
    ('password', 'John', 'Doe', 'john@example.com', '613-841-1122', '1990-01-01', 1),
    ('password', 'Jane', 'Smith', 'jane@example.com', '613-834-6573', '1995-05-05', 1),
    ('password', 'Bob', 'Lee', 'bob@example.com', '613-555-6677', '1999-08-23', 2),
    ('password', 'Zack', 'Hollmann', 'zh@example.com', '613-534-6763', '2002-05-13', 3)""")

    # Execute a command: insert initial data into members table
    cur.execute("""INSERT INTO members(user_id, loyalty_points, join_date) VALUES
    (1, 100, '2023-01-01'),
    (2, 150, '2023-02-05')""")
    
    # Execute a command: insert initial data into trainers table
    cur.execute("""INSERT INTO trainers(user_id, start_date) VALUES
    (3, '2020-12-01')""")

    # Execute a command: insert initial data into admins table
    cur.execute("""INSERT INTO admins(user_id) VALUES
    (4)""")
    
    # Execute a command: insert initial data into profiles table
    cur.execute("""INSERT INTO profiles(HRV, SPO2, RHR, "5k_goal", pushup_goal, "5k_best", pushup_best, member) VALUES
    ('Good', 'Normal', 'Low', '20 minutes', '50 pushups', '18 minutes', '45 pushups', 1),
    ('Excellent', 'High', 'Very low', '15 minutes', '40 pushups', '14 minutes', '38 pushups', 2)""")

    # Execute a command: insert initial data into rooms table
    cur.execute("""INSERT INTO rooms(location) VALUES
    ('Room 1'),
    ('Room 2')""")
    
    # Execute a command: insert initial data into personal_sessions table
    cur.execute("""INSERT INTO personal_sessions(date, trainer, member, room) VALUES
    ('2023-01-10 10:24:00', 3, 1, 1),
    ('2023-01-15 9:30:00', 3, 2, 2)""")
    
    # Execute a command: insert initial data into group_sessions table
    cur.execute("""INSERT INTO group_sessions(date, trainer, room) VALUES
    ('2023-02-05 13:20:00', 3, 1),
    ('2023-03-02 16:00:00', 3, 2""")
    
    # Execute a command: insert initial data into group_session_attendees table
    cur.execute("""INSERT INTO group_session_attendees(gs_id, member) VALUES
    (1, 1),
    (1, 2)""")
    
    # Execute a command: insert initial data into group_session_attendees table
    cur.execute("""INSERT INTO progress_notes(note, trainer, profile) VALUES
    ('Making good progress!', 3, 1),
    ('Needs to work on endurance', 3, 2)""")

    # Make the changes to the database persistent
    conn.commit()
    print("All tables populated successfully!")

except Exception as error:
    print("ERROR:", error)

# Close cursor and communication with the database
cur.close()
conn.close()