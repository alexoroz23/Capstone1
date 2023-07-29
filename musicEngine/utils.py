import os
import base64
import requests
from dotenv import load_dotenv
from models import User, db

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = requests.post(url, headers=headers, data=data)
    json_result = result.json()
    token = json_result.get("access_token")
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = requests.get(query_url, headers=headers)
    json_result = result.json()["artists"]["items"]

    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None

    return json_result[0]

def get_artist_songs(artist_name):
    token = get_token()

    # Search for the artist using the Spotify API
    artist = search_for_artist(token, artist_name)

    if not artist:
        return None

    artist_id = artist["id"]

    # Fetch the artist's top tracks using the Spotify API
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = requests.get(url, headers=headers)
    json_result = result.json()["tracks"]

    songs = []
    for track in json_result:
        song_details = {
            "name": track["name"],
            "album": track["album"]["name"],
            "preview_url": track.get("preview_url", None),
            # You can add more song details as needed
        }
        songs.append(song_details)

    return songs

def process_login(username, password):
    # Process user login
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return True
    else:
        return False

def create_user(username, email, password):
    # Create a new user account
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()