from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from services.course_service import get_all_courses
from services.co_service import get_cos_by_course
from fastapi import Request, Form
from fastapi.responses import RedirectResponse

from services.indirect_attainment_service import (
    get_indirect_attainment,
    save_indirect_attainment,
    has_indirect_attainment
)

templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get("/indirect-attainment", response_class=HTMLResponse)
@router.get("/indirect-attainment", response_class=HTMLResponse)
def indirect_attainment(
    request: Request,
    course_id: int = 0,
    saved: int = 0
):
    courses = get_all_courses()

    cos = []

    indirect_lookup = {}

    if course_id:

        cos = get_cos_by_course(course_id)

        rows = get_indirect_attainment(course_id)

        indirect_lookup = {
            row["co_id"]: row["indirect_percentage"]
            for row in rows
        }

    return templates.TemplateResponse(
    request=request,
    name="indirect_attainment.html",
    context={
        "title": "Indirect Attainment",
        "courses": courses,
        "course_id": course_id,
        "saved": saved,
        "cos": cos,
        "indirect_lookup": indirect_lookup
    }
    )
@router.post("/indirect-attainment/save")
async def save_indirect_attainment_page(request: Request):

    form = await request.form()

    course_id = int(form["course_id"])

    values = {}

    for key in form.keys():

        if key.startswith("co_"):

            co_id = int(key.replace("co_", ""))

            value = form[key]

            if value == "":
                percentage = 0
            else:
                percentage = float(value)

            values[co_id] = percentage

    save_indirect_attainment(course_id, values)

    return RedirectResponse(
    url=f"/indirect-attainment?course_id={course_id}&saved=1",
    status_code=303
    )