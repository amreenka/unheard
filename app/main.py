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
st.markdown(redirect_uri)
