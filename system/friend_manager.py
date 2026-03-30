import mysql.connector
from database.db_connection import connect_db


class FriendManager:
    def __init__(self):
        self.conn = connect_db()
        self.network = {}
        self.undo_stack = []

        self.load_users()

    def load_users(self):
        cursor = self.conn.cursor()

        # Load users
        cursor.execute("SELECT username FROM users")
        users = cursor.fetchall()

        for user in users:
            self.network[user[0]] = []

        # Load friendships
        cursor.execute("SELECT user1, user2 FROM friends")
        friendships = cursor.fetchall()

        for u1, u2 in friendships:
            self.network[u1].append(u2)
            self.network[u2].append(u1)

    # ✅ UPDATED: create_user now includes password
    def create_user(self, username, password):
        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        if cursor.fetchone():
            print(f"User {username} already exists")
            return False

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )
        self.conn.commit()

        self.network[username] = []
        print(f"User {username} created successfully")
        return True

    # ✅ NEW: login method
    def login(self, username, password):
        cursor = self.conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        if cursor.fetchone():
            print(f"Login successful. Welcome {username}!")
            return True
        else:
            print("Invalid username or password")
            return False

    def send_request(self, sender, receiver):
        print(f"{sender} sent a request to {receiver}")

    def accept_request(self, sender, receiver):
        self.network[sender].append(receiver)
        self.network[receiver].append(sender)

        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO friends (user1, user2) VALUES (%s, %s)",
            (sender, receiver)
        )
        self.conn.commit()

        self.undo_stack.append(("remove_friendship", sender, receiver))

        print(f"{receiver} accepted request from {sender}")

    def undo(self):
        if not self.undo_stack:
            print("Nothing to undo")
            return

        action = self.undo_stack.pop()

        if action[0] == "remove_friendship":
            u1, u2 = action[1], action[2]

            if u2 in self.network[u1]:
                self.network[u1].remove(u2)
            if u1 in self.network[u2]:
                self.network[u2].remove(u1)

            cursor = self.conn.cursor()
            cursor.execute(
                "DELETE FROM friends WHERE user1=%s AND user2=%s",
                (u1, u2)
            )
            self.conn.commit()

            print(f"Undo: Removed friendship between {u1} and {u2}")

    def display_network(self):
        for user in self.network:
            print(f"{user} -> {self.network[user]}")

    def delete_user(self, username):
        if username not in self.network:
            print(f"User {username} does not exist")
            return

        # Remove friendships from in-memory network
        friends = list(self.network[username])
        for friend in friends:
            if username in self.network.get(friend, []):
                self.network[friend].remove(username)

        del self.network[username]

        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM friends WHERE user1=%s OR user2=%s",
            (username, username)
        )
        cursor.execute(
            "DELETE FROM users WHERE username=%s",
            (username,)
        )
        self.conn.commit()

        print(f"User {username} deleted successfully")