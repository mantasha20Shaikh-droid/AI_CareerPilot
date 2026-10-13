from .skill_extractor import extract_skills
def analyze(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    required = extract_skills(job_description)
    matched = [s for s in required if s.lower() in {x.lower() for x in resume_skills}]
    missing = [s for s in required if s not in matched]
    coverage = round(len(matched) / len(required) * 100, 1) if required else 0.0
    strengths = ([f'Your resume mentions {", ".join(matched[:5])}.'] if matched else ['Your resume text was parsed, but no matching skills were detected from the job description.'])
    improvements = [f'Add evidence of {s} through a project, coursework, or work experience.' for s in missing[:6]]
    if not required: improvements.insert(0, 'The job description did not contain skills from the current dictionary. Add clearer technical requirements for a more useful comparison.')
    projects = [f'Build a portfolio project demonstrating {s}.' for s in missing[:3]]
    return {'resume_skills': resume_skills, 'required_skills': required, 'matched_skills': matched, 'missing_skills': missing, 'coverage': coverage, 'strengths': strengths, 'improvements': improvements, 'projects': projects}
