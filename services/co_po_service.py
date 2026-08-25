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
# Get All CO-PO Mappings
# ==========================================================
def get_all_mappings():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            m.id,

            m.course_id,
            c.course_code,
            c.course_name,

            m.co_id,
            co.co_code,

            m.po1,
            m.po2,
            m.po3,
            m.po4,
            m.po5,
            m.po6,
            m.po7,
            m.po8,
            m.po9,
            m.po10,
            m.po11,
            m.po12,

            m.pso1,
            m.pso2,
            m.pso3,

            m.is_active

        FROM CO_PO_Mapping m

        INNER JOIN Course c
            ON m.course_id = c.id

        INNER JOIN CourseOutcome co
            ON m.co_id = co.id

        ORDER BY
            c.course_code,
            co.co_code
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================================================
# Get One Mapping
# ==========================================================
def get_mapping(mapping_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM CO_PO_Mapping
        WHERE id = ?
    """, (mapping_id,))

    row = cursor.fetchone()

    conn.close()

    return row


# ==========================================================
# Check Existing Mapping
# ==========================================================
def mapping_exists(course_id, co_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM CO_PO_Mapping
        WHERE course_id = ?
          AND co_id = ?
    """, (course_id, co_id))

    row = cursor.fetchone()

    conn.close()

    return row is not None


# ==========================================================
# Add Mapping
# ==========================================================
def add_mapping(

    course_id,
    co_id,

    po1,
    po2,
    po3,
    po4,
    po5,
    po6,
    po7,
    po8,
    po9,
    po10,
    po11,
    po12,

    pso1,
    pso2,
    pso3,

    is_active

):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO CO_PO_Mapping(

            course_id,
            co_id,

            po1,
            po2,
            po3,
            po4,
            po5,
            po6,
            po7,
            po8,
            po9,
            po10,
            po11,
            po12,

            pso1,
            pso2,
            pso3,

            is_active

        )

        VALUES(

            ?, ?,

            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,

            ?, ?, ?,

            ?

        )

    """, (

        course_id,
        co_id,

        po1,
        po2,
        po3,
        po4,
        po5,
        po6,
        po7,
        po8,
        po9,
        po10,
        po11,
        po12,

        pso1,
        pso2,
        pso3,

        is_active

    ))

    conn.commit()
    conn.close()


# ==========================================================
# Update Mapping
# ==========================================================
def update_mapping(

    mapping_id,

    course_id,
    co_id,

    po1,
    po2,
    po3,
    po4,
    po5,
    po6,
    po7,
    po8,
    po9,
    po10,
    po11,
    po12,

    pso1,
    pso2,
    pso3,

    is_active

):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        UPDATE CO_PO_Mapping

        SET

            course_id=?,
            co_id=?,

            po1=?,
            po2=?,
            po3=?,
            po4=?,
            po5=?,
            po6=?,
            po7=?,
            po8=?,
            po9=?,
            po10=?,
            po11=?,
            po12=?,

            pso1=?,
            pso2=?,
            pso3=?,

            is_active=?

        WHERE id=?

    """, (

        course_id,
        co_id,

        po1,
        po2,
        po3,
        po4,
        po5,
        po6,
        po7,
        po8,
        po9,
        po10,
        po11,
        po12,

        pso1,
        pso2,
        pso3,

        is_active,

        mapping_id

    ))

    conn.commit()
    conn.close()


# ==========================================================
# Delete Mapping
# ==========================================================
def delete_mapping(mapping_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        DELETE
        FROM CO_PO_Mapping

        WHERE id = ?

    """, (mapping_id,))

    conn.commit()
    conn.close()
def get_course_mappings(course_id):
    """
    Returns all CO-PO/PSO mappings for a course.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM CO_PO_Mapping
        WHERE course_id = ?
          AND is_active = 1
        ORDER BY co_id
    """, (course_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows