from services.attainment_service import calculate_course_attainment
from services.co_po_service import get_course_mappings
from services.co_service import get_co_by_id


def get_attainment_level(percentage):
    if percentage < 60:
        return 1
    elif percentage < 70:
        return 2
    return 3


def get_direct_co_po_contribution(course_id):
    student_results = calculate_course_attainment(course_id)
    mappings = get_course_mappings(course_id)

    # ---------------------------------------------------------
    # Maximum mapping for each PO
    # ---------------------------------------------------------
    po_max = {}
    for i in range(1, 13):
        po_max[f"po{i}"] = max(
            (mapping[f"po{i}"] or 0) for mapping in mappings
        )

    # ---------------------------------------------------------
    # Maximum mapping for each PSO
    # ---------------------------------------------------------
    pso_max = {}
    for i in range(1, 4):
        pso_max[f"pso{i}"] = max(
            (mapping[f"pso{i}"] or 0) for mapping in mappings
        )

    # ---------------------------------------------------------
    # Average Direct CO Attainment
    # ---------------------------------------------------------
    co_totals = {}
    co_counts = {}

    for student in student_results.values():
        for co_id, score in student["co_scores"].items():
            co_totals[co_id] = co_totals.get(co_id, 0.0) + float(score)
            co_counts[co_id] = co_counts.get(co_id, 0) + 1

    direct_co = {}
    for co_id, total in co_totals.items():
        count = co_counts.get(co_id, 0)
        direct_co[co_id] = round(total / count, 2) if count else 0.00

    # ---------------------------------------------------------
    # Direct CO → PO / PSO Contribution
    # ---------------------------------------------------------
    results = []

    for mapping in mappings:
        co_id = mapping["co_id"]
        co = get_co_by_id(co_id)
        co_code = co["co_code"] if co else f"CO{co_id}"

        co_attainment = direct_co.get(co_id, 0.00)
        co_level = get_attainment_level(co_attainment)

        row = {
            "co_id": co_id,
            "co_code": co_code,
            "co_attainment": float(f"{co_attainment:.2f}"),
            "co_level": co_level,
        }

        # -----------------------------------------------------
        # PO Contribution
        # -----------------------------------------------------
        for i in range(1, 13):
            strength = mapping[f"po{i}"] or 0
            denominator = po_max[f"po{i}"]

            if strength == 0 or denominator == 0:
                value = 0.00
            else:
                value = float(
                    f"{(co_level * strength / denominator):.2f}"
                )

            row[f"po{i}"] = value

        # -----------------------------------------------------
        # PSO Contribution
        # -----------------------------------------------------
        for i in range(1, 4):
            strength = mapping[f"pso{i}"] or 0
            denominator = pso_max[f"pso{i}"]

            if strength == 0 or denominator == 0:
                value = 0.00
            else:
                value = float(
                    f"{(co_level * strength / denominator):.2f}"
                )

            row[f"pso{i}"] = value

        results.append(row)

    return results