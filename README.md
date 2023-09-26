# Music Library Manager

Music Library Manager is a Flask-based web application allowing users to manage their music libraries, edit metadata, and upload tracks to an AWS S3 bucket.

### Features
- **User Authentication:** Register, Login, Logout
- **Music Upload:** Users can upload their music tracks.
- **Music Management:** Users can view, edit, and delete their uploaded tracks.
- **Bulk Actions:** Perform actions such as editing and deleting on multiple tracks at once.

## Live App
Link

## Video Demo
Link

## Setup & Installation

#### 1. Clone the Repo
```sh
git clone https://github.com/CATT-CODE/music-library-manager.git
cd music-library-manager
```

#### 2. Set up a Virtual Environment (Mac)
```sh
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install the Requirements
```sh
pip install -r requirements.txt
```

#### 4. Configure Environment Variables
```sh
SECRET_KEY=
AWS_ACCESS_KEY=
AWS_SECRET_KEY=
AWS_BUCKET_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_NAME=
```

#### 5. Run the App
```sh
python3 run.py
```

## Endpoints & Routes

    @app.route('/'): Renders the index page displaying all the tracks for the authenticated user.
    @app.route('/login'): Renders the login page and handles user login.
    @app.route('/logout'): Handles user logout.
    @app.route('/register'): Renders the registration page and handles user registration.
    @app.route('/upload'): Renders the upload page and handles music upload.
    @app.route('/bulk_action'): Handles bulk actions for music tracks (delete, edit).
    @app.route('/process_bulk_edit'): Processes bulk edit actions for music tracks.
    @app.route('/process_global_bulk_edit'): Processes global bulk edit actions for music tracks.

