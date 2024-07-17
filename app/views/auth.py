from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    print('loggin')
    return {}
    # Login logic here
    pass

@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Registration logic here
    pass

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
