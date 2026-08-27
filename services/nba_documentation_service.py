"""
NBA Report Documentation Service

Contains:
1. Formula
2. Specimen Calculation
3. Interpretation

for Reports 2–7.
"""


def get_report2_documentation():

    return {

        "title": "Direct CO Attainment",

        "formula": [
            "Direct CO Attainment (%) = (Average CO Score / Maximum CO Marks) × 100",
            "",
            "Attainment Level",
            "Level 1 : Percentage < 60",
            "Level 2 : 60 ≤ Percentage < 70",
            "Level 3 : Percentage ≥ 70",
        ],

        "specimen": [
            "Example",
            "",
            "Average CO1 Score = 19.48",
            "Maximum CO Marks = 25",
            "",
            "Percentage = (19.48 / 25) × 100",
            "Percentage = 77.92 %",
            "",
            "Attainment Level = 3",
        ],

        "interpretation": (
            "The average score obtained by students for each Course Outcome "
            "is converted into a percentage. Based on the predefined threshold, "
            "an attainment level of 1, 2 or 3 is assigned."
        ),
    }
def get_report3_documentation():

    return {

        "title": "Indirect CO Attainment",

        "formula": [
            "Indirect CO Attainment (%) = Survey Percentage",
            "",
            "Attainment Level",
            "Level 1 : Percentage < 60",
            "Level 2 : 60 ≤ Percentage < 70",
            "Level 3 : Percentage ≥ 70",
        ],

        "specimen": [
            "Example",
            "",
            "Survey Percentage = 82%",
            "",
            "Attainment Level = 3",
        ],

        "interpretation": (
            "Indirect attainment is obtained from Course Exit Survey "
            "responses. The survey percentage is converted into an "
            "attainment level using the predefined thresholds."
        ),
    }
def get_report4_documentation():

    return {

        "title": "Final CO Attainment",

        "formula": [
            "Final CO Attainment = (0.8 × Direct Level) + (0.2 × Indirect Level)"
        ],

        "specimen": [
            "Example",
            "",
            "Direct Level = 3",
            "Indirect Level = 2",
            "",
            "Final Attainment = (0.8 × 3) + (0.2 × 2)",
            "Final Attainment = 2.8",
        ],

        "interpretation": (
            "Final Course Outcome attainment is computed by combining "
            "direct and indirect attainment with 80% and 20% weightage "
            "respectively."
        ),
    }
def get_report5_documentation():

    return {

        "title": "CO–PO / PSO Mapping",

        "formula": [
            "COs are mapped with POs and PSOs using mapping strengths.",
            "",
            "1 = Low",
            "2 = Medium",
            "3 = High",
        ],

        "specimen": [
            "Example",
            "",
            "CO1 → PO1 = 3",
            "CO1 → PO2 = 2",
            "CO1 → PO3 = 1",
            "CO1 → PO4 = 0",
        ],

        "interpretation": (
            "The mapping matrix indicates the contribution of each "
            "Course Outcome towards Programme Outcomes and Programme "
            "Specific Outcomes."
        ),
    }
def get_report6_documentation():

    return {

        "title": "Direct CO–PO / PSO Contribution",

        "formula": [
            "Contribution = (CO Attainment Level × Mapping Strength) ÷ Total Mapping Strength"
        ],

        "specimen": [
            "Example",
            "",
            "CO1 Attainment Level = 3",
            "PO1 Mapping = 2",
            "Total PO1 Mapping = 6",
            "",
            "Contribution = (3 × 2) ÷ 6",
            "Contribution = 1.00",
        ],

        "interpretation": (
            "Direct CO–PO contribution distributes the attainment level "
            "of each Course Outcome to the mapped Programme Outcomes "
            "and Programme Specific Outcomes in proportion to the "
            "mapping strengths."
        ),
    }
def get_report7_documentation():

    return {

        "title": "Indirect CO–PO / PSO Contribution",

        "formula": [
            "Indirect Contribution = (Indirect CO Attainment Level × Mapping Strength) ÷ Maximum Mapping in the Corresponding PO / PSO Column"
        ],

        "specimen": [
            "Given",
            "",
            "Indirect CO Attainment Level = 2",
            "PO2 Mapping Strength = 3",
            "Maximum Mapping in PO2 Column = 3",
            "",
            "Indirect Contribution =",
            "",
            "              2 × 3",
            "             ───────",
            "                 3",
            "",
            "             = 2.00",
        ],

        "interpretation": (
            "The indirect contribution of each Course Outcome to the "
            "Programme Outcomes and Programme Specific Outcomes is "
            "computed using the indirect CO attainment level and "
            "normalized by the maximum mapping available in the "
            "corresponding PO/PSO column."
        ),
    }
def get_report8_documentation():

    return {

        "title": "Final CO–PO / PSO Contribution",

        "formula": [
            "Final Contribution = (Final CO Attainment Level × Mapping Strength) ÷ Maximum Mapping in the Corresponding PO / PSO Column"
        ],

        "specimen": [
            "Given",
            "",
            "Final CO Attainment Level = 3",
            "PO2 Mapping Strength = 2",
            "Maximum Mapping in PO2 Column = 2",
            "",
            "Final Contribution =",
            "",
            "              3 × 2",
            "             ───────",
            "                 2",
            "",
            "             = 3.00",
        ],

        "interpretation": (
            "The final contribution of each Course Outcome to the "
            "Programme Outcomes and Programme Specific Outcomes is "
            "computed using the Final CO Attainment Level and "
            "normalized by the maximum mapping available in the "
            "corresponding PO / PSO column."
        ),
    }
def get_report9_documentation():

    return {

        "title": "Final PO–PSO Attainment Summary",

        "formula": [
            "PO / PSO Attainment = Sum of the Final CO → PO / PSO Contributions"
        ],

        "specimen": [
            "Given",
            "",
            "CO1 Contribution to PO1 = 2.80",
            "CO2 Contribution to PO1 = 1.90",
            "CO3 Contribution to PO1 = 2.10",
            "",
            "PO1 Attainment =",
            "",
            "2.80 + 1.90 + 2.10",
            "",
            "= 6.80",
        ],

        "interpretation": (
            "The Final Programme Outcome (PO) and Programme Specific "
            "Outcome (PSO) attainment is obtained by summing the Final "
            "CO → PO / PSO contribution values of all mapped Course "
            "Outcomes. The resulting values indicate the overall "
            "attainment achieved for each Programme Outcome and "
            "Programme Specific Outcome."
        ),
    }
