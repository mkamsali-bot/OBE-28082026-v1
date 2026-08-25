from typing import Optional

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from services.co_service import (
    get_all_cos,
    get_co,
    co_exists,
    add_co,
    update_co,
    delete_co
)

from services.course_service import get_all_courses


router = APIRouter()

templates = Jinja2Templates(directory="templates")


# ==========================================================
# Course Outcome Master
# ==========================================================
@router.get("/co")
def co(request: Request):

    courses = get_all_courses()

    cos = get_all_cos()

    return templates.TemplateResponse(
        request=request,
        name="co.html",
        context={
            "title": "Course Outcomes",
            "courses": courses,
            "cos": cos,
            "co": None
        }
    )


# ==========================================================
# Save Course Outcome
# ==========================================================
@router.post("/co/save")
def save_co(

    course_id: int = Form(...),
    co_code: str = Form(...),
    co_description: str = Form(...),

    bloom_level: str = Form(...),

    is_active: Optional[int] = Form(None)

):

    active = 1 if is_active else 0

    if not co_exists(course_id, co_code):

        add_co(
            course_id,
            co_code,
            co_description,
            bloom_level,
            active
        )

    return RedirectResponse(
        url="/co",
        status_code=303
    )

# ==========================================================
# Edit Course Outcome
# ==========================================================
@router.get("/co/edit/{id}")
def edit_co(id: int, request: Request):

    courses = get_all_courses()

    cos = get_all_cos()

    co = get_co(id)

    return templates.TemplateResponse(
        request=request,
        name="co.html",
        context={
            "title": "Course Outcomes",
            "courses": courses,
            "cos": cos,
            "co": co
        }
    )

# ==========================================================
# Update Course Outcome
# ==========================================================
@router.post("/co/update/{id}")
def update_co_record(

    id: int,

    course_id: int = Form(...),
    co_code: str = Form(...),
    co_description: str = Form(...),

    bloom_level: str = Form(...),

    is_active: Optional[int] = Form(None)

):

    active = 1 if is_active else 0

    update_co(

        id,
        course_id,
        co_code,
        co_description,
        bloom_level,
        active

    )

    return RedirectResponse(
        url="/co",
        status_code=303
    )

# ==========================================================
# Delete Course Outcome
# ==========================================================
@router.get("/co/delete/{id}")
def delete_co_record(id: int):

    delete_co(id)

    return RedirectResponse(
        url="/co",
        status_code=303
    )