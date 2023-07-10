from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    registration_date = db.Column(db.String(100), nullable=True)

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    artist = db.relationship('Artist', backref=db.backref('songs', lazy=True))

class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('recommendations', lazy=True))
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    artist = db.relationship('Artist', backref=db.backref('recommendations', lazy=True))
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    song = db.relationship('Song', backref=db.backref('recommendations', lazy=True))
    score = db.Column(db.Integer, nullable=False)

    @staticmethod
    def create_recommendation(user_id, artist_id, song_id, score):
        recommendation = Recommendation(
            user_id=user_id,
            artist_id=artist_id,
            song_id=song_id,
            score=score
        )
        db.session.add(recommendation)
        db.session.commit()
