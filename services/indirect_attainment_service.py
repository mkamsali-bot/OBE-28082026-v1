from database import get_connection

def row_to_dict(row):
    return dict(row)


# ==========================================================
# Get Indirect Attainment
# ==========================================================
def get_indirect_attainment(course_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM IndirectAttainment
        WHERE course_id = ?
        ORDER BY co_id
    """, (course_id,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ==========================================================
# Check Whether Indirect Attainment Exists
# ==========================================================
def has_indirect_attainment(course_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM IndirectAttainment
        WHERE course_id = ?
    """, (course_id,))

    count = cursor.fetchone()[0]

    conn.close()

    return count > 0

# ==========================================================
# Save Indirect Attainment
# ==========================================================

def save_indirect_attainment(course_id, values):

    conn = get_connection()

    cursor = conn.cursor()

    # Remove existing records
    cursor.execute("""
        DELETE FROM IndirectAttainment
        WHERE course_id = ?
    """, (course_id,))

    # Insert new records
    for co_id, percentage in values.items():

        cursor.execute("""
            INSERT INTO IndirectAttainment
            (
                course_id,
                co_id,
                indirect_percentage
            )
            VALUES (?, ?, ?)
        """, (
            course_id,
            co_id,
            percentage
        ))

    conn.commit()

    conn.close()