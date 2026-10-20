
from src.skill_gap import analyze_skill_gap


TEST_CASES = [
    {
        "name": "Case 1: Explicit skill",
        "resume": """
        Used Python and Pandas for data analysis.
        Created charts and dashboards using Matplotlib.
        """,
        "required": ["Python", "Data Visualization"],
        "expected_exact": {"python", "data visualization"},
    },
    {
        "name": "Case 2: Related wording",
        "resume": """
        Processed customer reviews and built a sentiment classification
        application using Python.
        """,
        "required": ["Natural Language Processing", "Python"],
        "expected_exact": {"python"},
    },
    {
        "name": "Case 3: Related but insufficient evidence",
        "resume": """
        Cleaned datasets and performed exploratory data analysis
        using Python and Pandas.
        """,
        "required": ["Data Visualization", "Data Analysis"],
        "expected_exact": {"data analysis"},
    },
]


def run_case(case):
    print("\n" + "=" * 65)
    print(case["name"])
    print("=" * 65)

    result = analyze_skill_gap(
        resume_text=case["resume"],
        required_skills=case["required"],
        semantic_threshold=0.72,
        minimum_margin=0.08,
    )

    actual_exact = {
        skill.casefold()
        for skill in result["matched_skills"]
    }

    print("Required skills:", case["required"])
    print("Exact matches:", result["matched_skills"])
    print("Semantic matches:", result["semantic_matches"])
    print("Review needed:", result["review_needed_skills"])
    print("Missing skills:", result["missing_skills"])

    if actual_exact == case["expected_exact"]:
        print("Exact-match check: PASS")
    else:
        print("Exact-match check: CHECK")
        print("Expected:", sorted(case["expected_exact"]))
        print("Actual:", sorted(actual_exact))

    # Semantic outcomes are displayed for manual evaluation.
    # We do not assume a semantic match is correct just because
    # the model returns a high similarity score.


def main():
    for case in TEST_CASES:
        run_case(case)

    print("\n" + "=" * 65)
    print("VALIDATION TESTS FINISHED")
    print("Review semantic suggestions manually; these are not proof of skill.")
    print("=" * 65)


if __name__ == "__main__":
    main()
