from typing import Annotated

from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.nba_report1_service import get_student_marks
from io import BytesIO
from fastapi.responses import StreamingResponse
from services.attainment_service import get_course_co_summary
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from fastapi.responses import StreamingResponse
from io import BytesIO
from services.indirect_attainment_service import get_indirect_attainment
from services.co_service import get_co_by_id

from services.attainment_service import get_course_co_summary
from services.nba_report2_excel_service import (
    generate_direct_co_attainment_excel
)
from services.final_attainment_service import (
    calculate_final_co_attainment
)
from services.nba_report4_excel_service import (
    generate_final_co_attainment_excel
)
from services.co_po_service import get_course_mappings
from services.nba_report5_excel import generate_report5_excel
from services.nba_report6_excel import generate_report6_excel
from services.nba_report7_service import (
    get_indirect_co_po_contribution
)
from services.nba_report7_excel import generate_report7_excel
router = APIRouter()

from services.report1_excel_service import generate_student_marks_excel


from services.course_service import (
    get_all_courses,
    get_courses_by_semester,
)

from services.nba_report_service import (
    get_course_type,
    get_course_details,
)
from services.nba_report3_excel_service import (
    generate_indirect_co_attainment_excel
)

from services.nba_report5_excel import generate_report5_excel
templates = Jinja2Templates(directory="templates")
from services.nba_report6_service import (
    get_direct_co_po_contribution
)


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
@router.get("/nba-report2", response_class=HTMLResponse)
def nba_report2(
    request: Request,
    course_id: int
):

    course = get_course_details(course_id)

    # Existing tested attainment function.
    # Target score will be confirmed from the existing configuration.
    target_score = 10

    attainment = get_course_co_summary(
        course_id,
        target_score
    )

    for row in attainment:

        percentage = row["attainment_percentage"]

        if percentage < 60:
            row["target_level"] = "LEVEL 1"

        elif percentage < 70:
            row["target_level"] = "LEVEL 2"

        else:
            row["target_level"] = "LEVEL 3"

    return templates.TemplateResponse(
        request=request,
        name="nba_report2.html",
        context={
            "title": "Direct CO Attainment",
            "course": course,
            "course_id": course_id,
            "semester": course["semester"],
            "attainment": attainment,
        }
    )

@router.get("/nba-report2-excel")
def nba_report2_excel(course_id: int):

    wb = generate_direct_co_attainment_excel(
        course_id,
        target_score=10
    )

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition":
            'attachment; filename="Direct_CO_Attainment.xlsx"'
        }
    )
@router.get("/nba-report3", response_class=HTMLResponse)
def nba_report3(
    request: Request,
    course_id: int
):

    course = get_course_details(course_id)

    rows = get_indirect_attainment(course_id)

    attainment = []

    for row in rows:

        percentage = row["indirect_percentage"]

        if percentage < 60:
            level = "LEVEL 1"
        elif percentage < 70:
            level = "LEVEL 2"
        else:
            level = "LEVEL 3"

        co = get_co_by_id(row["co_id"])

        attainment.append({
            "co_id": row["co_id"],
            "co_code": co["co_code"] if co else f"CO{row['co_id']}",
            "indirect_percentage": percentage,
            "target_level": level,
        })

    return templates.TemplateResponse(
        request=request,
        name="nba_report3.html",
        context={
            "title": "Indirect CO Attainment",
            "course": course,
            "course_id": course_id,
            "semester": course["semester"],
            "attainment": attainment,
        }
    )
@router.get("/nba-report3-excel")
def nba_report3_excel(course_id: int):

    wb = generate_indirect_co_attainment_excel(course_id)

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        headers={
            "Content-Disposition":
            'attachment; filename="Indirect_CO_Attainment.xlsx"'
        }
    )

@router.get("/nba-report4", response_class=HTMLResponse)
def nba_report4(
    request: Request,
    course_id: int
):

    course = get_course_details(course_id)

    # Existing attainment configuration currently used
    # by the tested attainment module.
    target_score = 10

    final_co = calculate_final_co_attainment(
        course_id,
        target_score
    )

    attainment = []

    for co_id, values in final_co.items():

        final_percentage = values["final"]

        if final_percentage < 60:
            level = "LEVEL 1"

        elif final_percentage < 70:
            level = "LEVEL 2"

        else:
            level = "LEVEL 3"

        co = get_co_by_id(co_id)

        attainment.append({
            "co_id": co_id,
            "co_code": (
                co["co_code"]
                if co
                else f"CO{co_id}"
            ),
            "direct": values["direct"],
            "indirect": values["indirect"],
            "final": values["final"],
            "target_level": level,
        })

    return templates.TemplateResponse(
        request=request,
        name="nba_report4.html",
        context={
            "title": "Final CO Attainment",
            "course": course,
            "course_id": course_id,
            "semester": course["semester"],
            "attainment": attainment,
        }
    )

