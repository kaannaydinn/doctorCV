# main.py

import streamlit as st
import os
from agents.analyzer import analyze_cv
from agents.improver import improve_cv
from utils.pdf_writer import save_cv_as_pdf
from utils.apify_agent import fetch_linkedin_data
from utils.skill_matcher import (
    extract_skills_from_text,
    extract_skills_from_job_description,
    compare_skills,
)
from utils.chart_generator import plot_skill_gap

# Klasörleri oluştur
os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)
os.makedirs("data", exist_ok=True)

# Başlık
st.set_page_config(page_title="DoctorCV", page_icon="🩺")
st.title("🩺 DoctorCV — CV Analizi ve Geliştirme")
st.markdown("CV’nizi yükleyin, başvurmak istediğiniz pozisyon + şirket + ülke bilgilerini girin.")

# Kullanıcıdan bilgi al
job_title = st.text_input("Pozisyon", placeholder="Örn: Data Analyst")
company_name = st.text_input("Şirket", placeholder="Örn: Trendyol")
location = st.selectbox("Ülke", options=[
    "Türkiye", "Almanya", "Amerika Birleşik Devletleri", "Fransa", "Hollanda", "İngiltere", "Kanada", "İtalya", "İsveç", "Diğer"
], index=0)
uploaded_file = st.file_uploader("📄 CV Yükle (.pdf veya .docx)", type=["pdf", "docx"])

# Girişler tam ise devam
if uploaded_file and job_title and company_name:
    filename = uploaded_file.name
    input_path = os.path.join("input", filename)

    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ CV yüklendi: {filename}")

    if st.button("🔍 CV'yi Analiz Et ve Geliştir"):
        # Apify verisi
        with st.spinner(f"🔗 LinkedIn verisi alınıyor ({job_title} @ {location})..."):
            job_data = fetch_linkedin_data(job_title, company_name, location)
            if not job_data.get("job_description"):
                st.warning("⚠️ Apify üzerinden açıklama alınamadı.")
            else:
                st.success("✅ Apify iş ilanı açıklaması başarıyla alındı.")

        # CV analizi
        with st.spinner("📊 CV analiz ediliyor..."):
            analysis = analyze_cv(input_path, job_data, job_title, company_name)
        st.subheader("📋 CV Analizi ve Öneriler")
        st.markdown("Bu bilgiler yalnızca inceleme içindir, geliştirilmiş CV'ye eklenmez.")
        st.text_area("Analiz", value=analysis, height=200)

        # CV geliştirme
        with st.spinner("🛠️ CV geliştiriliyor..."):
            improved_cv = improve_cv(input_path, analysis, job_data, job_title, company_name)
        st.subheader("✨ Geliştirilmiş CV")
        st.markdown("Bu metin yalnızca mevcut bilgilerle yeniden yazılmıştır.")
        st.text_area("Yeni CV Metni", value=improved_cv or "⚠️ İçerik üretilemedi.", height=300)

        # Skill karşılaştırması
        reference_text = job_data.get("job_description", "")
        reference_skills = extract_skills_from_job_description(reference_text)
        candidate_skills = extract_skills_from_text(improved_cv)
        missing_skills = compare_skills(candidate_skills, reference_skills)

        if missing_skills:
            st.subheader("🧠 Eksik Beceriler (LinkedIn verisine göre)")
            st.write(missing_skills)
            fig = plot_skill_gap(candidate_skills, reference_skills)
            if fig:
                st.pyplot(fig)
        else:
            st.info("🔍 Eksik beceri bulunamadı (Apify + OpenAI eşleşmesi)")

        # PDF çıktısı
        if improved_cv and len(improved_cv.strip()) > 10:
            output_filename = f"improved_{filename.replace('.docx', '.pdf').replace('.pdf', '.pdf')}"
            output_path = os.path.join("output", output_filename)
            save_cv_as_pdf(improved_cv, output_path)

            with open(output_path, "rb") as f:
                st.download_button(
                    label="📥 Geliştirilmiş CV'yi PDF olarak indir",
                    data=f,
                    file_name=output_filename,
                    mime="application/pdf"
                )
        else:
            st.error("⚠️ Geliştirilmiş CV metni boş olduğu için PDF oluşturulamadı.")
else:
    st.info("Lütfen CV, pozisyon ve şirket bilgilerini eksiksiz giriniz.")
