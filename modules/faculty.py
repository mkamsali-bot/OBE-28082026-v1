from typing import Optional

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from services.faculty_service import (
    get_all_faculties,
    get_faculty,
    faculty_exists,
    add_faculty,
    update_faculty,
    delete_faculty
)

from services.department_service import (
    get_active_departments
)

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# ---------------------------------------------------------
# Faculty Home
# ---------------------------------------------------------
@router.get("/faculty")
def faculty(request: Request):

    faculties = get_all_faculties()

    departments = get_active_departments()

    return templates.TemplateResponse(
        request=request,
        name="faculty.html",
        context={
            "title": "Faculty",
            "faculty": None,
            "faculties": faculties,
            "departments": departments
        }
    )


# ---------------------------------------------------------
# Save Faculty
# ---------------------------------------------------------
@router.post("/faculty/save")
def save_faculty(

    faculty_code: str = Form(...),
    faculty_name: str = Form(...),
    designation: str = Form(...),
    email: str = Form(...),
    mobile: str = Form(...),
    department_id: int = Form(...),
    is_active: Optional[int] = Form(None)

):

    active = 1 if is_active else 0

    if not faculty_exists(faculty_code):

        add_faculty(
            faculty_code,
            faculty_name,
            designation,
            email,
            mobile,
            department_id,
            active
        )

    return RedirectResponse(
        url="/faculty",
        status_code=303
    )


# ---------------------------------------------------------
# Edit Faculty
# ---------------------------------------------------------
@router.get("/faculty/edit/{id}")
def edit_faculty(request: Request, id: int):

    faculty = get_faculty(id)

    faculties = get_all_faculties()

    departments = get_active_departments()

    return templates.TemplateResponse(
        request=request,
        name="faculty.html",
        context={
            "title": "Faculty",
            "faculty": faculty,
            "faculties": faculties,
            "departments": departments
        }
    )


# ---------------------------------------------------------
# Update Faculty
# ---------------------------------------------------------
@router.post("/faculty/update/{id}")
def update_faculty_route(

    id: int,
    faculty_code: str = Form(...),
    faculty_name: str = Form(...),
    designation: str = Form(...),
    email: str = Form(...),
    mobile: str = Form(...),
    department_id: int = Form(...),
    is_active: Optional[int] = Form(None)

):

    active = 1 if is_active else 0

    update_faculty(
        id,
        faculty_code,
        faculty_name,
        designation,
        email,
        mobile,
        department_id,
        active
    )

    return RedirectResponse(
        url="/faculty",
        status_code=303
    )


# ---------------------------------------------------------
# Delete Faculty (Soft Delete)
# ---------------------------------------------------------
@router.get("/faculty/delete/{id}")
def delete_faculty_route(id: int):

    delete_faculty(id)

    return RedirectResponse(
        url="/faculty",
        status_code=303
    )