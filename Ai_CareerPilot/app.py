from pathlib import Path
import os
from flask import Flask, render_template
from config import Config
from extensions import db, login_manager, csrf, oauth
from models import User

def create_app(test_config=None):
    app=Flask(__name__,instance_relative_config=True)
    app.config.from_object(Config)
    if test_config: app.config.update(test_config)
    Path(app.instance_path).mkdir(parents=True,exist_ok=True); Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True,exist_ok=True)
    db.init_app(app); login_manager.init_app(app); csrf.init_app(app); oauth.init_app(app)
    from routes.main import main_bp
    from routes.auth import auth_bp, setup_oauth
    from routes.user import user_bp
    from routes.analysis import analysis_bp
    from routes.career import career_bp
    from routes.admin import admin_bp
    setup_oauth()
    for bp in (main_bp,auth_bp,user_bp,analysis_bp,career_bp,admin_bp): app.register_blueprint(bp)
    @login_manager.user_loader
    def load_user(user_id): return db.session.get(User,int(user_id))
    @app.errorhandler(403)
    def forbidden(e): return render_template('errors/403.html'),403
    @app.errorhandler(404)
    def not_found(e): return render_template('errors/404.html'),404
    @app.errorhandler(413)
    def too_large(e): return 'Upload too large. Maximum size is 5 MB.',413
    @app.context_processor
    def inject_globals(): return {'app_name':'AI CareerPilot'}
    with app.app_context():
        db.create_all()
        username=os.getenv('ADMIN_USERNAME','Mantasha'); password=os.getenv('ADMIN_PASSWORD','Mantasha')
        admin=User.query.filter_by(username=username).first()
        if not admin:
            email='admin@careerpilot.local'
            if User.query.filter_by(email=email).first(): email=f'{username.lower()}@careerpilot.local'
            admin=User(full_name=username,username=username,email=email,role='admin',target_role='Administrator'); admin.set_password(password); db.session.add(admin); db.session.commit()
    return app
app=create_app()
if __name__=='__main__':
    print('AI CareerPilot starting at http://127.0.0.1:5000')
    app.run(host='127.0.0.1',port=5000,debug=os.getenv('FLASK_ENV','development')=='development')
