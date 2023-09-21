from flask import render_template, request, redirect, url_for, flash
from . import app, db, login_manager
from .models import User, Track
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegistrationForm, UploadForm
import eyed3
import os
import tempfile

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        tracks = Track.query.filter_by(user_id=current_user.id).all()
    else:
        tracks = []
    return render_template('index.html', title='Home', tracks=tracks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('You are now registered!')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data

        _, tmp_filename = tempfile.mkstemp()
        file.save(tmp_filename)

        metadata = eyed3.load(tmp_filename)

        title = metadata.tag.title if metadata.tag.title else 'Unknown Title'
        artist = metadata.tag.artist if metadata.tag.artist else 'Unknown Artist'
        album = metadata.tag.album if metadata.tag.album else 'Unknown Album'
        genre = metadata.tag.genre if metadata.tag.genre else 'Unknown Genre'

        os.remove(tmp_filename)

        track = Track(title=title, artist=artist, album=album, genre=genre, user_id=current_user.id)
        db.session.add(track)
        db.session.commit()

        flash('Track uploaded successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('upload.html', form=form)


