import sqlite3
conn = sqlite3.connect("address_book.db")
obj = conn.iterdump()

for line in conn.iterdump():
    print(line)

# Use with context manager to write and close/save the file
with open("database_dump.sql", "w") as file:

    for line in conn.iterdump():
        file.write(f"{line}\n")
print("File written to disk.")