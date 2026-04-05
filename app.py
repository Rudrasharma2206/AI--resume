import streamlit as st
import pdfplumber
import os
import re
import requests
from dotenv import load_dotenv
 
load_dotenv()
 
st.set_page_config(
    page_title="ResumeCheck AI",
    page_icon="📋",
    layout="centered"
)
 
# ── Mistral Setup (direct API call — no SDK needed) ───────────────────────────
def get_mistral_response(prompt):
    api_key = os.getenv("MISTRAL_API_KEY", "")
    if not api_key:
        st.error("⚠️ MISTRAL_API_KEY not found. Add it to your .env file.")
        st.stop()
 
    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistral-small-latest",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
 
    if response.status_code != 200:
        st.error(f"Mistral API error {response.status_code}: {response.text}")
        st.stop()
 
    return response.json()["choices"][0]["message"]["content"]
 
 
def extract_pdf_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()
 
 
def analyze_resume(resume_text, job_role):
    prompt = f"""
You are an experienced recruiter and technical hiring manager. Review this resume for a {job_role} role.
 
RESUME:
{resume_text}
 
Give a structured analysis using EXACTLY these section headers (markdown ##):
 
## OVERALL SCORE
Score out of 100 with one sentence explanation. Example: "72/100 — Good foundation but missing key technical skills."
 
## STRENGTHS
3–5 bullet points highlighting what's working well in this resume.
 
## MISSING SKILLS
Bullet list of important skills and experiences missing for a {job_role} role.
 
## EXPERIENCE FEEDBACK
2–3 sentences on the quality and relevance of their experience section.
 
## PROJECTS FEEDBACK
2–3 sentences on their projects. If none exist, mention it clearly.
 
## WHAT TO IMPROVE
4–5 specific, actionable steps they should take to improve this resume.
 
## FINAL VERDICT
2–3 sentences summarizing overall readiness for {job_role} positions.
 
Be honest and specific. Avoid vague generic advice.
"""
    return get_mistral_response(prompt)
 
 
def get_score(text):
    m = re.search(r'\b(\d{1,3})\s*/\s*100\b', text)
    return int(m.group(1)) if m else None
 
 
# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("## 📋 ResumeCheck AI")
st.caption("Powered by Mistral AI · Get instant feedback on your resume")
st.divider()
 
st.markdown("**Step 1 — Select your target job role**")
job_role = st.selectbox("Job Role", [
    "Machine Learning Engineer",
    "Data Scientist",
    "Data Analyst",
    "Software Engineer (Backend)",
    "Software Engineer (Frontend)",
    "Full Stack Developer",
    "DevOps / Cloud Engineer",
    "AI / ML Research Intern",
    "Python Developer",
    "Business Analyst",
])
 
st.markdown("<br>", unsafe_allow_html=True)
 
st.markdown("**Step 2 — Upload your resume (PDF only)**")
uploaded = st.file_uploader("Upload Resume PDF", type=["pdf"])
 
st.markdown("<br>", unsafe_allow_html=True)
 
if st.button("🔍 Analyze My Resume", use_container_width=True):
    if not uploaded:
        st.warning("Please upload your resume PDF first.")
    else:
        with st.spinner("Analyzing your resume with Mistral AI..."):
            text = extract_pdf_text(uploaded)
            if not text:
                st.error("Could not extract text. Make sure it's not a scanned image PDF.")
                st.stop()
            result = analyze_resume(text, job_role)
 
        st.divider()
        st.markdown("### 📊 Your Resume Analysis")
 
        # Score metrics
        score = get_score(result)
        if score:
            label = "Strong ✅" if score >= 75 else "Needs Work ⚠️" if score >= 50 else "Weak ❌"
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Resume Score", f"{score} / 100")
            with col2:
                st.metric("Target Role", job_role[:20] + ("..." if len(job_role) > 20 else ""))
            with col3:
                st.metric("Status", label)
 
        st.markdown("<br>", unsafe_allow_html=True)
 
        # Parse sections into tabs
        tab_map = {
            "💪 Strengths":      "## STRENGTHS",
            "⚠️ Missing Skills": "## MISSING SKILLS",
            "💼 Experience":     "## EXPERIENCE FEEDBACK",
            "🚀 Projects":       "## PROJECTS FEEDBACK",
            "🔧 What to Fix":    "## WHAT TO IMPROVE",
            "📝 Verdict":        "## FINAL VERDICT",
        }
 
        content_map = {}
        lines = result.split("\n")
        current = None
        for line in lines:
            matched = False
            for tab_name, header in tab_map.items():
                if line.strip().startswith(header):
                    current = tab_name
                    matched = True
                    break
            if not matched and current:
                content_map[current] = content_map.get(current, "") + line + "\n"
 
        tabs = st.tabs(list(tab_map.keys()))
        for i, tab_name in enumerate(tab_map.keys()):
            with tabs[i]:
                content = content_map.get(tab_name, "").strip()
                st.markdown(content if content else "_No content found._")
 
        st.markdown("<br>", unsafe_allow_html=True)
 
        st.download_button(
            "⬇️ Download Full Analysis",
            data=result,
            file_name="resume_analysis.txt",
            mime="text/plain",
            use_container_width=True
        )
 
st.divider()
st.caption("Built with Python · Streamlit · Mistral AI")