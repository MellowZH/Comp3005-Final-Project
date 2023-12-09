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
    # Execute a command: create students table
    cur.execute("""CREATE TABLE students(
                student_id SERIAL PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                enrollment_date DATE)""")
    
    # Make the changes to the database persistent
    conn.commit()
    print('Student table created successfully!')

    # Execute a command: insert initial data into students table
    cur.execute("""INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
    ('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
    ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
    ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02')""")

    # Make the changes to the database persistent
    conn.commit()
    print("Student table populated successfully!")

except Exception as error:
    print("ERROR:", error)

# Close cursor and communication with the database
cur.close()
conn.close()