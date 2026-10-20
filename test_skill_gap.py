
from src.resume_parser import extract_resume_text
from src.skill_gap import analyze_skill_gap


resume_path = input(
    "Enter the full path of your resume: "
).strip().strip('"')

print("\nEnter the required skills, one per line.")
print("Type END on a new line when finished.")

required_skills = []

while True:
    skill = input().strip()

    if skill.upper() == "END":
        break

    if skill:
        required_skills.append(skill)


try:
    resume_text = extract_resume_text(resume_path)

    result = analyze_skill_gap(
        resume_text,
        required_skills
    )

    print("\nSKILL-GAP ANALYSIS")
    print("=" * 40)

    print("\nMATCHED SKILLS")
    for skill in result["matched_skills"]:
        print("-", skill)

    print("\nRELATED SKILLS — REVIEW REQUIRED")
    for skill in result["review_needed_skills"]:
        print("-", skill)

    print("\nMISSING SKILLS")
    for skill in result["missing_skills"]:
        print("-", skill)

    print("\nSUMMARY")
    print("Required skills:", result["total_required"])
    print("Strict skill coverage:",
          f'{result["strict_skill_coverage"]:.2f}%')

except Exception as error:
    print("Error:", error)
