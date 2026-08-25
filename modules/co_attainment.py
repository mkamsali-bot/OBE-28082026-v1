from fastapi import APIRouter
from services.indirect_attainment_service import get_indirect_attainment

from services.attainment_service import (
    get_course_marks,
    build_student_dictionary,
    get_student,
    get_student_marks,
    apply_co_weightages,
    calculate_course_attainment,
    calculate_co_attainment_percentage,
    get_course_co_summary,
    calculate_po_attainment,
    calculate_pso_attainment,
)

from services.co_weightage_service import get_weightages
from services.co_po_service import get_course_mappings

from services.final_attainment_service import (
    calculate_final_co_attainment,
)
router = APIRouter()
@router.get("/test-co-po/{course_id}")
def test_co_po(course_id: int):

    return get_course_mappings(course_id)

from services.attainment_service import calculate_po_attainment

@router.get("/test-po/{course_id}")
def test_po(course_id: int):

    return calculate_po_attainment(
        course_id,
        target_score=10
    )
@router.get("/course-attainment/{course_id}")
def course_attainment(course_id: int):

    target_score = 10

    # Get indirect attainment
    rows = get_indirect_attainment(course_id)

    indirect = {}

    for row in rows:
        indirect[row["co_id"]] = row["indirect_percentage"]

    return {
        "co": calculate_co_attainment_percentage(course_id, target_score),
        "indirect": indirect,
        "final_co": calculate_final_co_attainment(course_id, target_score),
        "po": calculate_po_attainment(course_id, target_score),
        "pso": calculate_pso_attainment(course_id, target_score)
    }