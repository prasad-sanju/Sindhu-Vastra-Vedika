from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.business.services import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            user = AuthService.register(request.form['name'].strip(), request.form['email'].strip(), request.form['password'])
            session['user_id'] = user.id
            session['user_name'] = user.name
            return redirect(url_for('main.home'))
        except ValueError as exc:
            flash(str(exc))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = AuthService.authenticate(request.form['email'].strip(), request.form['password'])
        if user:
            session['user_id'] = user.id
            session['user_name'] = user.name
            return redirect(url_for('main.home'))
        flash('Invalid email or password')
    return render_template('login.html')

@auth_bp.get('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))
