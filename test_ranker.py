
from pathlib import Path

from src.resume_parser import extract_resume_text
from src.ranker import rank_candidate


# ============================================================
# CONFIGURATION
# ============================================================

SEMANTIC_WEIGHT = 0.70
SKILL_WEIGHT = 0.30

# Initial experimental threshold used by src/skill_gap.py.
SKILL_SIMILARITY_THRESHOLD = 0.72


# ============================================================
# 1. READ MULTILINE JOB DESCRIPTION
# ============================================================

def read_multiline_input(prompt):
    """Read multiline text until the user types END."""
    print(prompt)
    print("Type END on a new line when finished.")

    lines = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        lines.append(line)

    return "\n".join(lines).strip()


# ============================================================
# 2. READ REQUIRED SKILLS
# ============================================================

def read_required_skills():
    """Read required skills, one per line."""
    print("\nEnter required skills, one per line.")
    print("Type END on a new line when finished.")

    skills = []

    while True:
        skill = input().strip()

        if skill.upper() == "END":
            break

        if skill:
            skills.append(skill)

    # Remove duplicate entries while preserving their order.
    return list(dict.fromkeys(skills))


# ============================================================
# 3. READ UNLIMITED RESUME PATHS
# ============================================================

def read_resume_paths():
    """Collect any number of PDF or DOCX resume paths."""
    paths = []

    print("\nEnter resume file paths one at a time.")
    print("Type END when all resumes have been entered.")

    while True:
        path = input(
            f"Resume {len(paths) + 1} (or END to finish): "
        ).strip().strip('"')

        if path.upper() == "END":
            break

        if not path:
            print("Path cannot be empty. Try again.")
            continue

        file_path = Path(path)

        if not file_path.is_file():
            print("File not found. Check the path and try again.")
            continue

        if file_path.suffix.lower() not in {".pdf", ".docx"}:
            print("Unsupported file type. Use PDF or DOCX.")
            continue

        paths.append(str(file_path))

    return paths


# ============================================================
# 4. DISPLAY ONE CANDIDATE
# ============================================================

def display_candidate_result(position, candidate):
    """Display ranking, similarity, and skill-gap information."""

    print(f"\nRank: {position}")
    print(f"Candidate: {candidate['candidate']}")
    print(f"File: {candidate['file_name']}")

    print(
        f"Semantic similarity: "
        f"{candidate['semantic_similarity']:.2f}%"
    )

    print(
        f"Strict skill coverage: "
        f"{candidate['skill_coverage']:.2f}%"
    )

    print(
        f"Combined ranking score: "
        f"{candidate['ranking_score']:.2f}%"
    )

    gap = candidate["skill_gap"]

    print("\nExact matched skills:")
    print(", ".join(gap["matched_skills"]) or "None")

    print("\nSemantic matches requiring review:")

    semantic_matches = gap.get("semantic_matches", [])

    if semantic_matches:
        for item in semantic_matches:
            print(
                f"- Required skill: {item['required_skill']} | "
                f"Related resume skill: "
                f"{item['related_resume_skill']} | "
                f"Similarity: {item['similarity']:.2f}%"
            )
    else:
        print("None")

    print("\nMissing skills:")
    print(", ".join(gap["missing_skills"]) or "None")

    if "semantic_skill_coverage" in gap:
        print(
            "\nSemantic skill coverage (exploratory): "
            f"{gap['semantic_skill_coverage']:.2f}%"
        )

    print("-" * 70)


# ============================================================
# 5. MAIN SCREENING WORKFLOW
# ============================================================

def main():
    print("=" * 70)
    print("AI-BASED RESUME SCREENING AND SKILL GAP ANALYSIS")
    print("=" * 70)

    # Get the job description.
    job_description = read_multiline_input(
        "\nPaste the job description:"
    )

    if not job_description:
        print("Error: Job description cannot be empty.")
        return

    # Get required skills.
    required_skills = read_required_skills()

    if not required_skills:
        print("Error: Enter at least one required skill.")
        return

    # Get unlimited resume paths.
    resume_paths = read_resume_paths()

    if not resume_paths:
        print("No resumes provided. Exiting.")
        return

    print("\nSCREENING CONFIGURATION")
    print("-" * 40)
    print(f"Resumes submitted: {len(resume_paths)}")
    print(f"Required skills entered: {len(required_skills)}")
    print(f"Semantic similarity weight: {SEMANTIC_WEIGHT:.0%}")
    print(f"Strict skill coverage weight: {SKILL_WEIGHT:.0%}")
    print(
        "Semantic skill threshold: "
        f"{SKILL_SIMILARITY_THRESHOLD:.2f}"
    )

    print("\nStarting resume screening...")
    print("=" * 70)

    results = []
    failed_resumes = []

    # Process each resume independently.
    for index, path in enumerate(resume_paths, start=1):
        file_path = Path(path)

        print(
            f"\nProcessing resume {index}/{len(resume_paths)}: "
            f"{file_path.name}"
        )

        try:
            # Extract resume text using the existing parser.
            resume_text = extract_resume_text(path)

            # Rank using the existing ranker.
            #
            # The ranker calls analyze_skill_gap(), which now
            # performs Sentence-BERT semantic skill comparisons.
            result = rank_candidate(
                resume_text=resume_text,
                job_description=job_description,
                required_skills=required_skills,
                semantic_weight=SEMANTIC_WEIGHT,
                skill_weight=SKILL_WEIGHT,
            )

            results.append({
                "candidate": file_path.stem,
                "file_name": file_path.name,
                **result,
            })

            print("Status: Successfully processed.")

        except Exception as error:
            failed_resumes.append({
                "file_name": file_path.name,
                "error": str(error),
            })

            print(f"Status: Failed - {error}")
            print("Continuing with the next resume.")

    # Stop if every resume failed.
    if not results:
        print("\nNo resumes could be processed successfully.")
        return

    # Rank candidates by combined score, highest first.
    results.sort(
        key=lambda item: item["ranking_score"],
        reverse=True,
    )

    # Display the complete ranked results.
    print("\n" + "=" * 70)
    print("FINAL CANDIDATE RANKING")
    print("=" * 70)

    for position, candidate in enumerate(results, start=1):
        display_candidate_result(position, candidate)

    # Processing summary.
    print("\n" + "=" * 70)
    print("SCREENING SUMMARY")
    print("=" * 70)

    print(f"Total resumes submitted: {len(resume_paths)}")
    print(f"Successfully processed: {len(results)}")
    print(f"Failed to process: {len(failed_resumes)}")

    print("\nSCORING CONFIGURATION")
    print(f"Semantic similarity weight: {SEMANTIC_WEIGHT:.0%}")
    print(f"Strict skill coverage weight: {SKILL_WEIGHT:.0%}")

    # Report files that could not be processed.
    if failed_resumes:
        print("\nFAILED RESUMES")

        for failed in failed_resumes:
            print(f"\nFile: {failed['file_name']}")
            print(f"Reason: {failed['error']}")

    print("\nIMPORTANT NOTES")
    print(
        "1. Ranking scores are preliminary screening indicators, "
        "not probabilities of being hired."
    )
    print(
        "2. Semantic skill matches require human review and do not "
        "count as exact skill matches in strict coverage."
    )
    print(
        "3. A missing skill means it was not detected by the current "
        "system; it does not prove that the candidate lacks it."
    )
    print(
        "4. Semantic similarity thresholds should be validated "
        "using representative resume examples."
    )





if __name__ == "__main__":
    main()
