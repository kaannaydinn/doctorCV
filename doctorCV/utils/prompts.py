# utils/prompts.py

ANALYSIS_PROMPT = """
Aşağıdaki CV metnini dikkatlice analiz et.

1. Genel bir değerlendirme yap: (anlaşılır mı, düzenli mi, profesyonel mi?)
2. Eksik olan veya geliştirilebilir yönleri belirt (madde madde yaz).
3. Geliştirme önerileri ver (net, uygulanabilir şekilde).

--- CV METNİ ---
{cv}
"""

IMPROVEMENT_PROMPT = """
Aşağıda bir CV metni ve bu metnin analiz özeti yer alıyor.

Senin görevin:
- Eksik veya zayıf bölümleri geliştir,
- Yeni bölümler ekle (örneğin: Hakkımda, Teknik Yetenekler),
- Geliştirilmiş yeni CV’yi tam metin olarak yaz.

--- ORİJİNAL CV METNİ ---
{cv}

--- ANALİZ ÖZETİ ---
{analysis}
"""
