import requests
import base64
import time
from threading import Thread
from PIL import Image
from io import BytesIO
import pygame
import os
from flask import Flask, request


# Spotify API credentials
CLIENT_ID = "d75124890f674fe48b0b0353f2e6ae6e"
CLIENT_SECRET = "1f093c931a73441694808a99a654340d"
REDIRECT_URI = "http://localhost:7777/callback"
SCOPES = "user-read-recently-played"

access_token = None
refresh_token = None
song_data = None
update_interval = 10  # Fetch new song info every 10 seconds

# Flask app for Spotify authentication
app = Flask(__name__)

@app.route("/")
def login():
    auth_url = (
        "https://accounts.spotify.com/authorize?"
        f"client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPES}"
    )
    return f'<a href="{auth_url}">Log in to Spotify</a>'

@app.route("/callback")
def callback():
    global access_token, refresh_token
    code = request.args.get("code")

    # Get access token
    token_url = "https://accounts.spotify.com/api/token"
    encoded_credentials = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode("utf-8")
    token_headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    response = requests.post(token_url, headers=token_headers, data=token_data)
    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info["access_token"]
        refresh_token = token_info["refresh_token"]

        # Start the fetch loop in a new thread
        Thread(target=fetch_song_data, daemon=True).start()
        return "Authorization successful. Display will update regularly!"
    else:
        return f"Error getting token: {response.text}"

def refresh_access_token():
    global access_token, refresh_token
    token_url = "https://accounts.spotify.com/api/token"
    encoded_credentials = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode("utf-8")
    token_headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    token_data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    response = requests.post(token_url, headers=token_headers, data=token_data)
    if response.status_code == 200:
        access_token = response.json()["access_token"]
    else:
        print("Error refreshing token:", response.status_code, response.text)

def fetch_song_data():
    global song_data
    while True:
        song_data = get_recently_played()
        time.sleep(update_interval)

def get_recently_played():
    global access_token
    api_url = "https://api.spotify.com/v1/me/player/recently-played?limit=1"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data["items"]:
            track = data["items"][0]["track"]
            album_cover_url = track["album"]["images"][0]["url"]
            song_name = track["name"]
            artist_name = track["artists"][0]["name"]
            return {"album_cover_url": album_cover_url, "song_name": song_name, "artist_name": artist_name}
    elif response.status_code == 401:  # Token expired
        refresh_access_token()
    return None

def main_display():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # Adjust to your screen resolution
    pygame.display.set_caption("Now Playing")
    font_large = pygame.font.Font(None, 50)
    font_small = pygame.font.Font(None, 30)
    clock = pygame.time.Clock()

    while True:
        if song_data:
            album_cover_url = song_data["album_cover_url"]
            song_name = song_data["song_name"]
            artist_name = song_data["artist_name"]

            # Fetch album cover
            response = requests.get(album_cover_url)
            album_cover = Image.open(BytesIO(response.content))
            album_cover = album_cover.resize((300, 300))  # Resize for display
            album_cover_path = "/tmp/album_cover.jpg"
            album_cover.save(album_cover_path)

            # Load album cover into Pygame
            album_image = pygame.image.load(album_cover_path)

            # Render text
            song_text = font_large.render(song_name, True, (255, 255, 255))
            artist_text = font_small.render(f"by {artist_name}", True, (255, 255, 255))

            # Fill screen with background color
            screen.fill((30, 30, 30))  # Dark gray

            # Display album cover and text
            screen.blit(album_image, (50, 90))
            screen.blit(song_text, (400, 150))
            screen.blit(artist_text, (400, 220))

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(30)

if __name__ == "__main__":
    Thread(target=app.run, kwargs={"port": 7777}, daemon=True).start()
    main_display()