def test_admin_page_requires_admin(client): assert client.get('/admin/').status_code in (302,401)
def test_admin_can_login(client):
    r=client.post('/login',data={'identity':'Mantasha','password':'Mantasha'},follow_redirects=True)
    assert r.status_code==200
