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

    showMenu()

def showMenu():
    getRole()
    if currUser.role == 'Member':
        memberMenu()
    elif currUser.role == 'Trainer':
        trainerMenu()
    
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

def printProfile():
    try:
        if currUser.role == 'Trainer':
            userID = input("Enter member's userID: ")
            cur.execute(f"""SELECT profile_id FROM profiles
                            WHERE member = {userID}""")
            profileID = int(cur.fetchone()[0])
        elif currUser.role == 'Member':
            profileID = currUser.profileID

        cur.execute(f"""SELECT * FROM profiles
                        WHERE profile_id = {profileID}""")
        rows = cur.fetchall()
    except Exception as error:
        print("ERROR:", error)
        return

    headers = ["profile_id", "hrv", "spo2", "rhr", "5k_goal", "pushup_goal", "5k_best", "pushup_best", "member"]
    print(''.join(f"{header:<15}" for header in headers))
    print("----------------------------------------------------------------------------------------------------------------------------------")

    for row in rows:
        print(''.join(f"{str(cell):<15}" for cell in row))

def updateHealthMetrics():
    res = input("Which metric would you like to update? (HRV, SPO2, RHR): ")
    if res == 'HRV':
        metric = 'hrv'
    elif res == 'SPO2':
        metric = 'spo2'
    elif res == 'RHR':
        metric = 'rhr'
    else:
        print("invalid response")
        return

    newMetric = input("What is your new metric: ")
        
    try:
        cur.execute(f"""UPDATE profiles
                        SET "{metric}" = '{newMetric}'
                        WHERE profile_id = {currUser.profileID}""")
        conn.commit()
    except Exception as error:
        print("ERROR:", error)

def updateGoals():
    res = input("Which goal would you like to update? (5k, pushups): ")
    if res == '5k':
        goal = '5k_goal'
    elif res == 'pushups':
        goal = 'pushup_goal'
    else:
        print("invalid goal")
        return

    newGoal = input("What is your new goal?: ")

    try:
        cur.execute(f"""UPDATE profiles
                        SET "{goal}" = '{newGoal}'
                        WHERE profile_id = {currUser.profileID}""")
        conn.commit()
    except Exception as error:
        print("ERROR:", error)

def updateBests():
    res = input("Which personal best would you like to update? (5k, pushups): ")
    if res == '5k':
        best = '5k_goal'
    elif res == 'pushups':
        best = 'pushup_goal'
    else:
        print("invalid response")
        return

    newBest = input("What is your new personal best?: ")
        
    try:
        cur.execute(f"""UPDATE profiles
                        SET "{best}" = '{newBest}'
                        WHERE profile_id = {currUser.profileID}""")
        conn.commit()
    except Exception as error:
        print("ERROR:", error)
    
