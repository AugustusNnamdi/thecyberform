import sqlite3
from datetime import datetime

connection = sqlite3.connect('database.db')

# Create tables
with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Posts
cur.execute( "INSERT INTO posts (title, content, author) VALUES (?,?,?)",
            ('Welcome to TheCyberForum', 'Content for the first post', 'admin')
            )

cur.execute( "INSERT INTO posts (title, content, author) VALUES (?,?,?)",
            ('Second Post', 'Content for the second post', 'admin')
            )

cur.execute( "INSERT INTO posts (title, content, author) VALUES (?,?,?)",
            ('Third Post', 'Content for the Third post', 'admin')
            )


# Users
from datetime import datetime

now = datetime.now().isoformat()
cur.execute( "INSERT INTO users (username, name, email, password, member_since) VALUES (?,?,?,?,?)",
            ('admin', 'admin', 'admin@gmail.com', 'admin', now)
            )

connection.commit()
connection.close()
