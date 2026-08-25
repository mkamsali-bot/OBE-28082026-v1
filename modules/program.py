from typing import Optional

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from services.program_service import (
    get_all_programs,
    get_program,
    program_exists,
    add_program,
    update_program,
    delete_program
)

from services.department_service import (
    get_active_departments
)

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# ==========================================================
# Program Home
# ==========================================================
@router.get("/program")
def program(request: Request):

    programs = get_all_programs()

    departments = get_active_departments()

    return templates.TemplateResponse(
        request=request,
        name="program.html",
        context={
            "title": "Program",
            "program": None,
            "programs": programs,
            "departments": departments
        }
    )


# ==========================================================
# Save Program
# ==========================================================
@router.post("/program/save")
def save_program(

    program_code: str = Form(...),
    program_name: str = Form(...),

    department_id: int = Form(...),

    duration: int = Form(...),

    is_active: Optional[int] = Form(None)

):

    active = 1 if is_active else 0

    if not program_exists(program_code):

        add_program(

            program_code,
            program_name,

            department_id,

            duration,

            active

        )

    return RedirectResponse(
        url="/program",
        status_code=303
    )
# ==========================================================
# Edit Program
# ==========================================================
@router.get("/program/edit/{id}")
def edit_program(request: Request, id: int):

    program = get_program(id)

    programs = get_all_programs()

    departments = get_active_departments()

    return templates.TemplateResponse(
        request=request,
        name="program.html",
        context={
            "title": "Program",
            "program": program,
            "programs": programs,
            "departments": departments
        }
    )


# ==========================================================
# Update Program
# ==========================================================
@router.post("/program/update/{id}")
def update_program_route(

    id: int,

    program_code: str = Form(...),
    program_name: str = Form(...),

    department_id: int = Form(...),

    duration: int = Form(...),

    is_active: Optional[int] = Form(None)

):

    active = 1 if is_active else 0

    update_program(

        id,

        program_code,
        program_name,

        department_id,

        duration,

        active

    )

    return RedirectResponse(
        url="/program",
        status_code=303
    )


# ==========================================================
# Delete Program
# ==========================================================
@router.get("/program/delete/{id}")
def delete_program_route(id: int):

    delete_program(id)

    return RedirectResponse(
        url="/program",
        status_code=303
    )