from flask import Flask, render_template, request 
from flask_sqlalchemy import SQLAlchemy
from utils import fetch_recommendations


app = Flask(__name__)

# Initialize the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///musicRec'
db = SQLAlchemy(app)

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Recommendation route
@app.route('/recommendations', methods=['POST'])
def recommendations():
    # Logic to fetch and generate music recommendations
    genre = request.form.get('genre')
    recommendations = fetch_recommendations(genre)

    return render_template('recs.html', recommendations=recommendations)


# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

    return render_template('login.html')

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
