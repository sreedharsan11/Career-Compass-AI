from flask import Flask, render_template, request, jsonify

from utils.resume_parser import extract_resume_info
from utils.jd_parser import extract_jd_info
from utils.scorer import calculate_match_score
from utils.gap_analysis import generate_gap_analysis
from utils.pdf_reader import extract_text_from_pdf
from utils.docx_reader import extract_text_from_docx

app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/roadmaps")
def roadmaps():
    return render_template("roadmaps.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/interview-prep")
def interview_prep():
    return render_template("interview_prep.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


def _extract_text_from_file(file_storage):
    if not file_storage or file_storage.filename == "":
        return ""

    filename = file_storage.filename.lower()
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_storage)
    if filename.endswith(".docx"):
        return extract_text_from_docx(file_storage)
    if filename.endswith(".txt"):
        file_storage.stream.seek(0)
        data = file_storage.read().decode(errors="ignore")
        return data

    file_storage.stream.seek(0)
    try:
        return file_storage.read().decode(errors="ignore")
    except Exception:
        return ""


@app.route("/api/match", methods=["POST"])
def match():
    resume_text = ""
    jd_text = ""

    if request.is_json:
        data = request.get_json()
        resume_text = (data.get("resume_text") or "").strip()
        jd_text = (data.get("jd_text") or "").strip()
    else:
        resume_text = (request.form.get("resume_text") or "").strip()
        jd_text = (request.form.get("jd_text") or "").strip()

        resume_file = request.files.get("resume_file")
        jd_file = request.files.get("jd_file")

        if resume_file and resume_file.filename:
            extracted = _extract_text_from_file(resume_file)
            if extracted.strip():
                resume_text = extracted.strip()

        if jd_file and jd_file.filename:
            extracted = _extract_text_from_file(jd_file)
            if extracted.strip():
                jd_text = extracted.strip()

    if not resume_text or not jd_text:
        return jsonify({"error": "Please provide resume and job description (either paste or upload)."}), 400

    resume_info = extract_resume_info(resume_text)
    jd_info = extract_jd_info(jd_text)

    scores = calculate_match_score(
        resume_info["skills"], jd_info["required_skills"],
        resume_info["tools"], jd_info["required_tools"]
    )

    gap = generate_gap_analysis(resume_info, jd_info)

    return jsonify({
        "scores": scores,
        "gap_analysis": gap
    })


if __name__ == "__main__":
    app.run(debug=True)
