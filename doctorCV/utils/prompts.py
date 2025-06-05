# utils/prompts.py

ANALYSIS_PROMPT = """
Analyze the CV text below.

1. Provide a general evaluation (language, structure, length)
2. Identify areas that are missing or need improvement (as bullet points)
3. Offer improvement suggestions (clear and actionable)

--- CV TEXT ---
{cv}
"""

IMPROVEMENT_PROMPT = """
Below is a CV text and its corresponding analysis summary.

Your task:
- Improve the incomplete and insufficient parts
- Add new sections (About Me, Technical Skills, etc.)
- Produce a fully rewritten and improved version of the CV

--- CV TEXT ---
{cv}

--- ANALYSIS SUMMARY ---
{analysis}
"""

CONTEXTUAL_ANALYSIS_PROMPT = """
The user's current CV text is provided below.  
The target position and company the user is applying to are also specified.

Additionally, real technical skills gathered from LinkedIn profiles are provided.

Your task:
1. Evaluate this CV technically (content, skills, relevance)
2. Identify missing skills
3. Improve the CV to better match the target position (add new sections if necessary)
4. Write the full improved CV text (plain text only, no markdown or styling)

--- CV TEXT ---
{cv}

--- TARGET POSITION & COMPANY ---
{position} @ {company}

--- REAL LINKEDIN DATA (TECHNICAL SKILLS) ---
{job_data}
"""
