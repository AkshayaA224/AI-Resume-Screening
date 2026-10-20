
import re
from typing import Optional


# ============================================================
# DOMAIN-INDEPENDENT SKILL VOCABULARY
# ============================================================

SKILL_ALIASES = {
    # IT AND PROGRAMMING
    "python": ["python", "python programming"],
    "java": ["java", "java programming"],
    "c": ["c programming", "c language"],
    "c++": ["c++", "cpp"],
    "c#": ["c#", "c sharp"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript"],
    "scala": ["scala"],
    "r programming": ["r programming", "r language"],
    "go": ["golang", "go programming"],
    "rust": ["rust programming", "rust language"],
    "php": ["php"],
    "ruby": ["ruby programming"],
    "kotlin": ["kotlin"],
    "swift": ["swift programming"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "react": ["react", "react.js", "reactjs"],
    "angular": ["angular", "angularjs"],
    "vue": ["vue", "vue.js", "vuejs"],
    "node.js": ["node.js", "nodejs"],
    "express.js": ["express.js", "expressjs"],
    "django": ["django"],
    "flask": ["flask"],
    "fastapi": ["fastapi", "fast api"],
    "spring boot": ["spring boot", "springboot"],
    "rest api": ["rest api", "rest apis", "restful api", "restful apis"],
    "graphql": ["graphql"],
    "microservices": ["microservices", "microservice architecture"],
    "object-oriented programming": [
        "object-oriented programming", "object oriented programming", "oop"
    ],
    "data structures": ["data structures", "data structure"],
    "algorithms": ["algorithms", "algorithm design"],
    "software development": ["software development"],
    "software testing": ["software testing", "test automation"],
    "unit testing": ["unit testing", "unit tests"],
    "selenium": ["selenium", "selenium webdriver"],
    "git": ["git", "version control with git"],
    "github": ["github"],
    "gitlab": ["gitlab"],
    "linux": ["linux"],
    "windows": ["windows operating system", "windows"],
    "docker": ["docker", "containerization"],
    "kubernetes": ["kubernetes", "k8s"],
    "jenkins": ["jenkins"],
    "ci/cd": ["ci/cd", "continuous integration", "continuous delivery"],
    "agile": ["agile methodology", "agile"],
    "scrum": ["scrum"],
    "cybersecurity": ["cybersecurity", "cyber security", "information security"],
    "networking": ["computer networking", "network administration"],
    "api development": ["api development", "api design"],

    # DATABASES AND DATA ENGINEERING
    "sql": ["sql", "structured query language"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "sqlite": ["sqlite"],
    "oracle database": ["oracle database", "oracle db"],
    "mongodb": ["mongodb", "mongo db"],
    "redis": ["redis"],
    "database management": ["database management", "dbms"],
    "database design": ["database design"],
    "data modeling": ["data modeling", "data modelling"],
    "data warehousing": ["data warehousing", "data warehouse"],
    "etl": ["etl", "extract transform load"],
    "apache spark": ["apache spark", "spark"],
    "pyspark": ["pyspark", "py spark"],
    "hadoop": ["hadoop", "apache hadoop"],
    "kafka": ["apache kafka", "kafka"],
    "airflow": ["apache airflow", "airflow"],
    "data pipelines": ["data pipeline", "data pipelines"],
    "data cleaning": ["data cleaning", "data cleansing"],
    "data preprocessing": ["data preprocessing", "data pre-processing"],

    # AI, MACHINE LEARNING, AND ANALYTICS
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "artificial intelligence": ["artificial intelligence", "ai"],
    "natural language processing": ["natural language processing", "nlp"],
    "generative ai": [
        "generative ai", "genai", "generative artificial intelligence"
    ],
    "large language models": [
        "large language models", "large language model", "llms", "llm"
    ],
    "computer vision": ["computer vision"],
    "neural networks": ["neural networks", "neural network"],
    "reinforcement learning": ["reinforcement learning"],
    "supervised learning": ["supervised learning"],
    "unsupervised learning": ["unsupervised learning"],
    "scikit-learn": ["scikit-learn", "scikit learn", "sklearn"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch", "py torch"],
    "keras": ["keras"],
    "hugging face": ["hugging face", "huggingface"],
    "opencv": ["opencv", "open cv"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],

    # Data Visualization includes explicit chart/dashboard evidence.
    "data visualization": [
        "data visualization",
        "data visualisation",
        "visualizing data",
        "visualising data",
        "visualized data",
        "visualised data",
        "visualization dashboard",
        "visualisation dashboard",
        "visualization dashboards",
        "visualisation dashboards",
        "created charts",
        "create charts",
        "creating charts",
        "built charts",
        "created plots",
        "creating plots",
        "created graphs",
        "creating graphs",
        "charts and dashboards",
        "interactive dashboard",
        "interactive dashboards",
        "matplotlib",
        "seaborn",
        "plotly",
        "tableau",
        "power bi",
        "bokeh",
    ],
    "matplotlib": ["matplotlib"],
    "seaborn": ["seaborn"],
    "plotly": ["plotly"],
    "tableau": ["tableau"],
    "power bi": ["power bi", "powerbi", "microsoft power bi"],
    "data analysis": ["data analysis", "data analytics"],
    "exploratory data analysis": ["exploratory data analysis", "eda"],
    "statistics": ["statistics", "statistical analysis"],
    "probability": ["probability theory"],
    "hypothesis testing": ["hypothesis testing"],
    "regression analysis": ["regression analysis"],
    "classification": ["classification algorithms", "classification"],
    "clustering": ["clustering", "cluster analysis"],
    "time series analysis": ["time series analysis", "time-series analysis"],
    "feature engineering": ["feature engineering"],
    "model evaluation": ["model evaluation", "model validation"],
    "sentiment analysis": ["sentiment analysis", "opinion mining"],
    "text mining": ["text mining"],
    "recommendation systems": ["recommendation systems", "recommender systems"],
    "prompt engineering": ["prompt engineering"],
    "retrieval augmented generation": [
        "retrieval augmented generation",
        "retrieval-augmented generation",
        "rag",
    ],
    "mlops": ["mlops", "machine learning operations"],
    "experiment tracking": ["experiment tracking", "ml experiment tracking"],

    # CLOUD AND DEVOPS
    "amazon web services": ["amazon web services", "aws"],
    "microsoft azure": ["microsoft azure", "azure"],
    "google cloud": ["google cloud platform", "google cloud", "gcp"],
    "cloud computing": ["cloud computing"],
    "terraform": ["terraform"],
    "ansible": ["ansible"],
    "prometheus": ["prometheus"],
    "grafana": ["grafana"],
    "serverless computing": ["serverless computing", "serverless"],

    # CIVIL ENGINEERING
    "civil engineering": ["civil engineering"],
    "autocad": ["autocad", "auto cad"],
    "revit": ["revit", "autodesk revit"],
    "staad.pro": ["staad.pro", "staad pro", "staad"],
    "etabs": ["etabs"],
    "primavera p6": ["primavera p6", "primavera"],
    "building information modeling": [
        "building information modeling",
        "building information modelling",
        "bim",
    ],
    "structural analysis": ["structural analysis"],
    "structural design": ["structural design"],
    "quantity surveying": ["quantity surveying", "quantity surveyor"],
    "construction management": ["construction management"],
    "project planning": ["project planning", "construction planning"],
    "site supervision": ["site supervision", "site management"],
    "concrete technology": ["concrete technology"],
    "geotechnical engineering": ["geotechnical engineering"],
    "transportation engineering": ["transportation engineering"],
    "surveying": ["surveying", "land surveying"],
    "estimation and costing": ["estimation and costing", "cost estimation"],
    "environmental engineering": ["environmental engineering"],
    "highway engineering": ["highway engineering"],
    "water resources engineering": ["water resources engineering"],
    "gis": ["geographic information system", "geographic information systems", "gis"],

    # MECHANICAL ENGINEERING
    "solidworks": ["solidworks", "solid works"],
    "catia": ["catia", "catia v5", "catia v6"],
    "ansys": ["ansys", "ansys workbench"],
    "creo": ["creo", "creo parametric", "ptc creo"],
    "computer aided manufacturing": ["computer aided manufacturing", "cam"],
    "gd&t": ["gd&t", "gd and t", "geometric dimensioning and tolerancing"],
    "cnc machining": ["cnc machining", "cnc programming"],
    "thermodynamics": ["thermodynamics"],
    "fluid mechanics": ["fluid mechanics"],
    "heat transfer": ["heat transfer"],
    "finite element analysis": ["finite element analysis", "fea"],
    "product design": ["product design"],
    "manufacturing processes": ["manufacturing processes", "manufacturing process"],
    "lean manufacturing": ["lean manufacturing"],
    "six sigma": ["six sigma"],
    "maintenance engineering": ["maintenance engineering", "industrial maintenance"],
    "robotics": ["robotics", "industrial robotics"],

    # ELECTRICAL AND ELECTRONICS
    "matlab": ["matlab"],
    "simulink": ["simulink"],
    "embedded systems": ["embedded systems", "embedded system design"],
    "vlsi": ["vlsi", "very large scale integration"],
    "verilog": ["verilog", "verilog hdl"],
    "vhdl": ["vhdl"],
    "pcb design": ["pcb design", "printed circuit board design"],
    "circuit design": ["circuit design", "electronic circuit design"],
    "power systems": ["power systems", "electrical power systems"],
    "power electronics": ["power electronics"],
    "electrical machines": ["electrical machines", "electric machines"],
    "control systems": ["control systems", "control system design"],
    "scada": ["scada", "supervisory control and data acquisition"],
    "plc programming": [
        "plc programming",
        "programmable logic controller programming",
    ],
    "instrumentation": ["instrumentation", "industrial instrumentation"],
    "internet of things": ["internet of things", "iot"],
    "arduino": ["arduino"],
    "raspberry pi": ["raspberry pi"],
    "digital signal processing": ["digital signal processing", "dsp"],
    "electrical wiring": ["electrical wiring", "electrical installation"],
    "electrical safety": ["electrical safety"],
    "renewable energy": ["renewable energy", "solar energy systems"],

    # FINANCE AND ACCOUNTING
    "financial analysis": ["financial analysis", "financial statement analysis"],
    "financial modelling": ["financial modelling", "financial modeling"],
    "financial reporting": ["financial reporting"],
    "accounting": ["accounting", "financial accounting"],
    "auditing": ["auditing", "internal audit", "external audit"],
    "taxation": ["taxation", "tax accounting"],
    "gst": ["goods and services tax", "gst"],
    "tally": ["tally", "tally erp", "tally prime"],
    "sap": ["sap", "sap erp"],
    "budgeting": ["budgeting", "budget preparation"],
    "financial forecasting": ["financial forecasting"],
    "risk management": ["risk management", "financial risk management"],
    "accounts payable": ["accounts payable"],
    "accounts receivable": ["accounts receivable"],
    "bank reconciliation": ["bank reconciliation", "bank reconciliations"],
    "payroll accounting": ["payroll accounting", "payroll processing"],
    "corporate finance": ["corporate finance"],
    "investment analysis": ["investment analysis", "portfolio analysis"],
    "excel": ["microsoft excel", "ms excel", "excel"],
    "quickbooks": ["quickbooks"],
    "bloomberg terminal": ["bloomberg terminal", "bloomberg"],
    "cost accounting": ["cost accounting"],
    "management accounting": ["management accounting"],

    # MARKETING AND BUSINESS
    "search engine optimization": ["search engine optimization", "seo"],
    "search engine marketing": ["search engine marketing", "sem"],
    "google analytics": ["google analytics", "ga4", "google analytics 4"],
    "digital marketing": ["digital marketing", "online marketing"],
    "content marketing": ["content marketing"],
    "social media marketing": ["social media marketing", "social media management"],
    "email marketing": ["email marketing", "email campaigns"],
    "market research": ["market research", "consumer research"],
    "brand management": ["brand management"],
    "campaign management": ["campaign management", "marketing campaigns"],
    "customer relationship management": ["customer relationship management", "crm"],
    "salesforce": ["salesforce"],
    "hubspot": ["hubspot"],
    "lead generation": ["lead generation", "prospecting"],
    "business analysis": ["business analysis", "business analyst"],
    "business intelligence": ["business intelligence", "bi reporting"],
    "kpi reporting": ["kpi reporting", "key performance indicator reporting"],
    "competitive analysis": ["competitive analysis", "competitor analysis"],
    "market segmentation": ["market segmentation"],
    "conversion rate optimization": ["conversion rate optimization", "cro"],
    "public relations": ["public relations", "pr"],
    "sales management": ["sales management"],
    "e-commerce": ["e-commerce", "ecommerce", "electronic commerce"],

    # HUMAN RESOURCES
    "recruitment": ["recruitment", "talent acquisition", "candidate sourcing"],
    "applicant tracking systems": [
        "applicant tracking system", "applicant tracking systems", "ats"
    ],
    "employee onboarding": ["employee onboarding", "onboarding"],
    "employee engagement": ["employee engagement"],
    "performance management": ["performance management", "performance appraisal"],
    "human resource information systems": [
        "human resource information system",
        "human resource information systems",
        "hris",
    ],
    "workforce planning": ["workforce planning", "manpower planning"],
    "employee relations": ["employee relations", "industrial relations"],
    "compensation and benefits": ["compensation and benefits", "benefits administration"],
    "hr policies": ["hr policies", "human resources policies"],
    "training and development": ["training and development", "learning and development"],
    "labor law compliance": [
        "labor law compliance", "labour law compliance", "employment law compliance"
    ],
    "human resources analytics": [
        "human resources analytics", "hr analytics", "people analytics"
    ],
    "payroll management": ["payroll management", "payroll administration"],
    "conflict resolution": ["conflict resolution"],
    "organizational development": ["organizational development"],
    "leave management": ["leave management"],
    "employee retention": ["employee retention"],

    # HEALTHCARE AND LIFE SCIENCES
    "medical coding": ["medical coding", "clinical coding"],
    "medical terminology": ["medical terminology"],
    "clinical research": ["clinical research", "clinical trials"],
    "clinical data management": ["clinical data management"],
    "electronic health records": [
        "electronic health records", "electronic medical records", "ehr", "emr"
    ],
    "patient care": ["patient care", "direct patient care"],
    "patient records management": [
        "patient records management", "medical records management"
    ],
    "laboratory techniques": ["laboratory techniques", "laboratory procedures"],
    "quality control": ["quality control", "qc"],
    "good clinical practice": ["good clinical practice", "gcp"],
    "good laboratory practice": ["good laboratory practice", "glp"],
    "pharmacovigilance": ["pharmacovigilance", "drug safety"],
    "public health": ["public health"],
    "epidemiology": ["epidemiology"],
    "bioinformatics": ["bioinformatics"],
    "biostatistics": ["biostatistics"],
    "healthcare compliance": ["healthcare compliance", "hipaa compliance"],
    "medical billing": ["medical billing", "medical claims processing"],
    "health information management": ["health information management", "him"],
    "first aid": ["first aid", "basic first aid"],
    "phlebotomy": ["phlebotomy"],
    "medical transcription": ["medical transcription"],
    "clinical documentation": ["clinical documentation"],
    "infection control": ["infection control"],
    "healthcare administration": ["healthcare administration", "hospital administration"],

    # GENERAL PROFESSIONAL SKILLS
    "communication": [
        "communication skills", "verbal communication", "written communication"
    ],
    "teamwork": ["teamwork", "team player", "collaboration"],
    "leadership": ["leadership", "team leadership"],
    "problem solving": ["problem solving", "problem-solving"],
    "critical thinking": ["critical thinking"],
    "time management": ["time management"],
    "project management": ["project management"],
    "presentation skills": ["presentation skills", "presentations"],
    "attention to detail": ["attention to detail"],
    "adaptability": ["adaptability", "adaptable"],
    "decision making": ["decision making", "decision-making"],
    "negotiation": ["negotiation", "negotiation skills"],
    "customer service": ["customer service", "customer support"],
    "technical writing": ["technical writing"],
    "research": ["research skills", "research methodology"],
}


# ============================================================
# NORMALIZATION AND LOOKUP
# ============================================================

def _normalise_text(text: str) -> str:
    """Lowercase text and normalize punctuation and whitespace."""
    text = str(text or "").casefold()
    text = text.replace("&", " and ")
    text = re.sub(r"[\u2010-\u2015]", "-", text)
    text = re.sub(r"[^a-z0-9+#./-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _term_pattern(term: str) -> re.Pattern:
    """Create a phrase pattern with alphanumeric boundaries."""
    normalized = _normalise_text(term)
    parts = normalized.split()
    body = r"\s+".join(re.escape(part) for part in parts)

    return re.compile(
        rf"(?<![a-z0-9]){body}(?![a-z0-9])",
        re.IGNORECASE,
    )


def contains_term(text: str, term: str) -> bool:
    """Check whether a complete phrase appears in text."""
    if not text or not term:
        return False

    normalized_text = _normalise_text(text)
    normalized_term = _normalise_text(term)

    if not normalized_text or not normalized_term:
        return False

    return bool(_term_pattern(normalized_term).search(normalized_text))


def _build_skill_lookup() -> dict:
    """Map canonical names and aliases to canonical skill names."""
    lookup = {}

    for canonical, aliases in SKILL_ALIASES.items():
        canonical_name = _normalise_text(canonical)
        lookup[canonical_name] = canonical_name

        for alias in aliases:
            alias_name = _normalise_text(alias)
            if alias_name:
                # Preserve the first mapping if an alias is ambiguous.
                lookup.setdefault(alias_name, canonical_name)

    return lookup


_SKILL_LOOKUP = _build_skill_lookup()


def normalize_skill_name(skill: str) -> str:
    """Return a canonical skill name when a known alias is supplied."""
    normalized = _normalise_text(skill)

    if not normalized:
        return ""

    return _SKILL_LOOKUP.get(normalized, normalized)


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_skills(
    text: str,
    extra_skills: Optional[list] = None,
) -> list:
    """
    Extract known skills and optional recruiter-defined skills.

    Recruiter-defined skills are checked as exact phrases, so they
    can be used without adding each new skill to SKILL_ALIASES.
    """
    if not text:
        return []

    found = set()

    # Find known skills using their canonical names and aliases.
    for canonical, aliases in SKILL_ALIASES.items():
        for candidate in [canonical] + aliases:
            if contains_term(text, candidate):
                found.add(_normalise_text(canonical))
                break

    # Find additional skills supplied by the recruiter.
    for skill in extra_skills or []:
        canonical = normalize_skill_name(skill)

        if canonical and contains_term(text, skill):
            found.add(canonical)

    return sorted(found)


# ============================================================
# CONTACT INFORMATION EXTRACTION
# ============================================================

def extract_email(text: str) -> Optional[str]:
    """Extract the first email address from the supplied text."""
    if not text:
        return None

    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)

    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    """Extract a plausible phone number; not full number validation."""
    if not text:
        return None

    pattern = (
        r"(?<!\w)"
        r"(?:\+?\d{1,3}[\s.-]?)?"
        r"(?:\(?\d{2,5}\)?[\s.-]?)?"
        r"\d{3,5}[\s.-]?\d{3,5}"
        r"(?!\w)"
    )

    for match in re.finditer(pattern, text):
        candidate = match.group(0).strip()
        digits = re.sub(r"\D", "", candidate)

        if 10 <= len(digits) <= 15:
            return candidate

    return None


# ============================================================
# COMPLETE RESUME ANALYSIS
# ============================================================

def analyze_resume(
    text: str,
    extra_skills: Optional[list] = None,
) -> dict:
    """Return contact details and extracted skills from resume text."""
    skills = extract_skills(text, extra_skills=extra_skills)

    return {
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": skills,
        "skill_count": len(skills),
    }
