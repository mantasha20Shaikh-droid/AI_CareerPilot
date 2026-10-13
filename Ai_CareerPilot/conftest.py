import pytest
from app import create_app
from extensions import db
@pytest.fixture()
def app(tmp_path):
    path=tmp_path/'test.db'
    app=create_app({'TESTING':True,'WTF_CSRF_ENABLED':False,'SQLALCHEMY_DATABASE_URI':'sqlite:///'+str(path),'UPLOAD_FOLDER':str(tmp_path/'uploads'),'SECRET_KEY':'test-secret'})
    with app.app_context(): db.drop_all(); db.create_all(); yield app; db.session.remove(); db.drop_all()
@pytest.fixture()
def client(app): return app.test_client()
