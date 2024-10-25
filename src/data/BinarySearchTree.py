import pandas as pd
from collections import defaultdict
from datetime import datetime
from src.data.bd import get_all_data


class Product:
  def __init__(self, product_id, category_code, brand, price):
    self.product_id = product_id
    self.category_code = category_code
    self.brand = brand
    self.price = price


class Purchase:
  def __init__(self, product, timestamp):
    self.product = product
    self.timestamp = timestamp


class Node:
  def __init__(self, user_id):
    self.user_id = user_id
    self.purchases = []  # Lista de objetos Purchase
    self.categories = defaultdict(int)  # Contador de categorías
    self.brands = defaultdict(int)      # Contador de marcas
    self.total_spent = 0.0
    self.left = None
    self.right = None


class EcommerceRecommendationSystem:
  def __init__(self):
    self.root = None
    self.product_catalog = {}  # Catálogo de productos

  def load_data(self):
    """Carga y procesa el dataset"""
    # df = pd.read_csv(csv_path)
    df = get_all_data()

    # Procesar cada compra
    for _, row in df.iterrows():
      # Crear o actualizar producto en el catálogo
      product_id = str(row['product_id'])
      if product_id not in self.product_catalog:
        self.product_catalog[product_id] = Product(
            product_id=product_id,
            category_code=row['category_code'],
            brand=row['brand'],
            price=row['price']
        )

      # Crear objeto Purchase
      purchase = Purchase(
          product=self.product_catalog[product_id],
          timestamp=datetime.strptime(
              row['event_time'], '%Y-%m-%d %H:%M:%S UTC')
      )

      # Insertar en el árbol
      self.insert_purchase(row['user_id'], purchase)

  def insert_purchase(self, user_id, purchase):
    """Inserta una compra en el árbol"""
    if not self.root:
      self.root = Node(user_id)
      self._update_user_stats(self.root, purchase)
    else:
      self._insert_recursive(self.root, user_id, purchase)

  def _insert_recursive(self, node, user_id, purchase):
    if user_id == node.user_id:
      self._update_user_stats(node, purchase)
    elif user_id < node.user_id:
      if node.left is None:
        node.left = Node(user_id)
      self._insert_recursive(node.left, user_id, purchase)
    else:
      if node.right is None:
        node.right = Node(user_id)
      self._insert_recursive(node.right, user_id, purchase)

  def _update_user_stats(self, node, purchase):
    """Actualiza las estadísticas del usuario con una nueva compra"""
    node.purchases.append(purchase)
    node.categories[purchase.product.category_code] += 1
    node.brands[purchase.product.brand] += 1
    node.total_spent += purchase.product.price

  def calculate_similarity(self, user1_node, user2_node):
    """Calcula la similitud entre dos usuarios basada en múltiples factores"""
    # Similitud de categorías
    categories1 = set(user1_node.categories.keys())
    categories2 = set(user2_node.categories.keys())
    category_similarity = len(categories1.intersection(
        categories2)) / len(categories1.union(categories2)) if categories1 or categories2 else 0

    # Similitud de marcas
    brands1 = set(user1_node.brands.keys())
    brands2 = set(user2_node.brands.keys())
    brand_similarity = len(brands1.intersection(brands2)) / \
        len(brands1.union(brands2)) if brands1 or brands2 else 0

    # Similitud de rango de precios
    avg_price1 = user1_node.total_spent / \
        len(user1_node.purchases) if user1_node.purchases else 0
    avg_price2 = user2_node.total_spent / \
        len(user2_node.purchases) if user2_node.purchases else 0
    max_price = max(avg_price1, avg_price2)
    price_similarity = 1 - abs(avg_price1 - avg_price2) / \
        max_price if max_price > 0 else 0

    # Peso combinado de similitudes
    return (0.4 * category_similarity + 0.3 * brand_similarity + 0.3 * price_similarity)

  def find_similar_users(self, target_user_id, k=5):
    """Encuentra los k usuarios más similares al usuario objetivo"""
    target_node = self._find_user(self.root, target_user_id)
    if not target_node:
      return []

    similar_users = []
    self._traverse_and_find_similar(self.root, target_node, similar_users)

    # Ordenar por similitud y obtener los k más similares
    similar_users.sort(key=lambda x: x[1], reverse=True)
    return similar_users[:k]

  def _find_user(self, node, user_id):
    """Encuentra un usuario en el árbol"""
    if not node or node.user_id == user_id:
      return node
    if user_id < node.user_id:
      return self._find_user(node.left, user_id)
    return self._find_user(node.right, user_id)

  def _traverse_and_find_similar(self, node, target_node, similar_users):
    """Recorre el árbol calculando similitudes"""
    if not node:
      return

    if node.user_id != target_node.user_id:
      similarity = self.calculate_similarity(target_node, node)
      similar_users.append((node.user_id, similarity))

    self._traverse_and_find_similar(node.left, target_node, similar_users)
    self._traverse_and_find_similar(node.right, target_node, similar_users)

  def get_recommendations(self, user_id, k=5):
    """Genera recomendaciones para un usuario"""
    similar_users = self.find_similar_users(user_id, k)
    if not similar_users:
      return []

    user_node = self._find_user(self.root, user_id)
    if not user_node:
      return []

    # Productos ya comprados por el usuario objetivo
    user_products = {p.product.product_id for p in user_node.purchases}

    # Recolectar recomendaciones de usuarios similares
    recommendations = defaultdict(float)
    for similar_user_id, similarity in similar_users:
      similar_user = self._find_user(self.root, similar_user_id)
      for purchase in similar_user.purchases:
        if purchase.product.product_id not in user_products:
          recommendations[purchase.product] += similarity

    # Ordenar y retornar las mejores recomendaciones
    sorted_recommendations = sorted(
        recommendations.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [(prod.product_id, prod.category_code, prod.brand, prod.price, score)
            for prod, score in sorted_recommendations[:k]]
