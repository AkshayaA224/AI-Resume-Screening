
from src.skill_gap import analyze_skill_gap
from src.skill_extractor import extract_skills, normalize_skill_name


def run_test(title, resume_text, required_skills, expected_matches, expected_coverage):
    print("\n" + "=" * 65)
    print(title)
    print("=" * 65)

    result = analyze_skill_gap(
        resume_text=resume_text,
        required_skills=required_skills,
    )

    actual_matches = {
        normalize_skill_name(skill)
        for skill in result["matched_skills"]
    }

    expected = {
        normalize_skill_name(skill)
        for skill in expected_matches
    }

    print("Required skills:", required_skills)
    print("Extracted skills:", extract_skills(
        resume_text,
        extra_skills=required_skills,
    ))
    print("Exact matches:", result["matched_skills"])
    print("Semantic matches:", result["semantic_matches"])
    print("Review needed:", result["review_needed_skills"])
    print("Missing skills:", result["missing_skills"])
    print("Strict coverage:", result["strict_skill_coverage"], "%")

    matches_pass = actual_matches == expected
    coverage_pass = (
        result["strict_skill_coverage"] == expected_coverage
    )

    print("Exact-match test:", "PASS" if matches_pass else "FAIL")
    print("Coverage test:", "PASS" if coverage_pass else "FAIL")

    if not matches_pass:
        print("Expected exact matches:", sorted(expected))
        print("Actual exact matches:", sorted(actual_matches))

    if not coverage_pass:
        print("Expected coverage:", expected_coverage)
        print("Actual coverage:", result["strict_skill_coverage"])

    return matches_pass and coverage_pass


def test_civil_engineering():
    resume_text = """
    Civil Engineering graduate with experience using AutoCAD.
    Worked on structural analysis and building design.
    Familiar with STAAD.Pro and quantity surveying.
    """

    required_skills = [
        "AutoCAD",
        "STAAD.Pro",
        "Structural Analysis",
        "Revit",
        "Quantity Surveying",
    ]

    # Four of the five requirements appear in the resume.
    expected_matches = [
        "AutoCAD",
        "STAAD.Pro",
        "Structural Analysis",
        "Quantity Surveying",
    ]

    return run_test(
        title="CIVIL ENGINEERING RECRUITMENT TEST",
        resume_text=resume_text,
        required_skills=required_skills,
        expected_matches=expected_matches,
        expected_coverage=80.0,
    )


def test_ai_ml():
    resume_text = """
    Developed machine learning applications using Python and Pandas.
    Worked on Natural Language Processing (NLP).
    Created charts and visualizations using Matplotlib.
    """

    required_skills = [
        "Python",
        "Pandas",
        "NLP",
        "Data Visualization",
        "Git",
    ]

    # Git is deliberately absent from the sample resume.
    expected_matches = [
        "Python",
        "Pandas",
        "NLP",
        "Data Visualization",
    ]

    return run_test(
        title="AI/ML RECRUITMENT TEST",
        resume_text=resume_text,
        required_skills=required_skills,
        expected_matches=expected_matches,
        expected_coverage=80.0,
    )


def main():
    civil_passed = test_civil_engineering()
    ai_ml_passed = test_ai_ml()

    print("\n" + "=" * 65)
    print("OVERALL DOMAIN TEST SUMMARY")
    print("=" * 65)
    print("Civil engineering:", "PASS" if civil_passed else "FAIL")
    print("AI/ML:", "PASS" if ai_ml_passed else "FAIL")

    if civil_passed and ai_ml_passed:
        print("Both domain tests passed.")
    else:
        print("At least one test failed. Review the output above.")


if __name__ == "__main__":
    main()