@router.get("/nba-report4-excel")
def nba_report4_excel(course_id: int):

    wb = generate_final_co_attainment_excel(
        course_id,
        target_score=10
    )

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition":
            'attachment; filename="Final_CO_Attainment.xlsx"'
        }
    )
@router.get("/nba-report5", response_class=HTMLResponse)
def nba_report5(
    request: Request,
    course_id: int
):

    course = get_course_details(course_id)

    mappings = get_course_mappings(course_id)

    return templates.TemplateResponse(
        request=request,
        name="nba_report5.html",
        context={
            "title": "CO → PO Mapping",
            "course": course,
            "course_id": course_id,
            "semester": course["semester"],
            "mappings": mappings,
        }
    )
@router.get("/nba-report5-excel")
def nba_report5_excel(course_id: int):

    wb = generate_report5_excel(course_id)

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition":
            'attachment; filename="CO_PO_Mapping.xlsx"'
        }
    )

@router.get("/nba-report6", response_class=HTMLResponse)
def nba_report6(
    request: Request,
    course_id: int
):

    course = get_course_details(course_id)

    contribution = get_direct_co_po_contribution(course_id)

    return templates.TemplateResponse(
        request=request,
        name="nba_report6.html",
        context={
            "title": "Direct CO → PO Contribution",
            "course": course,
            "course_id": course_id,
            "semester": course["semester"],
            "contribution": contribution,
        }
    )
@router.get("/nba-report6-excel")
def nba_report6_excel(course_id: int):

    wb = generate_report6_excel(course_id)

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition":
            'attachment; filename="Direct_CO_PO_Contribution.xlsx"'
        }
    )
def nba_report7(
    request: Request,
    course_id: int
):
    course = get_course_details(course_id)

    contribution = get_indirect_co_po_contribution(
        course_id
    )

    return templates.TemplateResponse(
        request=request,
        name="nba_report7.html",
        context={
            "title": "Indirect CO → PO Contribution",
            "course": course,
            "course_id": course_id,
            "semester": course["semester"],
            "contribution": contribution,
        }
    )
@router.get("/nba-report7-excel")
def nba_report7_excel(course_id: int):

    wb = generate_report7_excel(course_id)

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition":
            'attachment; filename="Indirect_CO_PO_Contribution.xlsx"'
        }
    )

from services.nba_report8_service import get_final_co_po_contribution
@router.get("/nba-report8", response_class=HTMLResponse)
def nba_report8(
    request: Request,
    course_id: int
):

    course = get_course_details(course_id)

    contribution = get_final_co_po_contribution(
        course_id,
        target_score=10
    )

    return templates.TemplateResponse(
        request=request,
        name="nba_report8.html",
        context={
            "title": "Final CO → PO Contribution",
            "course": course,
            "course_id": course_id,
            "semester": course["semester"],
            "contribution": contribution,
        }
    )
from services.nba_report8_excel import generate_report8_excel
@router.get("/nba-report8-excel")
def nba_report8_excel(course_id: int):

    wb = generate_report8_excel(
        course_id,
        target_score=10
    )

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition":
            'attachment; filename="Final_CO_PO_Contribution.xlsx"'
        }
    )

from services.attainment_service import (
    calculate_po_attainment,
    calculate_pso_attainment,
)

from services.nba_report8_service import (
    get_final_co_po_contribution
)
@router.get("/nba-report9", response_class=HTMLResponse)
def nba_report9(
    request: Request,
    course_id: int
):

    course = get_course_details(course_id)

    target_score = 10

    po = calculate_po_attainment(
        course_id,
        target_score
    )

    pso = calculate_pso_attainment(
        course_id,
        target_score
    )

    contribution = get_final_co_po_contribution(
        course_id,
        target_score
    )

    return templates.TemplateResponse(
        request=request,
        name="nba_report9.html",
        context={
            "title": "Final PO & PSO Attainment Summary",
            "course": course,
            "course_id": course_id,
            "semester": course["semester"],
            "po": po,
            "pso": pso,
            "contribution": contribution,
        }
    )
from services.nba_report9_excel import generate_report9_excel
@router.get("/nba-report9-excel")
def nba_report9_excel(course_id: int):

    wb = generate_report9_excel(
        course_id,
        target_score=10
    )

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition":
            'attachment; filename="Final_PO_PSO_Attainment_Summary.xlsx"'
        }
    )