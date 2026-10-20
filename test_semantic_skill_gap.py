
from src.skill_gap import analyze_skill_gap


def run_test(title, resume_text, required_skills):
    print("\n" + "=" * 65)
    print(title)
    print("=" * 65)

    result = analyze_skill_gap(
        resume_text=resume_text,
        required_skills=required_skills,
        semantic_threshold=0.72,
        minimum_margin=0.08,
    )

    print("Exact matches:", result["matched_skills"])
    print("Semantic matches:", result["semantic_matches"])
    print("Review needed:", result["review_needed_skills"])
    print("Missing skills:", result["missing_skills"])
    print("Strict coverage:", result["strict_skill_coverage"], "%")
    print("Exploratory semantic coverage:",
          result["semantic_skill_coverage"], "%")


def main():
    # Test 1: Data analysis alone should not establish data visualization.
    resume_without_visualization = """
    Used Python and Pandas to clean datasets.
    Performed data analysis and exploratory data analysis.
    Prepared data for machine learning experiments.
    """

    run_test(
        "TEST 1: Resume with data analysis but no visualization evidence",
        resume_without_visualization,
        ["Data Analysis", "Data Visualization"],
    )

    # Test 2: The resume includes concrete visualization-related evidence.
    resume_with_visualization = """
    Performed exploratory data analysis using Python and Pandas.
    Created data visualization charts and dashboards using Matplotlib.
    Used Seaborn to plot trends and compare data distributions.
    """

    run_test(
        "TEST 2: Resume with explicit visualization evidence",
        resume_with_visualization,
        ["Data Analysis", "Data Visualization"],
    )


if __name__ == "__main__":
    main()
