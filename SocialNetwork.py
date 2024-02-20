from UsersAndPosts import User
from typing import List


class SocialNetwork:
    instance = None

    def __new__(cls, *args):
        """Overrides the __new__ method to implement the Singleton pattern."""
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    # Constructor:
    def __init__(self, name):
        """ Initializes a new instance of the SocialNetwork class."""
        self.name = name
        self.users = []
        self.connected_users = []
        print(f"The social network {self.name} was created!")

    def __str__(self):
        """ Returns: A string representation of the social network."""
        result = f"{self.name} social network:"
        for user in self.users:
            result = result + "\n" + f"{user}"
        return result

    def log_in(self, username, password):
        """sign in a user with the given username and password. """
        for user in self.users:
            if user.get_username() == username and user.get_password() == password:
                if user not in self.connected_users:
                    self.connected_users.append(user)
                    user.set_is_connected(True)
                    print(f"{user.get_username()} connected")

    def log_out(self, username):
        """sign out a user with the given username."""
        for user in self.connected_users:
            if user.get_username() == username:
                self.connected_users.remove(user)
                user.set_is_connected(False)
                print(f"{user.get_username()} disconnected")

    def sign_up(self, username, password):
        """Registers a new user with the given username and password, logs them in, and returns the user object."""
        for signed_user in self.users:
            if signed_user.get_username() == username:
                pass
        if len(password) < 4 or len(password) > 8:
            pass
        user = User(username, password)
        self.users.append(user)
        self.connected_users.append(user)
        user.set_is_connected(True)
        return user
