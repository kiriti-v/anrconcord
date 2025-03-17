import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="Spotify API Test",
    page_icon="🎵",
    layout="wide"
)

# API URL
API_URL = "http://localhost:8000"

# Function to fetch emerging artists
def fetch_spotify_artists():
    try:
        response = requests.get(f"{API_URL}/artists/spotify-emerging")
        if response.status_code == 200:
            return response.json()["artists"]
        else:
            st.error(f"Error fetching emerging artists: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error fetching emerging artists: {e}")
        return []

# Main app
st.title("Spotify API Test")
st.write("This is a simple app to test the Spotify API connection.")

# Fetch and display artists
if st.button("Fetch Spotify Artists"):
    with st.spinner("Fetching artists from Spotify..."):
        artists = fetch_spotify_artists()
    
    if not artists:
        st.warning("No artists found. Check if the API server is running.")
    else:
        st.success(f"Found {len(artists)} artists!")
        
        # Display artists in a grid
        cols = st.columns(2)
        
        for i, artist in enumerate(artists):
            col = cols[i % 2]
            
            with col:
                artist_name = artist['artist']['name']
                genres = ", ".join(artist['artist'].get('genres', [])[:3]) if artist['artist'].get('genres') else "N/A"
                momentum_score = artist.get('momentum_score', 0)
                
                # Get artist image URL
                image_url = artist['artist'].get('image_url', '')
                
                # Display artist card
                with st.container():
                    if image_url:
                        st.image(image_url, width=200)
                    
                    st.subheader(artist_name)
                    st.write(f"**Genres:** {genres}")
                    st.write(f"**Momentum Score:** {momentum_score:.2f}")
                    
                    # Display insights
                    if artist.get('insights'):
                        st.write("**Why they're trending:**")
                        for insight in artist.get('insights', []):
                            st.write(f"- {insight}")
                    
                    st.divider() 