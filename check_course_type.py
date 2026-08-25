import sqlite3

conn = sqlite3.connect("obe.db")
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

# Show the Course table structure
print("\n===== COURSE TABLE COLUMNS =====")
cursor.execute("PRAGMA table_info(Course)")
for row in cursor.fetchall():
    print(row["name"], "-", row["type"])

# Show sample data
print("\n===== SAMPLE COURSE DATA =====")
cursor.execute("SELECT * FROM Course LIMIT 5")
rows = cursor.fetchall()

for row in rows:
    print(dict(row))

conn.close()