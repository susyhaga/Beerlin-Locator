import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from beerlin import app, db, bcrypt
from beerlin.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from beerlin.models import User, Local
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
from flask import jsonify



@ app.route("/")
@ app.route("/home")
def home():
      return render_template(
        'home.html', 
        map_key=app.config['GOOGLE_MAPS_API_KEY'],
        profiles=[]
    )


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('map'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('map'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('map'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/imagens', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='imagens/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)





@ app.route("/map")
def map():
    local = Local.query.all()
    print(local)
    return render_template('map.html', title='Map', local=local)


# JSON Api routes
# ----------------
@app.route("/api/get_stores_in_radius")
def get_stores_in_radius():
    latitude = float(request.args.get('lat'))
    longitude = float(request.args.get('lng'))
    radius = int(request.args.get('radius'))

    # TODO: Validate the input? 

    stores = Local.get_stores_within_radius(lat=latitude, lng=longitude, radius=radius)
   
    result = []
    for s in stores:
        result.append(s.toDict())
    return jsonify(result)