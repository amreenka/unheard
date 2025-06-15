import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

# Create Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-top-read",
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI")
))

# Streamlit UI
st.title("🎵 Unheard: Your Spotify Top Tracks")

try:
    results = sp.current_user_top_tracks(limit=10, time_range='short_term')
    for i, item in enumerate(results['items']):
        st.write(f"{i+1}. {item['name']} by {item['artists'][0]['name']}")
except:
    st.warning("Please log in to Spotify and paste the full redirected URL with the code.")

