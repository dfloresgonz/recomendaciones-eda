class User:
    def __init__(self, name, username, password, profile_pic):
        self.name = name
        self.username = username
        self.password = password
        self.profile_pic = profile_pic

    def __repr__(self):
        return f"User(name={self.name}, username={self.username})"