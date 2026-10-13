def test_user_dashboard_requires_login(client): assert client.get('/dashboard').status_code in (302,401)
def test_analysis_is_private(client): assert client.get('/analysis/999').status_code in (302,401)
