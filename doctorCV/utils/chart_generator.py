# utils/chart_generator.py

import matplotlib.pyplot as plt

def plot_gap_analysis(candidate_skills, reference_skills):
    """
    Adayın becerileri ile pozisyondan beklenen becerileri karşılaştıran
    ikili sütun grafik (tick chart) döndürür.
    """
    def normalize(skill):
        return skill.split("(")[0].strip().lower()

    cv_set = set([normalize(s) for s in candidate_skills])
    ref_set = set([normalize(s) for s in reference_skills])
    all_skills = sorted(ref_set.union(cv_set))

    candidate_flags = [1 if skill in cv_set else 0 for skill in all_skills]
    reference_flags = [1 if skill in ref_set else 0 for skill in all_skills]

    fig, ax = plt.subplots(figsize=(8, len(all_skills) * 0.4))
    bar_width = 0.35
    indices = range(len(all_skills))

    ax.barh([i + bar_width for i in indices], reference_flags, bar_width, label='Pozisyon Beklentisi', color='#4682B4')
    ax.barh(indices, candidate_flags, bar_width, label='Adayın Becerisi', color='#90EE90')

    ax.set_yticks([i + bar_width / 2 for i in indices])
    ax.set_yticklabels(all_skills)
    ax.invert_yaxis()  # En üstte en önemli
    ax.set_xlabel("Durum")
    ax.set_title("📊 Gap Analysis – Beceri Karşılaştırması")
    ax.legend()
    plt.tight_layout()

    return fig
