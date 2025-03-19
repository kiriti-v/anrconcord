import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
from datetime import datetime, timedelta
import random
import base64
from pathlib import Path

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Emerging Artist Discovery",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper functions
def simulate_artist_data(num_artists=10):
    """Simulate emerging artist data for demo purposes"""
    artists = []
    
    # List of potential genres
    genres = ["Pop", "Hip-Hop", "R&B", "Electronic", "Rock", "Alternative", "Indie", "Dance", "Latin", "K-Pop"]
    
    # List of potential insights
    insight_templates = [
        "Viral TikTok trend",
        "Featured on influential playlist",
        "Collaboration with established artist",
        "Strong social media growth",
        "Consistent streaming growth",
        "Recent press coverage",
        "Upcoming tour announced",
        "Strong engagement metrics",
        "Crossover appeal",
        "International breakthrough"
    ]
    
    # Generate random artist names
    first_names = ["Emma", "Liam", "Olivia", "Noah", "Ava", "Elijah", "Sophia", "Lucas", "Isabella", "Mason",
                  "Mia", "Logan", "Charlotte", "Ethan", "Amelia", "Jayden", "Harper", "Oliver", "Evelyn", "Jacob"]
    
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
                 "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson"]
    
    band_templates = ["The {}", "{} Collective", "{} & The Band", "DJ {}", "{} Project", "{}"]
    
    for i in range(num_artists):
        # Generate artist name
        if random.random() < 0.7:  # 70% chance of solo artist
            if random.random() < 0.5:
                name = random.choice(first_names)
            else:
                name = f"{random.choice(first_names)} {random.choice(last_names)}"
        else:  # 30% chance of band
            template = random.choice(band_templates)
            name = template.format(random.choice(last_names))
        
        # Generate artist data
        artist_genres = random.sample(genres, random.randint(1, 3))
        popularity = random.randint(30, 70)  # Emerging artists typically have mid-range popularity
        followers = random.randint(10000, 500000)
        
        # Generate momentum metrics
        streaming_growth = random.uniform(0.05, 0.5)  # 5% to 50% growth
        social_growth = random.uniform(0.1, 0.7)  # 10% to 70% growth
        playlist_score = random.uniform(0.2, 0.8)  # 20% to 80% score
        viral_score = random.uniform(0.1, 0.9)  # 10% to 90% score
        
        # Calculate overall momentum score (weighted average)
        momentum_score = (streaming_growth * 0.4) + (social_growth * 0.3) + (playlist_score * 0.2) + (viral_score * 0.1)
        momentum_score = round(momentum_score * 2, 2)  # Scale up and round
        
        # Generate insights
        num_insights = random.randint(2, 4)
        insights = random.sample(insight_templates, num_insights)
        
        # Generate streaming history (last 30 days)
        streaming_history = []
        base_streams = popularity * 100  # Base streams based on popularity
        growth_factor = 1 + (momentum_score / 10)  # Growth based on momentum
        
        for j in range(30):
            date = (datetime.now() - timedelta(days=30-j)).strftime('%Y-%m-%d')
            # Add some randomness but ensure overall growth trend
            daily_fluctuation = random.uniform(0.8, 1.2)
            growth_trend = (1 + (j/30) * (growth_factor-1))
            streams = int(base_streams * daily_fluctuation * growth_trend)
            streaming_history.append({"date": date, "streams": streams})
        
        # Generate social engagement data
        social_engagement = []
        base_likes = popularity * 20  # Base likes based on popularity
        base_shares = popularity * 5  # Base shares
        base_comments = popularity * 10  # Base comments
        
        for j in range(30):
            date = (datetime.now() - timedelta(days=30-j)).strftime('%Y-%m-%d')
            # Add some randomness but ensure overall growth trend
            daily_fluctuation = random.uniform(0.8, 1.2)
            growth_trend = (1 + (j/30) * (growth_factor-1))
            
            likes = int(base_likes * daily_fluctuation * growth_trend)
            shares = int(base_shares * daily_fluctuation * growth_trend)
            comments = int(base_comments * daily_fluctuation * growth_trend)
            
            social_engagement.append({
                "date": date, 
                "likes": likes, 
                "shares": shares, 
                "comments": comments
            })
        
        # Generate tracks
        num_tracks = random.randint(3, 5)
        tracks = []
        for j in range(num_tracks):
            track_name = f"Track {j+1}"
            track_popularity = random.randint(max(20, popularity-20), min(100, popularity+20))
            tracks.append({
                "name": track_name,
                "popularity": track_popularity
            })
        
        # Create artist object
        artist = {
            "artist": {
                "name": name,
                "genres": artist_genres,
                "popularity": popularity,
                "followers": followers
            },
            "momentum_score": momentum_score,
            "streaming_growth": streaming_growth,
            "social_growth": social_growth,
            "playlist_score": playlist_score,
            "viral_score": viral_score,
            "insights": insights,
            "streaming_history": streaming_history,
            "social_engagement": social_engagement,
            "raw_data": {
                "tracks": tracks
            }
        }
        
        artists.append(artist)
    
    # Sort by momentum score (descending)
    artists.sort(key=lambda x: x["momentum_score"], reverse=True)
    
    return artists

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
    
    /* Sidebar styling */
    .css-1d391kg, .css-1lcbmhc {
        background-color: #333333;
    }
    
    /* Logo container */
    .logo-container {
        padding: 1rem 0;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* Logo image */
    .logo-image {
        max-width: 100%;
        height: auto;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for artist data
if 'emerging_artists' not in st.session_state:
    st.session_state.emerging_artists = simulate_artist_data(num_artists=10)

# # Function to load and display the logo
# def display_logo():
#     try:
#         # Path to the logo file
#         logo_path = Path("/Users/kiriti/PycharmProjects/anrconcord/ConcordMusicPublishing-Lockup-Black-full.webp")
        
#         # Read the image file and convert to base64
#         with open(logo_path, "rb") as f:
#             logo_data = f.read()
#             logo_base64 = base64.b64encode(logo_data).decode()
        
#         # Display the logo with white background to make it visible on dark sidebar
#         st.sidebar.markdown(
#             f"""
#             <div style="background-color: white; padding: 10px; border-radius: 5px; margin-bottom: 20px; text-align: center;">
#                 <img src="data:image/webp;base64,{logo_base64}" style="max-width: 100%; height: auto;">
#             </div>
#             """,
#             unsafe_allow_html=True
#         )
#     except Exception as e:
#         st.sidebar.error(f"Could not load logo: {e}")

# # Display the logo
# display_logo()

# Sidebar title and description
st.sidebar.markdown("<div class='main-header'>Concord Music Group A&R Dashboard Demo</div>", unsafe_allow_html=True)
st.sidebar.markdown("Discover emerging artists with data-driven insights")

# Sidebar navigation
st.sidebar.markdown("<div class='sub-header'>Navigation</div>", unsafe_allow_html=True)
page = st.sidebar.radio("", ["Spotify Emerging Artists", "Emerging Artists", "Artist Search", "About"], key="navigation")

# Sidebar filters
st.sidebar.markdown("---")
st.sidebar.markdown("<div class='sub-header'>Filters</div>", unsafe_allow_html=True)
days_filter = st.sidebar.slider("Analysis Period (Days)", min_value=7, max_value=90, value=30, step=1)
limit_filter = st.sidebar.slider("Number of Artists", min_value=5, max_value=20, value=10, step=1)

# Main content
if page == "Emerging Artists":
    st.markdown("<div class='main-header'>Top Emerging Artists</div>", unsafe_allow_html=True)
    st.markdown("These artists are showing significant momentum based on streaming growth, social engagement, and playlist additions.")
    
    # Add a refresh button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Refresh Data", help="Generate new simulated data"):
            st.session_state.emerging_artists = simulate_artist_data(num_artists=limit_filter)
            st.experimental_rerun()
    
    # Get emerging artists from session state
    emerging_artists = st.session_state.emerging_artists[:limit_filter]
    
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
                    st.session_state[f"show_details_{i}"] = True

                # If details should be shown for this artist
                if st.session_state.get(f"show_details_{i}", False):
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
                        if st.button("More Analysis", key=f"more_analysis_{artist_name.replace(' ', '_')}_{i}"):
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
                                    streaming_data = []
                                    base_streams = popularity * 100  # Base streams based on popularity
                                    growth_factor = 1 + (momentum / 10)  # Growth based on momentum
                                    
                                    for j in range(30):
                                        date = (datetime.now() - timedelta(days=30-j)).strftime('%Y-%m-%d')
                                        # Add some randomness but ensure overall growth trend
                                        daily_fluctuation = random.uniform(0.8, 1.2)
                                        growth_trend = (1 + (j/30) * (growth_factor-1))
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
                                    social_data = []
                                    base_likes = popularity * 20  # Base likes based on popularity
                                    base_shares = popularity * 5  # Base shares
                                    base_comments = popularity * 10  # Base comments
                                    growth_factor = 1 + (momentum / 5)  # Growth based on momentum
                                    
                                    for j in range(30):
                                        date = (datetime.now() - timedelta(days=30-j)).strftime('%Y-%m-%d')
                                        # Add some randomness but ensure overall growth trend
                                        daily_fluctuation = random.uniform(0.8, 1.2)
                                        growth_trend = (1 + (j/30) * (growth_factor-1))
                                        
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

elif page == "Spotify Emerging Artists":
    st.markdown("<div class='main-header'>Emerging Artists Demo</div>", unsafe_allow_html=True)
    st.markdown("[Combination of real and simulated data, intended to show features] These artists are showing significant momentum based on Spotify data combined with simulated metrics for a complete view.")
    
    # Add a refresh button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Refresh Data", help="Generate new simulated data", key="refresh_spotify"):
            st.session_state.emerging_artists = simulate_artist_data(num_artists=limit_filter)
            st.experimental_rerun()
    
    # Get emerging artists from session state
    emerging_artists = st.session_state.emerging_artists[:limit_filter]
    
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
                if st.button(f"View Details", key=f"view_spotify_{i}"):
                    st.session_state[f"show_details_spotify_{i}"] = True

                # If details should be shown for this artist
                if st.session_state.get(f"show_details_spotify_{i}", False):
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
                        if st.button("More Analysis", key=f"more_analysis_spotify_{artist_name.replace(' ', '_')}_{i}"):
                            st.session_state[f"show_analysis_spotify_{i}"] = True
                        
                        # Show detailed analysis if button was clicked
                        if st.session_state.get(f"show_analysis_spotify_{i}", False):
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
                                    streaming_data = []
                                    base_streams = popularity * 100  # Base streams based on popularity
                                    growth_factor = 1 + (momentum / 10)  # Growth based on momentum
                                    
                                    for j in range(30):
                                        date = (datetime.now() - timedelta(days=30-j)).strftime('%Y-%m-%d')
                                        # Add some randomness but ensure overall growth trend
                                        daily_fluctuation = random.uniform(0.8, 1.2)
                                        growth_trend = (1 + (j/30) * (growth_factor-1))
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
                                    social_data = []
                                    base_likes = popularity * 20  # Base likes based on popularity
                                    base_shares = popularity * 5  # Base shares
                                    base_comments = popularity * 10  # Base comments
                                    growth_factor = 1 + (momentum / 5)  # Growth based on momentum
                                    
                                    for j in range(30):
                                        date = (datetime.now() - timedelta(days=30-j)).strftime('%Y-%m-%d')
                                        # Add some randomness but ensure overall growth trend
                                        daily_fluctuation = random.uniform(0.8, 1.2)
                                        growth_trend = (1 + (j/30) * (growth_factor-1))
                                        
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
                            if st.button("Hide Analysis", key=f"hide_analysis_spotify_{artist_name.replace(' ', '_')}_{i}"):
                                st.session_state[f"show_analysis_spotify_{i}"] = False
                                st.experimental_rerun()
                        
                        # Close button
                        if st.button("Close", key=f"close_details_spotify_{i}"):
                            st.session_state[f"show_details_spotify_{i}"] = False
                            st.experimental_rerun()

elif page == "Artist Search":
    st.markdown("<div class='main-header'>Artist Search</div>", unsafe_allow_html=True)
    st.markdown("Search for specific artists to analyze their momentum and potential.")
    
    # Search box
    search_query = st.text_input("Search for an artist", "")
    
    if search_query:
        # Filter artists by name (case-insensitive)
        search_results = [
            artist for artist in st.session_state.emerging_artists 
            if search_query.lower() in artist['artist']['name'].lower()
        ]
        
        if not search_results:
            st.warning(f"No artists found for '{search_query}'. Please try a different search term.")
        else:
            st.markdown(f"<div class='sub-header'>Search Results for '{search_query}'</div>", unsafe_allow_html=True)
            
            # Display search results
            for i, artist in enumerate(search_results):
                st.markdown(f"""
                <div class='artist-card'>
                    <h3>{artist['artist']['name']}</h3>
                    <p><strong>Genres:</strong> {', '.join(artist['artist']['genres']) if artist['artist']['genres'] else 'N/A'}</p>
                    <p><strong>Followers:</strong> {artist['artist']['followers']:,}</p>
                    <p><strong>Popularity:</strong> {artist['artist']['popularity']}/100</p>
                    <p><strong>Momentum Score:</strong> {artist['momentum_score']:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # View details button
                if st.button(f"View Details", key=f"view_search_{i}"):
                    st.session_state[f"show_details_search_{i}"] = True

                # If details should be shown for this artist
                if st.session_state.get(f"show_details_search_{i}", False):
                    with st.expander(f"Details for {artist['artist']['name']}", expanded=True):
                        # Artist info
                        st.subheader(artist['artist']['name'])
                        st.write(f"**Genres:** {', '.join(artist['artist']['genres']) if artist['artist']['genres'] else 'N/A'}")
                        st.write(f"**Popularity:** {artist['artist']['popularity']}/100")
                        st.write(f"**Followers:** {artist['artist']['followers']:,}")
                        
                        # Momentum metrics
                        st.write("**Momentum Metrics:**")
                        st.write(f"- **Momentum Score:** {artist['momentum_score']:.2f}")
                        st.write(f"- **Streaming Growth:** {artist.get('streaming_growth', 0)*100:.1f}%")
                        st.write(f"- **Social Growth:** {artist.get('social_growth', 0)*100:.1f}%")
                        st.write(f"- **Viral Score:** {artist.get('viral_score', 0)*100:.1f}%")
                        
                        # Close button
                        if st.button("Close", key=f"close_search_{i}"):
                            st.session_state[f"show_details_search_{i}"] = False
                            st.experimental_rerun()

else:  # About page
    st.markdown("<div class='main-header'>About the Tool</div>", unsafe_allow_html=True)
    
    st.markdown("""
    ## Emerging Artist Discovery Tool
    
    This tool helps A&R teams discover and evaluate emerging music artists showing early signs of breakout success.
    
    ### Key Features
    
    - **Data-Driven Discovery**: Identify emerging artists based on streaming growth, social engagement, and playlist additions
    - **Comprehensive Analysis**: Evaluate artists across multiple metrics and platforms
    - **Actionable Insights**: Understand why an artist is trending and their growth potential
    
    ### How It Works
    
    1. **Data Collection**: We gather data from Spotify and social platforms
    2. **Momentum Scoring**: Our algorithm calculates a momentum score based on multiple weighted factors
    3. **Ranking & Insights**: Artists are ranked by momentum score and provided with insights about their growth
    
    ### Data Sources
    
    - **Spotify API**: Streaming data, playlist additions, and artist information
    - **Social Media Data**: Social engagement metrics
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #666666; font-size: 0.8rem;'>© 2025 Kirtii Vundavilli for Concord Music Group</p>", unsafe_allow_html=True) 
