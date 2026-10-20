import os
import tempfile
import pandas as pd
import plotly.express as px
import streamlit as st

from src.resume_parser import extract_resume_text
from src.ranker import rank_candidate


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Resume Screening",
    page_icon="📄",
    layout="wide"
)


# --------------------------------------------------
# PROFESSIONAL SOFT-COLOR THEME
# --------------------------------------------------

st.markdown("""
<style>
/* Main application */
.stApp {
    background-color: #FAF9FC;
    color: #343247;
}

/* Main content spacing */
.block-container {
    max-width: 1450px;
    padding-top: 2.2rem;
    padding-bottom: 3rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #F0EDF7;
    border-right: 1px solid #E5DFEF;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #51446F;
}

/* Headings */
h1, h2, h3 {
    color: #353149;
    letter-spacing: -0.4px;
}

h1 {
    font-weight: 700;
}

h2, h3 {
    font-weight: 600;
}

/* Paragraphs and labels */
p, label, .stMarkdown {
    color: #514F63;
}

/* Input fields */
.stTextInput input,
.stTextArea textarea,
[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #DED9E9 !important;
    border-radius: 10px !important;
    color: #343247 !important;
}

/* Input focus */
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #A99BCB !important;
    box-shadow: 0 0 0 2px #EAE4F5 !important;
}

/* Upload area */
[data-testid="stFileUploader"] {
    background-color: #F4F1F9;
    border: 1px dashed #C9BFDF;
    border-radius: 14px;
    padding: 12px;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    background-color: #8172A8;
    color: #FFFFFF;
    border: 1px solid #8172A8;
    border-radius: 10px;
    padding: 0.55rem 1rem;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #6E5D98;
    border-color: #6E5D98;
    color: #FFFFFF;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E7E2EF;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 3px 12px rgba(66, 53, 94, 0.04);
}

[data-testid="stMetricLabel"] {
    color: #777187;
}

[data-testid="stMetricValue"] {
    color: #51446F;
    font-weight: 700;
}

/* Data tables */
[data-testid="stDataFrame"] {
    background-color: #FFFFFF;
    border: 1px solid #E7E2EF;
    border-radius: 12px;
    overflow: hidden;
}

/* Expanders */
[data-testid="stExpander"] {
    background-color: #FFFFFF;
    border: 1px solid #E7E2EF;
    border-radius: 12px;
}

/* Alerts and information boxes */
[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background-color: #8DAF9A;
}

/* Slider accent */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background-color: #8172A8;
    border-color: #8172A8;
}

/* Section dividers */
hr {
    border-color: #E8E3EF;
}

/* Footer text */
.small-caption {
    color: #827C91;
    font-size: 0.85rem;
}

/* Responsive layout */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def extract_uploaded_resume(uploaded_file):
    """
    Save an uploaded PDF or DOCX temporarily and extract
    its text using the existing resume parser.
    """
    extension = os.path.splitext(uploaded_file.name)[1].lower()

    if extension not in [".pdf", ".docx"]:
        raise ValueError("Only PDF and DOCX files are supported.")

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_path = temp_file.name

        resume_text = extract_resume_text(temp_path)

        if not resume_text or not resume_text.strip():
            raise ValueError(
                "No readable text was found. "
                "The resume may be scanned or empty."
            )

        return resume_text

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def get_value(data, possible_keys, default=None):
    """Retrieve a value while supporting common key variations."""
    if not isinstance(data, dict):
        return default

    for key in possible_keys:
        if key in data:
            return data[key]

    return default


def normalize_skill_list(value):
    """Convert a skill collection into a clean list of strings."""
    if value is None:
        return []

    if isinstance(value, str):
        return [value] if value.strip() else []

    if isinstance(value, (list, tuple, set)):
        return [str(item) for item in value]

    return []


def percentage(value):
    """Convert a decimal score to a percentage when necessary."""
    try:
        number = float(value)

        if 0 <= number <= 1:
            return number * 100

        return number
    except (TypeError, ValueError):
        return 0.0


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.title("⚙️ Screening Settings")

    st.write(
        "Configure how candidate relevance and skill "
        "coverage contribute to the ranking."
    )

    semantic_weight = st.slider(
        "Semantic similarity weight",
        min_value=0,
        max_value=100,
        value=70,
        step=5
    )

    skill_weight = 100 - semantic_weight

    st.metric(
        "Strict skill coverage weight",
        f"{skill_weight}%"
    )

    st.caption(
        "The two weights always add up to 100%. "
        "The skill coverage score uses exact detected matches."
    )


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("📄 AI-Based Resume Screening")
st.subheader("Resume Ranking and Skill Gap Analysis")

st.write(
    "Upload resumes, provide a job description, and identify "
    "how well each candidate matches the role."
)

st.info(
    "Screening results are preliminary decision-support indicators. "
    "Review the original resumes before making recruitment decisions."
)


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

st.header("1. Job Requirements")

job_title = st.text_input(
    "Job title",
    placeholder="Example: AI/ML Engineer"
)

job_description = st.text_area(
    "Job description",
    height=220,
    placeholder=(
        "Paste the responsibilities, qualifications, "
        "and technical requirements for the role here."
    )
)

required_skills_text = st.text_area(
    "Required skills — one skill per line",
    height=180,
    placeholder=(
        "Python\n"
        "SQL\n"
        "Machine Learning\n"
        "Pandas\n"
        "Data Analysis\n"
        "NLP\n"
        "Data Visualization\n"
        "Git"
    )
)

required_skills = [
    skill.strip()
    for skill in required_skills_text.splitlines()
    if skill.strip()
]


# --------------------------------------------------
# RESUME UPLOAD
# --------------------------------------------------

st.header("2. Upload Candidate Resumes")

uploaded_files = st.file_uploader(
    "Select one or more resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True,
    help="Upload text-based PDF or DOCX resumes."
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} resume(s) selected.")

    for uploaded_file in uploaded_files:
        st.write(f"📎 {uploaded_file.name}")


# --------------------------------------------------
# RUN SCREENING
# --------------------------------------------------

st.header("3. Run Screening")

run_screening = st.button(
    "🚀 Screen and Rank Candidates",
    type="primary",
    use_container_width=True
)

if run_screening:

    if not job_title.strip():
        st.error("Please enter a job title.")

    elif not job_description.strip():
        st.error("Please enter a job description.")

    elif not required_skills:
        st.error("Please enter at least one required skill.")

    elif not uploaded_files:
        st.error("Please upload at least one resume.")

    else:
        results = []
        failures = []

        semantic_weight_decimal = semantic_weight / 100
        skill_weight_decimal = skill_weight / 100

        progress = st.progress(0)
        status = st.empty()

        for index, uploaded_file in enumerate(uploaded_files):

            status.write(
                f"Processing {index + 1}/{len(uploaded_files)}: "
                f"{uploaded_file.name}"
            )

            try:
                resume_text = extract_uploaded_resume(uploaded_file)

                screening_result = rank_candidate(
                    resume_text=resume_text,
                    job_description=job_description,
                    required_skills=required_skills,
                    semantic_weight=semantic_weight_decimal,
                    skill_weight=skill_weight_decimal
                )

                if not isinstance(screening_result, dict):
                    raise ValueError(
                        "The ranker did not return the expected result."
                    )

                semantic_similarity = percentage(
                    get_value(
                        screening_result,
                        ["semantic_similarity", "similarity_score"],
                        0
                    )
                )

                skill_coverage = percentage(
                    get_value(
                        screening_result,
                        ["skill_coverage", "strict_skill_coverage"],
                        0
                    )
                )

                ranking_score = percentage(
                    get_value(
                        screening_result,
                        ["ranking_score", "combined_score"],
                        (
                            semantic_weight_decimal * semantic_similarity
                            + skill_weight_decimal * skill_coverage
                        )
                    )
                )

                gap = get_value(
                    screening_result,
                    ["skill_gap", "gap_analysis"],
                    {}
                )

                if not isinstance(gap, dict):
                    gap = {}

                matched_skills = normalize_skill_list(
                    get_value(
                        gap,
                        ["matched", "matched_skills", "exact_matches"],
                        []
                    )
                )

                semantic_matches = normalize_skill_list(
                    get_value(
                        gap,
                        [
                            "semantic_matches",
                            "review_needed_skills",
                            "review_needed"
                        ],
                        []
                    )
                )

                missing_skills = normalize_skill_list(
                    get_value(
                        gap,
                        ["missing_skills", "missing"],
                        []
                    )
                )

                results.append({
                    "candidate": os.path.splitext(uploaded_file.name)[0],
                    "file_name": uploaded_file.name,
                    "semantic_similarity": semantic_similarity,
                    "skill_coverage": skill_coverage,
                    "ranking_score": ranking_score,
                    "matched_skills": matched_skills,
                    "semantic_matches": semantic_matches,
                    "missing_skills": missing_skills,
                    "resume_text": resume_text
                })

            except Exception as error:
                failures.append({
                    "file_name": uploaded_file.name,
                    "error": str(error)
                })

            progress.progress((index + 1) / len(uploaded_files))

        status.empty()
        progress.empty()

        # Rank candidates by combined score.
        results.sort(
            key=lambda item: item["ranking_score"],
            reverse=True
        )

        st.session_state["screening_results"] = results
        st.session_state["screening_failures"] = failures
        st.session_state["screening_job_title"] = job_title
        st.session_state["screening_required_skills"] = required_skills

        st.success("Screening process completed.")


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

if "screening_results" in st.session_state:

    results = st.session_state["screening_results"]
    failures = st.session_state["screening_failures"]

    st.divider()
    st.header("4. Screening Dashboard")

    if results:

        best_candidate = results[0]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Processed", len(results))
        col2.metric("Failed", len(failures))
        col3.metric(
            "Top Candidate",
            best_candidate["candidate"]
        )
        col4.metric(
            "Top Score",
            f'{best_candidate["ranking_score"]:.2f}%'
        )

        st.subheader("Candidate Ranking")

        ranking_table = pd.DataFrame([
            {
                "Rank": index + 1,
                "Candidate": result["candidate"],
                "Resume": result["file_name"],
                "Semantic Similarity (%)": round(
                    result["semantic_similarity"], 2
                ),
                "Strict Skill Coverage (%)": round(
                    result["skill_coverage"], 2
                ),
                "Combined Score (%)": round(
                    result["ranking_score"], 2
                )
            }
            for index, result in enumerate(results)
        ])

        st.dataframe(
            ranking_table,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Candidate Score Comparison")

        # Convert the ranking table to long format for grouped bars.
        chart_data = ranking_table.melt(
            id_vars=["Candidate"],
            value_vars=[
                "Semantic Similarity (%)",
                "Strict Skill Coverage (%)",
                "Combined Score (%)"
            ],
            var_name="Metric",
            value_name="Score"
        )

        fig = px.bar(
            chart_data,
            x="Candidate",
            y="Score",
            color="Metric",
            barmode="group",
            text="Score",
            color_discrete_sequence=[
                            "#A99BCB", 
                            "#91B7A1",  
                            "#E3BFA3"   
            ],
            title="Candidate Performance by Screening Metric",
            labels={
                "Candidate": "Candidate",
                "Score": "Score (%)",
                "Metric": "Screening Metric"
            },
            range_y=[0, 100]
        )

        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside",
            cliponaxis=False
        )

        fig.update_layout(
            yaxis_title="Score (%)",
            xaxis_title="Candidate",
            yaxis=dict(range=[0, 115]),
            legend_title="Metric",
            margin=dict(t=70, b=40),
            height=480,
            bargap=0.25,
            bargroupgap=0.08
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # --------------------------------------------------
        # INDIVIDUAL CANDIDATE ANALYSIS
        # --------------------------------------------------

        st.subheader("Candidate Skill Gap Analysis")

        candidate_options = [
            result["file_name"] for result in results
        ]

        selected_file = st.selectbox(
            "Choose a candidate to inspect",
            candidate_options
        )

        selected_result = next(
            result for result in results
            if result["file_name"] == selected_file
        )

        st.markdown(f"### {selected_result['candidate']}")

        a, b, c = st.columns(3)

        a.metric(
            "Combined Score",
            f'{selected_result["ranking_score"]:.2f}%'
        )

        b.metric(
            "Semantic Similarity",
            f'{selected_result["semantic_similarity"]:.2f}%'
        )

        c.metric(
            "Strict Skill Coverage",
            f'{selected_result["skill_coverage"]:.2f}%'
        )

        matched = selected_result["matched_skills"]
        review = selected_result["semantic_matches"]
        missing = selected_result["missing_skills"]

        left, middle, right = st.columns(3)

        with left:
            st.markdown("#### ✅ Exact Matches")
            if matched:
                for skill in matched:
                    st.write(f"• {skill}")
            else:
                st.write("No exact skill matches detected.")

        with middle:
            st.markdown("#### 🔎 Review Needed")
            if review:
                for skill in review:
                    st.write(f"• {skill}")
                st.caption(
                    "These suggestions require human verification."
                )
            else:
                st.write("No review-needed matches reported.")

        with right:
            st.markdown("#### ❌ Not Detected")
            if missing:
                for skill in missing:
                    st.write(f"• {skill}")
            else:
                st.write("No missing skills reported.")

        with st.expander("View extracted resume text"):
            st.text(selected_result["resume_text"])

        # --------------------------------------------------
        # DOWNLOAD RESULTS
        # --------------------------------------------------

        st.subheader("Download Results")

        # Detailed export containing ranking and skill-gap information.
        detailed_export = pd.DataFrame([
            {
                "Rank": index + 1,
                "Candidate": result["candidate"],
                "Resume": result["file_name"],
                "Semantic Similarity (%)": round(
                    result["semantic_similarity"], 2
                ),
                "Strict Skill Coverage (%)": round(
                    result["skill_coverage"], 2
                ),
                "Combined Score (%)": round(
                    result["ranking_score"], 2
                ),
                "Exact Matched Skills": "; ".join(
                    result["matched_skills"]
                ),
                "Review-Needed Skills": "; ".join(
                    result["semantic_matches"]
                ),
                "Missing Skills": "; ".join(
                    result["missing_skills"]
                )
            }
            for index, result in enumerate(results)
        ])

        csv_data = detailed_export.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            label="⬇️ Download Detailed Screening Report (CSV)",
            data=csv_data,
            file_name="resume_screening_detailed_report.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.caption(
            "The report contains candidate rankings, screening scores, "
            "exact skill matches, review-needed skills and missing skills."
        )

