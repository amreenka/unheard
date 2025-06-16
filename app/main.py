from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import spotipy

st.set_page_config(page_title="Unheard", page_icon="🎵")
st.title("🎵 Unheard: Discover Your Top Tracks")

client_id = st.secrets["SPOTIPY_CLIENT_ID"]
client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
redirect_uri = st.secrets["SPOTIPY_REDIRECT_URI"]

auth_manager = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="user-read-private user-top-read"
)

# Parse code from URL
query_params = st.query_params
auth_code = query_params.get("code", [None])[0]

# Show login link if not logged in
if not auth_code:
    auth_url = auth_manager.get_authorize_url()
    st.markdown(f"[🔐 Click here to log in to Spotify]({auth_url})")
    st.stop()

# Exchange code for token
try:
    token_info = auth_manager.get_access_token(auth_code, as_dict=False)
    sp = spotipy.Spotify(auth=token_info)

    # Success!
    user = sp.current_user()
    st.success(f"✅ Logged in as {user['display_name']}")
    st.image(user["images"][0]["url"], width=150)

except Exception as e:
    st.error("⚠️ Spotify auth failed")
    st.code(str(e))
    st.stop()

