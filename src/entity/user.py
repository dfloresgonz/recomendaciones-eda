class User:
  def __init__(self, name, username, profile_pic, _id):
    self.name = name
    self.username = username
    self.profile_pic = profile_pic
    self.id = int(_id)

  def __repr__(self):
    return f"User(name={self.name}, username={self.username})"
