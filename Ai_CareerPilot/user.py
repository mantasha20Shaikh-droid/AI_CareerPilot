from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False, default='CareerPilot User')
    username = db.Column(db.String(40), unique=True, nullable=False, index=True)
    email = db.Column(db.String(160), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='user', nullable=False, index=True)
    active = db.Column(db.Boolean, default=True, nullable=False)
    target_role = db.Column(db.String(120), default='Data Analyst')
    experience_level = db.Column(db.String(40), default='Entry level')
    learning_goals = db.Column(db.Text, default='')
    google_id = db.Column(db.String(200), unique=True)
    github_id = db.Column(db.String(200), unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return bool(self.password_hash) and check_password_hash(self.password_hash, password)
    @property
    def is_active(self): return self.active
