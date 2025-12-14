def calculate_match_score(resume_skills, jd_skills, resume_tools, jd_tools):
    rs = set(resume_skills)
    js = set(jd_skills)
    rt = set(resume_tools)
    jt = set(jd_tools)

    skill_matched = rs & js
    tool_matched = rt & jt

    skill_score = (len(skill_matched) / len(js) * 10) if js else 0
    tool_score = (len(tool_matched) / len(jt) * 10) if jt else 0

    if js and jt:
        overall = 0.7 * skill_score + 0.3 * tool_score
    elif js:
        overall = skill_score
    elif jt:
        overall = tool_score
    else:
        overall = 0

    skill_score = round(skill_score, 1)
    tool_score = round(tool_score, 1)
    overall = round(overall, 1)

    if overall >= 8:
        label = "Strong Match"
    elif overall >= 5:
        label = "Moderate Match"
    else:
        label = "Weak Match"

    summary = f"{label} – {overall}/10"
    if js:
        summary += f" (Skills matched: {len(skill_matched)}/{len(js)})"
    if jt:
        summary += f", Tools matched: {len(tool_matched)}/{len(jt)})"

    return {
        "overall_score": overall,
        "match_label": label,
        "summary": summary,
        "matched_skills": sorted(skill_matched),
        "matched_tools": sorted(tool_matched),
    }
