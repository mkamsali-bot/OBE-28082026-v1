from database import get_connection


# ---------------------------------------------------------
# Get All Program Outcomes
# ---------------------------------------------------------
def get_all_pos():

    conn = get_connection()

    rows = conn.execute("""

        SELECT

            ProgramOutcome.*,
            Department.department_name

        FROM ProgramOutcome

        LEFT JOIN Department
            ON ProgramOutcome.department_id = Department.id

        ORDER BY
            Department.department_name,
            ProgramOutcome.po_code

    """).fetchall()

    conn.close()

    return rows


# ---------------------------------------------------------
# Get One Program Outcome
# ---------------------------------------------------------
def get_po(id):

    conn = get_connection()

    row = conn.execute("""

        SELECT *

        FROM ProgramOutcome

        WHERE id=?

    """, (id,)).fetchone()

    conn.close()

    return row


# ---------------------------------------------------------
# Check Duplicate PO
# ---------------------------------------------------------
def po_exists(po_code, department_id):

    conn = get_connection()

    row = conn.execute("""

        SELECT id

        FROM ProgramOutcome

        WHERE

            po_code=?
            AND department_id=?

    """, (

        po_code.upper(),
        department_id

    )).fetchone()

    conn.close()

    return row


# ---------------------------------------------------------
# Add PO
# ---------------------------------------------------------
def add_po(

    po_code,
    po_description,
    department_id,
    is_active

):

    conn = get_connection()

    conn.execute("""

        INSERT INTO ProgramOutcome
        (

            po_code,
            po_description,
            department_id,
            is_active

        )

        VALUES
        (
            ?,?,?,?
        )

    """, (

        po_code.upper(),
        po_description.strip(),
        department_id,
        is_active

    ))

    conn.commit()
    conn.close()


# ---------------------------------------------------------
# Update PO
# ---------------------------------------------------------
def update_po(

    id,
    po_code,
    po_description,
    department_id,
    is_active

):

    conn = get_connection()

    conn.execute("""

        UPDATE ProgramOutcome

        SET

            po_code=?,
            po_description=?,
            department_id=?,
            is_active=?,
            updated_at=CURRENT_TIMESTAMP

        WHERE id=?

    """, (

        po_code.upper(),
        po_description.strip(),
        department_id,
        is_active,
        id

    ))

    conn.commit()
    conn.close()


# ---------------------------------------------------------
# Soft Delete
# ---------------------------------------------------------
def delete_po(id):

    conn = get_connection()

    conn.execute("""

        UPDATE ProgramOutcome

        SET

            is_active=0,
            updated_at=CURRENT_TIMESTAMP

        WHERE id=?

    """, (id,))

    conn.commit()
    conn.close()


# ---------------------------------------------------------
# Load Default AICTE / NBA Program Outcomes
# ---------------------------------------------------------
def load_default_pos(department_id):

    conn = get_connection()

    count = conn.execute("""

        SELECT COUNT(*)

        FROM ProgramOutcome

        WHERE department_id=?

    """, (department_id,)).fetchone()[0]

    if count > 0:
        conn.close()
        return False

    default_pos = [

        ("PO1", "Engineering knowledge: Apply the knowledge of mathematics, science, engineering fundamentals and an engineering specialization to solve complex engineering problems."),

        ("PO2", "Problem analysis: Identify, formulate, review research literature and analyze complex engineering problems using first principles of mathematics, natural sciences and engineering sciences."),

        ("PO3", "Design/development of solutions: Design solutions for complex engineering problems and design system components or processes that meet specified needs with due consideration for public health, safety and environmental factors."),

        ("PO4", "Conduct investigations of complex problems using research-based knowledge, including design of experiments, analysis and interpretation of data and synthesis of information."),

        ("PO5", "Modern tool usage: Create, select and apply appropriate techniques, resources and modern engineering and IT tools with an understanding of their limitations."),

        ("PO6", "The engineer and society: Apply reasoning informed by contextual knowledge to assess societal, health, safety, legal and cultural issues relevant to professional engineering practice."),

        ("PO7", "Environment and sustainability: Understand the impact of professional engineering solutions in societal and environmental contexts and demonstrate knowledge of sustainable development."),

        ("PO8", "Ethics: Apply ethical principles and commit to professional ethics, responsibilities and norms of engineering practice."),

        ("PO9", "Individual and teamwork: Function effectively as an individual and as a member or leader in diverse and multidisciplinary teams."),

        ("PO10", "Communication: Communicate effectively on complex engineering activities with the engineering community and society at large."),

        ("PO11", "Project management and finance: Demonstrate knowledge and understanding of engineering management principles and apply them as a member or leader to manage projects."),

        ("PO12", "Life-long learning: Recognize the need for and have the preparation and ability to engage in independent and life-long learning.")

    ]

    for code, description in default_pos:

        conn.execute("""

            INSERT INTO ProgramOutcome
            (

                po_code,
                po_description,
                department_id,
                is_active

            )

            VALUES
            (
                ?,?,?,1
            )

        """, (

            code,
            description,
            department_id

        ))

    conn.commit()
    conn.close()

    return True