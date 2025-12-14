// ---------- Dashboard: match analysis (paste + file upload) ----------

const analyzeBtn = document.getElementById("analyzeBtn");
const resumeTextEl = document.getElementById("resumeText");
const jdTextEl = document.getElementById("jdText");
const resumeFileEl = document.getElementById("resumeFile");
const jdFileEl = document.getElementById("jdFile");

const matchResultEl = document.getElementById("matchResult");
const overallScoreEl = document.getElementById("overallScore");
const gapAnalysisEl = document.getElementById("gapAnalysis");
const actionTipsEl = document.getElementById("actionTips");

if (analyzeBtn) {
    analyzeBtn.addEventListener("click", async () => {
        const formData = new FormData();

        const resumeText = (resumeTextEl?.value || "").trim();
        const jdText = (jdTextEl?.value || "").trim();

        formData.append("resume_text", resumeText);
        formData.append("jd_text", jdText);

        if (resumeFileEl && resumeFileEl.files[0]) {
            formData.append("resume_file", resumeFileEl.files[0]);
        }
        if (jdFileEl && jdFileEl.files[0]) {
            formData.append("jd_file", jdFileEl.files[0]);
        }

        analyzeBtn.disabled = true;
        analyzeBtn.textContent = "Analyzing...";

        try {
            const res = await fetch("/api/match", {
                method: "POST",
                body: formData,
            });

            if (!res.ok) {
                let errText = "Error analyzing match.";
                try {
                    const err = await res.json();
                    errText = err.error || errText;
                } catch (_) {}
                alert(errText);
                return;
            }

            const data = await res.json();
            renderMatchResult(data);
        } catch (err) {
            console.error(err);
            alert("Network error. Is backend running?");
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = "Analyze Match";
        }
    });
}

function renderMatchResult(data) {
    if (!matchResultEl) return;

    const scores = data.scores;
    const gap = data.gap_analysis;

    matchResultEl.classList.remove("hidden");

    overallScoreEl.textContent = scores.summary;

    const lines = gap.analysis_lines || [];
    if (lines.length) {
        const html = "<ul>" + lines.map(line => `<li>${line}</li>`).join("") + "</ul>";
        gapAnalysisEl.innerHTML = html;
    } else {
        gapAnalysisEl.textContent = "No major issues found. Your resume is already close to this JD.";
    }

    actionTipsEl.innerHTML = "";
    (gap.tips_lines || []).forEach(tip => {
        const li = document.createElement("li");
        li.textContent = tip;
        actionTipsEl.appendChild(li);
    });
}

// ---------- Profile (localStorage) ----------

const profileNameEl = document.getElementById("profileName");
const profileEmailEl = document.getElementById("profileEmail");
const profilePhoneEl = document.getElementById("profilePhone");
const profileRoleEl = document.getElementById("profileRole");
const profileSkillsEl = document.getElementById("profileSkills");
const profileLinksEl = document.getElementById("profileLinks");
const saveProfileBtn = document.getElementById("saveProfileBtn");
const profileSummaryEl = document.getElementById("profileSummary");

function loadProfile() {
    if (!profileSummaryEl) return;
    const raw = localStorage.getItem("cc_profile");
    if (!raw) return;

    try {
        const p = JSON.parse(raw);
        if (profileNameEl) profileNameEl.value = p.name || "";
        if (profileEmailEl) profileEmailEl.value = p.email || "";
        if (profilePhoneEl) profilePhoneEl.value = p.phone || "";
        if (profileRoleEl) profileRoleEl.value = p.role || "";
        if (profileSkillsEl) profileSkillsEl.value = p.skills || "";
        if (profileLinksEl) profileLinksEl.value = p.links || "";
        renderProfileSummary(p);
    } catch (e) {
        console.error("Error parsing profile:", e);
    }
}

function renderProfileSummary(p) {
    if (!profileSummaryEl) return;
    const name = p.name || "You";
    const role = p.role || "your target role";
    const skills = p.skills || "";
    const links = p.links || "";

    const lines = [];
    lines.push(`${name}, you are currently targeting <b>${role}</b>.`);
    if (skills) {
        lines.push(`Your key skills: ${skills}.`);
    } else {
        lines.push(`You have not yet listed your key skills. Add them to get a clearer picture.`);
    }
    if (links) {
        lines.push(`Important links: ${links}. Make sure recruiters can easily open your GitHub and LinkedIn.`);
    } else {
        lines.push(`Consider adding GitHub and LinkedIn links so companies can quickly check your work.`);
    }
    lines.push(`Next step: align your skills and projects with the roadmaps for ${role} and keep updating your resume.`);

    profileSummaryEl.innerHTML = lines.map(l => `<p>${l}</p>`).join("");
}

if (saveProfileBtn) {
    saveProfileBtn.addEventListener("click", () => {
        const p = {
            name: profileNameEl?.value.trim() || "",
            email: profileEmailEl?.value.trim() || "",
            phone: profilePhoneEl?.value.trim() || "",
            role: profileRoleEl?.value.trim() || "",
            skills: profileSkillsEl?.value.trim() || "",
            links: profileLinksEl?.value.trim() || "",
        };
        localStorage.setItem("cc_profile", JSON.stringify(p));
        renderProfileSummary(p);
        alert("Profile saved in this browser.");
    });
}

// Load profile on page load (if profile page)
loadProfile();
