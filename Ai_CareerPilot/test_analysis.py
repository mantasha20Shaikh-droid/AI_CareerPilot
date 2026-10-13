from services.resume_analyzer import analyze
def test_skill_matching():
    result=analyze('Python Pandas SQL Git','Need Python, SQL, Excel and Power BI')
    assert result['matched_skills']==['Python','SQL']
    assert result['missing_skills']==['Excel','Power BI']
    assert result['coverage']==50.0
def test_empty_job_description():
    result=analyze('Python','')
    assert result['coverage']==0 and result['required_skills']==[]
