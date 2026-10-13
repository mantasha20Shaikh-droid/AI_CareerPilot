import re
SKILL_GROUPS = {
 'Programming': ['Python','Java','JavaScript','C++','C','SQL'],
 'AI & ML': ['Artificial Intelligence','Machine Learning','Deep Learning','NLP','Computer Vision','TensorFlow','PyTorch','Scikit-learn'],
 'Data': ['Pandas','NumPy','Excel','Power BI','Tableau','Statistics','Data Analytics','Data Analysis'],
 'Web & Frameworks': ['Flask','Django','FastAPI','HTML','CSS','Bootstrap','React'],
 'Tools & Cloud': ['Git','GitHub','Docker','Linux','AWS','Azure','Power BI']
}
ALL_SKILLS = sorted(set(s for group in SKILL_GROUPS.values() for s in group), key=len, reverse=True)
def extract_skills(text):
    source = (text or '').lower()
    found=[]
    for skill in ALL_SKILLS:
        pattern = r'(?<![a-z0-9+#])' + re.escape(skill.lower()) + r'(?![a-z0-9+#])'
        if re.search(pattern, source): found.append(skill)
    return found
def skill_category(skill):
    for category, skills in SKILL_GROUPS.items():
        if skill in skills: return category
    return 'Other'
