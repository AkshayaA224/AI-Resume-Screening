
from pathlib import Path

import pymupdf
from src.resume_parser import extract_resume_text
from src.skill_extractor import extract_skills


test_terms = [
    "python",
    "sql",
    "machine learning",
    "java",
    "data analysis",
    "pandas",
    "tensorflow",
    "docker",
]


while True:
    path = input(
        "\nEnter resume path (or END to stop): "
    ).strip().strip('"')

    if path.upper() == "END":
        break

    try:
        text = extract_resume_text(path)

        print("\nFILE:", Path(path).name)
        print("Extracted character count:", len(text))
        print("\nFIRST 1500 CHARACTERS:")
        print("-" * 50)
        print(repr(text[:1500]))
        print("-" * 50)

        print("\nKEYWORD CHECK:")
        for term in test_terms:
            print(f"{term}: {term.lower() in text.lower()}")

        print("\nEXTRACTED SKILLS:")
        print(extract_skills(text))

        # Check whether the PDF contains selectable text.
        if Path(path).suffix.lower() == ".pdf":
            with pymupdf.open(path) as pdf:
                print("PDF pages:", len(pdf))
                print(
                    "Characters per page:",
                    [len(page.get_text().strip()) for page in pdf]
                )

    except Exception as error:
        print("Error:", error)
