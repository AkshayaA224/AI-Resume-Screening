from src.resume_parser import extract_resume_text
from src.matcher import calculate_similarity, calculate_match_percentage


resume_path = input(
    "Enter the full path of your resume: "
).strip().strip('"')

print("\nPaste the job description below.")
print("When finished, type END on a new line.")

lines = []

while True:
    line = input()
    if line.strip() == "END":
        break
    lines.append(line)

job_description = "\n".join(lines).strip()

try:
    resume_text = extract_resume_text(resume_path)

    similarity = calculate_similarity(
        resume_text,
        job_description
    )

    percentage = calculate_match_percentage(
        resume_text,
        job_description
    )

    print("\nSEMANTIC MATCHING RESULTS")
    print("=" * 40)
    print(f"Cosine similarity: {similarity:.4f}")
    print(f"Similarity percentage: {percentage:.2f}%")

    print(
        "\nNote: This percentage represents semantic similarity, "
        "not the probability of being hired."
    )

except Exception as error:
    print(f"\nError: {error}")
