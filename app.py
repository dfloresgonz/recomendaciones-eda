from flask import Flask, render_template, request, redirect, url_for, session
from src.services.login import authenticate
from src.entity.user import User

app = Flask(__name__)
app.secret_key = 'abc123xyz'

# Simular credenciales para validar el login
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

@app.route('/')
def index():
    user_sess = session.get('sess_user')
    if user_sess:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = authenticate(username, password)
    
    # Validar credenciales
    if user is not None:
        session['sess_user'] = user.__dict__
        return redirect(url_for('home'))
    else:
        return "Invalid credentials. Please try again."

@app.route('/home')
def home():
    user_sess = session.get('sess_user')
    if user_sess:
        user = User(user_sess['name'], user_sess['username'], user_sess['password'], user_sess['profile_pic'])
        return render_template('home.html', user=user)
    else:
        return redirect(url_for('index'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear the session to log the user out
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
