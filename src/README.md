# AI-Based Resume Screening and Skill Gap Analysis

An AI-powered application that screens resumes against a job description, ranks candidates, and identifies matching skills, missing skills, and potential skill matches that require human review.

## Overview

Recruiters often need to review many resumes for a single job opening. This project helps streamline the initial screening process by combining semantic similarity analysis with skill-based evaluation.

The application accepts a job description, a list of required skills, and multiple resumes in PDF or DOCX format. It extracts resume text, evaluates candidate-job relevance, calculates skill coverage, and presents ranked results through an interactive Streamlit dashboard.

## Key Features

- **Resume Parsing:** Extract text from PDF and DOCX files.
- **Semantic Similarity:** Uses Sentence-BERT embeddings to measure the relevance of a resume to a job description.
- **Skill Extraction:** Identifies skills using a skill dictionary, aliases, and normalization.
- **Skill Gap Analysis:** Reports matched skills, missing skills, and potential semantic matches requiring human review.
- **Candidate Ranking:** Combines semantic similarity and strict skill coverage into a weighted score.
- **Interactive Dashboard:** Displays candidate rankings, scores, skill-gap details, and charts.
- **CSV Export:** Allows screening results to be downloaded for further analysis.
- **Automated Tests:** Includes test files for parsing, matching, ranking, skill extraction, and skill-gap analysis.

## System Architecture

The application follows this workflow:

1. The recruiter enters the job description and required skills.
2. Multiple PDF or DOCX resumes are uploaded.
3. Resume text is extracted using PyMuPDF and python-docx.
4. Semantic similarity and skill extraction are performed.
5. Skill gaps and strict skill coverage are calculated.
6. Candidates are ranked using a weighted scoring method.
7. Results are displayed on the dashboard and can be exported as a CSV file.

## Technologies Used

| Component | Technology |
|---|---|
| Programming Language | Python |
| Web Dashboard | Streamlit |
| PDF Parsing | PyMuPDF |
| DOCX Parsing | python-docx |
| Semantic Similarity | Sentence-Transformers |
| Embedding Model | all-MiniLM-L6-v2 |
| Similarity Calculation | Cosine Similarity |
| Machine Learning Utilities | Scikit-learn |
| Data Processing | NumPy, Pandas |
| Visualization | Plotly |
| Testing | Python test scripts |

## Scoring Method

The default combined candidate score uses two components:

- Semantic similarity: 70%
- Strict skill coverage: 30%

**Combined Score = (0.70 × Semantic Similarity) + (0.30 × Strict Skill Coverage)**

The weights can be adjusted through the dashboard. Strict skill coverage is based on explicitly detected required skills; potential semantic matches are shown separately for human review.

## Project Structure

```text
AI-Resume-Screening/
├── app.py
├── requirements.txt
├── .gitignore
├── src/
│   ├── matcher.py
│   ├── ranker.py
│   ├── resume_parser.py
│   ├── skill_extractor.py
│   └── skill_gap.py
├── test_additional_domains.py
├── test_candidate_skills.py
├── test_domain_skills.py
├── test_matcher.py
├── test_parser.py
├── test_ranker.py
├── test_semantic_skill_gap.py
├── test_semantic_validation.py
├── test_skill_extractor.py
└── test_skill_gap.py
```

## Installation and Setup

### Prerequisites

- Python 3.10 or a compatible Python version
- Git
- pip

### 1. Clone the repository

```bash
git clone https://github.com/AkshayaA224/AI-Resume-Screening.git
cd AI-Resume-Screening
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the application

```powershell
streamlit run app.py --server.fileWatcherType none
```

The terminal will display a local URL where you can open the dashboard in your browser.

The first use of the semantic model may require an internet connection to download the pretrained model.

## How to Use

1. Open the Streamlit dashboard.
2. Enter a job title and job description.
3. Enter the required skills, one per line.
4. Upload one or more PDF or DOCX resumes.
5. Review candidate rankings and scores.
6. Inspect matched skills, missing skills, and suggestions requiring review.
7. Download the results as a CSV file if needed.

## Important Limitations

- The ranking score is a screening indicator, not a probability of being hired.
- A skill not detected in a resume may still be possessed by the candidate.
- Semantic skill suggestions require human verification.
- Recruiters should review original resumes and consider relevant qualifications beyond automated scores.

This project is intended to support human decision-making, not replace it.

## Future Enhancements

- Add more skill categories and domain-specific evaluation.
- Improve explainability of candidate ranking.
- Add recruiter feedback and configurable screening criteria.
- Expand evaluation using diverse, appropriately anonymized test resumes.
- Improve accessibility and dashboard reporting.

## Author

**Akshaya A**

GitHub: [AkshayaA224](https://github.com/AkshayaA224)
