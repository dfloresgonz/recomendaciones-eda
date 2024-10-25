import os
import sqlite3
import csv
import pandas as pd


def init_db():
  db_path = 'src/data/database.db'
  if not os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
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
    conn.commit()
    conn.close()


def agregar_compra(user_id, product_id, category, brand, price, event_time):
  conn = sqlite3.connect('src/data/database.db')
  cursor = conn.cursor()
  cursor.execute('''
        INSERT INTO purchases (user_id, product_id, category_code, brand, price, event_time)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, product_id, category, brand, price, event_time))
  conn.commit()
  conn.close()


def _get_purchases(user_id):
  conn = sqlite3.connect('src/data/database.db')
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


def get_all_data():
  conn = sqlite3.connect('src/data/database.db')
  query = 'SELECT * FROM purchases'
  df = pd.read_sql_query(query, conn)
  conn.close()
  return df


def migrate_csv_to_db(csv_path, db_path='src/data/database.db'):
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


# Inicializar la base de datos
init_db()

# Migrar datos del archivo CSV a la base de datos SQLite
# csv_path = 'src/data/kz.csv'
# migrate_csv_to_db(csv_path)
