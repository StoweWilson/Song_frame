import requests
import base64
import time
from threading import Thread
from PIL import Image
from io import BytesIO
import pygame
import os
import json
from flask import Flask, request

# Spotify API credentials
CLIENT_ID = " Add Client Id here"
CLIENT_SECRET = "add Cleint Secret here"
REDIRECT_URI = "http://localhost:7777/callback"
SCOPES = "user-read-currently-playing user-read-recently-played"


access_token = None
refresh_token = None
song_data = None
update_interval = 2  # Fetch new song info every 2 seconds for real-time updates


app = Flask(__name__)

# Load tokens from file (if available)
def load_tokens():
    global access_token, refresh_token
    if os.path.exists("tokens.json"):
        with open("tokens.json", "r") as f:
            tokens = json.load(f)
            access_token = tokens.get("access_token")
            refresh_token = tokens.get("refresh_token")
            print("Tokens loaded successfully.")
    else:
        print("No tokens found. You will need to log in.")

# Save tokens to file
def save_tokens():
    global access_token, refresh_token
    with open("tokens.json", "w") as f:
        json.dump({"access_token": access_token, "refresh_token": refresh_token}, f)
    print("Tokens saved successfully.")


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
        save_tokens()  # Save tokens to file
        return "Authorization successful. You can now close this tab."
    else:
        return f"Error getting token: {response.text}"

# Refresh the access token using the refresh token
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
        token_info = response.json()
        access_token = token_info["access_token"]
        save_tokens()  # Save updated tokens
    else:
        print("Error refreshing token:", response.status_code, response.text)

# Fetch currently playing song data
def fetch_song_data():
    global song_data
    while True:
        song_data = get_currently_playing()
        time.sleep(update_interval)

# Get currently playing song from Spotify
def get_currently_playing():
    global access_token
    api_url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data and data.get("item"):
            track = data["item"]
            album_cover_url = track["album"]["images"][0]["url"]
            song_name = track["name"]
            artist_name = track["artists"][0]["name"]
            return {"album_cover_url": album_cover_url, "song_name": song_name, "artist_name": artist_name}
    elif response.status_code == 204:  # No content (no song currently playing)
        return None
    elif response.status_code == 401:  # Token expired
        refresh_access_token()
    return None

def truncate_text(text, font, max_width):
    """
    Truncate text to fit within the given max width, adding '...' if necessary.
    """
    while font.size(text)[0] > max_width:
        if len(text) > 3:
            text = text[:-4] + "..."
        else:
            break
    return text

# Pygame display for currently playing song
def main_display():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
    pygame.display.set_caption("Now Playing")
    font_large = pygame.font.Font(None, 60)
    font_small = pygame.font.Font(None, 30)
    clock = pygame.time.Clock()

    is_fullscreen = True

    while True:
        for event in pygame.event.get():
           if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:  # Press 'F' to toggle full-screen mode
                if is_fullscreen:
                    screen = pygame.display.set_mode((800, 600))  # Switch to windowed mode
                    is_fullscreen = False
                else:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Switch to full-screen
                    is_fullscreen = True
            elif event.type == pygame.QUIT:
                pygame.quit()
                return

        if song_data:
            # Fetch song details
            album_cover_url = song_data["album_cover_url"]
            song_name = song_data["song_name"]
            artist_name = song_data["artist_name"]

            # Fetch album cover
            response = requests.get(album_cover_url)
            album_cover = Image.open(BytesIO(response.content))

            # Get screen dimensions
            screen_width, screen_height = screen.get_size()

            # Dynamically calculate album size and font size based on screen size
            album_size = int(screen_height * 0.5)  
            font_large_size = int(screen_height * 0.05) 
            font_small_size = int(screen_height * 0.03) 

            # Resize album cover
            album_cover = album_cover.resize((album_size, album_size))  # Make the album square
            album_cover_path = "/tmp/album_cover.jpg"
            album_cover.save(album_cover_path)

            # Load album cover into Pygame
            album_image = pygame.image.load(album_cover_path)

            # Calculate positions
            image_x = screen_width // 12 
            image_y = (screen_height - album_size) // 2  

            text_x = image_x + album_size + 20  
            text_width = screen_width - text_x - 20  

            # Align text with the middle of the album cover
            text_y = image_y + (album_size // 2) - (font_large_size // 2)  

            # adds .... if text doesn't fit
            song_name = truncate_text(song_name, font_large, text_width)
            artist_name = truncate_text(artist_name, font_small, text_width)

            # Render text
            song_text = font_large.render(song_name, True, (255, 255, 255)) 
            artist_text = font_small.render(f"by {artist_name}", True, (255, 255, 255))

            # background color
            screen.fill((30, 30, 30))  

            # Display album cover
            screen.blit(album_image, (image_x, image_y))

            # Display text inline with album cover
            screen.blit(song_text, (text_x, text_y))
            screen.blit(artist_text, (text_x, text_y + font_large_size + 10)) 

        
        pygame.display.flip()

        
        clock.tick(30)

if __name__ == "__main__":
    load_tokens() 
    if access_token and refresh_token:
        Thread(target=fetch_song_data, daemon=True).start()
        main_display()
    else:
        print("Starting Flask server for login...")
        print("Visit http://localhost:7777/ to log in.")
        app.run(host="0.0.0.0", port=7777)