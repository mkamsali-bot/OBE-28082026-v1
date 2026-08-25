from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from services.course_service import get_all_courses

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# ==========================================================
# Marks Entry Home
# ==========================================================

@router.get("/marks")
def marks(
    request: Request,
    course_id: int | None = None
):

    courses = get_all_courses()

    selected_course = None

    if course_id:

        for course in courses:

            if course["id"] == course_id:
                selected_course = course
                break

    return templates.TemplateResponse(
        "marks.html",
        {
            "request": request,
            "title": "Marks Entry",
            "courses": courses,
            "selected_course": selected_course,
            "course_id": course_id
        }
    )
    from services.student_service import get_students_by_course
from services.co_service import get_cos_by_course
from services.co_weightage_service import get_course_type


# ==========================================================
# Load Students for Selected Course
# ==========================================================

@router.get("/marks/load")
def load_marks(
    request: Request,
    course_id: int
):

    courses = get_all_courses()

    students = get_students_by_course(course_id)

    cos = get_cos_by_course(course_id)

    course_type = get_course_type(course_id)

    assessment_components = []

    if course_type == "Theory":

        assessment_components = [
            "LE",
            "SE1",
            "SE2"
        ]

    elif course_type == "Theory + Practical":

        assessment_components = [
            "LE",
            "SE1",
            "SE2",
            "MID1",
            "MID2",
            "Record"
        ]

    elif course_type == "Capstone Project":

        assessment_components = [
            "Evaluation"
        ]

    elif course_type == "Internship":

        assessment_components = [
            "Evaluation"
        ]

    return templates.TemplateResponse(
        "marks.html",
        {
            "request": request,
            "title": "Marks Entry",
            "courses": courses,
            "selected_course": next(
                (c for c in courses if c["id"] == course_id),
                None
            ),
            "course_id": course_id,
            "students": students,
            "cos": cos,
            "course_type": course_type,
            "assessment_components": assessment_components
        }
    )
    from fastapi import Form
from fastapi.responses import RedirectResponse

from services.marks_service import save_marks


# ==========================================================
# Save Marks
# ==========================================================

@router.post("/marks/save")
def save_student_marks(

    course_id: int = Form(...),

    assessment_component: str = Form(...),

    student_id: list[int] = Form(...),

    co_id: list[int] = Form(...),

    marks: list[float] = Form(...)

):

    save_marks(

        course_id=course_id,

        assessment_component=assessment_component,

        student_ids=student_id,

        co_ids=co_id,

        marks=marks

    )

    return RedirectResponse(

        url=f"/marks/load?course_id={course_id}",

        status_code=303

    )
    from fastapi.responses import JSONResponse

from services.marks_service import (
    get_marks,
    delete_marks
)


# ==========================================================
# View Marks
# ==========================================================

@router.get("/marks/view")
def view_marks(

    request: Request,

    course_id: int,

    assessment_component: str

):

    courses = get_all_courses()

    students = get_students_by_course(course_id)

    cos = get_cos_by_course(course_id)

    saved_marks = get_marks(

        course_id=course_id,

        assessment_component=assessment_component

    )

    return templates.TemplateResponse(

        "marks.html",

        {

            "request": request,

            "title": "Marks Entry",

            "courses": courses,

            "selected_course": next(
                (c for c in courses if c["id"] == course_id),
                None
            ),

            "course_id": course_id,

            "students": students,

            "cos": cos,

            "assessment_component": assessment_component,

            "saved_marks": saved_marks

        }

    )


# ==========================================================
# Delete Marks
# ==========================================================

@router.post("/marks/delete")
def remove_marks(

    course_id: int = Form(...),

    assessment_component: str = Form(...)

):

    delete_marks(

        course_id=course_id,

        assessment_component=assessment_component

    )

    return RedirectResponse(

        url=f"/marks/load?course_id={course_id}",

        status_code=303

    )


# ==========================================================
# Assessment Components (AJAX)
# ==========================================================

@router.get("/marks/components/{course_id}")
def assessment_components(course_id: int):

    course_type = get_course_type(course_id)

    if course_type == "Theory":

        components = [
            "LE",
            "SE1",
            "SE2"
        ]

    elif course_type == "Theory + Practical":

        components = [
            "LE",
            "SE1",
            "SE2",
            "MID1",
            "MID2",
            "Record"
        ]

    elif course_type in ("Capstone Project", "Internship"):

        components = [
            "Evaluation"
        ]

    else:

        components = []

    return JSONResponse(

        {

            "course_type": course_type,

            "assessment_components": components

        }

    )