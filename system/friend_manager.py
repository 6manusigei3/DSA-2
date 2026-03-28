from structures.graph import Graph
from structures.stack import Stack
from database.db_connection import connect_db

class FriendManager:
    def __init__(self):
        self.graph = Graph()
        self.actions = Stack()

    def create_user(self, username):
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
        db.commit()

        self.graph.add_user(username)
        self.actions.push(("add_user", username))

        db.close()

    def add_friend(self, user1, user2):
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("SELECT id FROM users WHERE username=%s", (user1,))
        id1 = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM users WHERE username=%s", (user2,))
        id2 = cursor.fetchone()[0]

        cursor.execute("INSERT INTO friendships VALUES (%s, %s)", (id1, id2))
        cursor.execute("INSERT INTO friendships VALUES (%s, %s)", (id2, id1))

        db.commit()
        db.close()

        self.graph.add_edge(user1, user2)
        self.actions.push(("add_friend", user1, user2))
