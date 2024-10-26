from src.services.BinarySearchTree import EcommerceRecommendationSystem
from src.repository.bd import _get_purchases

recommender = EcommerceRecommendationSystem()


def _load_data():
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


def _get_similar_users(user_id):
  users = recommender.find_similar_users(user_id)
  users_dict_list = []
  for user in users:
    user_dict = {
        'user_id': user[0],
        'similarity_score': user[1],
        'purchases': get_purchases(user[0])
    }
    users_dict_list.append(user_dict)
  return users_dict_list
