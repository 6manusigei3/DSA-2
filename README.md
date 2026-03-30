# Social Network App

## How to open the project from GitHub

1. Clone the repository:

```bash
git clone https://github.com/6manusigei3/DSA-2.git
cd DSA-2
```

2. Install dependencies.

Option A (recommended): create a virtual environment first:

```bash
python3 -m venv venv
source venv/bin/activate
```

Then install:

```bash
pip install -r requirements.txt
```

3. Prepare the MySQL database.

- Start your MySQL server.
- Create the database and user:

```sql
CREATE DATABASE social_network;
CREATE USER 'social_user'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON social_network.* TO 'social_user'@'localhost';
FLUSH PRIVILEGES;
```

- Create the required tables:

```sql
CREATE TABLE users (
  username VARCHAR(255) PRIMARY KEY,
  password VARCHAR(255)
);

CREATE TABLE friends (
  user1 VARCHAR(255),
  user2 VARCHAR(255)
);
```

4. Start the web app:

```bash
python3 app.py
```

5. Open your browser at:

```text
http://127.0.0.1:5000
```

This project is a small Python-based social network system that stores users and friendships in a MySQL database. It supports both a command-line interface and a Flask web interface. The app supports registration, login, friend requests, friendship acceptance, recommendations, undoing a friendship action, and deleting users.

## Project Structure

- `main.py`
  - Entry point for the application.
  - Provides a CLI menu for authentication and social network operations.
  - Uses ANSI colors for terminal display.

- `system/`
  - `__init__.py` – package marker.
  - `friend_manager.py` – core application logic for users, friendships, undo operations, and user deletion.
  - `recommendation_engine.py` – computes friend recommendations from the current network.

- `database/`
  - `__init__.py` – package marker.
  - `db_connection.py` – database connection helper using `mysql.connector`.

- `structures/`
  - Present in the project but not currently used by the main CLI flow.

- `tests/`
  - Present in the project but not currently populated.

## System Design Process

### 1. Use Cases Generation

The project supports these main use cases:

- User registration and login.
- Sending and accepting friend requests.
- Viewing the friendship network.
- Recommending friends based on friends-of-friends.
- Undoing the last friendship action.
- Deleting a user and removing their friendships.
- Running either a CLI version (`main.py`) or a web version (`app.py`).

### 2. Constraints and Analysis

Important constraints and analysis decisions:

- The system uses MySQL for persistent storage.
- User data and friendships are stored in simple `users` and `friends` tables.
- The in-memory representation is an adjacency list in `FriendManager`.
- Passwords are stored in plaintext for this prototype, but hashing is recommended.
- The app must run locally and requires a MySQL server.
- The web interface is implemented with Flask and the CLI interface with Python terminal input.

### 3. Basic Design

The architecture includes:

- `app.py` for the Flask web interface.
- `main.py` for the terminal-based CLI interface.
- `system/friend_manager.py` for core social network operations.
- `system/recommendation_engine.py` for friend recommendations.
- `database/db_connection.py` for MySQL connectivity.

Data flow:

- Controllers (`main.py` / `app.py`) call `FriendManager` methods.
- `FriendManager` loads users and friendships from the database into an adjacency list.
- Actions update both the in-memory graph and the database.

### 4. Bottlenecks

Current bottlenecks include:

- Friend recommendations iterate friends-of-friends, which can grow in cost as the network grows.
- `FriendManager` stores the whole network in memory, which is less efficient for very large data sets.
- The app does not currently persist pending requests, so request handling is simulated.
- Plaintext password storage is insecure and must be fixed for production.

### 5. Scalability

Planned improvements for better scalability:

- Add a pending-requests table and use proper request state management.
- Use hashed passwords and stronger authentication.
- Add database indexes on `username` and friend columns.
- Move graph operations to more efficient data structures or services for larger networks.
- Use pagination and web UI caching for large network displays.
- Consider a REST API backend and a separate frontend for better scaling.

