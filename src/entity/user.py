class User:
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def __repr__(self):
        return f"User(name={self.name}, username={self.username})"