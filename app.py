from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from src.services.login import authenticate
from src.entity.user import User
from src.services.recomendaciones import get_recommendaciones, get_purchases, _get_similar_users, _load_data
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'abc123xyz'


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
    session['sess_user'] = user
    return jsonify({'success': True})
  else:
    return jsonify({'success': False, 'error': 'Credenciales incorrectas'})


@app.route('/home')
def home():
  user_sess = session.get('sess_user')
  if user_sess:
    user = User(user_sess['name'], user_sess['username'],
                user_sess['profile_pic'], int(user_sess['id']))

    _load_data()

    products = get_recommendaciones(int(user_sess['id']), k=5)
    purchases = get_purchases(int(user_sess['id']))
    similar_users = _get_similar_users(int(user_sess['id']))
    return render_template('home.html', user=user, products=products, purchases=purchases, similar_users=similar_users)
  else:
    return redirect(url_for('index'))


@app.route('/buy', methods=['POST'])
def buy_product():
  data = request.get_json()
  product_id = data['product_id']
  price = data['price']
  category_code = data['category_code']
  brand = data['brand']

  # Connect to SQLite database
  conn = sqlite3.connect('src/data/database.db')
  cursor = conn.cursor()

  # Insert into purchases table
  user_id = int(session.get('sess_user')['id'])
  event_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

  cursor.execute(
      """INSERT INTO purchases (user_id, product_id, category_code, brand, price, event_time) 
      VALUES (?,?,?,?,?,?)
      """, (user_id, product_id, category_code, brand, price, event_time,))
  conn.commit()

  # Close the connection
  conn.close()

  return jsonify({'success': True})


@app.route('/logout', methods=['POST'])
def logout():
  session.clear()  # Clear the session to log the user out
  return redirect(url_for('index'))


if __name__ == '__main__':
  app.run(debug=True)
