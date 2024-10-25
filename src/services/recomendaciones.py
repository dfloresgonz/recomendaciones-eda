from src.data.main import get_recommendaciones, get_purchases, get_similar_users


def get_recomendaciones(user_id, k=5):
  return get_recommendaciones(user_id, k)


def _get_purchases(user_id):
  return get_purchases(user_id)


def _get_similar_users(user_id):
  users = get_similar_users(user_id)
  users_dict_list = []
  for user in users:
    user_dict = {
        'user_id': user[0],
        'similarity_score': user[1],
        # Asumiendo que el tercer elemento es la lista de compras
        'purchases': get_purchases(user[0])
    }
    users_dict_list.append(user_dict)
  return users_dict_list
