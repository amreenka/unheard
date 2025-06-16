import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Page setup
st.set_page_config(page_title="Unheard", page_icon="🎵")
st.title("🎵 Unheard: Your Top Spotify Tracks")

# Get secrets from Streamlit (Cloud or local secrets.toml)
client_id = st.secrets["SPOTIPY_CLIENT_ID"]
client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
redirect_uri = st.secrets["SPOTIPY_REDIRECT_URI"]

# Parse query parameters (Spotify will redirect with ?code=...)
query_params = st.experimental_get_query_params()
auth_code = query_params.get("code", [None])[0]

auth_manager = SpotifyOAuth(
    scope="user-top-read",
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    cache_path=".spotifycache"
)

if not auth_code:
    # If no auth code yet, create login link
    auth_url = auth_manager.get_authorize_url()
    st.markdown(f"👉 [Click here to log in with Spotify]({auth_url})")
    st.stop()

# Exchange code for token
token_info = auth_manager.get_access_token(auth_code, as_dict=False)
sp = spotipy.Spotify(auth=token_info)

# Fetch and show top tracks
st.subheader("🎧 Your Top 10 Tracks:")
top_tracks = sp.current_user_top_tracks(limit=10, time_range="short_term")
for i, item in enumerate(top_tracks["items"]):
    name = item["name"]
    artist = item["artists"][0]["name"]
    st.markdown(f"{i+1}. **{name}** by *{artist}*")
