
from system.friend_manager import FriendManager

fm = FriendManager()

print("Creating users...")
fm.create_user("Alice")
fm.create_user("Bob")

print("Adding friendship...")
fm.add_friend("Alice", "Bob")

print("Done!")
