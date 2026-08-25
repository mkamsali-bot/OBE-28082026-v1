from database import get_connection


# ==========================================================
# Get All PSOs
# ==========================================================
def get_all_psos():

    conn = get_connection()

    rows = conn.execute("""

        SELECT

            ProgramSpecificOutcome.id,
            ProgramSpecificOutcome.pso_code,
            ProgramSpecificOutcome.pso_description,
            ProgramSpecificOutcome.department_id,
            ProgramSpecificOutcome.is_active,
            Department.department_name

        FROM ProgramSpecificOutcome

        LEFT JOIN Department
            ON ProgramSpecificOutcome.department_id = Department.id

        ORDER BY

            Department.department_name,
            ProgramSpecificOutcome.pso_code

    """).fetchall()

    conn.close()

    return rows


# ==========================================================
# Get Single PSO
# ==========================================================
def get_pso(id):

    conn = get_connection()

    row = conn.execute("""

        SELECT *

        FROM ProgramSpecificOutcome

        WHERE id = ?

    """, (id,)).fetchone()

    conn.close()

    return row


# ==========================================================
# Check Duplicate PSO
# ==========================================================
def pso_exists(pso_code, department_id):

    conn = get_connection()

    row = conn.execute("""

        SELECT id

        FROM ProgramSpecificOutcome

        WHERE

            UPPER(pso_code)=UPPER(?)
            AND department_id=?

    """, (

        pso_code,
        department_id

    )).fetchone()

    conn.close()

    return row is not None


# ==========================================================
# Add PSO
# ==========================================================
def add_pso(

    pso_code,
    pso_description,
    department_id,
    is_active

):

    conn = get_connection()

    conn.execute("""

        INSERT INTO ProgramSpecificOutcome
        (

            pso_code,
            pso_description,
            department_id,
            is_active

        )

        VALUES
        (
            ?, ?, ?, ?
        )

    """, (

        pso_code.upper(),
        pso_description.strip(),
        department_id,
        is_active

    ))

    conn.commit()
    conn.close()


# ==========================================================
# Update PSO
# ==========================================================
def update_pso(

    id,
    pso_code,
    pso_description,
    department_id,
    is_active

):

    conn = get_connection()

    conn.execute("""

        UPDATE ProgramSpecificOutcome

        SET

            pso_code=?,
            pso_description=?,
            department_id=?,
            is_active=?,
            updated_at=CURRENT_TIMESTAMP

        WHERE id=?

    """, (

        pso_code.upper(),
        pso_description.strip(),
        department_id,
        is_active,
        id

    ))

    conn.commit()
    conn.close()


# ==========================================================
# Soft Delete
# ==========================================================
def delete_pso(id):

    conn = get_connection()

    conn.execute("""

        UPDATE ProgramSpecificOutcome

        SET

            is_active=0,
            updated_at=CURRENT_TIMESTAMP

        WHERE id=?

    """, (id,))

    conn.commit()
    conn.close()


# ==========================================================
# Load Default PSOs
# ==========================================================
def load_default_psos(department_id):

    conn = get_connection()

    count = conn.execute("""

        SELECT COUNT(*)

        FROM ProgramSpecificOutcome

        WHERE department_id=?

    """, (department_id,)).fetchone()[0]

    if count > 0:

        conn.close()
        return False

    default_psos = [

        (
            "PSO1",
            "Ability to apply domain knowledge to identify, analyze and solve discipline-specific engineering problems."
        ),

        (
            "PSO2",
            "Ability to design, develop and implement engineering solutions using modern engineering tools and technologies."
        ),

        (
            "PSO3",
            "Ability to pursue higher education, research, entrepreneurship and professional practice with ethics and lifelong learning."
        )

    ]

    for code, description in default_psos:

        conn.execute("""

            INSERT INTO ProgramSpecificOutcome
            (

                pso_code,
                pso_description,
                department_id,
                is_active

            )

            VALUES
            (
                ?, ?, ?, 1
            )

        """, (

            code,
            description,
            department_id

        ))

    conn.commit()
    conn.close()

    return True