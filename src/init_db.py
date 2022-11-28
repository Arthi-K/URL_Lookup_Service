import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO url_table (url_addr, content) VALUES (?, ?)",
            ('tiny.com', 'Content for the first url')
            )

cur.execute("INSERT INTO url_table (url_addr, content) VALUES (?, ?)",
            ('amaze.com', 'Content for the second url')
            )

connection.commit()
connection.close()