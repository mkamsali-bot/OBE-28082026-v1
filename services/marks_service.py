import sqlite3

DATABASE = "obe.db"


# ==========================================================
# Database Connection
# ==========================================================

def get_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


# ==========================================================
# Convert Row to Dictionary
# ==========================================================

def row_to_dict(row):

    return dict(row)


# ==========================================================
# Get Marks for a Course & Assessment
# ==========================================================

def get_marks(

    course_id,

    assessment_component

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM Marks

        WHERE course_id=?

        AND assessment_component=?

        ORDER BY student_id, co_id

    """,(course_id,assessment_component))

    rows = cursor.fetchall()

    conn.close()

    return [row_to_dict(r) for r in rows]
    # ==========================================================
# Save Marks
# ==========================================================

def save_marks(

    course_id,

    assessment_component,

    student_ids,

    co_ids,

    marks

):

    conn = get_connection()

    cursor = conn.cursor()

    for student_id, co_id, mark in zip(student_ids, co_ids, marks):

        cursor.execute("""

            SELECT id

            FROM Marks

            WHERE course_id=?

            AND assessment_component=?
            AND student_id=?
            AND co_id=?

        """, (

            course_id,
            assessment_component,
            student_id,
            co_id

        ))

        existing = cursor.fetchone()

        if existing:

            cursor.execute("""

                UPDATE Marks

                SET

                    marks=?,
                    updated_at=CURRENT_TIMESTAMP

                WHERE id=?

            """, (

                mark,
                existing["id"]

            ))

        else:

            cursor.execute("""

                INSERT INTO Marks(

                    course_id,
                    assessment_component,
                    student_id,
                    co_id,
                    marks,
                    created_at

                )

                VALUES(

                    ?,?,?,?,?,CURRENT_TIMESTAMP

                )

            """, (

                course_id,
                assessment_component,
                student_id,
                co_id,
                mark

            ))

    conn.commit()

    conn.close()
    # ==========================================================
# Delete Marks
# ==========================================================

def delete_marks(

    course_id,

    assessment_component

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        DELETE FROM Marks

        WHERE course_id=?
        AND assessment_component=?

    """, (

        course_id,

        assessment_component

    ))

    conn.commit()

    conn.close()


# ==========================================================
# Get Marks by Student
# ==========================================================

def get_marks_by_student(

    student_id

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM Marks

        WHERE student_id=?

        ORDER BY course_id,
                 assessment_component,
                 co_id

    """, (

        student_id,

    ))

    rows = cursor.fetchall()

    conn.close()

    return [row_to_dict(row) for row in rows]


# ==========================================================
# Get Marks by Course
# ==========================================================

def get_marks_by_course(

    course_id

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM Marks

        WHERE course_id=?

        ORDER BY reg_no,
         assessment_component
    """, (

        course_id,

    ))

    rows = cursor.fetchall()

    conn.close()

    return [row_to_dict(row) for row in rows]
    # ==========================================================
# Check Whether Marks Exist
# ==========================================================

def marks_exist(

    course_id,

    assessment_component

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM Marks

        WHERE course_id=?
        AND assessment_component=?

    """, (

        course_id,

        assessment_component

    ))

    count = cursor.fetchone()[0]

    conn.close()

    return count > 0


# ==========================================================
# Get Marks for One Student & One Assessment
# ==========================================================

def get_student_marks(

    course_id,

    student_id,

    assessment_component

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM Marks

        WHERE course_id=?
        AND student_id=?
        AND assessment_component=?

        ORDER BY co_id

    """, (

        course_id,

        student_id,

        assessment_component

    ))

    rows = cursor.fetchall()

    conn.close()

    return [row_to_dict(row) for row in rows]


# ==========================================================
# Get Marks for One CO
# ==========================================================

def get_co_marks(

    course_id,

    co_id,

    assessment_component

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM Marks

        WHERE course_id=?
        AND co_id=?
        AND assessment_component=?

        ORDER BY student_id

    """, (

        course_id,

        co_id,

        assessment_component

    ))

    rows = cursor.fetchall()

    conn.close()

    return [row_to_dict(row) for row in rows]


# ==========================================================
# Count Marks Entries
# ==========================================================

def count_marks(

    course_id

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM Marks

        WHERE course_id=?

    """, (

        course_id,

    ))

    total = cursor.fetchone()[0]

    conn.close()

    return total
    # ==========================================================
# Update One Mark
# ==========================================================

def update_mark(

    mark_id,

    marks

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        UPDATE Marks

        SET

            marks=?,

            updated_at=CURRENT_TIMESTAMP

        WHERE id=?

    """,(marks, mark_id))

    conn.commit()

    conn.close()


# ==========================================================
# Delete Marks of One Student
# ==========================================================

def delete_student_marks(

    course_id,

    student_id,

    assessment_component

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        DELETE FROM Marks

        WHERE course_id=?
        AND student_id=?
        AND assessment_component=?

    """,(course_id, student_id, assessment_component))

    conn.commit()

    conn.close()


# ==========================================================
# Assessment Summary
# ==========================================================

def get_assessment_summary(

    course_id,

    assessment_component

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            co_id,

            COUNT(*) AS students,

            AVG(marks) AS average_marks,

            MIN(marks) AS minimum_marks,

            MAX(marks) AS maximum_marks

        FROM Marks

        WHERE course_id=?
        AND assessment_component=?

        GROUP BY co_id

        ORDER BY co_id

    """,(course_id, assessment_component))

    rows = cursor.fetchall()

    conn.close()

    return [row_to_dict(row) for row in rows]


# ==========================================================
# Get All Marks
# ==========================================================

def get_all_marks():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM Marks

        ORDER BY

            course_id,

            assessment_component,

            student_id,

            co_id

    """)

    rows = cursor.fetchall()

    conn.close()

    return [row_to_dict(row) for row in rows]