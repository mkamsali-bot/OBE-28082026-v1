from typing import Annotated

from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.nba_report1_service import get_student_marks
from io import BytesIO
from fastapi.responses import StreamingResponse

from services.report1_excel_service import generate_student_marks_excel


from services.course_service import (
    get_all_courses,
    get_courses_by_semester,
)

from services.nba_report_service import (
    get_course_type,
    get_course_details,
)

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/nba-reports", response_class=HTMLResponse)
def nba_reports(
    request: Request,
    semester: Annotated[int | None, Query(ge=1, le=8)] = None,
    course_id: str | None = None,
):

    if semester:
        courses = get_courses_by_semester(semester)
    else:
        courses = []

    course_type = None
    course = None
    course_id_int = None

    if course_id and course_id.strip():
        course_id_int = int(course_id)
        course_type = get_course_type(course_id_int)
        course = get_course_details(course_id_int)

    return templates.TemplateResponse(
        request=request,
        name="nba_reports.html",
        context={
            "title": "NBA Reports",
            "courses": courses,
            "semester": semester,
            "course_id": course_id_int,
            "course_type": course_type,
            "course": course,
        }
    )



@router.get("/nba-report1")
def nba_report1(course_id: int):

    wb = generate_student_marks_excel(course_id)

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition":
            'attachment; filename="Student_Marks_Register.xlsx"'
        }
    )