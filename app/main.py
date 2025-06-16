import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

st.set_page_config(page_title="Unheard", page_icon="🎵")
st.title("🎵 Unheard: Discover Your Top Tracks")

# Spotify credentials from Streamlit Cloud secrets
client_id = st.secrets["SPOTIPY_CLIENT_ID"]
client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
redirect_uri = st.secrets["SPOTIPY_REDIRECT_URI"]

# Create OAuth manager
auth_manager = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="user-top-read user-read-private",
    show_dialog=True,
    cache_path=None
)

# Check query params for Spotify authorization code
query_params = st.query_params
code = query_params.get("code", [None])[0] if "code" in query_params else None
st.write("Authorization code:", code)

if not code:
    auth_url = auth_manager.get_authorize_url()
    st.markdown(f"[🔐 Log in with Spotify]({auth_url})")
    st.stop()

try:
    st.write("Attempting to get access token...")
    access_token = auth_manager.get_access_token(code, as_dict=False)
    st.success("Access token received!")
    st.code(access_token)

    sp = spotipy.Spotify(auth=access_token)
    st.success("Spotify client initialized!")

    user = sp.current_user()
    st.success(f"Logged in as {user['display_name']}")
    if user.get("images"):
        st.image(user["images"][0]["url"], width=150)

    st.subheader("🎧 Your Top 10 Tracks:")
    top_tracks = sp.current_user_top_tracks(limit=10)

    for i, item in enumerate(top_tracks["items"]):
        name = item["name"]
        artist = item["artists"][0]["name"]
        st.markdown(f"{i + 1}. **{name}** by *{artist}*")

except Exception as e:
    st.error("⚠️ Spotify login failed or token invalid.")
    st.code(str(e))

