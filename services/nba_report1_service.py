from database import get_connection
from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

from services.nba_report_service import (
    get_course_details,
    get_course_type,
)
def get_student_marks(course_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            reg_no,
            student_name,
            assessment_component,
            marks
        FROM Marks
        WHERE course_id = ?
        ORDER BY reg_no, assessment_component
    """, (course_id,))

    rows = cursor.fetchall()
    conn.close()

    students = {}

    for row in rows:

        reg_no = row["reg_no"]

        if reg_no not in students:

            students[reg_no] = {
                "reg_no": reg_no,
                "student_name": row["student_name"]
            }

        students[reg_no][row["assessment_component"]] = row["marks"]

    return list(students.values())