def printSchedule():
    if currUser.role == 'Member':
        try:
            cur.execute(f"""SELECT date, first_name, last_name, room, session_type
                            FROM (
                                SELECT s.member, s.date, u.first_name, u.last_name, s.room, 'Personal' AS session_type
                                FROM personal_sessions s
                                JOIN users u ON s.trainer = u.user_id
                            ) ps
                            WHERE ps.member = {currUser.id}
                            UNION
                            SELECT date, first_name, last_name, room, session_type
                            FROM (
                                SELECT s.gs_id, s.date, u.first_name, u.last_name, s.room, 'Group' AS session_type
                                FROM group_sessions s
                                JOIN users u ON s.trainer = u.user_id
                            ) gs
                            INNER JOIN group_session_attendees gsa ON gs.gs_id = gsa.gs_id
                            WHERE gsa.member = {currUser.id}
                            ORDER BY date ASC""")
            schedule = cur.fetchall()
        except Exception as error:
            print("ERROR:", error)
    
        if schedule:
            headers = ["Date", "Time", 'Trainer', 'Room', 'Type']
            print(''.join(f"{header:<15}" for header in headers))
            print("---------------------------------------------------------------")
            for session in schedule:
                session_date, first_name, last_name, room, session_type = session
                print(f"{session_date.strftime('%Y-%m-%d'):<15}{session_date.strftime('%H:%M:%S'):<15}{(first_name + " " + last_name):<15}{room:<15}{session_type:<15}")
        else:
            print("You are not registed for any sessions")
    
    elif currUser.role == 'Trainer':
        try:
            cur.execute(f"""SELECT date, room, 'Personal' AS session_type FROM personal_sessions
                            WHERE trainer = {currUser.id}
                            UNION
                            SELECT date, room, 'Group' AS session_type FROM group_sessions
                            WHERE trainer = {currUser.id}
                            ORDER BY date ASC""")
            schedule = cur.fetchall()
        except Exception as error:
            print("ERROR:", error)
        
        if schedule:
            headers = ["Date", "Time", 'Room', 'Type']
            print(''.join(f"{header:<15}" for header in headers))
            print("--------------------------------------------------------")
            for session in schedule:
                session_date, room, session_type = session
                print(f"{session_date.strftime('%Y-%m-%d'):<15}{session_date.strftime('%H:%M:%S'):<15}{room:<15}{session_type:<15}")

def registerForSession():
    try:
        cur.execute(f"""SELECT gs_id, date 
                        FROM group_sessions
                        WHERE gs_id NOT IN (
                            SELECT gs_id
                            FROM group_session_attendees
                            WHERE member = {currUser.id})""")
        sessions = cur.fetchall()

        if sessions == []:
            raise Exception("You are already in all available group sessions")
        
        headers = ['Session ID', "Date"]
        print("You can register for the following sessions:\n ")
        print(''.join(f"{header:<15}" for header in headers))
        print("--------------------------------------------")
        
        for session in sessions:
            print(''.join(f"{str(cell):<15}" for cell in session))
        
        sessionID = input("\nWhich session would you like to register in (type the ID): ")
        cur.execute(f"""INSERT INTO group_session_attendees (gs_id, member)
                        VALUES ({sessionID}, {currUser.id})""")
        conn.commit()
        print("\nYou have successfully registered for this session. Here is your updated schedule:")
        printSchedule()

    except Exception as error:
            print("ERROR:", error)

def checkLoyaltyPoints():
    try:
        cur.execute(f"""SELECT loyalty_points FROM members
                        WHERE user_id = {currUser.id}""")
        
        print("\nYou have " + str(cur.fetchone()[0]) + " loyalty points")
    
    except Exception as error:
        print("ERROR:", error)

def memberMenu():
    # Get member profile_id
    getProfile()
    
    while True:
        opt = input (
"""\nWhat would you like to do? \n1. View profile \n2. Update health metrics \n3. Update fitness goals \n4. Update fitness achievements \n5. Check schedule
6. Register for group session \n7. Check loyalty points \n8. Logout \n---> """
)
        match opt:
            case '1':
                printProfile()
            case '2':
                updateHealthMetrics()
            case '3':
                updateGoals()
            case '4':
                updateBests()
            case '5':
                printSchedule()
            case '6':
                registerForSession()
            case '7':
                checkLoyaltyPoints()
            case '8':
                global currUser 
                currUser = User()
                break
            case _:
                print("Invalid option. Please choose a valid option.")

    # Close cursor and communication with the database
    cur.close()
    conn.close()           

def trainerMenu():
    while True:
        opt = input (
"""\nWhat would you like to do? \n1. Check schedule \n2. View member profile \n3. Logout \n---> """
)
        match opt:
            case '1':
                printSchedule()
            case '2':
                printProfile()
            case '3':
                global currUser 
                currUser = User()
                break
            case _:
                print("Invalid option. Please choose a valid option.")

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
    # Get cmd line arguments and pass them to the desired function
    # globals()[args[1]](*args[2:])