from models import User
def test_registration_and_password_hash(client,app):
    r=client.post('/register',data={'full_name':'Test User','username':'testuser','email':'test@example.com','password':'strong-password','confirm_password':'strong-password'},follow_redirects=True)
    assert r.status_code==200
    with app.app_context():
        u=User.query.filter_by(username='testuser').first(); assert u and u.password_hash!='strong-password' and u.check_password('strong-password')
def test_login_logout(client):
    client.post('/register',data={'full_name':'Test User','username':'testuser','email':'test@example.com','password':'strong-password','confirm_password':'strong-password'})
    client.get('/logout'); r=client.post('/login',data={'identity':'testuser','password':'strong-password'},follow_redirects=True); assert r.status_code==200
    assert client.get('/logout',follow_redirects=True).status_code==200
def test_admin_seed(app):
    with app.app_context(): assert User.query.filter_by(username='Mantasha',role='admin').first()
