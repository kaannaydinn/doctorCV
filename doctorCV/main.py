import streamlit as st
import os
import re
import tempfile
import requests
from agents.analyzer import analyze_cv
from agents.improver import improve_cv
from utils.pdf_writer import save_cv_as_pdf
from utils.apify_agent import fetch_linkedin_data
from utils.skill_matcher import extract_skills_from_text, extract_skills_from_job_description
from utils.job_extractor import load_job_data, extract_company_block
from streamlit_lottie import st_lottie
import openai

# Page setup
st.set_page_config(page_title="DoctorCV", page_icon="🩺", layout="centered")

# Apple-style UI in English
st.markdown("""
    <style>
        html, body, .stApp {
            background-color: #F9F9F9;
            font-family: -apple-system, BlinkMacSystemFont, 'San Francisco', 'Helvetica Neue', Helvetica, Arial, sans-serif;
            color: #1c1c1e;
        }
        h1 {
            color: #1c1c1e;
            font-weight: 600;
        }
        .stTextInput>div>div>input,
        .stSelectbox>div>div>div>input {
            background-color: #ffffff;
            color: #1c1c1e;
            border: 1px solid #c7c7cc;
            border-radius: 8px;
        }
        .stButton>button {
            background-color: #007AFF;
            color: white;
            font-weight: 600;
            border-radius: 8px;
            padding: 0.6em 1.5em;
        }
        .stButton>button:hover {
            background-color: #005FCC;
        }
    </style>
""", unsafe_allow_html=True)

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Header
st.markdown("""
    <div style='text-align: center; margin-top: 20px; margin-bottom: 5px;'>
        <h1>🩺 DoctorCV</h1>
        <p style='font-size: 16px; color: #3a3a3c;'>Your AI-powered resume improvement assistant</p>
    </div>
""", unsafe_allow_html=True)

# Form input
with st.form(key="cv_form"):
    st.subheader("📄 Upload Your Resume")
    uploaded_file = st.file_uploader("Select a PDF or DOCX file", type=["pdf", "docx"])
    job_title = st.text_input("Target Job Title", placeholder="e.g. Data Analyst")
    company_name = st.text_input("Company Name (optional)", placeholder="e.g. Apple")

    col1, col2 = st.columns(2)
    with col1:
        location = st.selectbox("Location", options=[
            "Türkiye", "Germany", "United States", "France", "Netherlands",
            "United Kingdom", "Canada", "Italy", "Sweden", "Other"
        ], index=0)
    with col2:
        seniority_level = st.selectbox("Seniority Level", [
            "(Leave blank)", "Associate", "Entry level", "Internship", "Mid-Senior level", "Not Applicable"
        ])
        if seniority_level == "(Leave blank)":
            seniority_level = None

    industry = st.selectbox("Industry", [
        "(Leave blank)",
        "Banking", "Computer Games", "Financial Services",
        "IT Services and IT Consulting", "Manufacturing",
        "Pharmaceutical Manufacturing", "Retail",
        "Software Development", "Technology, Information and Media"
    ])
    if industry == "(Leave blank)":
        industry = None

    submitted = st.form_submit_button("🚀 Start Analysis")

if not submitted:
    st.markdown("#### 👋 Let's get started! Upload your resume to begin.")
    lottie = load_lottie_url("https://lottie.host/406c7ab4-d19e-49f1-82b4-7bffabf87c00/ZI8ZbV6ZlF.json")
    if lottie:
        st_lottie(lottie, height=300)

if submitted and uploaded_file and job_title and location:
    filename = uploaded_file.name
    # Geçici dosya oluştur
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[-1]) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        input_path = temp_file.name
    st.success(f"📄 Resume uploaded: {filename}")

    local_job_data = load_job_data(company_name, job_title, location)
    if local_job_data:
        job_desc = local_job_data.get("job_description", "")
        company_block = extract_company_block(job_desc, company_name)
        if company_block:
            st.markdown("### 🏢 Company-specific Description")
            st.markdown(company_block)
            if st.checkbox("💡 Summarize key requirements with GPT", value=True):
                with st.spinner("Analyzing with GPT..."):
                    response = openai.ChatCompletion.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are an experienced HR professional."},
                            {"role": "user", "content": f"List the key technical and soft skills expected based on the following job ad:\n\n{company_block}"}
                        ],
                        temperature=0.4,
                        max_tokens=500
                    )
                    st.markdown("#### 🧠 GPT Summary:")
                    st.markdown(response["choices"][0]["message"]["content"])

    with st.spinner("🔎 Fetching job data from LinkedIn..."):
        job_data = fetch_linkedin_data(
            job_title=job_title,
            company_name=company_name,
            location=location,
            seniority_level=seniority_level,
            industries=industry,
            job_function=None
        )

    if not job_data.get("job_description"):
        st.warning("⚠️ Could not fetch job description.")
    else:
        st.success("✅ Job description retrieved.")

    with st.spinner("🧠 Analyzing resume..."):
        analysis = analyze_cv(input_path, job_data, job_title, company_name)
    st.subheader("📋 Resume Analysis & Recommendations")
    st.text_area("Analysis", value=analysis, height=200)

    with st.spinner("🛠️ Improving resume..."):
        improved_cv = improve_cv(input_path, analysis, job_data, job_title, company_name)
    st.subheader("✨ Improved Resume")
    st.text_area("Improved Text", value=improved_cv or "⚠️ Could not generate content.", height=300)

    reference_text = job_data.get("job_description", "")
    reference_skills_raw = extract_skills_from_job_description(reference_text)
    reference_skills = [re.split(r"[:%(]", s)[0].strip().lower() for s in reference_skills_raw]

    candidate_skills_raw = extract_skills_from_text(improved_cv)
    candidate_skills = [re.sub(r"\s*\(.*?\)", "", s).strip().lower() for s in candidate_skills_raw]

    st.subheader("📊 Skill Comparison")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ✅ Expected Skills")
        for skill in sorted(set(reference_skills)) or ["_No data_"]:
            st.markdown(f"- {skill}")
    with col2:
        st.markdown("#### 🙋 Your Skills")
        for skill in sorted(set(candidate_skills)) or ["_None extracted_"]:
            st.markdown(f"- {skill}")

    if improved_cv and len(improved_cv.strip()) > 10:
        output_filename = f"improved_{filename.replace('.docx', '.pdf').replace('.pdf', '.pdf')}"
        output_path = os.path.join("output", output_filename)
        save_cv_as_pdf(improved_cv, output_path)
        with open(output_path, "rb") as f:
            st.download_button("📥 Download Improved Resume", data=f, file_name=output_filename, mime="application/pdf")
    else:
        st.error("⚠️ PDF could not be created.")

# Footer
st.markdown("""
    <hr style="margin-top: 40px;">
    <div style='text-align: center;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/5/5d/Bosphorus_University.jpg' width='250' style='border-radius: 6px; margin-bottom: 8px;'/>
        <p style='color: #666; font-size: 13px;'>Made with ❤️ in Istanbul by Boğaziçi MIS Students</p>
    </div>
""", unsafe_allow_html=True)
