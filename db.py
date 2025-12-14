import sqlite3

DB_NAME = "lamp.db"

def get_state():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT state FROM lamp WHERE id=1")
    state = cur.fetchone()[0]
    conn.close()
    return state

def set_state(new_state):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE lamp SET state=? WHERE id=1", (new_state,))
    conn.commit()
    conn.close()