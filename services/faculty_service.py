from database import get_connection


# ---------------------------------------------------------
# Get All Faculties
# ---------------------------------------------------------
def get_all_faculties():

    conn = get_connection()

    rows = conn.execute("""

        SELECT
            Faculty.*,
            Department.department_name

        FROM Faculty

        LEFT JOIN Department
            ON Faculty.department_id = Department.id

        ORDER BY faculty_code

    """).fetchall()

    conn.close()

    return rows


# ---------------------------------------------------------
# Get One Faculty
# ---------------------------------------------------------
def get_faculty(id):

    conn = get_connection()

    row = conn.execute("""

        SELECT *

        FROM Faculty

        WHERE id=?

    """, (id,)).fetchone()

    conn.close()

    return row


# ---------------------------------------------------------
# Check Duplicate Faculty Code
# ---------------------------------------------------------
def faculty_exists(code):

    conn = get_connection()

    row = conn.execute("""

        SELECT id

        FROM Faculty

        WHERE faculty_code=?

    """, (code.upper(),)).fetchone()

    conn.close()

    return row


# ---------------------------------------------------------
# Add Faculty
# ---------------------------------------------------------
def add_faculty(
    code,
    name,
    designation,
    email,
    mobile,
    department_id,
    active
):

    conn = get_connection()

    conn.execute("""

        INSERT INTO Faculty
        (
            faculty_code,
            faculty_name,
            designation,
            email,
            mobile,
            department_id,
            is_active
        )

        VALUES
        (
            ?,?,?,?,?,?,?
        )

    """,
    (
        code.upper(),
        name.strip(),
        designation.strip(),
        email.strip(),
        mobile.strip(),
        department_id,
        active
    ))

    conn.commit()
    conn.close()


# ---------------------------------------------------------
# Update Faculty
# ---------------------------------------------------------
def update_faculty(
    id,
    code,
    name,
    designation,
    email,
    mobile,
    department_id,
    active
):

    conn = get_connection()

    conn.execute("""

        UPDATE Faculty

        SET

            faculty_code=?,
            faculty_name=?,
            designation=?,
            email=?,
            mobile=?,
            department_id=?,
            is_active=?,
            updated_at=CURRENT_TIMESTAMP

        WHERE id=?

    """,
    (
        code.upper(),
        name.strip(),
        designation.strip(),
        email.strip(),
        mobile.strip(),
        department_id,
        active,
        id
    ))

    conn.commit()
    conn.close()


# ---------------------------------------------------------
# Soft Delete
# ---------------------------------------------------------
def delete_faculty(id):

    conn = get_connection()

    conn.execute("""

        UPDATE Faculty

        SET

            is_active=0,
            updated_at=CURRENT_TIMESTAMP

        WHERE id=?

    """,
    (id,)
    )

    conn.commit()
    conn.close()