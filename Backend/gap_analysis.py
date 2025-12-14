def generate_gap_analysis(resume_info, jd_info):
    rs = set(resume_info.get("skills", []))
    rt = set(resume_info.get("tools", []))
    js = set(jd_info.get("required_skills", []))
    jt = set(jd_info.get("required_tools", []))

    missing_skills = sorted(js - rs)
    missing_tools = sorted(jt - rt)

    analysis_lines = []

    # Coverage stats based directly on resume vs JD
    if js:
        analysis_lines.append(
            f"- You cover {len(rs & js)} out of {len(js)} key technical skills mentioned in this JD."
        )
    else:
        analysis_lines.append(
            "- This JD does not list many explicit skills, so focus on general fundamentals and common tools."
        )

    if jt:
        analysis_lines.append(
            f"- You cover {len(rt & jt)} out of {len(jt)} tools / technologies mentioned in the JD."
        )

    # Missing items explicitly
    if missing_skills:
        first_skills = ", ".join(missing_skills[:7])
        analysis_lines.append(
            f"- Important technical skills missing from your resume compared to this JD: {first_skills}."
        )
    if missing_tools:
        first_tools = ", ".join(missing_tools[:7])
        analysis_lines.append(
            f"- Tools / platforms missing or not clearly visible in your resume: {first_tools}."
        )

    # Additional checks from resume text (formatting / structure)
    raw_resume = resume_info.get("raw_text", "").lower()
    if "github" not in raw_resume:
        analysis_lines.append(
            "- Your resume does not clearly mention a GitHub profile. Recruiters expect code samples for tech roles."
        )
    if "project" not in raw_resume:
        analysis_lines.append(
            "- There is no clear PROJECTS section. Projects are crucial to prove your skills as a fresher."
        )
    if "summary" not in raw_resume and "objective" not in raw_resume:
        analysis_lines.append(
            "- A short SUMMARY or CAREER OBJECTIVE at the top is missing. It helps recruiters understand your target role quickly."
        )
    if len(raw_resume.split()) < 150:
        analysis_lines.append(
            "- Your resume seems very short. You might not be showcasing enough projects, skills, or responsibilities."
        )
    if len(raw_resume.split()) > 600:
        analysis_lines.append(
            "- Your resume seems quite long. Try to keep it focused and concise (1 page for fresher/entry-level)."
        )

    if not analysis_lines:
        analysis_lines.append(
            "- Your resume already aligns well with this JD. Focus on clearer formatting and measurable results in your bullets."
        )

    # Actionable tips – directly driven by the gaps found
    tips_lines = []

    if missing_skills:
        tips_lines.append(
            f"• Choose 2–3 core missing skills from the JD (for example: {', '.join(missing_skills[:3])}) and learn them with one mini-project each."
        )
        tips_lines.append(
            "• After learning these skills, update your SKILLS section and mention them clearly under the correct category (Languages / Frameworks / Libraries)."
        )
    if missing_tools:
        tips_lines.append(
            f"• Practice the missing tools (for example: {', '.join(missing_tools[:3])}) by building a small demo and then add them both in Skills and in your project descriptions."
        )

    if 'project' not in raw_resume:
        tips_lines.append(
            "• Create at least 2–3 solid projects that use the main skills and tools from this JD, and list them in a dedicated PROJECTS section."
        )
    else:
        tips_lines.append(
            "• Improve your existing project bullets by adding impact: describe the problem, what you built, tools used, and the result (e.g., performance, usability, or accuracy)."
        )

    if 'github' not in raw_resume:
        tips_lines.append(
            "• Add your GitHub link near the top of your resume and ensure the repositories mentioned in your projects are public and well-documented."
        )

    tips_lines.append(
        "• Re-order your SKILLS section so that the skills requested in this JD appear in the first 5–7 items the recruiter reads."
    )
    tips_lines.append(
        "• For each job you apply to, quickly scan the JD, highlight repeated keywords, and mirror those (honestly) in your Skills and Projects."
    )
    tips_lines.append(
        "• If you are a fresher, highlight internships, online courses, and hands-on labs as proof of practical exposure, not just theory."
    )
    tips_lines.append(
        "• Keep the design simple: 1 page, clear headings (Summary, Skills, Projects, Experience, Education), enough white space, and consistent fonts."
    )

    # remove duplicates
    seen = set()
    unique_tips = []
    for t in tips_lines:
        if t not in seen:
            seen.add(t)
            unique_tips.append(t)

    single_tip = unique_tips[0] if unique_tips else (
        "Overall your profile is good; focus on clearer resume formatting and stronger project descriptions."
    )

    return {
        "missing_skills": missing_skills,
        "missing_tools": missing_tools,
        "analysis_lines": analysis_lines,
        "tips_lines": unique_tips,
        "single_improvement_tip": single_tip,
    }
