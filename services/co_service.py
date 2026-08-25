from database import get_connection
def row_to_dict(row):
    return dict(row)

# ==========================================================
# Get All Course Outcomes
# ==========================================================
def get_all_cos():
    with get_connection() as conn:
        return conn.execute("""
            SELECT
                co.id,
                co.course_id,
                c.course_code,
                c.course_name,
                co.co_code,
                co.co_description,
                co.blooms_level,
                co.is_active
            FROM CourseOutcome co
            INNER JOIN Course c ON co.course_id = c.id
            ORDER BY c.course_code, co.co_code
        """).fetchall()

def get_co_by_id(co_id):

    with get_connection() as conn:

        row = conn.execute("""
            SELECT
                id,
                co_code,
                co_description,
                course_id
            FROM CourseOutcome
            WHERE id = ?
        """, (co_id,)).fetchone()

    return row


# ==========================================================
# Get Single Course Outcome
# ==========================================================
def get_co(id):
    with get_connection() as conn:
        return conn.execute("""
            SELECT *
            FROM CourseOutcome
            WHERE id = ?
        """, (id,)).fetchone()


# ==========================================================
# Check Duplicate CO
# ==========================================================
def co_exists(course_id, co_code, exclude_id=None):
    """
    Checks if a CO code already exists for a course.
    Pass `exclude_id` when updating to ignore self-matches.
    """
    query = """
        SELECT id
        FROM CourseOutcome
        WHERE course_id = ?
          AND UPPER(co_code) = UPPER(?)
    """
    params = [course_id, co_code]

    if exclude_id is not None:
        query += " AND id != ?"
        params.append(exclude_id)

    with get_connection() as conn:
        row = conn.execute(query, params).fetchone()
        return row is not None


# ==========================================================
# Add Course Outcome
# ==========================================================
def add_co(course_id, co_code, co_description, blooms_level, is_active=1):
    cleaned_code = co_code.upper().strip() if co_code else ""
    cleaned_desc = co_description.strip() if co_description else ""

    with get_connection() as conn:
        conn.execute("""
            INSERT INTO CourseOutcome (
                course_id,
                co_code,
                co_description,
                blooms_level,
                is_active
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            course_id,
            cleaned_code,
            cleaned_desc,
            blooms_level,
            is_active
        ))
        conn.commit()


# ==========================================================
# Update Course Outcome
# ==========================================================
def update_co(id, course_id, co_code, co_description, blooms_level, is_active):
    cleaned_code = co_code.upper().strip() if co_code else ""
    cleaned_desc = co_description.strip() if co_description else ""

    with get_connection() as conn:
        conn.execute("""
            UPDATE CourseOutcome
            SET
                course_id = ?,
                co_code = ?,
                co_description = ?,
                blooms_level = ?,
                is_active = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            course_id,
            cleaned_code,
            cleaned_desc,
            blooms_level,
            is_active,
            id
        ))
        conn.commit()


# ==========================================================
# Soft Delete Course Outcome
# ==========================================================
def delete_co(id):
    with get_connection() as conn:
        conn.execute("""
            UPDATE CourseOutcome
            SET
                is_active = 0,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (id,))
        conn.commit()


# ==========================================================
# Get Course-wise COs
# ==========================================================
def get_course_cos(course_id):
    with get_connection() as conn:
        return conn.execute("""
            SELECT *
            FROM CourseOutcome
            WHERE course_id = ?
              AND is_active = 1
            ORDER BY co_code
        """, (course_id,)).fetchall()


# ==========================================================
# Get Active Course Outcomes
# ==========================================================
def get_active_cos():
    with get_connection() as conn:
        return conn.execute("""
            SELECT
                co.id,
                co.course_id,
                c.course_code,
                c.course_name,
                co.co_code,
                co.co_description,
                co.blooms_level,
                co.is_active
            FROM CourseOutcome co
            INNER JOIN Course c ON co.course_id = c.id
            WHERE co.is_active = 1
            ORDER BY c.course_code, co.co_code
        """).fetchall()
# ==========================================================
# Get COs by Course
# ==========================================================

def get_cos_by_course(course_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM CourseOutcome

        WHERE course_id = ?
        AND is_active = 1

        ORDER BY id

    """, (course_id,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]
