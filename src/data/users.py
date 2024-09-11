from src.entity.user import User

def get_users():
  users = []

  users.append(User('Diego Flores', 'diego', '123456'))
  users.append(User('Carlos Mercedes', 'carlos', '123456'))
  users.append(User('Guillermo Soto', 'guillermo', '123456'))
  users.append(User('Manuel Berrospi', 'manuel', '123456'))

  return users