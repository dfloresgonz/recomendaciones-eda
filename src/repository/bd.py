import os
import sqlite3
import csv
import pandas as pd

DATABASE_PATH = 'src/data/database.db'
PURCHASES_DATASET = 'src/data/purchases_dataset.csv'
USERS_DATASET = 'src/data/users.csv'


def init_db():
  if os.path.exists(DATABASE_PATH):
    return
  conn = sqlite3.connect(DATABASE_PATH)
  cursor = conn.cursor()
  cursor.execute('''
          CREATE TABLE IF NOT EXISTS purchases (
              user_id INTEGER,
              product_id INTEGER,
              category_code TEXT,
              brand TEXT,
              price REAL,
              event_time TEXT
          )
      ''')
  cursor.execute('''
          CREATE TABLE users (
              id INTEGER PRIMARY KEY,
              name TEXT NOT NULL,
              username TEXT NOT NULL,
              password TEXT NOT NULL,
              profile_pic TEXT NOT NULL
          )
      ''')

  conn.commit()
  conn.close()
  migrate_csv_to_db(PURCHASES_DATASET)
  migrate__users_csv_to_db(USERS_DATASET)


def agregar_compra(user_id, product_id, category, brand, price, event_time):
  conn = sqlite3.connect(DATABASE_PATH)
  cursor = conn.cursor()
  cursor.execute('''
        INSERT INTO purchases (user_id, product_id, category_code, brand, price, event_time)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, product_id, category, brand, price, event_time))
  conn.commit()
  conn.close()


def _get_purchases(user_id):
  conn = sqlite3.connect(DATABASE_PATH)
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM purchases WHERE user_id = ?', (user_id,))
  recommendations = cursor.fetchall()
  conn.close()

  recommendations_dict = [
      {
          'user_id': rec[0],
          'product_id': rec[1],
          'category_code': rec[2],
          'brand': rec[3],
          'price': round(rec[4], 2)
      }
      for rec in recommendations
  ]
  return recommendations_dict


def get_user_by_credentials(username, password):
  conn = sqlite3.connect(DATABASE_PATH)
  cursor = conn.cursor()
  cursor.execute(
      'SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
  user = cursor.fetchall()
  conn.close()

  if not user:
    return None

  user = user[0]

  user_dict = {
      'id': user[0],
      'name': user[1],
      'username': user[2],
      'profile_pic': user[4]
  }

  return user_dict


def get_all_data():
  conn = sqlite3.connect(DATABASE_PATH)
  query = 'SELECT * FROM purchases'
  df = pd.read_sql_query(query, conn)
  conn.close()
  return df


def buy_product(product_bought):
  product_id = product_bought['product_id']
  price = product_bought['price']
  category_code = product_bought['category_code']
  brand = product_bought['brand']
  user_id = product_bought['user_id']
  event_time = product_bought['event_time']

  print(f'product_id: {product_id}')
  print(f'price: {price}')
  print(f'category_code: {category_code}')
  print(f'brand: {brand}')
  print(f'user_id: {user_id}')
  print(f'event_time: {event_time}')

  # Connect to SQLite database
  conn = sqlite3.connect(DATABASE_PATH)
  cursor = conn.cursor()

  cursor.execute(
      """INSERT INTO purchases (user_id, product_id, category_code, brand, price, event_time)
      VALUES (?,?,?,?,?,?)
      """, (user_id, product_id, category_code, brand, price, event_time,))
  conn.commit()
  rowcount = cursor.rowcount
  cursor.close()
  conn.close()
  return rowcount


def get_products_sale(user_id):
  conn = sqlite3.connect(DATABASE_PATH)
  cursor = conn.cursor()
  cursor.execute(
      """ SELECT product_id, category_code, brand, price
            FROM purchases AS p 
           WHERE p.user_id <> ?
             AND category_code <> ''
             AND brand <> ''
           GROUP BY product_id, category_code, brand, price
          """, (user_id,))
  productos = cursor.fetchall()
  conn.close()

  productos_dict = [
      {
          'product_id': rec[0],
          'category_code': rec[1],
          'brand': rec[2],
          'price': round(rec[3], 2)
      }
      for rec in productos
  ]
  return productos_dict


def migrate_csv_to_db(csv_path, db_path=DATABASE_PATH):
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()

  with open(csv_path, mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # Saltar la cabecera si existe
    for row in reader:
      cursor.execute('''
                INSERT INTO purchases (user_id, product_id, category_code, brand, price, event_time)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (int(row[7]), int(row[2]), row[4], row[5], float(row[6]), row[0]))

  conn.commit()
  conn.close()


def migrate__users_csv_to_db(csv_path, db_path=DATABASE_PATH):
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()

  with open(csv_path, mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # Saltar la cabecera si existe
    for row in reader:
      cursor.execute('''
                INSERT INTO users (id, name, username, password, profile_pic)
                VALUES (?, ?, ?, ?, ?)
            ''', (int(row[4]), row[0], row[1], row[2], row[3]))

  conn.commit()
  conn.close()


# Inicializar la base de datos
init_db()
