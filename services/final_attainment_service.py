from services.attainment_service import calculate_co_attainment_percentage

from services.indirect_attainment_service import (
    get_indirect_attainment
)

def calculate_final_co_attainment(
    course_id,
    target_score,
    direct_weight=0.80,
    indirect_weight=0.20
):
    direct = calculate_co_attainment_percentage(
        course_id,
        target_score
    )

    indirect_rows = get_indirect_attainment(course_id)

    indirect = {}

    for row in indirect_rows:
        indirect[row["co_id"]] = row["indirect_percentage"]

    result = {}

    for co_id, row in direct.items():

        direct_percentage = row["percentage"]

        indirect_percentage = indirect.get(co_id, 0)

        final_percentage = round(
            (direct_percentage * direct_weight)
            +
            (indirect_percentage * indirect_weight),
            2
        )

        result[co_id] = {
            "direct": direct_percentage,
            "indirect": indirect_percentage,
            "final": final_percentage
        }

    return result