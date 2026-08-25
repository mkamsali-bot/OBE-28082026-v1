from typing import Optional

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from services.course_service import (
    get_all_courses,
    get_course,
    course_exists,
    add_course,
    update_course,
    delete_course,
    get_all_programs,
    get_all_faculties
)
from services.department_service import (
    get_all_departments
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ---------------------------------------------------------
# Helper Validation
# ---------------------------------------------------------
def validate_course(
    course_code: str,
    course_name: str,
    semester: int,
    credits: float
) -> list[str]:
    errors = []

    if not course_code.strip():
        errors.append("Course Code is required.")

    if not course_name.strip():
        errors.append("Course Name is required.")

    if semester < 1 or semester > 8:
        errors.append("Semester must be between 1 and 8.")

    if credits < 0:
        errors.append("Credits cannot be negative.")

    return errors


# ---------------------------------------------------------
# Course List View
# ---------------------------------------------------------
@router.get("/course")
def course(request: Request):
    courses = get_all_courses()
    departments = get_all_departments()
    programs = get_all_programs()
    faculties = get_all_faculties()

    return templates.TemplateResponse(
        request=request,
        name="course.html",
        context={
            "title": "Course Master",
            "courses": courses,
            "departments": departments,
            "programs": programs,
            "faculties": faculties,
            "course": None
        }
    )


# ---------------------------------------------------------
# Save Course
# ---------------------------------------------------------
@router.post("/course/save")
def save_course(
    course_code: str = Form(...),
    course_name: str = Form(...),
    department_id: int = Form(...),
    program_id: int = Form(...),
    faculty_id: Optional[int] = Form(None),
    semester: int = Form(...),
    credits: float = Form(...),
    regulation: str = Form(...),
    course_type: str = Form(...),
    is_active: Optional[int] = Form(None)
):
    # Basic field validation
    errors = validate_course(course_code, course_name, semester, credits)
    if errors or course_exists(course_code):
        return RedirectResponse(
            url="/course",
            status_code=303
        )

    active = 1 if is_active else 0

    add_course(
        course_code,
        course_name,
        department_id,
        program_id,
        faculty_id,
        semester,
        credits,
        regulation,
        course_type,
        active
    )

    return RedirectResponse(
        url="/course",
        status_code=303
    )


# ---------------------------------------------------------
# Edit Course View
# ---------------------------------------------------------
@router.get("/course/edit/{id}")
def edit_course(request: Request, id: int):
    course_data = get_course(id)
    courses = get_all_courses()
    departments = get_all_departments()
    programs = get_all_programs()
    faculties = get_all_faculties()

    return templates.TemplateResponse(
        request=request,
        name="course.html",
        context={
            "title": "Course Master",
            "course": course_data,
            "courses": courses,
            "departments": departments,
            "programs": programs,
            "faculties": faculties
        }
    )


# ---------------------------------------------------------
# Update Course
# ---------------------------------------------------------
@router.post("/course/update/{id}")
def update_course_route(
    id: int,
    course_code: str = Form(...),
    course_name: str = Form(...),
    department_id: int = Form(...),
    program_id: int = Form(...),
    faculty_id: Optional[int] = Form(None),
    semester: int = Form(...),
    credits: float = Form(...),
    regulation: str = Form(...),
    course_type: str = Form(...),
    is_active: Optional[int] = Form(None)
):
    # Validation check
    errors = validate_course(course_code, course_name, semester, credits)
    if errors:
        return RedirectResponse(
            url="/course",
            status_code=303
        )

    active = 1 if is_active else 0

    update_course(
        id,
        course_code,
        course_name,
        department_id,
        program_id,
        faculty_id,
        semester,
        credits,
        regulation,
        course_type,
        active
    )

    return RedirectResponse(
        url="/course",
        status_code=303
    )


# ---------------------------------------------------------
# Delete Course (Soft Delete)
# ---------------------------------------------------------
@router.get("/course/delete/{id}")
def delete(id: int):
    delete_course(id)

    return RedirectResponse(
        url="/course",
        status_code=303
    )
# ---------------------------------------------------------
# Course API
# ---------------------------------------------------------
@router.get("/courses")
def get_courses_api():

    return get_all_courses()