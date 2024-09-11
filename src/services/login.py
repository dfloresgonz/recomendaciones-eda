from src.data.users import get_users

def authenticate(username, password):
  users = get_users()

  for user in users:
    if user.username == username and user.password == password:
      return user
  
  return None