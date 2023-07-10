import requests
from models import User  

def fetch_recommendations(genre):
    # Logic to fetch music recommendations based on the selected genre
    # Make API calls to the Spotify API to retrieve the recommendations
    # You can use the requests library to make the HTTP requests
    
    # Example code to fetch recommendations
    url = f'https://api.spotify.com/v1/recommendations?genre={genre}'
    response = requests.get(url)
    
    if response.status_code == 200:
        recommendations = response.json()
        return recommendations['tracks']
    else:
        return []


def process_login(username, password):
    #process user login

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return True
    else:
        return False

def create_user(username, email, password):
    #create a new user account
    user = User(username=username, email=email)
    user.set_password(password) 
    db.session.add(user)
    db.session.commit()
