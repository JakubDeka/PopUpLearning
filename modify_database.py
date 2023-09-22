import sqlite3


connection = sqlite3.connect("french_words.db")
cursor = connection.cursor()
# cursor.execute("""
#     ALTER TABLE adjectives
#     ADD difficulty text;
#     """)
# rows = cursor.fetchall()
# for row in rows:
#     print(row)
connection.commit()
connection.close()