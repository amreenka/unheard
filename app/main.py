import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Page setup
st.set_page_config(page_title="Unheard", page_icon="🎵")
st.title("🎵 Unheard: Discover Your Top Tracks")

