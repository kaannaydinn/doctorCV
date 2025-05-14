# utils/chart_generator.py

import matplotlib.pyplot as plt

def plot_skill_gap(cv_skills, reference_skills):
    """Eksik becerileri gösteren bar chart döndürür"""
    cv_set = set([s.lower() for s in cv_skills])
    ref_set = set([s.lower() for s in reference_skills])
    missing = list(ref_set - cv_set)

    if not missing:
        return None

    # Basit bar chart — her eksik beceri = 1 puan
    skills = sorted(missing)
    values = [1] * len(skills)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(skills, values)
    ax.set_title("Eksik Beceriler")
    ax.set_xlabel("Eksik Beceriler")
    ax.set_yticks(range(len(skills)))
    ax.set_yticklabels(skills)
    ax.set_xticks([])  # Skor göstermek istemiyoruz
    plt.tight_layout()

    return fig
