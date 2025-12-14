import sqlite3
connect=sqlite3.connect("lamp.db")
cursor=connect.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS lamp(
id INTEGER PRIMARY KEY,
state TEXT NULL
)
""")

cursor.execute("INSERT OR IGNORE INTO  lamp (id,state) VALUES (1,'OFF')")
connect.commit()
connect.close()
print ("Database created")