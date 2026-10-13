from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from extensions import db, oauth
from models import User, ActivityLog
from urllib.parse import urlparse
import os

auth_bp=Blueprint('auth',__name__)
def log(event): db.session.add(ActivityLog(user_id=current_user.id if current_user.is_authenticated else None,event=event)); db.session.commit()
@auth_bp.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated: return redirect(url_for('user.dashboard'))
    if request.method=='POST':
        name=request.form.get('full_name','').strip(); username=request.form.get('username','').strip(); email=request.form.get('email','').strip().lower(); password=request.form.get('password',''); confirm=request.form.get('confirm_password','')
        errors=[]
        if len(name)<2: errors.append('Enter your full name.')
        if len(username)<3 or not username.replace('_','').isalnum(): errors.append('Username must be at least 3 letters/numbers (underscores allowed).')
        if '@' not in email or '.' not in email.split('@')[-1]: errors.append('Enter a valid email address.')
        if len(password)<8: errors.append('Password must be at least 8 characters.')
        if password!=confirm: errors.append('Passwords do not match.')
        if User.query.filter_by(username=username).first(): errors.append('Username is already taken.')
        if User.query.filter_by(email=email).first(): errors.append('Email is already registered.')
        if errors:
            for e in errors: flash(e,'danger')
        else:
            u=User(full_name=name,username=username,email=email,role='user'); u.set_password(password); db.session.add(u); db.session.commit(); login_user(u); db.session.add(ActivityLog(user_id=u.id,event='Registered account')); db.session.commit(); flash('Account created successfully.','success'); return redirect(url_for('user.dashboard'))
    return render_template('auth/register.html')
@auth_bp.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('admin.dashboard' if current_user.role=='admin' else 'user.dashboard'))
    if request.method=='POST':
        identity=request.form.get('identity','').strip(); password=request.form.get('password','')
        u=User.query.filter(db.or_(User.username==identity,User.email==identity.lower())).first()
        if u and u.active and u.check_password(password):
            login_user(u, remember=bool(request.form.get('remember'))); db.session.add(ActivityLog(user_id=u.id,event='Logged in')); db.session.commit(); return redirect(url_for('admin.dashboard' if u.role=='admin' else 'user.dashboard'))
        flash('Invalid credentials or inactive account.','danger')
    return render_template('auth/login.html')
@auth_bp.route('/logout',methods=['GET','POST'])
def logout():
    if current_user.is_authenticated: log('Logged out')
    logout_user(); flash('You have been logged out.','info'); return redirect(url_for('main.landing'))

def setup_oauth():
    if os.getenv('GOOGLE_CLIENT_ID') and os.getenv('GOOGLE_CLIENT_SECRET'):
        oauth.register(name='google',client_id=os.getenv('GOOGLE_CLIENT_ID'),client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',client_kwargs={'scope':'openid email profile'})
    if os.getenv('GITHUB_CLIENT_ID') and os.getenv('GITHUB_CLIENT_SECRET'):
        oauth.register(name='github',client_id=os.getenv('GITHUB_CLIENT_ID'),client_secret=os.getenv('GITHUB_CLIENT_SECRET'),authorize_url='https://github.com/login/oauth/authorize',access_token_url='https://github.com/login/oauth/access_token',api_base_url='https://api.github.com/',client_kwargs={'scope':'user:email'})
@auth_bp.route('/auth/<provider>')
def oauth_login(provider):
    if provider not in ('google','github'): return 'Unsupported provider',404
    client=oauth.create_client(provider)
    if not client: flash(f'{provider.title()} sign-in is not configured. Add its credentials to .env.','warning'); return redirect(url_for('auth.login'))
    callback=url_for('auth.oauth_callback',provider=provider,_external=True)
    return client.authorize_redirect(callback)
@auth_bp.route('/auth/<provider>/callback')
def oauth_callback(provider):
    client=oauth.create_client(provider)
    if not client: flash('OAuth provider is not configured.','warning'); return redirect(url_for('auth.login'))
    try:
        token=client.authorize_access_token()
        if provider=='google': info=token.get('userinfo') or client.parse_id_token(token); pid=str(info.get('sub')); email=(info.get('email') or '').lower(); name=info.get('name') or email.split('@')[0]; username=''.join(c for c in email.split('@')[0] if c.isalnum() or c=='_')[:30] or provider+pid[-6:]
        else:
            resp=client.get('user',token=token); info=resp.json(); pid=str(info.get('id')); email=info.get('email')
            if not email:
                er=client.get('user/emails',token=token); email=next((x['email'] for x in er.json() if x.get('primary') and x.get('verified')),None)
            if not email: flash('GitHub did not provide a verified email. Set it public or use email/password login.','warning'); return redirect(url_for('auth.login'))
            email=email.lower(); name=info.get('name') or info.get('login') or email.split('@')[0]; username=''.join(c for c in info.get('login','githubuser') if c.isalnum() or c=='_')[:30]
        u=User.query.filter_by(email=email).first()
        field='google_id' if provider=='google' else 'github_id'
        linked=User.query.filter_by(**{field:pid}).first()
        if linked: u=linked
        elif u and getattr(u,field) not in (None,pid): flash('This email is already associated with another sign-in. Please use your existing login.','warning'); return redirect(url_for('auth.login'))
        elif u: setattr(u,field,pid)
        else:
            base=username or provider+'user'; candidate=base; i=1
            while User.query.filter_by(username=candidate).first(): candidate=f'{base[:34]}{i}'; i+=1
            u=User(full_name=name,username=candidate,email=email,role='user'); setattr(u,field,pid); db.session.add(u)
        db.session.commit(); login_user(u); return redirect(url_for('user.dashboard'))
    except Exception:
        current_app.logger.exception('OAuth callback failed'); flash('Sign-in failed. Check provider configuration and callback URL.','danger'); return redirect(url_for('auth.login'))
