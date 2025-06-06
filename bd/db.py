import sqlite3

DB_PATH = "steam_friends_cs2.db"

def buscar_nicks(parcial: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT steam_id, nickname FROM friends WHERE nickname LIKE ?", (f"%{parcial}%",))
    resultados = cursor.fetchall()
    conn.close()
    return resultados