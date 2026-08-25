from database import get_connection

# =====================================================
# READ OPERATIONS
# =====================================================

def get_all_courses():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                c.*,
                d.department_name,
                p.program_name,
                f.faculty_name
            FROM Course c
            LEFT JOIN Department d ON c.department_id = d.id
            LEFT JOIN Program p ON c.program_id = p.id
            LEFT JOIN Faculty f ON c.faculty_id = f.id
            WHERE c.is_active = 1
            ORDER BY c.course_code
        """)
        return cursor.fetchall()


def get_course(course_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT *
            FROM Course
            WHERE id = ?
        """, (course_id,))
        return cursor.fetchone()


def get_all_programs():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, program_code, program_name, department_id
            FROM Program
            WHERE is_active = 1
            ORDER BY program_name
        """)
        return cursor.fetchall()


def get_all_faculties():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, faculty_code, faculty_name, department_id
            FROM Faculty
            WHERE is_active = 1
            ORDER BY faculty_name
        """)
        return cursor.fetchall()


def course_exists(course_code, exclude_id=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        if exclude_id:
            cursor.execute("""
                SELECT COUNT(*) FROM Course 
                WHERE course_code = ? AND id != ?
            """, (course_code, exclude_id))
        else:
            cursor.execute("""
                SELECT COUNT(*) FROM Course 
                WHERE course_code = ?
            """, (course_code,))
        return cursor.fetchone()[0] > 0


# =====================================================
# WRITE OPERATIONS
# =====================================================

def add_course(
    course_code,
    course_name,
    department_id,
    program_id,
    faculty_id,
    semester,
    credits,
    regulation,
    course_type,
    is_active=1
):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Course (
                course_code, course_name, department_id, program_id, 
                faculty_id, semester, credits, regulation, 
                course_type, is_active
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            course_code, course_name, department_id, program_id,
            faculty_id, semester, credits, regulation,
            course_type, is_active
        ))
        conn.commit()


def update_course(
    course_id,
    course_code,
    course_name,
    department_id,
    program_id,
    faculty_id,
    semester,
    credits,
    regulation,
    course_type,
    is_active
):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Course
            SET
                course_code = ?,
                course_name = ?,
                department_id = ?,
                program_id = ?,
                faculty_id = ?,
                semester = ?,
                credits = ?,
                regulation = ?,
                course_type = ?,
                is_active = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            course_code, course_name, department_id, program_id,
            faculty_id, semester, credits, regulation,
            course_type, is_active, course_id
        ))
        conn.commit()


def delete_course(course_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Course
            SET
                is_active = 0,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (course_id,))
        conn.commit()


# =====================================================
# ALIASES & COMPATIBILITY
# =====================================================

def get_active_courses():
    return get_all_courses()
from database import get_connection

def get_courses_by_semester(semester):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM course
        WHERE semester = ?
        ORDER BY course_code
    """, (semester,))

    courses = cursor.fetchall()

    conn.close()

    return courses