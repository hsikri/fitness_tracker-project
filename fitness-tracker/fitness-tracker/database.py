import sqlite3

def initialize_database():
    conn = sqlite3.connect('fitness_tracker.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS workouts 
                 (id INTEGER PRIMARY KEY, user_id INTEGER, date TEXT, exercise TEXT, duration INTEGER)''')
    conn.commit()
    conn.close()

def get_user(username, password):
    conn = sqlite3.connect('fitness_tracker.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

def add_workout(user_id, date, exercise, duration):
    conn = sqlite3.connect('fitness_tracker.db')
    c = conn.cursor()
    c.execute("INSERT INTO workouts (user_id, date, exercise, duration) VALUES (?, ?, ?, ?)", (user_id, date, exercise, duration))
    conn.commit()
    workout_id = c.lastrowid
    conn.close()
    return workout_id

def get_workouts(user_id):
    conn = sqlite3.connect('fitness_tracker.db')
    c = conn.cursor()
    c.execute("SELECT * FROM workouts WHERE user_id=?", (user_id,))
    workouts = c.fetchall()
    conn.close()
    return workouts
