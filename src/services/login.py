from src.repository.bd import get_user_by_credentials


def authenticate(username, password):
  user = get_user_by_credentials(username, password)

  return user
