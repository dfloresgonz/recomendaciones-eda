from src.data.BinarySearchTree import EcommerceRecommendationSystem
from src.data.bd import _get_purchases

# Crear una instancia global de EcommerceRecommendationSystem
recommender = EcommerceRecommendationSystem()
recommender.load_data()


def get_recommendaciones(user_id, k=5):
  recommendations = recommender.get_recommendations(user_id, k=5)
  recommendations_dict = [
      {
          'product_id': rec[0],
          'category_code': rec[1],
          'brand': rec[2],
          'price': round(rec[3], 2),
          'score': round(rec[4], 2)
      }
      for rec in recommendations
  ]
  return recommendations_dict


def get_purchases(user_id):
  return _get_purchases(user_id)


def get_similar_users(user_id):
  similar_users = recommender.find_similar_users(user_id)
  return similar_users
