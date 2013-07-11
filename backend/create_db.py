import sqlite3


conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE users(name_db text, email_db text, password_db text, time_db text)")
conn.commit()
conn.close()
