from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Connect to MySQL (use container's service name as host)
def get_db_connection():
    return mysql.connector.connect(
        host='mysql',
        user='root',
        password='rootpass',
        database='users_db'
    )

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            msg = "Login successful!"
        else:
            msg = "Invalid credentials!"
    return render_template('login.html', message=msg)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        cursor.close()
        conn.close()
        msg = "Signup successful!"
    return render_template('signup.html', message=msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
