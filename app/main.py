import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import time

# Page setup
st.set_page_config(page_title="Unheard", page_icon="🎵")
st.title("🎵 Unheard: Your Top Spotify Tracks")

# Spotify credentials
client_id = st.secrets["SPOTIPY_CLIENT_ID"]
client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
redirect_uri = st.secrets["SPOTIPY_REDIRECT_URI"]

# OAuth setup
auth_manager = SpotifyOAuth(
    scope="user-top-read",
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    cache_path=".spotifycache",
    show_dialog=True
)

# Try to get token manually
token_info = auth_manager.get_cached_token()

if not token_info:
    auth_url = auth_manager.get_authorize_url()
    st.markdown(f"[Click here to log into Spotify]({auth_url})")
    st.stop()

# If token exists, continue
sp = spotipy.Spotify(auth_manager=auth_manager)

with st.spinner("Fetching your top tracks..."):
    results = sp.current_user_top_tracks(limit=10, time_range='short_term')
    time.sleep(1)

st.subheader("🎧 Your Top 10 Tracks:")
for i, item in enumerate(results['items']):
    st.markdown(f"{i+1}. **{item['name']}** by *{item['artists'][0]['name']}*")
