from services.attainment_service import calculate_course_attainment
from services.co_po_service import get_course_mappings
from services.co_service import get_co_by_id


def get_direct_co_po_contribution(course_id):

    student_results = calculate_course_attainment(course_id)
    mappings = get_course_mappings(course_id)

    # ---------------------------------------------------------
    # Average direct CO attainment
    # ---------------------------------------------------------
    co_totals = {}
    co_counts = {}

    for student in student_results.values():

        for co_id, score in student["co_scores"].items():

            co_totals[co_id] = (
                co_totals.get(co_id, 0.0) + float(score)
            )

            co_counts[co_id] = (
                co_counts.get(co_id, 0) + 1
            )

    direct_co = {}

    for co_id, total in co_totals.items():

        count = co_counts.get(co_id, 0)

        direct_co[co_id] = (
            round(total / count, 2)
            if count
            else 0.0
        )

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

    # ---------------------------------------------------------
    # Contribution
    # ---------------------------------------------------------
    results = []

    for mapping in mappings:

        co_id = mapping["co_id"]

        co = get_co_by_id(co_id)

        co_code = (
            co["co_code"]
            if co
            else f"CO{co_id}"
        )

        co_attainment = direct_co.get(
            co_id,
            0.0
        )

        row = {
            "co_id": co_id,
            "co_code": co_code,
            "co_attainment": co_attainment,
        }

        # PO
        for i in range(1, 13):

            strength = mapping[f"po{i}"] or 0
            denominator = po_sums[f"po{i}"]

            if strength == 0 or denominator == 0:
                value = 0.0
            else:
                value = round(
                    co_attainment * strength / denominator,
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
                    co_attainment * strength / denominator,
                    2
                )

            row[f"pso{i}"] = value

        results.append(row)

    return results