import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
from datetime import datetime, timedelta

# Add a flag to check if page config has been set
if 'page_config_set' not in st.session_state:
    # Page configuration - MUST be the first Streamlit command
    st.set_page_config(
        page_title="Emerging Artist Discovery",
        page_icon="🎵",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.session_state.page_config_set = True

# Add parent directory to path to import app modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

# Set API port manually if import fails
try:
    from app.utils.config import API_PORT
    from app.utils.logger import logger
except ImportError:
    API_PORT = 8000
    import logging
    logger = logging.getLogger("streamlit")

# API base URL - Use localhost instead of 0.0.0.0 for browser access
API_URL = f"http://localhost:{API_PORT}"

# Helper functions
def fetch_emerging_artists(use_spotify=False):
    """Fetch emerging artists from the API"""
    try:
        # Use the Spotify endpoint if requested
        endpoint = "/artists/spotify-emerging" if use_spotify else "/emerging/artists"
        response = requests.get(f"{API_URL}{endpoint}")
        if response.status_code == 200:
            return response.json()["artists"]
        else:
            st.error(f"Error fetching emerging artists: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error fetching emerging artists: {e}")
        return []

def fetch_artist_data(artist_name, days=30, force_refresh=False):
    """Fetch data for a specific artist from API"""
    try:
        response = requests.get(
            f"{API_URL}/artists/{artist_name}",
            params={"days": days, "force_refresh": force_refresh}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching artist data: {e}")
        st.error(f"Error fetching artist data: {e}")
        return None

def search_artists(query, limit=10):
    """Search for artists by name"""
    try:
        response = requests.get(f"{API_URL}/artists/search", params={"query": query, "limit": limit})
        response.raise_for_status()
        return response.json()["artists"]
    except Exception as e:
        logger.error(f"Error searching artists: {e}")
        st.error(f"Error searching artists: {e}")
        return []

def plot_streaming_history(streaming_data):
    """Create a line chart of streaming history"""
    if not streaming_data:
        return None
    
    df = pd.DataFrame(streaming_data)
    df['date'] = pd.to_datetime(df['date'])
    
    fig = px.line(
        df, 
        x='date', 
        y='streams',
        title='Daily Streaming Trends',
        labels={'streams': 'Daily Streams', 'date': 'Date'},
        template='plotly_dark'
    )
    
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Streams',
        hovermode='x unified',
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    fig.update_traces(line=dict(color='white', width=2))
    
    return fig

def plot_social_engagement(engagement_data):
    """Create a line chart of social engagement"""
    if not engagement_data:
        return None
    
    df = pd.DataFrame(engagement_data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Create a figure with secondary y-axis
    fig = go.Figure()
    
    # Add likes
    fig.add_trace(
        go.Scatter(
            x=df['date'], 
            y=df['likes'],
            name='Likes',
            line=dict(color='#ffffff', width=2)
        )
    )
    
    # Add shares
    fig.add_trace(
        go.Scatter(
            x=df['date'], 
            y=df['shares'],
            name='Shares',
            line=dict(color='#aaaaaa', width=2)
        )
    )
    
    # Add comments
    fig.add_trace(
        go.Scatter(
            x=df['date'], 
            y=df['comments'],
            name='Comments',
            line=dict(color='#666666', width=2)
        )
    )
    
    fig.update_layout(
        title='Social Media Engagement Trends',
        xaxis_title='Date',
        yaxis_title='Count',
        hovermode='x unified',
        template='plotly_dark',
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig

def plot_momentum_radar(artist_data):
    """Create a radar chart of momentum metrics"""
    categories = ['Streaming Growth', 'Social Growth', 'Playlist Score', 'Viral Score']
    
    values = [
        artist_data.get('streaming_growth', 0) * 100,  # Convert to percentage
        artist_data.get('social_growth', 0) * 100,     # Convert to percentage
        artist_data.get('playlist_score', 0) * 100,    # Convert to percentage
        artist_data.get('viral_score', 0) * 100        # Convert to percentage
    ]
    
    # Cap values at 100 for better visualization
    values = [min(v, 100) for v in values]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Momentum Metrics',
        line_color='white',
        fillcolor='rgba(255, 255, 255, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                color='white'
            ),
            angularaxis=dict(
                color='white'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig

# Custom CSS for Concord-themed dark mode with black and white aesthetic
st.markdown("""
<style>
    /* Global styles */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    
    /* Headers */
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 1rem;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    
    /* Artist cards */
    .artist-card {
        background-color: #121212;
        border-radius: 12px;
        padding: 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(255, 255, 255, 0.1);
        border: 1px solid #333333;
        color: #ffffff;
        transition: transform 0.2s, box-shadow 0.2s;
        position: relative;
    }
    
    .artist-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(255, 255, 255, 0.15);
    }
    
    /* Artist image */
    .artist-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 1rem;
        border: 1px solid #333333;
    }
    
    /* Progress bar background */
    .progress-bar-bg {
        background-color: #333333;
        border-radius: 10px;
        height: 10px;
        width: 100%;
        margin-bottom: 15px;
    }
    
    /* Progress bar fill */
    .progress-bar-fill {
        background-color: #ffffff;
        border-radius: 10px;
        height: 10px;
    }
    
    /* Insight tags */
    .insight-tag {
        background-color: #333333;
        color: #ffffff;
        padding: 0.3rem 0.6rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        display: inline-block;
        font-weight: 600;
        border: 1px solid #555555;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("<div class='main-header'>Concord Music Group A&R Dashboard Demo</div>", unsafe_allow_html=True)
st.sidebar.markdown("Discover emerging artists with data-driven insights")

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Spotify Emerging Artists", "Emerging Artists", "Artist Search", "About"], key="main_navigation")

# Sidebar filters
st.sidebar.markdown("---")
st.sidebar.markdown("<div class='sub-header'>Filters</div>", unsafe_allow_html=True)
days_filter = st.sidebar.slider("Analysis Period (Days)", min_value=7, max_value=90, value=30, step=1)
limit_filter = st.sidebar.slider("Number of Artists", min_value=5, max_value=20, value=10, step=1)

# Main content
if page == "Spotify Emerging Artists":
    st.markdown("<div class='main-header'>🎵 Real Spotify Emerging Artists</div>", unsafe_allow_html=True)
    st.markdown("These artists are showing significant momentum based on real Spotify data combined with simulated metrics for a complete view.")
    
    # Add a refresh button
    col1, col2 = st.columns([3, 1])
    with col2:
        force_refresh = st.button("Refresh Data", help="Force refresh the Spotify data")
    
    # Fetch emerging artists from Spotify
    with st.spinner("Fetching real emerging artists from Spotify..."):
        emerging_artists = fetch_emerging_artists(use_spotify=True)
    
    if not emerging_artists:
        st.warning("No emerging artists found from Spotify. Please check your Spotify API credentials or try again later.")
    else:
        # Display artists in a grid
        cols = st.columns(2)
        
        for i, artist in enumerate(emerging_artists):
            col = cols[i % 2]
            
            with col:
                # Create a container for the entire card including the button
                with st.container():
                    # Artist card with all content inside - using simpler HTML
                    artist_name = artist['artist']['name']
                    genres = ", ".join(artist['artist'].get('genres', [])[:3]) if artist['artist'].get('genres') else "N/A"
                    momentum_score = artist.get('momentum_score', 0)
                    normalized_score = min(100, int(momentum_score * 50))
                    
                    insights_html = ""
                    for insight in artist.get('insights', []):
                        insights_html += f'<span class="insight-tag">{insight}</span>'
                    
                    # Get artist image URL
                    image_url = artist['artist'].get('image_url', '')
                    image_html = f'<img src="{image_url}" class="artist-image" alt="{artist_name}" />' if image_url else ''
                    
                    st.markdown(f"""
                    <div class='artist-card'>
                        {image_html}
                        <h3>{artist_name}</h3>
                        <p><strong>Genres:</strong> {genres}</p>
                        <p><strong>Momentum Score:</strong> {momentum_score:.2f}</p>
                        <div class="progress-bar-bg">
                            <div class="progress-bar-fill" style="width: {normalized_score}%;"></div>
                        </div>
                        <p><strong>Why they're trending:</strong></p>
                        <p>{insights_html}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # View details button
                    if st.button(f"View Details", key=f"view_spotify_{i}"):
                        st.session_state[f"show_details_{i}"] = True

                    # If details should be shown for this artist
                    if st.session_state.get(f"show_details_{i}", False):
                        with st.expander(f"Details for {artist_name}", expanded=True):
                            # Display artist image
                            if image_url:
                                st.image(image_url, width=200)
                            
                            # Artist info
                            st.subheader(artist_name)
                            st.write(f"**Genres:** {genres}")
                            st.write(f"**Popularity:** {artist['artist'].get('popularity', 'N/A')}/100")
                            st.write(f"**Followers:** {artist['artist'].get('followers', 0):,}")
                            
                            # Momentum metrics
                            st.write("**Momentum Metrics:**")
                            st.write(f"- **Momentum Score:** {momentum_score:.2f}")
                            st.write(f"- **Streaming Growth:** {artist.get('streaming_growth', 0)*100:.1f}%")
                            st.write(f"- **Social Growth:** {artist.get('social_growth', 0)*100:.1f}%")
                            st.write(f"- **Viral Score:** {artist.get('viral_score', 0)*100:.1f}%")
                            
                            # Tracks section
                            st.write("**Top Tracks:**")
                            if 'raw_data' in artist and 'tracks' in artist['raw_data']:
                                tracks = artist['raw_data']['tracks']
                                for track in tracks[:5]:  # Show top 5 tracks
                                    st.write(f"- **{track['name']}** (Popularity: {track.get('popularity', 'N/A')}/100)")
                            
                            # Add "More Analysis" button
                            if st.button("More Analysis", key=f"more_analysis_{i}"):
                                st.session_state[f"show_analysis_{i}"] = True
                            
                            # Show detailed analysis if button was clicked
                            if st.session_state.get(f"show_analysis_{i}", False):
                                st.markdown("---")
                                st.subheader(f"Detailed Analysis for {artist_name}")
                                
                                # Create tabs for different analysis views
                                tab1, tab2, tab3 = st.tabs(["Streaming Trends", "Social Engagement", "Momentum Analysis"])
                                
                                with tab1:
                                    st.write("### Streaming Trends")
                                    if 'streaming_history' in artist and artist['streaming_history']:
                                        streaming_fig = plot_streaming_history(artist['streaming_history'])
                                        if streaming_fig:
                                            st.plotly_chart(streaming_fig, use_container_width=True)
                                        else:
                                            st.info("No streaming data available for this artist.")
                                    else:
                                        # Generate simulated streaming data if none exists
                                        st.write("Showing simulated streaming data based on artist popularity")
                                        
                                        # Create simulated streaming history based on artist popularity
                                        popularity = artist['artist'].get('popularity', 50)
                                        momentum = artist.get('momentum_score', 1.0)
                                        
                                        # Generate last 30 days of data
                                        import random
                                        from datetime import datetime, timedelta
                                        
                                        streaming_data = []
                                        base_streams = popularity * 100  # Base streams based on popularity
                                        growth_factor = 1 + (momentum / 10)  # Growth based on momentum
                                        
                                        for i in range(30):
                                            date = (datetime.now() - timedelta(days=30-i)).strftime('%Y-%m-%d')
                                            # Add some randomness but ensure overall growth trend
                                            daily_fluctuation = random.uniform(0.8, 1.2)
                                            growth_trend = (1 + (i/30) * (growth_factor-1))
                                            streams = int(base_streams * daily_fluctuation * growth_trend)
                                            streaming_data.append({"date": date, "streams": streams})
                                        
                                        streaming_fig = plot_streaming_history(streaming_data)
                                        st.plotly_chart(streaming_fig, use_container_width=True)
                                
                                with tab2:
                                    st.write("### Social Engagement")
                                    if 'social_engagement' in artist and artist['social_engagement']:
                                        social_fig = plot_social_engagement(artist['social_engagement'])
                                        if social_fig:
                                            st.plotly_chart(social_fig, use_container_width=True)
                                        else:
                                            st.info("No social engagement data available for this artist.")
                                    else:
                                        # Generate simulated social engagement data if none exists
                                        st.write("Showing simulated social engagement data based on artist popularity")
                                        
                                        # Create simulated social engagement based on artist popularity
                                        popularity = artist['artist'].get('popularity', 50)
                                        momentum = artist.get('momentum_score', 1.0)
                                        
                                        # Generate last 30 days of data
                                        import random
                                        from datetime import datetime, timedelta
                                        
                                        social_data = []
                                        base_likes = popularity * 20  # Base likes based on popularity
                                        base_shares = popularity * 5  # Base shares
                                        base_comments = popularity * 10  # Base comments
                                        growth_factor = 1 + (momentum / 5)  # Growth based on momentum
                                        
                                        for i in range(30):
                                            date = (datetime.now() - timedelta(days=30-i)).strftime('%Y-%m-%d')
                                            # Add some randomness but ensure overall growth trend
                                            daily_fluctuation = random.uniform(0.8, 1.2)
                                            growth_trend = (1 + (i/30) * (growth_factor-1))
                                            
                                            likes = int(base_likes * daily_fluctuation * growth_trend)
                                            shares = int(base_shares * daily_fluctuation * growth_trend)
                                            comments = int(base_comments * daily_fluctuation * growth_trend)
                                            
                                            social_data.append({
                                                "date": date, 
                                                "likes": likes, 
                                                "shares": shares, 
                                                "comments": comments
                                            })
                                        
                                        social_fig = plot_social_engagement(social_data)
                                        st.plotly_chart(social_fig, use_container_width=True)
                                
                                with tab3:
                                    st.write("### Momentum Analysis")
                                    momentum_fig = plot_momentum_radar(artist)
                                    st.plotly_chart(momentum_fig, use_container_width=True)
                                    
                                    st.write("### Why This Artist Is Trending")
                                    for insight in artist.get('insights', []):
                                        st.markdown(f"- {insight}")
                                
                                # Button to hide detailed analysis
                                if st.button("Hide Analysis", key=f"hide_analysis_{artist_name.replace(' ', '_')}_{i}"):
                                    st.session_state[f"show_analysis_{i}"] = False
                                    st.experimental_rerun()
                            
                            # Close button
                            if st.button("Close", key=f"close_details_{i}"):
                                st.session_state[f"show_details_{i}"] = False
                                st.experimental_rerun()

elif page == "Emerging Artists":
    st.markdown("<div class='main-header'>🔥 Top Emerging Artists (Simulated)</div>", unsafe_allow_html=True)
    st.markdown("These artists are showing significant momentum based on simulated data for streaming growth, social engagement, and playlist additions.")
    
    # Fetch emerging artists
    with st.spinner("Discovering emerging artists..."):
        emerging_artists = fetch_emerging_artists(use_spotify=False)
    
    if not emerging_artists:
        st.warning("No emerging artists found. Please try again later.")
    else:
        # Display artists in a grid
        cols = st.columns(2)
        
        for i, artist in enumerate(emerging_artists):
            col = cols[i % 2]
            
            with col:
                # Create a container for the entire card including the button
                with st.container():
                    # Artist card with all content inside - using simpler HTML
                    artist_name = artist['artist']['name']
                    genres = ", ".join(artist['artist'].get('genres', [])[:3]) if artist['artist'].get('genres') else "N/A"
                    momentum_score = artist.get('momentum_score', 0)
                    normalized_score = min(100, int(momentum_score * 50))
                    
                    insights_html = ""
                    for insight in artist.get('insights', []):
                        insights_html += f'<span class="insight-tag">{insight}</span>'
                    
                    st.markdown(f"""
                    <div class='artist-card'>
                        <h3>{artist_name}</h3>
                        <p><strong>Genres:</strong> {genres}</p>
                        <p><strong>Momentum Score:</strong> {momentum_score:.2f}</p>
                        <div class="progress-bar-bg">
                            <div class="progress-bar-fill" style="width: {normalized_score}%;"></div>
                        </div>
                        <p><strong>Why they're trending:</strong></p>
                        <p>{insights_html}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # View details button
                    if st.button(f"View Details", key=f"view_{i}"):
                        st.session_state[f"show_details_sim_{i}"] = True

                    # If details should be shown for this artist
                    if st.session_state.get(f"show_details_sim_{i}", False):
                        with st.expander(f"Details for {artist_name}", expanded=True):
                            # Artist info
                            st.subheader(artist_name)
                            st.write(f"**Genres:** {genres}")
                            st.write(f"**Popularity:** {artist['artist'].get('popularity', 'N/A')}/100")
                            st.write(f"**Followers:** {artist['artist'].get('followers', 0):,}")
                            
                            # Momentum metrics
                            st.write("**Momentum Metrics:**")
                            st.write(f"- **Momentum Score:** {momentum_score:.2f}")
                            st.write(f"- **Streaming Growth:** {artist.get('streaming_growth', 0)*100:.1f}%")
                            st.write(f"- **Social Growth:** {artist.get('social_growth', 0)*100:.1f}%")
                            st.write(f"- **Viral Score:** {artist.get('viral_score', 0)*100:.1f}%")
                            
                            # Tracks section
                            st.write("**Top Tracks:**")
                            if 'raw_data' in artist and 'tracks' in artist['raw_data']:
                                tracks = artist['raw_data']['tracks']
                                for track in tracks[:5]:  # Show top 5 tracks
                                    st.write(f"- **{track['name']}** (Popularity: {track.get('popularity', 'N/A')}/100)")
                            
                            # Add "More Analysis" button
                            if st.button("More Analysis", key=f"more_analysis_sim_{i}"):
                                st.session_state[f"show_analysis_sim_{i}"] = True
                            
                            # Show detailed analysis if button was clicked
                            if st.session_state.get(f"show_analysis_sim_{i}", False):
                                st.markdown("---")
                                st.subheader(f"Detailed Analysis for {artist_name}")
                                
                                # Create tabs for different analysis views
                                tab1, tab2, tab3 = st.tabs(["Streaming Trends", "Social Engagement", "Momentum Analysis"])
                                
                                with tab1:
                                    st.write("### Streaming Trends")
                                    if 'streaming_history' in artist and artist['streaming_history']:
                                        streaming_fig = plot_streaming_history(artist['streaming_history'])
                                        if streaming_fig:
                                            st.plotly_chart(streaming_fig, use_container_width=True)
                                        else:
                                            st.info("No streaming data available for this artist.")
                                    else:
                                        # Generate simulated streaming data if none exists
                                        st.write("Showing simulated streaming data based on artist popularity")
                                        
                                        # Create simulated streaming history based on artist popularity
                                        popularity = artist['artist'].get('popularity', 50)
                                        momentum = artist.get('momentum_score', 1.0)
                                        
                                        # Generate last 30 days of data
                                        import random
                                        from datetime import datetime, timedelta
                                        
                                        streaming_data = []
                                        base_streams = popularity * 100  # Base streams based on popularity
                                        growth_factor = 1 + (momentum / 10)  # Growth based on momentum
                                        
                                        for i in range(30):
                                            date = (datetime.now() - timedelta(days=30-i)).strftime('%Y-%m-%d')
                                            # Add some randomness but ensure overall growth trend
                                            daily_fluctuation = random.uniform(0.8, 1.2)
                                            growth_trend = (1 + (i/30) * (growth_factor-1))
                                            streams = int(base_streams * daily_fluctuation * growth_trend)
                                            streaming_data.append({"date": date, "streams": streams})
                                        
                                        streaming_fig = plot_streaming_history(streaming_data)
                                        st.plotly_chart(streaming_fig, use_container_width=True)
                                
                                with tab2:
                                    st.write("### Social Engagement")
                                    if 'social_engagement' in artist and artist['social_engagement']:
                                        social_fig = plot_social_engagement(artist['social_engagement'])
                                        if social_fig:
                                            st.plotly_chart(social_fig, use_container_width=True)
                                        else:
                                            st.info("No social engagement data available for this artist.")
                                    else:
                                        # Generate simulated social engagement data if none exists
                                        st.write("Showing simulated social engagement data based on artist popularity")
                                        
                                        # Create simulated social engagement based on artist popularity
                                        popularity = artist['artist'].get('popularity', 50)
                                        momentum = artist.get('momentum_score', 1.0)
                                        
                                        # Generate last 30 days of data
                                        import random
                                        from datetime import datetime, timedelta
                                        
                                        social_data = []
                                        base_likes = popularity * 20  # Base likes based on popularity
                                        base_shares = popularity * 5  # Base shares
                                        base_comments = popularity * 10  # Base comments
                                        growth_factor = 1 + (momentum / 5)  # Growth based on momentum
                                        
                                        for i in range(30):
                                            date = (datetime.now() - timedelta(days=30-i)).strftime('%Y-%m-%d')
                                            # Add some randomness but ensure overall growth trend
                                            daily_fluctuation = random.uniform(0.8, 1.2)
                                            growth_trend = (1 + (i/30) * (growth_factor-1))
                                            
                                            likes = int(base_likes * daily_fluctuation * growth_trend)
                                            shares = int(base_shares * daily_fluctuation * growth_trend)
                                            comments = int(base_comments * daily_fluctuation * growth_trend)
                                            
                                            social_data.append({
                                                "date": date, 
                                                "likes": likes, 
                                                "shares": shares, 
                                                "comments": comments
                                            })
                                        
                                        social_fig = plot_social_engagement(social_data)
                                        st.plotly_chart(social_fig, use_container_width=True)
                                
                                with tab3:
                                    st.write("### Momentum Analysis")
                                    momentum_fig = plot_momentum_radar(artist)
                                    st.plotly_chart(momentum_fig, use_container_width=True)
                                    
                                    st.write("### Why This Artist Is Trending")
                                    for insight in artist.get('insights', []):
                                        st.markdown(f"- {insight}")
                                
                                # Button to hide detailed analysis
                                if st.button("Hide Analysis", key=f"hide_analysis_sim_{artist_name.replace(' ', '_')}_{i}"):
                                    st.session_state[f"show_analysis_sim_{i}"] = False
                                    st.experimental_rerun()
                            
                            # Close button
                            if st.button("Close", key=f"close_details_sim_{i}"):
                                st.session_state[f"show_details_sim_{i}"] = False
                                st.experimental_rerun()

elif page == "Artist Search":
    st.markdown("<div class='main-header'>🔍 Artist Search</div>", unsafe_allow_html=True)
    st.markdown("Search for specific artists to analyze their momentum and potential.")
    
    # Search box
    search_query = st.text_input("Search for an artist", "")
    
    if search_query:
        with st.spinner(f"Searching for '{search_query}'..."):
            search_results = search_artists(search_query)
        
        if not search_results:
            st.warning(f"No artists found for '{search_query}'. Please try a different search term.")
        else:
            st.markdown(f"<div class='sub-header'>Search Results for '{search_query}'</div>", unsafe_allow_html=True)
            
            # Display search results
            for i, artist in enumerate(search_results):
                st.markdown(f"""
                <div class='artist-card'>
                    <h3>{artist['name']}</h3>
                    <p><strong>Genres:</strong> {', '.join(artist['genres']) if artist['genres'] else 'N/A'}</p>
                    <p><strong>Followers:</strong> {artist['followers']:,}</p>
                    <p><strong>Popularity:</strong> {artist['popularity']}/100</p>
                </div>
                """, unsafe_allow_html=True)
                
                # View details button
                st.button(f"Analyze Artist", key=f"analyze_{i}")

else:  # About page
    st.markdown("<div class='main-header'>ℹ️ About</div>", unsafe_allow_html=True)
    
    st.markdown("""
    ## Emerging Artist Discovery Tool
    
    This tool helps A&R teams discover and evaluate emerging music artists showing early signs of breakout success.
    
    ### Key Features
    
    - **Data-Driven Discovery**: Identify emerging artists based on streaming growth, social engagement, and playlist additions
    - **Comprehensive Analysis**: Evaluate artists across multiple metrics and platforms
    - **Actionable Insights**: Understand why an artist is trending and their growth potential
    
    ### How It Works
    
    1. **Data Collection**: We gather data from Spotify and social platforms (simulated TikTok data for the MVP)
    2. **Momentum Scoring**: Our algorithm calculates a momentum score based on multiple weighted factors
    3. **Ranking & Insights**: Artists are ranked by momentum score and provided with insights about their growth
    
    ### Data Sources
    
    - **Spotify API**: Streaming data, playlist additions, and artist information
    - **TikTok Data**: Social engagement metrics (simulated for the MVP)
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #666666; font-size: 0.8rem;'>© 2025 Kirtii Vundavilli for Concord Music Group</p>", unsafe_allow_html=True)

# Display selected page
st.header(f"Selected page: {page}")
st.write("The full dashboard will be implemented once this minimal version works.") 