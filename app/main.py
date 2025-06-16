import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Page setup
st.set_page_config(page_title="Unheard", page_icon="🎵")
st.title("🎵 Unheard: Spotify Login Test")

# Spotify app credentials
client_id = st.secrets["SPOTIPY_CLIENT_ID"]
client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
redirect_uri = st.secrets["SPOTIPY_REDIRECT_URI"]

# Get ?code from URL (for login response)
query_params = st.experimental_get_query_params()
auth_code = query_params.get("code", [None])[0]

# Spotipy auth manager
auth_manager = SpotifyOAuth(
    scope="user-read-private",
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    cache_path=".spotifycache"
)

# If no token yet, show login link
if not auth_code:
    auth_url = auth_manager.get_authorize_url()
    st.markdown(f"👉 [Click here to log in with Spotify]({auth_url})")
    st.stop()

# Use the auth code to get an access token
token_info = auth_manager.get_access_token(auth_code, as_dict=False)
sp = spotipy.Spotify(auth=token_info)

# Show user's Spotify display name
user = sp.current_user()
st.success(f"✅ Successfully connected to Spotify as **{user['display_name']}**")

