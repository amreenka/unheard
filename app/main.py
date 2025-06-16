import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

st.set_page_config(page_title="Unheard", page_icon="🎵")
st.title("🎵 Unheard: Discover Your Top Tracks")

# Spotify credentials
client_id = st.secrets["SPOTIPY_CLIENT_ID"]
client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
redirect_uri = st.secrets["SPOTIPY_REDIRECT_URI"]

# OAuth manager
auth_manager = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="user-top-read user-read-private",
    show_dialog=True,
)

# Get code from query params (no parentheses!)
code = st.query_params.get("code", [None])[0]

if not code:
    auth_url = auth_manager.get_authorize_url()
    st.markdown(f"[🔐 Log in with Spotify]({auth_url})")
    st.stop()

try:
    token_info = auth_manager.get_access_token(code, as_dict=False)
    sp = spotipy.Spotify(auth=token_info)

    user = sp.current_user()
    st.success(f"Logged in as {user['display_name']}")
    st.image(user["images"][0]["url"], width=150)

    # Display top tracks
    st.subheader("🎧 Your Top 10 Tracks:")
    top_tracks = sp.current_user_top_tracks(limit=10)

    for i, item in enumerate(top_tracks['items']):
        name = item['name']
        artist = item['artists'][0]['name']
        st.markdown(f"{i+1}. **{name}** by *{artist}*")

except Exception as e:
    st.error("⚠️ Spotify login failed or token invalid.")
    st.code(str(e))
    st.stop()

