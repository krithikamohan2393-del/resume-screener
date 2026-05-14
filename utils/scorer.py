import re
from utils.skill_extractor import ROLE_SKILLS

def calculate_score(resume_text, extracted_skills, job_role):
    breakdown = {}
    breakdown["Skills Match"] = _score_skills(extracted_skills, job_role)
    breakdown["Experience"] = _score_experience(resume_text)
    breakdown["Education"] = _score_education(resume_text)
    breakdown["Resume Quality"] = _score_quality(resume_text)
    weights = {"Skills Match": 0.40, "Experience": 0.25, "Education": 0.15, "Resume Quality": 0.20}
    overall = sum(breakdown[k] * weights[k] for k in weights)
    return round(overall), breakdown

def _score_skills(extracted_skills, job_role):
    required = ROLE_SKILLS.get(job_role, [])
    if not required:
        return min(100, len(extracted_skills) * 8)
    extracted_lower = [s.lower() for s in extracted_skills]
    matched = sum(1 for skill in required if skill.lower() in extracted_lower)
    extra_bonus = min(20, (len(extracted_skills) - matched) * 2)
    return min(100, round((matched / len(required)) * 80 + extra_bonus))

def _score_experience(text):
    text_lower = text.lower()
    score = 40
    match = re.search(r"(\d+)\s*\+?\s*years?\s+of\s+experience", text_lower)
    if match:
        years = int(match.group(1))
        score = 95 if years >= 5 else 85 if years >= 3 else 70 if years >= 1 else 60
    else:
        if any(kw in text_lower for kw in ["intern", "internship", "trainee"]):
            score += 20
        project_count = sum(text_lower.count(kw) for kw in ["project", "built", "developed", "implemented"])
        score += 20 if project_count >= 5 else 12 if project_count >= 3 else 6 if project_count >= 1 else 0
    return min(100, score)

def _score_education(text):
    text_lower = text.lower()
    score = 40
    if any(kw in text_lower for kw in ["ph.d", "phd", "doctorate"]):
        score = 100
    elif any(kw in text_lower for kw in ["master", "m.tech", "m.sc", "mba"]):
        score = 90
    elif any(kw in text_lower for kw in ["bachelor", "b.tech", "b.sc", "b.e", "b.com"]):
        score = 75
    elif any(kw in text_lower for kw in ["diploma", "12th", "hsc"]):
        score = 55
    if any(kw in text_lower for kw in ["iit", "nit", "iim", "bits", "vit"]):
        score = min(100, score + 10)
    gpa_match = re.search(r"(?:cgpa|gpa)[\s:]*(\d+\.?\d*)", text_lower)
    if gpa_match:
        gpa = float(gpa_match.group(1))
        score = min(100, score + (8 if gpa >= 9.0 else 4 if gpa >= 8.0 else 0))
    return min(100, score)

def _score_quality(text):
    text_lower = text.lower()
    score = 0
    word_count = len(text.split())
    score += 25 if word_count >= 500 else 15 if word_count >= 300 else 8 if word_count >= 150 else 0
    if re.search(r"[\w.-]+@[\w.-]+\.\w+", text): score += 15
    if re.search(r"\+?\d[\d\s\-()]{8,}", text): score += 10
    if any(kw in text_lower for kw in ["github", "linkedin", "portfolio"]): score += 15
    sections = ["skills", "experience", "education", "projects", "achievements", "summary"]
    for s in sections:
        if s in text_lower: score += 5
    return min(100, score)