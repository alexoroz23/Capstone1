from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    registration_date = db.Column(db.String(100), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    artist = db.relationship('Artist', backref=db.backref('songs', lazy=True))

    def __init__(self, title, artist):
        self.title = title
        self.artist = artist

def get_artist_songs(artist_name):
    artist = Artist.query.filter_by(name=artist_name).first()
    if artist:
        songs = Song.query.filter_by(artist_id=artist.id).all()
        return songs
    else:
        return []

def create_user(username, email, password):
    # create a new user account
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
