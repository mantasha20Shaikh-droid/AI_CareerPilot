from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from functools import wraps
from extensions import db
from models import User, ResumeAnalysis, ActivityLog, AdminAuditLog
admin_bp=Blueprint('admin',__name__,url_prefix='/admin')
def admin_required(fn):
    @wraps(fn)
    @login_required
    def wrapped(*args,**kwargs):
        if current_user.role!='admin': abort(403)
        return fn(*args,**kwargs)
    return wrapped
def audit(event): db.session.add(AdminAuditLog(admin_id=current_user.id,event=event)); db.session.commit()
@admin_bp.route('/')
@admin_required
def dashboard():
    return render_template('admin/dashboard.html',users=User.query.order_by(User.created_at.desc()).limit(8).all(),analyses=ResumeAnalysis.query.order_by(ResumeAnalysis.created_at.desc()).limit(8).all(),user_count=User.query.count(),analysis_count=ResumeAnalysis.query.count(),activity=ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(10).all())
@admin_bp.route('/users')
@admin_required
def users():
    q=request.args.get('q','').strip(); query=User.query
    if q: query=query.filter(db.or_(User.username.ilike(f'%{q}%'),User.email.ilike(f'%{q}%'),User.full_name.ilike(f'%{q}%')))
    return render_template('admin/users.html',users=query.order_by(User.created_at.desc()).all(),q=q)
@admin_bp.route('/users/<int:user_id>')
@admin_required
def user_detail(user_id):
    u=User.query.get_or_404(user_id); return render_template('admin/user_detail.html',u=u)
@admin_bp.route('/users/<int:user_id>/toggle',methods=['POST'])
@admin_required
def toggle_user(user_id):
    u=User.query.get_or_404(user_id)
    if u.id==current_user.id: flash('You cannot deactivate your own account.','danger')
    elif u.role=='admin' and u.active and User.query.filter_by(role='admin',active=True).count()<=1: flash('Cannot deactivate the final active administrator.','danger')
    else: u.active=not u.active; db.session.commit(); audit(f'Changed active status for user #{u.id}'); flash('User status updated.','success')
    return redirect(url_for('admin.users'))
@admin_bp.route('/analyses')
@admin_required
def analyses(): return render_template('admin/analyses.html',analyses=ResumeAnalysis.query.order_by(ResumeAnalysis.created_at.desc()).all())
@admin_bp.route('/analytics')
@admin_required
def analytics():
    from sqlalchemy import func
    roles=db.session.query(ResumeAnalysis.job_title,func.count(ResumeAnalysis.id)).group_by(ResumeAnalysis.job_title).all()
    return render_template('admin/analytics.html',roles=roles,user_count=User.query.count(),analysis_count=ResumeAnalysis.query.count())
@admin_bp.route('/settings')
@admin_required
def settings():
    import os
    return render_template('admin/settings.html',ai_configured=bool(os.getenv('AI_API_KEY') and os.getenv('AI_BASE_URL') and os.getenv('AI_MODEL')),google=bool(os.getenv('GOOGLE_CLIENT_ID') and os.getenv('GOOGLE_CLIENT_SECRET')),github=bool(os.getenv('GITHUB_CLIENT_ID') and os.getenv('GITHUB_CLIENT_SECRET')))
@admin_bp.route('/audit-logs')
@admin_required
def audit_logs(): return render_template('admin/audit_logs.html',logs=AdminAuditLog.query.order_by(AdminAuditLog.created_at.desc()).limit(100).all())
