from project import app, db
from flask import render_template, request, redirect, url_for, session, flash, Markup
from project.forms import RegisterForm, LoginForm, ClientForm
from project.models import User, Client
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

login_manager = LoginManager()


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.
    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(user_id)



@app.route('/')
def dashboard():
    clients = Client.query.all()
    return render_template('index.html', clients=clients)


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = Markup('User already exists! Would you like to <a href="/login">log in </a> instead?')
    form = RegisterForm()
    if form.validate_on_submit() and request.method == 'POST':
        if User.query.filter_by(email=form.email.data).first():
            flash(message, category='info')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(email=form.email.data, password=hashed_password, authenticated=True)
        db.session.add(new_user)
        db.session.commit()
        flash(new_user.email + ' is now registered!', category='info')
        return redirect(url_for('dashboard'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    message = Markup('Account does not exist, do you want to <a href="/register">create</a> one instead?')
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash(message, category='info')
            return redirect(url_for('login'))
        if check_password_hash(user.password, form.password.data):
            user.authenticated = True
            flash('Logged in!', category='info')
            return redirect(url_for('dashboard'))
        flash('Login credentials incorrect', category='danger')
        return redirect(url_for('login'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out!', category='info')
    return redirect(url_for('login'))


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = ClientForm()
    if form.validate_on_submit():
        name = form.name.data
        pib = form.pib.data
        contact = form.contact.data
        client = Client(name=name, pib=pib, contact=contact)
        db.session.add(client)
        db.session.commit()
        flash('New client added!')
        return redirect(url_for('dashboard'))
    return render_template('add.html', form=form)


@app.route('/edit')
def edit():
    return 'Edit entry'


@app.route('/delete')
def delete():
    return 'Delete entry'
