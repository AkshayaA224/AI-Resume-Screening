
from src.resume_parser import extract_resume_text
from src.skill_extractor import analyze_resume

file_path = input("Enter the full path of your resume: ").strip().strip('"')

try:
    resume_text = extract_resume_text(file_path)
    result = analyze_resume(resume_text)

    print("\nRESUME ANALYSIS")
    print("=" * 40)
    print("Email:", result["email"])
    print("Phone:", result["phone"])
    print("Character count:", result["character_count"])

    print("\nEXTRACTED SKILLS")
    print("-" * 40)

    for skill in result["skills"]:
        print("-", skill)

    print("\nTotal skills found:", len(result["skills"]))

except Exception as error:
    print("Error:", error)
