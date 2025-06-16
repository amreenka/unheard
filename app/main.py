import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Page setup
st.set_page_config(page_title="Unheard", page_icon="🎵")
st.title("🎵 Unheard: Discover Your Top Tracks")

# Load Spotify credentials from Streamlit secrets
client_id = st.secrets["SPOTIPY_CLIENT_ID"]
client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
redirect_uri = st.secrets["SPOTIPY_REDIRECT_URI"]

# Create Spotify client
try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope="user-top-read",
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        cache_path=".spotifycache",     # ✅ Fix: Save token in a safe location
        show_dialog=True                # ✅ Fix: Ensure login appears every time
    ))

    results = sp.current_user_top_tracks(limit=10, time_range='short_term')
    st.subheader("🎧 Your Top 10 Tracks (Short Term):")

    for i, item in enumerate(results['items']):
        name = item['name']
        artist = item['artists'][0]['name']
        st.markdown(f"{i+1}. **{name}** by *{artist}*")

except spotipy.exceptions.SpotifyOauthError as e:
    st.error("⚠️ Spotify login failed. Make sure your redirect URI and secrets are correct.")
    st.code(str(e))

except Exception as e:
    st.error("🚨 Something went wrong.")
    st.code(str(e))
