import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Page setup
st.set_page_config(page_title="Unheard", page_icon="🎵")
st.title("🎵 Unheard: Your Top Spotify Tracks")

# Get secrets from Streamlit Cloud (or .streamlit/secrets.toml locally)
client_id = st.secrets["SPOTIPY_CLIENT_ID"]
client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
redirect_uri = st.secrets["SPOTIPY_REDIRECT_URI"]

# Auth manager
auth_manager = SpotifyOAuth(
    scope="user-top-read",
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    cache_path=".spotifycache",
    show_dialog=True
)

try:
    # Connect to Spotipy
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Fetch top tracks
    results = sp.current_user_top_tracks(limit=10, time_range='short_term')

    st.subheader("🎧 Your Top 10 Tracks (Last ~4 Weeks):")

    # Display each track nicely
    for i, item in enumerate(results["items"]):
        track = item["name"]
        artist = item["artists"][0]["name"]
        st.markdown(f"**{i+1}. {track}** by *{artist}*")

except Exception as e:
    st.error("Something went wrong with Spotify login or data fetching.")
    st.code(str(e))
