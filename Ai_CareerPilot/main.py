from flask import Blueprint, render_template
main_bp=Blueprint('main',__name__)
@main_bp.route('/')
def landing(): return render_template('landing.html')
@main_bp.route('/privacy')
def privacy(): return render_template('privacy.html')
@main_bp.route('/terms')
def terms(): return render_template('terms.html')
