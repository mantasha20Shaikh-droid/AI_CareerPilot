from extensions import db
class RoadmapTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    stage = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(180), nullable=False)
    description = db.Column(db.Text, default='')
    duration = db.Column(db.String(50), default='1-2 weeks')
    completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
class InterviewQuestionSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    role = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(40), nullable=False)
    questions = db.Column(db.JSON, default=list)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
class LearningResourceBookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    resource_key = db.Column(db.String(100), nullable=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'resource_key', name='uq_bookmark_user_resource'),)
