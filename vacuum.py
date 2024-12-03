# Compress SQLite3 database
import sqlite3
conn = sqlite3.connect("address_book.db")
conn.execute("VACUUM")
print("Database vacuumed")
conn.close()
