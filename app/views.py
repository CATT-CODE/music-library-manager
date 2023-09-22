from flask import render_template, request, redirect, url_for, flash
from . import app, db, login_manager
from .models import User, Track, Artist
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegistrationForm, UploadForm, EditMetadataForm
import eyed3
import os
import tempfile

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/index')
@app.route('/')
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
        files = request.files.getlist('files')
        
        for file in files:
            _, tmp_filename = tempfile.mkstemp()
            file.save(tmp_filename)

            metadata = eyed3.load(tmp_filename)

            title = metadata.tag.title if metadata.tag.title else 'Unknown Title'
            artist_name = metadata.tag.artist if metadata.tag.artist else 'Unknown Artist'
            album = metadata.tag.album if metadata.tag.album else 'Unknown Album'
            genre = metadata.tag.genre if metadata.tag.genre else 'Unknown Genre'

            artist = Artist.query.filter(Artist.name.ilike(artist_name)).first()
            if not artist:
                artist = Artist(name=artist_name)
                db.session.add(artist)
                db.session.flush()

            if title != 'Unknown Title':
                existing_track = Track.query.filter_by(title=title, artist_id=artist.id).first()
                if existing_track:
                    os.remove(tmp_filename) 
                    continue

            os.remove(tmp_filename)

            track = Track(title=title, artist_id=artist.id, album=album, genre=genre, user_id=current_user.id)
            db.session.add(track)

        db.session.commit()

        flash(f'{len(files)} track(s) uploaded successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('upload.html', title='Upload', form=form)


@app.route('/edit_metadata/<int:track_id>', methods=['GET', 'POST'])
@login_required
def edit_metadata(track_id):
    track = Track.query.get_or_404(track_id)

    form = EditMetadataForm()

    if form.validate_on_submit():
        track.title = form.title.data or track.title
        artist_name = form.artist_name.data or track.artist.name
        artist = Artist.query.filter(Artist.name.ilike(artist_name)).first()
        if not artist:
            artist = Artist(name=artist_name)
            db.session.add(artist)
            db.session.flush()

        track.artist_id = artist.id
        track.album = form.album.data or track.album
        track.genre = form.genre.data or track.genre

        db.session.commit()
        flash('Metadata updated successfully', 'success')
        return redirect(url_for('index'))
    
    if request.method == 'GET':
        form.title.data = track.title
        form.artist_name.data = track.artist.name
        form.album.data = track.album
        form.genre.data = track.genre

    return render_template('edit_metadata.html', title='Edit Track', form=form)

@app.route('/delete_track/<int:track_id>', methods=['POST'])
@login_required
def delete_track(track_id):
    track = Track.query.get_or_404(track_id)
    if track.user_id != current_user.id:
        flash('Must login to delete tracks.', 'danger')
        return redirect(url_for('index'))

    db.session.delete(track)
    db.session.commit()
    flash('Track deleted successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/bulk_action', methods=['POST'])
@login_required
def bulk_action():
    

    selected_tracks = request.form.getlist('selected_tracks')
    action = request.form.get('action')
    print(action)

    tracks = Track.query.filter(Track.id.in_(selected_tracks)).all()

    if action == "Bulk Delete":
        for track in tracks:
            if track.user_id != current_user.id:
                flash('You do not have permission to delete tracks.', 'danger')
                return redirect(url_for('index'))
            db.session.delete(track)
        db.session.commit()
        flash(f'{len(tracks)} tracks deleted successfully!', 'success')
        return redirect(url_for('index'))

    elif action == "Bulk Edit":
        return render_template('bulk_edit.html', tracks=tracks)

    else:
        return redirect(url_for('index'))
