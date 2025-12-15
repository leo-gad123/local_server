import sqlite3

conn = sqlite3.connect("lamp.db")
cur = conn.cursor()

cur.execute("SELECT * FROM lamp")
rows = cur.fetchall()

for row in rows:
    print(row)

conn.close()
