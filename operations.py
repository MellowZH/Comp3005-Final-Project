import sys
import psycopg2

from postgresConfig import *

#Class to keep track of logged in user
class User:
    id = 0
    role = ''
    profileID = 0

# Open a connection to the postgres database using parameters from config file
conn = psycopg2.connect(database = DATABASE_NAME, 
                        user = USER_NAME, 
                        host= HOST,
                        password = PASSWORD,
                        port = PORT)

# Open a cursor to perform database operations
cur = conn.cursor()

currUser = User()

def login():
    while True:
        user_id = input("Enter userID: ")
        password = input("Enter password: ")

        try:
            #Validate login
            cur.execute(f"""SELECT * FROM users
                            WHERE user_id = {user_id}""")

            if cur.fetchall() == []:
                raise Exception("invalid userID")
            
            cur.execute(f"""SELECT password FROM users
                            WHERE user_id = {user_id}""")

            if password != cur.fetchone()[0]:
                raise Exception("invalid password")
            
            # Set logged in user_id since login was successful  
            currUser.id = user_id
            print('Welcome')
            break

        except Exception as error:
            print("ERROR:", error)

def getRole():
    try:
        # Get role of logged in user
        cur.execute(f"""SELECT role FROM users
                        WHERE user_id = {currUser.id}""")
        
        role_id = int(cur.fetchone()[0])
        
        cur.execute(f"""SELECT role_name FROM roles
                        WHERE role_id = {role_id}""")
        
        currUser.role = cur.fetchone()[0]
    
    except Exception as error:
        print("ERROR:", error)

def getProfile():
    try:
        # Get profile of logged in user
        cur.execute(f"""SELECT profile_id FROM profiles
                        WHERE member = {currUser.id}""")
        
        currUser.profileID = int(cur.fetchone()[0])
    
    except Exception as error:
        print("ERROR:", error)

def setGoals():
    # Only members can set goals on their profile
    print(currUser.role)
    if currUser.role == 'Member':
        goal = input("Which goal would you like to set? (5k, pushups): ")
        if goal == '5k':
            newGoal = input("What is your new goal?: ")
            try:
                cur.execute(f"""UPDATE profiles
                                SET "5k_goal" = '{newGoal}'
                                WHERE profile_id = {currUser.profileID}""")
                conn.commit()
            except Exception as error:
                print("ERROR:", error)

def getAllStudents():
    # Execute a command: select all data from students table
    cur.execute("""SELECT * FROM students
                   ORDER BY student_id ASC""")
    
    # Print table headers
    print(f"{'student_id':<12} {'first_name':<12} {'last_name':<12} {'email':<28} {'enrollment_date':<15}")
    print("------------------------------------------------------------------------------------")
    
    # Fetch all data from previous command, parse then print. 
    rows = cur.fetchall()
    for row in rows:
        student_id, first_name, last_name, email, enrollment_date = row
        enrollment_date = enrollment_date.strftime("%Y-%m-%d")
        print(f"{student_id:<12} {first_name:<12} {last_name:<12} {email:<28} {enrollment_date:<15}")

    # Close cursor and communication with the database
    cur.close()
    conn.close()

def addStudent(first_name, last_name, email, enrollment_date):
    try:
        # Execute a command: insert data into students table
        cur.execute(f"""INSERT INTO students (first_name, last_name, email, enrollment_date) 
                        VALUES('{first_name}','{last_name}','{email}','{enrollment_date}')""")
        # Make the changes to the database persistent
        conn.commit()
        
        print('Student added successfully!')
        print("Here's the updated table: \n")
        getAllStudents()

    except Exception as error:
        print("ERROR:", error)
        # Close cursor and communication with the database
        cur.close()
        conn.close()

def updateStudentEmail(student_id, new_email):
    try:
        #Validate student_id
        cur.execute(f"""SELECT * FROM students
                        WHERE student_id = {student_id}""")

        if cur.fetchall() == []:
            raise Exception("student_id does not exist in table")
        
        # Execute a command: modify a students email
        cur.execute(f"""UPDATE students 
                        SET email = '{new_email}' 
                        WHERE student_id = {student_id}""")
        # Make the changes to the database persistent
        conn.commit()

        print('Student email updated successfully!')
        print("Here's the updated table: \n")
        getAllStudents()


    except Exception as error:
        print("ERROR:", error)
        # Close cursor and communication with the database
        cur.close()
        conn.close()
    

def deleteStudent(student_id):
    try:
         #Validate student_id
        cur.execute(f"""SELECT * FROM students
                        WHERE student_id = {student_id}""")
        if cur.fetchall() == []:
            raise Exception("student_id does not exist in table")
        
        # Execute a command: delete student from database
        cur.execute(f"""DELETE from students 
                        WHERE student_id = {student_id}""")
        # Make the changes to the database persistent
        conn.commit()

        print('Student deleted successfully!')
        print("Here's the updated table: \n")
        getAllStudents()

    except Exception as error:
        print("ERROR:", error)
         # Close cursor and communication with the database
        cur.close()
        conn.close()

    
if __name__ == '__main__':
    args = sys.argv
    login()
    getRole()
    getProfile()
    setGoals()
    # Get cmd line arguments and pass them to the desired function
    # globals()[args[1]](*args[2:])