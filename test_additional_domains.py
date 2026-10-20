
from src.skill_extractor import extract_skills, normalize_skill_name

TEST_CASES = [
    {
        "domain": "Mechanical Engineering",
        "resume": """
        Mechanical engineer experienced in CATIA, ANSYS Workbench,
        thermodynamics, and CNC machining.
        """,
        "required": [
            "CATIA",
            "ANSYS",
            "Thermodynamics",
            "CNC Machining",
            "SolidWorks",
        ],
    },
    {
        "domain": "Electrical and Electronics",
        "resume": """
        Electronics engineer skilled in MATLAB, Simulink, embedded
        systems, PCB design, and Verilog.
        """,
        "required": [
            "MATLAB",
            "Simulink",
            "Embedded Systems",
            "PCB Design",
            "VHDL",
        ],
    },
    {
        "domain": "Finance and Accounting",
        "resume": """
        Finance professional experienced in financial analysis,
        Tally Prime, GST, auditing, and bank reconciliation.
        """,
        "required": [
            "Financial Analysis",
            "Tally",
            "GST",
            "Auditing",
            "SAP",
        ],
    },
    {
        "domain": "Marketing",
        "resume": """
        Digital marketer experienced in SEO, Google Analytics,
        content marketing, social media marketing, and HubSpot.
        """,
        "required": [
            "SEO",
            "Google Analytics",
            "Content Marketing",
            "Social Media Marketing",
            "Salesforce",
        ],
    },
    {
        "domain": "Human Resources",
        "resume": """
        HR professional experienced in recruitment, talent acquisition,
        employee onboarding, HRIS, and performance management.
        """,
        "required": [
            "Recruitment",
            "Employee Onboarding",
            "HRIS",
            "Performance Management",
            "Payroll Accounting",
        ],
    },
    {
        "domain": "Healthcare",
        "resume": """
        Healthcare professional with experience in clinical research,
        medical coding, patient care, pharmacovigilance, and epidemiology.
        """,
        "required": [
            "Clinical Research",
            "Medical Coding",
            "Patient Care",
            "Pharmacovigilance",
            "Bioinformatics",
        ],
    },
]


def run_tests():
    all_passed = True

    for case in TEST_CASES:
        extracted = set(extract_skills(case["resume"]))
        extracted_normalized = {
            normalize_skill_name(skill) for skill in extracted
        }

        required_normalized = [
            normalize_skill_name(skill)
            for skill in case["required"]
        ]

        matched = [
            skill for skill in required_normalized
            if skill in extracted_normalized
        ]

        missing = [
            skill for skill in required_normalized
            if skill not in extracted_normalized
        ]

        coverage = (
            len(matched) / len(required_normalized) * 100
            if required_normalized else 100.0
        )

        # Each test has four explicitly present skills
        # and one deliberately absent skill.
        passed = len(matched) == 4 and len(missing) == 1
        all_passed = all_passed and passed

        print(f"\n{'=' * 55}")
        print(f"Domain: {case['domain']}")
        print(f"Extracted skills: {sorted(extracted)}")
        print(f"Matched skills: {matched}")
        print(f"Missing skills: {missing}")
        print(f"Strict skill coverage: {coverage:.2f}%")
        print(f"Test result: {'PASS' if passed else 'FAIL'}")

    print(f"\n{'=' * 55}")
    print(
        "OVERALL RESULT:",
        "ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED"
    )


if __name__ == "__main__":
    run_tests()
