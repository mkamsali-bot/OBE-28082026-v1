import sqlite3

DB_NAME = "obe.db"


# ==========================================================
# Database Connection
# ==========================================================
def get_connection():

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    return conn


# ==========================================================
# Get All Programs
# ==========================================================
def get_all_programs():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            p.id,
            p.program_code,
            p.program_name,
            p.department_id,
            p.duration,
            p.is_active,

            d.department_code,
            d.department_name

        FROM Program p

        INNER JOIN Department d

            ON p.department_id = d.id

        ORDER BY

            p.program_code

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================================================
# Get Active Programs
# ==========================================================
def get_active_programs():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM Program

        WHERE is_active = 1

        ORDER BY program_code

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================================================
# Get Program By ID
# ==========================================================
def get_program(program_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM Program

        WHERE id = ?

    """, (program_id,))

    row = cursor.fetchone()

    conn.close()

    return row


# ==========================================================
# Check Duplicate Program
# ==========================================================
def program_exists(program_code):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT id

        FROM Program

        WHERE program_code = ?

    """, (program_code,))

    row = cursor.fetchone()

    conn.close()

    return row is not None


# ==========================================================
# Add Program
# ==========================================================
def add_program(

    program_code,
    program_name,
    department_id,
    duration,
    is_active

):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO Program(

            program_code,
            program_name,
            department_id,
            duration,
            is_active

        )

        VALUES(

            ?, ?, ?, ?, ?

        )

    """, (

        program_code,
        program_name,
        department_id,
        duration,
        is_active

    ))

    conn.commit()

    conn.close()


# ==========================================================
# Update Program
# ==========================================================
def update_program(

    program_id,

    program_code,
    program_name,
    department_id,
    duration,
    is_active

):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        UPDATE Program

        SET

            program_code = ?,
            program_name = ?,
            department_id = ?,
            duration = ?,
            is_active = ?

        WHERE id = ?

    """, (

        program_code,
        program_name,
        department_id,
        duration,
        is_active,

        program_id

    ))

    conn.commit()

    conn.close()


# ==========================================================
# Delete Program
# ==========================================================
def delete_program(program_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        DELETE

        FROM Program

        WHERE id = ?

    """, (program_id,))

    conn.commit()

    conn.close()