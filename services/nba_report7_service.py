from services.co_po_service import get_course_mappings
from services.co_service import get_co_by_id
from services.indirect_attainment_service import get_indirect_attainment


def get_indirect_co_po_contribution(course_id):
    indirect_rows = get_indirect_attainment(course_id)
    mappings = get_course_mappings(course_id)

    # ---------------------------------------------------------
    # Convert indirect percentage to attainment level
    # ---------------------------------------------------------
    indirect_levels = {}

    for row in indirect_rows:
        percentage = float(row["indirect_percentage"])

        if percentage < 60:
            level = 1.0
        elif percentage < 70:
            level = 2.0
        else:
            level = 3.0

        indirect_levels[row["co_id"]] = {
            "percentage": percentage,
            "level": level,
        }

    # ---------------------------------------------------------
    # Maximum Mapping in each PO / PSO Column
    # ---------------------------------------------------------
    po_max = {}
    for i in range(1, 13):
        po_max[f"po{i}"] = max(
            (mapping[f"po{i}"] or 0) for mapping in mappings
        )

    pso_max = {}
    for i in range(1, 4):
        pso_max[f"pso{i}"] = max(
            (mapping[f"pso{i}"] or 0) for mapping in mappings
        )

    # ---------------------------------------------------------
    # Build contribution rows
    # ---------------------------------------------------------
    results = []

    for mapping in mappings:
        co_id = mapping["co_id"]
        co = get_co_by_id(co_id)
        co_code = co["co_code"] if co else f"CO{co_id}"

        indirect_data = indirect_levels.get(
            co_id,
            {
                "percentage": 0.0,
                "level": 0.0,
            },
        )

        level = indirect_data["level"]

        row = {
            "co_id": co_id,
            "co_code": co_code,
            "indirect_percentage": indirect_data["percentage"],
            "co_attainment": level,
        }

        # -----------------------------------------------------
        # PO contribution
        # -----------------------------------------------------
        for i in range(1, 13):
            mapping_value = mapping[f"po{i}"] or 0
            denominator = po_max[f"po{i}"]

            if mapping_value == 0 or denominator == 0:
                contribution = 0.0
            else:
                contribution = round(
                    level * mapping_value / denominator,
                    2,
                )

            row[f"po{i}"] = contribution

        # -----------------------------------------------------
        # PSO contribution
        # -----------------------------------------------------
        for i in range(1, 4):
            mapping_value = mapping[f"pso{i}"] or 0
            denominator = pso_max[f"pso{i}"]

            if mapping_value == 0 or denominator == 0:
                contribution = 0.0
            else:
                contribution = round(
                    level * mapping_value / denominator,
                    2,
                )

            row[f"pso{i}"] = contribution

        results.append(row)

    return results