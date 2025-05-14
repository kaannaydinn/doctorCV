# utils/prompts.py

ANALYSIS_PROMPT = """
Aşağıdaki CV metnini analiz et.

1. Genel bir değerlendirme yap: (dil, yapı, uzunluk)
2. Eksik veya geliştirilmeye açık yönleri belirt (madde madde)
3. Geliştirme önerileri ver (net ve uygulanabilir)

--- CV METNİ ---
{cv}
"""

IMPROVEMENT_PROMPT = """
Aşağıda bir CV metni ve bu metne ait analiz özeti yer alıyor.

Senin görevin:
- Eksik ve yetersiz alanları geliştir
- Yeni bölümler ekle (Hakkımda, Teknik Beceriler vb.)
- Geliştirilmiş CV metnini üret (tümüyle yeniden yaz)

--- CV METNİ ---
{cv}

--- ANALİZ ÖZETİ ---
{analysis}
"""

CONTEXTUAL_ANALYSIS_PROMPT = """
Kullanıcının mevcut CV metni aşağıda verilmiştir.  
Ayrıca kullanıcının başvurmak istediği pozisyon ve şirket belirtilmiştir.

Ek olarak, gerçek LinkedIn profillerinden toplanan teknik beceriler de verilmiştir.

Senin görevin:
1. Bu CV’yi teknik açıdan değerlendir (içerik, beceriler, uyum)
2. Eksik becerileri tespit et
3. CV’yi hedef pozisyona uygun şekilde geliştir (gerekiyorsa yeni bölümler ekle)
4. Geliştirilmiş tam CV metnini yaz (sadece metin, markdown veya stil olmadan)

--- CV METNİ ---
{cv}

--- HEDEF POZİSYON & ŞİRKET ---
{position} @ {company}

--- GERÇEK LINKEDIN VERİSİ (TEKNİK BECERİLER) ---
{job_data}
"""
