from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret_key"

# Database initialization
def initialize_database():
    conn = sqlite3.connect('fitness_tracker.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS workouts 
                 (id INTEGER PRIMARY KEY, user_id INTEGER, date TEXT, exercise TEXT, duration INTEGER)''')
    conn.commit()
    conn.close()

# Route for the home page
@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('fitness_tracker.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html', error="Invalid username or password")

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('fitness_tracker.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))  # Redirect to login page after successful registration
    return render_template('register.html')  # Render the registration form HTML

# Route for user dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        conn = sqlite3.connect('fitness_tracker.db')
        c = conn.cursor()
        c.execute("SELECT * FROM workouts WHERE user_id=?", (1,))
        workouts = c.fetchall()
        conn.close()
        return render_template('dashboard.html', username=username, workouts=workouts)
    else:
        return redirect(url_for('home'))

# Modified route for logging out
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))  # Redirect to the home page (login) after logout

'''# Route for adding a workout
@app.route('/add_workout', methods=['POST'])
def add_workout():
    if 'username' in session:
        date = request.form['date']
        exercise = request.form['exercise']
        duration = request.form['duration']
        conn = sqlite3.connect('fitness_tracker.db')
        c = conn.cursor()
        c.execute("INSERT INTO workouts (user_id, date, exercise, duration) VALUES (?, ?, ?, ?)", (1, date, exercise, duration))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('home'))
'''
# Routes for other functionalities...

# Route for water intake page
@app.route('/water_intake')
def water_intake():
    return render_template('water_intake.html')

# Route for adding water intake data
@app.route('/add_water_intake', methods=['POST'])
def add_water_intake():
    liters = request.form['liters']
    timestamp = request.form['timestamp']
    # Insert water intake data into database
    return redirect(url_for('dashboard'))

# Route for the workout page
@app.route('/workout')
def workout():
    return render_template('workout.html')

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)

