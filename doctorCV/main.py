# main.py

import streamlit as st
import os
from agents.analyzer import analyze_cv
from agents.improver import improve_cv
from utils.pdf_writer import save_cv_as_pdf

os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)


# Bu satır ilk Streamlit komutu olmalı
st.set_page_config(page_title="DoctorCV", page_icon="🩺")

st.title("🩺 DoctorCV — CV Analizi ve Geliştirme")
st.markdown("Lütfen CV dosyanızı yükleyin ve ardından analizi başlatın.")

# Dosya yükleme
uploaded_file = st.file_uploader("📄 CV dosyanızı yükleyin (.pdf veya .docx)", type=["pdf", "docx"])

if uploaded_file:
    filename = uploaded_file.name
    input_path = os.path.join("input", filename)

    # Dosyayı kaydet
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ Dosya yüklendi: {filename}")

    # Analiz ve geliştirme işlemleri
    if st.button("🔍 CV'yi Analiz Et ve Geliştir"):
        with st.spinner("🔍 Analiz yapılıyor..."):
            analysis = analyze_cv(input_path)
        st.subheader("📋 CV Analizi")
        st.text_area("Analiz", value=analysis, height=200)

        with st.spinner("🛠️ Geliştirme yapılıyor..."):
            improved_cv = improve_cv(input_path, analysis)

        # DEBUG: terminal çıktısı
        print("📦 Geliştirilmiş CV metni:\n", improved_cv)

        st.subheader("✨ Geliştirilmiş CV")
        st.text_area("Yeni CV Metni", value=improved_cv or "⚠️ Hiçbir içerik üretilmedi", height=300)

        # PDF olarak kaydet (boşsa kaydetme)
        if improved_cv and len(improved_cv.strip()) > 10:
            output_filename = f"improved_{filename.replace('.docx', '.pdf').replace('.pdf', '.pdf')}"
            output_path = os.path.join("output", output_filename)
            save_cv_as_pdf(improved_cv, output_path)

            with open(output_path, "rb") as f:
                st.download_button(
                    label="📥 Geliştirilmiş CV'yi PDF Olarak İndir",
                    data=f,
                    file_name=output_filename,
                    mime="application/pdf"
                )
        else:
            st.error("⚠️ Geliştirilmiş CV metni boş olduğu için PDF oluşturulamadı.")
