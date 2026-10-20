
from src.resume_parser import extract_resume_text

file_path = input("Enter the full path of your resume: ").strip()
file_path = file_path.strip('"')

try:
    text = extract_resume_text(file_path)

    print("\nResume extracted successfully!\n")
    print("-" * 60)
    print(text[:5000])
    print("-" * 60)
    print(f"\nTotal characters extracted: {len(text)}")

except Exception as error:
    print(f"Error: {error}")
