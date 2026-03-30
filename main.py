from system.friend_manager import FriendManager
from system.recommendation_engine import recommend_friends

# Initialize
fm = FriendManager()

# Colors (ANSI)
class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def get_input(prompt):
    return input(Color.BLUE + prompt + Color.END)


# 🔐 AUTH MENU (NEW)
def auth_menu():
    print(Color.CYAN + "\n" + "="*40)
    print("        🔐 AUTHENTICATION")
    print("="*40 + Color.END)
    print(Color.YELLOW + "1." + Color.END + " Register")
    print(Color.YELLOW + "2." + Color.END + " Login")
    print(Color.YELLOW + "3." + Color.END + " Exit")
    print(Color.CYAN + "="*40 + Color.END)

    choice = get_input("👉 Enter choice: ")

    if choice == "1":
        username = get_input("👤 Enter username: ")
        password = get_input("🔑 Enter password: ")
        fm.create_user(username, password)
        return None

    elif choice == "2":
        username = get_input("👤 Enter username: ")
        password = get_input("🔑 Enter password: ")

        if fm.login(username, password):
            return username
        else:
            return None

    elif choice == "3":
        print(Color.RED + "👋 Exiting..." + Color.END)
        exit()

    else:
        print(Color.RED + "❌ Invalid choice" + Color.END)
        return None


# 🎯 MAIN MENU (UPDATED)
def print_menu():
    print(Color.CYAN + "\n" + "="*40)
    print("      🌐 SOCIAL NETWORK SYSTEM")
    print("="*40 + Color.END)
    print(Color.YELLOW + "1." + Color.END + " Send Friend Request")
    print(Color.YELLOW + "2." + Color.END + " Accept Friend Request")
    print(Color.YELLOW + "3." + Color.END + " View Network")
    print(Color.YELLOW + "4." + Color.END + " Recommend Friends")
    print(Color.YELLOW + "5." + Color.END + " Undo Last Action")
    print(Color.YELLOW + "6." + Color.END + " Logout")
    print(Color.YELLOW + "7." + Color.END + " Delete User")
    print(Color.CYAN + "="*40 + Color.END)


# 🚀 MAIN SYSTEM LOOP
def menu():
    current_user = None

    while True:
        # 🔐 Force login first
        while not current_user:
            current_user = auth_menu()

        print(Color.GREEN + f"\n✅ Logged in as {current_user}" + Color.END)

        print_menu()
        choice = get_input("👉 Enter choice: ")

        if choice == "1":
            receiver = get_input("📥 Send request to: ")
            fm.send_request(current_user, receiver)

        elif choice == "2":
            sender = get_input("📤 Accept request from: ")
            fm.accept_request(sender, current_user)

        elif choice == "3":
            print(Color.GREEN + "\n📊 Network:" + Color.END)
            fm.display_network()

        elif choice == "4":
            recs = recommend_friends(fm, current_user)
            print(Color.GREEN + "✨ Recommendations:" + Color.END, recs)

        elif choice == "5":
            fm.undo()

        elif choice == "6":
            print(Color.YELLOW + "🔓 Logged out" + Color.END)
            current_user = None

        elif choice == "7":
            username = get_input("🗑️ Delete username: ")
            fm.delete_user(username)
            if username == current_user:
                print(Color.YELLOW + "🔓 Your account was deleted; logging out." + Color.END)
                current_user = None

        else:
            print(Color.RED + "❌ Invalid choice. Try again." + Color.END)


# Run program
menu()