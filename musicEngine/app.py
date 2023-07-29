from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from utils import process_login, create_user, get_artist_songs
import secrets

app = Flask(__name__)

# Generate a secure secret key for Flask-WTF
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key

# Initialize the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///musicRec'
db = SQLAlchemy(app)

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Artist search route
@app.route('/artist/search', methods=['GET', 'POST'])
def search_artist():
    if request.method == 'POST':
        artist_name = request.form.get('artist_name')

        # Logic to fetch the artist and their songs
        songs = get_artist_songs(artist_name)

        if not songs:
            return render_template('artist_not_found.html', artist_name=artist_name)

        return render_template('artist_songs.html', artist_name=artist_name, songs=songs)

    return render_template('artist_selection.html')

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Process user login
        if process_login(username, password):
            # Set up a session or cookie to keep the user logged in if needed
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Create a new user account
        create_user(username, email, password)

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
