import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import spacy

from parser import parse_resume
from matcher import compute_similarity
from utils import read_pdf, read_docx

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Extract JD skills
def extract_jd_skills(text):
    keywords = []
    doc = nlp(text.lower())
    
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"]:
            keywords.append(token.text)
    
    return list(set(keywords))

# Highlight skills
def highlight_skills(text, skills):
    for skill in skills:
        text = text.replace(skill, f"**{skill}**")
    return text


# Page config
st.set_page_config(page_title="AI Resume Screener", layout="wide")

st.title("🤖 AI Resume Screening System (Advanced)")

# Sidebar
st.sidebar.markdown("## 🧠 ATS Input Panel")

# JD input
jd_text = st.sidebar.text_area(
    "✍️ Enter Job Description",
    height=200,
    placeholder="Paste or type the job description here..."
)

# Resume upload
resume_files = st.sidebar.file_uploader(
    "📂 Upload Resumes", type=["pdf", "docx"], accept_multiple_files=True
)

run = st.sidebar.button("🚀 Analyze Resumes")

# MAIN LOGIC
if run and jd_text and resume_files:

    jd_skills = extract_jd_skills(jd_text)

    results = []
    all_skills = []

    for file in resume_files:
        file_path = os.path.join("temp", file.name)

        # Save uploaded file
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        # Read resume
        if file.name.endswith(".pdf"):
            text = read_pdf(file_path)
        else:
            text = read_docx(file_path)

        parsed = parse_resume(text)
        score = compute_similarity(text, jd_text)

        missing_skills = list(set(jd_skills) - set(parsed["skills"]))
        all_skills.extend(parsed["skills"])

        results.append({
            "Name": parsed["name"],
            "Email": parsed["email"],
            "Skills": ", ".join(parsed["skills"]),
            "Score": round(score, 2),
            "Missing Skills": ", ".join(missing_skills)
        })

    df = pd.DataFrame(results).sort_values(by="Score", ascending=False)

    # 🏆 Results
    st.header("🏆 Top Candidates")

    for _, row in df.iterrows():
        st.subheader(row["Name"])
        st.write(f"📧 {row['Email']}")

        highlighted = highlight_skills(row["Skills"], jd_skills)
        st.write(f"🛠 Skills: {highlighted}")

        st.write(f"❌ Missing: {row['Missing Skills']}")

        percent = int(row["Score"] * 100)

        st.progress(percent / 100)
        st.write(f"🎯 Match Score: {percent}%")

        # Color feedback
        if percent > 80:
            st.success("🔥 Excellent Match")
        elif percent > 60:
            st.warning("👍 Good Match")
        else:
            st.error("⚠️ Low Match")

        st.markdown("---")

    # 📊 Dashboard (Pie Chart)
    st.header("📊 Analytics Dashboard")

    skill_counts = pd.Series(all_skills).value_counts().head(10)

    if not skill_counts.empty:
        fig, ax = plt.subplots()

        ax.pie(
            skill_counts.values,
            labels=skill_counts.index,
            autopct='%1.1f%%',
            startangle=90
        )

        ax.axis('equal')

        st.pyplot(fig)
    else:
        st.warning("No skills data available for chart")

    # 📥 Download CSV
    st.header("📥 Download Results")

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Shortlisted Candidates",
        data=csv,
        file_name="shortlisted_candidates.csv",
        mime="text/csv"
    )

else:
    st.info("👈 Enter Job Description and upload resumes from sidebar")