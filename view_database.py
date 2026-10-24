
import sqlite3

con = sqlite3.connect("instance/inventory.db")
cur = con.cursor()

# Show all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cur.fetchall()

print("TABLES:", tables)

# Show data from every table
for table in tables:
    name = table[0]
    print("\nTable:", name)

    cur.execute(f'SELECT * FROM "{name}"')
    print("Columns:", [col[0] for col in cur.description])

    for row in cur.fetchall():
        print(row)

con.close()
