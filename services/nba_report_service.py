from database import get_connection



def get_course_type(course_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT course_type
        FROM Course
        WHERE id = ?
    """, (course_id,))

    row = cursor.fetchone()

    conn.close()

    print("Course Type from DB:", row)

    return row["course_type"]

from database import get_connection

def get_course_details(course_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM course
        WHERE id = ?
    """, (course_id,))

    course = cursor.fetchone()

    conn.close()

    return course