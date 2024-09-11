from src.entity.user import User

def get_users():
  users = []

  users.append(User('Diego Flores', 'diego', '123456', 'https://randomuser.me/api/portraits/men/10.jpg'))
  users.append(User('Carlos Mercedes', 'carlos', '123456', 'https://randomuser.me/api/portraits/men/20.jpg'))
  users.append(User('Guillermo Soto', 'guillermo', '123456', 'https://randomuser.me/api/portraits/men/30.jpg'))
  users.append(User('Manuel Berrospi', 'manuel', '123456', 'https://randomuser.me/api/portraits/men/40.jpg'))

  return users