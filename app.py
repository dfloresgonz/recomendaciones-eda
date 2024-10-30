from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from src.services.login import authenticate
from src.entity.user import User
from src.services.recomendaciones import get_recommendaciones, get_purchases, _get_similar_users, _load_data
import sqlite3
import src.services.buy as buy_service

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
    products_sale = buy_service.get_products_sale(int(user_sess['id']))
    purchases = get_purchases(int(user_sess['id']))
    similar_users = _get_similar_users(int(user_sess['id']))
    return render_template('home.html', user=user, products=products, purchases=purchases, similar_users=similar_users, products_sale=products_sale)
  else:
    return redirect(url_for('index'))


@app.route('/buy', methods=['POST'])
def buy_product():
  data = request.get_json()

  product_bought = {
      'product_id': data['product_id'],
      'price': data['price'],
      'category_code': data['category_code'],
      'brand': data['brand'],
      'user_id': int(session.get('sess_user')['id'])
  }

  buy_service.buy_product(product_bought)

  return jsonify({'success': True})


@app.route('/logout', methods=['POST'])
def logout():
  session.clear()  # Clear the session to log the user out
  return redirect(url_for('index'))


if __name__ == '__main__':
  app.run(debug=True)
