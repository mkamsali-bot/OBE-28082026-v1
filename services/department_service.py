from database import get_connection


def get_all_departments():
    conn = get_connection()

    rows = conn.execute("""
        SELECT *
        FROM Department
        ORDER BY department_code
    """).fetchall()

    conn.close()
    return rows


def get_department(id):
    conn = get_connection()

    row = conn.execute(
        "SELECT * FROM Department WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()
    return row


def department_exists(code):
    conn = get_connection()

    row = conn.execute(
        "SELECT id FROM Department WHERE department_code=?",
        (code.upper(),)
    ).fetchone()

    conn.close()
    return row is not None  # Explicitly returns True or False


def add_department(code, name, active):
    conn = get_connection()

    conn.execute("""
        INSERT INTO Department
        (
            department_code,
            department_name,
            is_active
        )
        VALUES
        (
            ?,?,?
        )
    """,
    (
        code.upper(),
        name.strip(),
        active
    ))

    conn.commit()
    conn.close()


def update_department(id, code, name, active):
    conn = get_connection()

    conn.execute("""
        UPDATE Department
        SET
            department_code=?,
            department_name=?,
            is_active=?,
            updated_at=CURRENT_TIMESTAMP
        WHERE id=?
    """,
    (
        code.upper(),
        name.strip(),
        active,
        id
    ))

    conn.commit()
    conn.close()


def delete_department(id):
    conn = get_connection()

    conn.execute("""
        UPDATE Department
        SET
            is_active=0,
            updated_at=CURRENT_TIMESTAMP
        WHERE id=?
    """,
    (id,)
    )

    conn.commit()
    conn.close()


def get_active_departments():
    conn = get_connection()

    rows = conn.execute("""
        SELECT
            id,
            department_name
        FROM Department
        WHERE is_active = 1
        ORDER BY department_name
    """).fetchall()

    conn.close()
    return rows