from .resume_parser import _extract, SKILL_KEYWORDS, TOOL_KEYWORDS


def extract_jd_info(text: str):
    required_skills = _extract(text, SKILL_KEYWORDS)
    required_tools = _extract(text, TOOL_KEYWORDS)
    return {
        "required_skills": required_skills,
        "required_tools": required_tools,
        "raw_text": text,
    }
