-- Create roles table
CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name TEXT NOT NULL
);

-- Create users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    password TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    DOB DATE,
    role INT NOT NULL REFERENCES roles(role_id)
);

-- Create members table
CREATE TABLE members (
    user_id INT PRIMARY KEY REFERENCES users(user_id),
    loyalty_points INT,
    join_date DATE
);

-- Create trainers table
CREATE TABLE trainers (
    user_id INT PRIMARY KEY REFERENCES users(user_id),
    start_date DATE
);

-- Create admins table
CREATE TABLE admins (
    user_id INT PRIMARY KEY REFERENCES users(user_id)
);

-- Create profiles table
CREATE TABLE profiles (
    profile_id SERIAL PRIMARY KEY,
    HRV TEXT,
    SPO2 TEXT,
    RHR TEXT,
    "5k_goal" TEXT,
    pushup_goal TEXT,
    "5k_best" TEXT,
    pushup_best TEXT,
    member INT NOT NULL REFERENCES members(user_id)
);

-- Create rooms table
CREATE TABLE rooms (
    room_id SERIAL PRIMARY KEY,
    location TEXT NOT NULL
);

-- Create personal sessions table
CREATE TABLE personal_sessions (
    ps_id SERIAL PRIMARY KEY,
    date TIMESTAMP,
    trainer INT NOT NULL REFERENCES trainers(user_id),
    member INT REFERENCES members(user_id),
    room INT NOT NULL REFERENCES rooms(room_id)
);

-- Create group sessions table
CREATE TABLE group_sessions (
    gs_id SERIAL PRIMARY KEY,
    date TIMESTAMP,
    trainer INT NOT NULL REFERENCES trainers(user_id),
    room INT NOT NULL REFERENCES rooms(room_id)
);

-- Create group session attendees table
CREATE TABLE group_session_attendees (
    gs_id INT REFERENCES group_sessions(gs_id),
    member INT REFERENCES members(user_id),
    PRIMARY KEY(gs_id, member)
);

-- Create progress notes table
CREATE TABLE progress_notes (
    note_id SERIAL PRIMARY KEY,
    note TEXT NOT NULL,
    trainer INT NOT NULL REFERENCES trainers(user_id),
    profile INT NOT NULL REFERENCES profiles(profile_id)
);