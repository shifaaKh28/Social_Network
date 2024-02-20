import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from typing import List


class PostFactory:
    """ A factory class for creating different types of posts."""

    @staticmethod
    def post_factory(user, *args):
        post = None
        if args[0] == "Text":
            post = TextPost(user, args[1])
        if args[0] == "Image":
            post = ImagePost(user, args[1])
        if args[0] == "Sale":
            post = SalePost(user, args[1], args[2], args[3])
        post.send_notification(user, "post", "")
        return post


class Post:
    # Constructor:
    def __init__(self, user):
        self.publisher = user
        self.likes = []
        self.comments = []

    # Methods:
    def get_publisher(self):
        return self.publisher

    def send_notification(self, publisher, type: str, text: str):
        """ send_notification method for sending notifications to users. """
        if type == "like":
            notification = f"{publisher.get_username()} liked your post"
            self.publisher.update(notification)
            print(f"notification to {self.publisher.get_username()}: {publisher.get_username()} liked your post")

        if type == "comment":
            notification = f"{publisher.get_username()} commented on your post"
            self.publisher.update(notification)
            print(f"notification to {self.publisher.get_username()}: "
                  f"{publisher.get_username()} commented on your post: {text}")

        if type == "post":
            notification = f"{publisher.get_username()} has a new post"
            for follower in publisher.get_followers():
                follower.update(notification)

    def like(self, user):
        if not user.connected():
            pass
        if user not in self.likes:
            self.likes.append(user)
        if self.publisher != user:
            self.send_notification(user, "like", "")

    def comment(self, user, text):
        if not user.connected():
            pass
        self.comments.append((user, text))
        if self.publisher != user:
            self.send_notification(user, "comment", text)


class TextPost(Post):
    # Constructor:
    def __init__(self, user, text):
        super().__init__(user)
        self.__text = "\"" + text + "\""

    # Methods:
    def get_text(self):
        return self.__text

    def __str__(self):
        return f"{self.get_publisher().get_username()} published a post:\n{self.__text}\n"


class ImagePost(Post):
    # Constructor:
    def __init__(self, user, path):
        super().__init__(user)
        self.__path = path

    def display(self):
        try:
            img = mpimg.imread(self.__path)
            plt.imshow(img)
            plt.axis('off')  # Turn off axis
            plt.show()
        except FileNotFoundError:
            pass
        print("Shows picture")

    def __str__(self):
        return f"{self.get_publisher().get_username()} posted a picture\n"


class SalePost(Post):
    # Constructor
    def __init__(self, user, description: str, price: int, town: str):
        super().__init__(user)
        self.__description = description
        self.__price = price
        self.__town = town
        self.__sold = False

    def discount(self, percent, password: str):
        if not super().get_publisher().connected():
            pass
        if password == self.get_publisher().get_password():
            if percent <= 100:
                self.__price = float(self.__price) * (float(100 - percent) / 100)
                print("Discount on {} product! the new price is: {}".format(self.get_publisher().get_username(),
                                                                            self.__price))

    def sold(self, password):
        if not super().get_publisher().connected():
            pass
        if password == self.get_publisher().get_password():
            self.__sold = True
            print("{}'s product is sold".format(self.get_publisher().get_username()))

    def __str__(self):
        if self.__sold:
            status = "Sold!"
        else:
            status = "For sale!"
        return f"{self.get_publisher().get_username()} posted a product for sale:\n{status} {self.__description}," \
               f" price: {self.__price}, pickup from: {self.__town}\n"


class Observer:
    """ Initializes an empty list of notifications."""

    def __init__(self):
        self.notifications = []


class User(Observer):
    # Constructor:
    def __init__(self, username, password):
        super().__init__()
        self.posts = []
        self.followers = []
        self.username = username
        self.password = password
        self.is_connected = False

    # Methods that related to the users
    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def connected(self):
        return self.is_connected

    def set_is_connected(self, connected: bool):
        self.is_connected = connected

    def follow(self, user):
        """ Allows this user to start following another user."""
        if not self.is_connected:
            pass
        if user == self:
            return None
        user.add(self)
        print(f"{self.get_username()} started following {user.get_username()}")

    def unfollow(self, user):
        """ Allows this user to start unfollowing another user."""
        if not self.is_connected:
            pass
        if self in user.get_followers():
            user.remove(self)
            print(f"{self.username} unfollowed {user.get_username()}")

    def __str__(self):
        """ Returns A string containing the user's name, number of posts, and number of followers."""
        return f"User name: {self.username}, Number of posts: {len(self.posts)}, " \
               f"Number of followers: {len(self.followers)}"

    def print_notifications(self):
        print(f"{self.username}'s notifications:")
        for notification in self.notifications:
            print(notification)

    def add(self, observer: 'Observer'):
        """ Adds an observer to the list of followers if it's not already present. """
        if observer not in self.followers:
            self.followers.append(observer)

    def remove(self, observer: 'Observer'):
        """Removes an observer from the list of followers if it's present.  """
        if observer in self.followers:
            self.followers.remove(observer)

    def get_followers(self):
        return self.followers

    def update(self, notification: str):
        self.notifications.append(notification)

    def publish_post(self, *args):
        post = PostFactory.post_factory(self, *args)
        self.posts.append(post)  # Updating the self posts list
        print(post)
        return post
