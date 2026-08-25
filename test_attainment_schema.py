from database import get_connection

conn = get_connection()
cursor = conn.cursor()

for table in [
    "Marks",
    "CourseOutcome",
    "COWeightage",
    "CO_Assessment_Weightage",
    "IndirectAttainment",
    "CO_PO_Mapping",
]:
    print("\n===== " + table + " =====")
    cursor.execute(f"PRAGMA table_info({table})")
    for row in cursor.fetchall():
        print(row["name"], "-", row["type"])

conn.close()