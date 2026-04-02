from flask import Blueprint,request,render_template,make_response,redirect,url_for,flash
from app.extensions import db
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.user import User

bp=Blueprint("auth",__name__)

@bp.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')

    if not email or not password:
        flash('Email and password are required.', 'error')
        return redirect(url_for('auth.login'))

    user = db.session.execute(
        db.select(User).filter_by(email=email)
    ).scalar_one_or_none()

    if not user or not check_password_hash(user.password_hash, password):
        flash('Email and password are required.', 'error')
        return redirect(url_for('auth.login'))

    access_token = create_access_token(identity=str(user.id))

    response=redirect(url_for('main.index'))

    flash('Log In successful!', 'success')
    response.set_cookie('access_token_cookie',access_token,httponly=True)

    return response

@bp.route('/register',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')

    if not email or not password:
        flash('Email and password are required.', 'error')
        return redirect(url_for('auth.register'))
    
    existing_user = db.session.execute(
        db.select(User).filter_by(email=email)
    ).scalar_one_or_none()

    if existing_user:
        flash('Email already registered. Try another', 'error')
        return redirect(url_for('auth.register'))
    
    new_user = User(email=email, password_hash=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=str(new_user.id))

    response=redirect(url_for('main.index'))
    flash('Registration successful!', 'success')
    response.set_cookie('access_token_cookie',access_token,httponly=True)

    return response