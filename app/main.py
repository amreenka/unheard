import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Page setup

st.set_page_config(page_title="Unheard: Test", page_icon="✅")

st.title("✅ App Loaded Successfully")
st.write("If you're seeing this, Streamlit is running and completed execution.")
st.success("🎉 No errors. App ran to completion.")
