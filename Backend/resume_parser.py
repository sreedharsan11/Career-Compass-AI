import re

SKILL_KEYWORDS = [
    "python", "java", "c", "c++", "javascript", "html", "css", "react",
    "node", "sql", "mysql", "postgresql", "mongodb",
    "machine learning", "ml", "data analysis", "data science",
    "excel", "power bi", "tableau",
    "git", "docker", "flask", "django", "rest api",
]

TOOL_KEYWORDS = [
    "numpy", "pandas", "matplotlib", "scikit-learn",
    "tensorflow", "pytorch", "jupyter",
    "vs code", "vscode", "postman", "figma",
]

SOFT_SKILLS = [
    "communication", "teamwork", "leadership",
    "problem solving", "time management", "presentation"
]


def _normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9+\s\.]", " ", text)
    return text


def _extract(text: str, keywords):
    text = _normalize(text)
    found = set()
    for kw in keywords:
        pattern = r"\b" + re.escape(kw.lower()) + r"\b"
        if re.search(pattern, text):
            found.add(kw.lower())
    return sorted(found)


def extract_resume_info(text: str):
    skills = _extract(text, SKILL_KEYWORDS)
    tools = _extract(text, TOOL_KEYWORDS)
    soft = _extract(text, SOFT_SKILLS)
    return {
        "skills": skills,
        "tools": tools,
        "soft_skills": soft,
        "raw_text": text,
    }
