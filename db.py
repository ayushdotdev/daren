import sqlite3

DB_PATH = "databases/warnings.db"

def add_warning(user_id: int, guild_id: int, moderator_id: int, reason: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO warnings (user_id, guild_id, moderator_id, reason)
            VALUES (?, ?, ?, ?)
        """, (user_id, guild_id, moderator_id, reason))
        conn.commit()
        
  
def get_warns(user_id, guild_id):
    warns = []
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM warnings
        WHERE user_id = ? AND guild_id = ?
        """,(user_id,guild_id))
        rows = cursor.fetchall()
        for row in rows:
            warns.append(row)
    return warns
  
# def check():
#     with sqlite3.connect(DB_PATH) as conn:
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT * FROM warnings
#         """)
#         rows = cursor.fetchall()
#         for row in rows:
#           print(row)
#         
#         
# 
# check()