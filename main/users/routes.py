from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from main import db
from main.models import User, Post
from main.users.forms import (RegistrationForm, LoginForm, UpdateAccount,
                                   RequestResetForm, ResetPasswordForm)
from main.users.utils import save_picture, send_reset_email,Hash
import os

users = Blueprint('users',__name__)

@users.route('/registration',methods=['GET','POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash = Hash()
        password = hash.pass_encrypt(form.password.data)
        user = User(username=form.username.data,email=form.email.data,password=password)
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
            user.image_file = picture_file
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created.You are now able to login!', 'success')
        return redirect(url_for('users.login'))
    return render_template('registration.html',title='registration',form=form)

@users.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('others.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        hash = Hash()
        password = hash.pass_decrypt(user.password)
        if user and (form.password.data == password):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('others.home'))
        else:
            flash(f'Login unsuccessful. Please check your username and password', 'danger')
    return render_template('login.html',title='login',form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('others.home'))



@users.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccount()
    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Account has been updated', 'success')
        return redirect(url_for('users.account'))  # important
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = current_user.image_file
    return render_template('account.html',title='account',image_file = image_file,form=form)

@users.route('/reset_password',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('others.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instruction to reset your password.Check your email','info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',title='Reset Password',form=form)

@users.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('others.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token.",'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hash = Hash()
        password = hash.pass_encrypt(form.password.data)
        user.password = password
        db.session.commit()
        flash(f'Your password has been updated.You are now able to login!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',title='Reset Password',form=form)