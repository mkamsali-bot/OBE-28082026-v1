from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font

from services.nba_report1_service import get_student_marks
from services.nba_report_service import (
    get_course_details,
    get_course_type,
)


def generate_student_marks_excel(course_id):
    wb = Workbook()
    ws = wb.active
    ws.title = "Student Marks Register"

    course = get_course_details(course_id)
    course_type = get_course_type(course_id)
    students = get_student_marks(course_id)

    ws["A1"] = "NBA REPORT 1"
    ws["A2"] = "Student Marks Register"

    ws["A1"].font = Font(size=16, bold=True)
    ws["A2"].font = Font(size=14, bold=True)

    ws["A4"] = "Course Code"
    ws["B4"] = course["course_code"]

    ws["A5"] = "Course Name"
    ws["B5"] = course["course_name"]

    ws["A6"] = "Course Type"
    ws["B6"] = course_type

    if course_type == "Theory":
        headers = ["Reg No", "Student Name", "LE", "SE1", "SE2"]

    elif course_type == "Theory + Practical":
        headers = [
            "Reg No",
            "Student Name",
            "LE",
            "SE1",
            "SE2",
            "MID1",
            "MID2",
            "Record",
            "Final Theory",
            "Final Practical",
        ]

    elif course_type == "Capstone Project":
        headers = ["Reg No", "Student Name", "Evaluation"]

    elif course_type == "Internship":
        headers = ["Reg No", "Student Name", "Evaluation"]

    header_row = 8

    for col, header in enumerate(headers, start=1):
        cell = ws.cell(row=header_row, column=col)
        cell.value = header
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")

    data_row = header_row + 1

    for student in students:
        ws.cell(row=data_row, column=1).value = student["reg_no"]
        ws.cell(row=data_row, column=2).value = student["student_name"]
        ws.cell(row=data_row, column=3).value = student.get("LE", "")
        ws.cell(row=data_row, column=4).value = student.get("SE1", "")
        ws.cell(row=data_row, column=5).value = student.get("SE2", "")

        data_row += 1

    return wb