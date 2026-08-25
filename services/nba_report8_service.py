from services.final_attainment_service import calculate_final_co_attainment
from services.co_po_service import get_course_mappings
from services.co_service import get_co_by_id


def get_final_co_po_contribution(course_id, target_score=10):

    final_co = calculate_final_co_attainment(
        course_id,
        target_score
    )

    mappings = get_course_mappings(course_id)

    # ---------------------------------------------------------
    # PO/PSO column totals
    # ---------------------------------------------------------
    po_sums = {
        f"po{i}": 0
        for i in range(1, 13)
    }

    pso_sums = {
        f"pso{i}": 0
        for i in range(1, 4)
    }

    for mapping in mappings:

        for i in range(1, 13):
            po_sums[f"po{i}"] += mapping[f"po{i}"] or 0

        for i in range(1, 4):
            pso_sums[f"pso{i}"] += mapping[f"pso{i}"] or 0

    results = []

    # ---------------------------------------------------------
    # Contribution
    # ---------------------------------------------------------
    for mapping in mappings:

        co_id = mapping["co_id"]

        co = get_co_by_id(co_id)

        co_code = (
            co["co_code"]
            if co
            else f"CO{co_id}"
        )

        values = final_co.get(
            co_id,
            {
                "direct": 0.0,
                "indirect": 0.0,
                "final": 0.0,
            }
        )

        final_attainment = float(
            values["final"]
        )

        row = {
            "co_id": co_id,
            "co_code": co_code,
            "co_attainment": final_attainment,
        }

        # PO
        for i in range(1, 13):

            strength = mapping[f"po{i}"] or 0
            denominator = po_sums[f"po{i}"]

            if strength == 0 or denominator == 0:
                value = 0.0
            else:
                value = round(
                    final_attainment * strength / denominator,
                    2
                )

            row[f"po{i}"] = value

        # PSO
        for i in range(1, 4):

            strength = mapping[f"pso{i}"] or 0
            denominator = pso_sums[f"pso{i}"]

            if strength == 0 or denominator == 0:
                value = 0.0
            else:
                value = round(
                    final_attainment * strength / denominator,
                    2
                )

            row[f"pso{i}"] = value

        results.append(row)

    return results