## Features

- Register new users with username and password.
- Login existing users.
- Send friend requests (simulated command output).
- Accept friend requests and store friendships in the database.
- View the in-memory friendship network.
- Recommend friends based on "friends of friends" logic.
- Undo the last accepted friendship action.
- Delete a user and all their friendships.

## How It Works

### `main.py`

- Loads `FriendManager` from `system.friend_manager`.
- Shows an authentication menu until a user logs in.
- Displays a social network menu after login.
- Routes user choices to appropriate methods.

### `system/friend_manager.py`

- Connects to MySQL through `database.db_connection.connect_db()`.
- Loads all users and friendships into an in-memory graph structure.
- `create_user(username, password)` inserts new users into the `users` table.
- `login(username, password)` verifies credentials against the database.
- `accept_request(sender, receiver)` creates a friendship record in the `friends` table and updates the in-memory graph.
- `display_network()` prints each user and their friend list.
- `delete_user(username)` removes the user from the in-memory graph and deletes their records from both `users` and `friends` tables.
- `undo()` reverses the most recent friendship creation by deleting it from both memory and the database.

### `system/recommendation_engine.py`

- `recommend_friends(graph, user)` returns a sorted recommendation list.
- Uses friends-of-friends scoring to recommend users not already friends with the current user.

### `database/db_connection.py`

- Connects to a MySQL server.
- Current configuration:
  - host: `localhost`
  - user: `social_user`
  - password: `1234`
  - database: `social_network`
  - `ssl_disabled=True`

## Database Schema

The application expects at least two tables:

- `users`
  - `username` (primary key or unique)
  - `password`

- `friends`
  - `user1`
  - `user2`

Friendships are stored as pairs and loaded into an undirected in-memory graph.

## Setup

1. Install required Python package:

```bash
pip install mysql-connector-python
```

2. Create the MySQL database and user, for example:

```sql
CREATE DATABASE social_network;
CREATE USER 'social_user'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON social_network.* TO 'social_user'@'localhost';
FLUSH PRIVILEGES;
```

3. Create tables in `social_network`:

```sql
CREATE TABLE users (
  username VARCHAR(255) PRIMARY KEY,
  password VARCHAR(255)
);

CREATE TABLE friends (
  user1 VARCHAR(255),
  user2 VARCHAR(255)
);
```

4. Install web dependencies and run the web app:

```bash
pip install -r requirements.txt
python3 app.py
```

5. Open your browser at `http://127.0.0.1:5000`.

## Notes

- Friendship request sending is currently simulated by printing a message.
- The recommendation engine only suggests users who are friends of your friends and are not already direct friends.
- Deleting a user removes them from both the local network and the database.

## Data Structures and Algorithms

This project is built around key DSA concepts:

- **Graph data structure**
  - The social network is represented as an adjacency list in `FriendManager`.
  - `self.network = { username: [friend1, friend2, ...], ... }`
  - Each user is a node and each friendship is an edge.
- **Graph operations**
  - `accept_request(sender, receiver)` adds an edge between two nodes.
  - `display_network()` traverses the graph and prints each node's neighbors.
  - `delete_user(username)` removes a node and all incident edges.
- **Recommendation algorithm**
  - `recommend_friends(graph, user)` performs a friends-of-friends traversal.
  - It counts how often each candidate appears through mutual friends.
  - It sorts those candidates by score to return the strongest recommendations.
- **Stack behavior for undo**
  - `self.undo_stack` stores the last friendship action.
  - `undo()` pops the last action and reverses it, demonstrating LIFO behavior.

This makes the project suitable for a DSA video because it uses graph modeling, traversal, counting/sorting algorithms, and a stack-based undo mechanism.

## Improvements

Potential future enhancements:

- Persist pending friend requests in the database.
- Replace plaintext password storage with hashed passwords.
- Add proper input validation and error handling.
- Implement tests under `tests/`.
