import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import json
from datetime import datetime, timedelta
import random
from app.utils.logger import logger

# Set up Spotify client
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

def get_spotify_client():
    """Get authenticated Spotify client"""
    try:
        # Check if credentials are valid (not placeholders)
        if not client_id or not client_secret or client_id == "your_spotify_client_id" or client_secret == "your_spotify_client_secret":
            logger.warning("Spotify credentials not set or using placeholder values. Using simulated data only.")
            return None
            
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    except Exception as e:
        logger.error(f"Error connecting to Spotify API: {e}")
        return None

def get_artist_data(artist_name):
    """Get artist data from Spotify API"""
    logger.info(f"Fetching data for artist: {artist_name}")
    
    sp = get_spotify_client()
    if not sp:
        logger.warning("Spotify client not available, using simulated data")
        # Return simulated data
        return simulate_artist_data(artist_name)
    
    try:
        # Search for the artist
        logger.debug(f"Searching for artist: {artist_name}")
        results = sp.search(q=f'artist:{artist_name}', type='artist', limit=1)
        if not results['artists']['items']:
            logger.warning(f"No results found for artist: {artist_name}")
            return simulate_artist_data(artist_name)
        
        artist = results['artists']['items'][0]
        logger.info(f"Found artist: {artist['name']} (id: {artist['id']})")
        
        # Get artist's top tracks
        logger.debug(f"Fetching top tracks for artist: {artist['name']}")
        top_tracks = sp.artist_top_tracks(artist['id'])
        
        # Get playlists featuring the artist
        logger.debug(f"Fetching playlists featuring artist: {artist['name']}")
        playlists_results = sp.search(q=artist_name, type='playlist', limit=10)
        playlists = playlists_results['playlists']['items']
        
        # Format the data to match our existing structure
        formatted_artist = {
            'id': artist['id'],
            'name': artist['name'],
            'popularity': artist['popularity'],
            'followers': artist['followers']['total'],
            'genres': artist['genres'],
            'image_url': artist['images'][0]['url'] if artist['images'] else None
        }
        
        formatted_tracks = []
        for track in top_tracks['tracks']:
            formatted_tracks.append({
                'id': track['id'],
                'name': track['name'],
                'popularity': track['popularity'],
                'album': track['album']['name'],
                'release_date': track['album']['release_date'],
                'preview_url': track['preview_url']
            })
        
        formatted_playlists = []
        for playlist in playlists:
            formatted_playlists.append({
                'id': playlist['id'],
                'name': playlist['name'],
                'owner': playlist['owner']['display_name'],
                'tracks_total': playlist['tracks']['total'],
                'image_url': playlist['images'][0]['url'] if playlist['images'] else None
            })
        
        logger.info(f"Successfully fetched data for artist: {artist['name']}")
        return {
            'artist': formatted_artist,
            'tracks': formatted_tracks,
            'playlists': formatted_playlists
        }
    
    except Exception as e:
        logger.error(f"Error fetching artist data: {e}")
        return simulate_artist_data(artist_name)

def simulate_artist_data(artist_name):
    """Simulate artist data when Spotify API is not available"""
    logger.info(f"Simulating data for artist: {artist_name}")
    
    # Generate a random popularity score
    popularity = random.randint(50, 90)
    
    # Simulate artist data
    artist = {
        'id': f"sim_{artist_name.replace(' ', '').lower()}",
        'name': artist_name,
        'popularity': popularity,
        'followers': random.randint(10000, 1000000),
        'genres': random.sample(['pop', 'rock', 'hip hop', 'r&b', 'electronic', 'indie'], k=random.randint(1, 3)),
        'image_url': None
    }
    
    # Simulate tracks
    tracks = []
    for i in range(5):
        tracks.append({
            'id': f"sim_track_{i}",
            'name': f"Simulated Track {i+1}",
            'popularity': random.randint(50, 90),
            'album': f"Simulated Album {i//2 + 1}",
            'release_date': f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            'preview_url': None
        })
    
    # Simulate playlists
    playlists = []
    for i in range(3):
        playlists.append({
            'id': f"sim_playlist_{i}",
            'name': f"Simulated Playlist {i+1}",
            'owner': f"Simulated User {i+1}",
            'tracks_total': random.randint(20, 100),
            'image_url': None
        })
    
    return {
        'artist': artist,
        'tracks': tracks,
        'playlists': playlists
    }

def simulate_streaming_history(popularity, days=30):
    """Simulate streaming history based on artist popularity"""
    history = []
    base_streams = popularity * 100  # Higher popularity = more streams
    
    for i in range(days):
        date = (datetime.now() - timedelta(days=days-i)).strftime("%Y-%m-%d")
        
        # Add some randomness but maintain a trend based on popularity
        daily_variance = random.uniform(0.7, 1.3)
        # Add a slight upward trend for more popular artists
        trend_factor = 1 + (0.01 * i * (popularity / 100))
        
        streams = int(base_streams * daily_variance * trend_factor)
        history.append({
            'date': date,
            'streams': streams
        })
    
    return history

def simulate_social_engagement(popularity, days=30):
    """Simulate social media engagement based on artist popularity"""
    engagement = []
    
    # Base metrics scaled by popularity
    base_likes = popularity * 10
    base_shares = popularity * 1.5
    base_comments = popularity * 1
    base_views = popularity * 100
    base_mentions = popularity * 0.5
    
    for i in range(days):
        date = (datetime.now() - timedelta(days=days-i)).strftime("%Y-%m-%d")
        
        # Regular engagement with random variance
        variance = random.uniform(0.8, 1.2)
        
        # Simulate a viral spike in the last week for some artists
        viral_factor = 1.0
        if i >= days - 7 and popularity > 50 and random.random() > 0.7:
            viral_factor = random.uniform(2.5, 5.0)
        
        likes = int(base_likes * variance * viral_factor)
        shares = int(base_shares * variance * viral_factor)
        comments = int(base_comments * variance * viral_factor)
        views = int(base_views * variance * viral_factor)
        mentions = int(base_mentions * variance * viral_factor)
        
        # Calculate engagement ratio
        engagement_ratio = round((likes + shares + comments) / views, 4) if views > 0 else 0
        
        engagement.append({
            'date': date,
            'likes': likes,
            'shares': shares,
            'comments': comments,
            'views': views,
            'mentions': mentions,
            'engagement_ratio': engagement_ratio
        })
    
    return engagement

def simulate_trending_hashtags(artist_name, popularity):
    """Simulate trending hashtags based on artist name and popularity"""
    hashtags = []
    
    # Create artist-specific hashtags
    artist_words = artist_name.split()
    
    # Common hashtag patterns
    patterns = [
        f"#{artist_name.replace(' ', '')}",
        f"#{artist_name.replace(' ', '')}Music",
        f"#{artist_name.replace(' ', '')}Fan",
        f"#{artist_name.replace(' ', '')}Live",
        f"#{artist_name.replace(' ', '')}Trend"
    ]
    
    # Add more specific hashtags if artist name has multiple words
    if len(artist_words) > 1:
        for word in artist_words:
            if len(word) > 3:  # Only use meaningful words
                patterns.append(f"#{word}{artist_words[0]}")
    
    # Generate hashtag data
    for i, hashtag in enumerate(patterns):
        # More popular artists have more posts
        post_count = int(popularity * 10000 * random.uniform(0.5, 1.5))
        
        # First few hashtags are more likely to be trending
        is_trending = (i < 4 and popularity > 40) or (random.random() > 0.8 and popularity > 60)
        
        hashtags.append({
            'hashtag': hashtag,
            'post_count': post_count,
            'is_trending': is_trending
        })
    
    return hashtags

def simulate_viral_content(artist_name, popularity):
    """Simulate viral content based on artist popularity"""
    if popularity < 40:
        # Less popular artists less likely to have viral content
        if random.random() > 0.7:  # 30% chance
            return []
    
    # Number of viral content pieces based on popularity
    count = min(3, max(1, int(popularity / 30)))
    
    content_types = ["fan edit", "reaction", "lip sync", "cover", "dance challenge"]
    
    viral_content = []
    for i in range(count):
        content_type = random.choice(content_types)
        
        # More popular artists get more engagement
        base_engagement = popularity * 10000
        variance = random.uniform(0.5, 2.0)
        
        likes = int(base_engagement * variance * random.uniform(0.8, 1.2))
        shares = int(likes * random.uniform(0.1, 0.3))
        comments = int(likes * random.uniform(0.05, 0.15))
        views = int(likes * random.uniform(3, 8))
        
        # Date within last 30 days
        days_ago = random.randint(1, 30)
        created_at = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        viral_content.append({
            "id": f"sim_content_{i}",
            "content_type": content_type,
            "title": f"{artist_name} {content_type} - viral TikTok #{i+1}",
            "creator": f"Simulated Creator {i}",
            "likes": likes,
            "shares": shares,
            "comments": comments,
            "views": views,
            "created_at": created_at
        })
    
    # Sort by engagement (likes + shares + comments)
    viral_content.sort(key=lambda x: x['likes'] + x['shares'] + x['comments'], reverse=True)
    
    return viral_content

def calculate_metrics(spotify_data):
    """Calculate metrics based on Spotify data and simulated data"""
    artist = spotify_data['artist']
    popularity = artist['popularity']
    
    # Simulate streaming history
    streaming_history = simulate_streaming_history(popularity)
    
    # Calculate streaming growth (last 7 days vs previous 7 days)
    recent_streams = sum(day['streams'] for day in streaming_history[-7:])
    previous_streams = sum(day['streams'] for day in streaming_history[-14:-7])
    streaming_growth = (recent_streams - previous_streams) / previous_streams if previous_streams > 0 else 0
    
    # Simulate social engagement
    tiktok_engagement = simulate_social_engagement(popularity)
    
    # Calculate social growth (last 7 days vs previous 7 days)
    recent_engagement = sum(day['likes'] + day['shares'] + day['comments'] for day in tiktok_engagement[-7:])
    previous_engagement = sum(day['likes'] + day['shares'] + day['comments'] for day in tiktok_engagement[-14:-7])
    social_growth = (recent_engagement - previous_engagement) / previous_engagement if previous_engagement > 0 else 0
    
    # Calculate playlist score (0-1 based on number of playlists)
    playlist_score = min(1.0, len(spotify_data['playlists']) / 10)
    
    # Simulate trending hashtags
    trending_hashtags = simulate_trending_hashtags(artist['name'], popularity)
    
    # Simulate viral content
    viral_content = simulate_viral_content(artist['name'], popularity)
    
    # Calculate viral score (0-1 based on viral content)
    viral_score = min(1.0, len(viral_content) / 3)
    
    # Calculate momentum score (weighted average of all factors)
    momentum_score = (
        streaming_growth * 0.3 +
        social_growth * 0.3 +
        playlist_score * 0.2 +
        viral_score * 0.2
    )
    
    # Ensure momentum score is positive for demo purposes
    momentum_score = max(0.5, momentum_score)
    
    # Generate insights
    insights = []
    if social_growth > 0:
        insights.append(f"{int(social_growth*100)}% increase in social engagement")
    if len(spotify_data['playlists']) > 0:
        insights.append(f"Added to {len(spotify_data['playlists'])} playlists")
    if viral_content:
        insights.append("Viral content with high engagement")
    
    return {
        'momentum_score': momentum_score,
        'streaming_growth': streaming_growth,
        'social_growth': social_growth,
        'playlist_score': playlist_score,
        'viral_score': viral_score,
        'insights': insights,
        'streaming_history': streaming_history,
        'tiktok_engagement': tiktok_engagement,
        'trending_hashtags': trending_hashtags,
        'viral_content': viral_content,
        'timestamp': datetime.now().isoformat()
    }

def get_complete_artist_data(artist_name):
    """Get complete artist data with real Spotify data and simulated metrics"""
    # Get real Spotify data
    spotify_data = get_artist_data(artist_name)
    if not spotify_data:
        return None
    
    # Calculate and simulate additional metrics
    metrics = calculate_metrics(spotify_data)
    
    # Combine all data
    complete_data = {
        'artist': spotify_data['artist'],
        'momentum_score': metrics['momentum_score'],
        'streaming_growth': metrics['streaming_growth'],
        'social_growth': metrics['social_growth'],
        'playlist_score': metrics['playlist_score'],
        'viral_score': metrics['viral_score'],
        'insights': metrics['insights'],
        'raw_data': {
            'artist': spotify_data['artist'],
            'tracks': spotify_data['tracks'],
            'playlists': spotify_data['playlists'],
            'streaming_history': metrics['streaming_history'],
            'tiktok_engagement': metrics['tiktok_engagement'],
            'trending_hashtags': metrics['trending_hashtags'],
            'viral_content': metrics['viral_content'],
            'timestamp': metrics['timestamp']
        }
    }
    
    return complete_data

def get_emerging_artists_from_spotify(limit=10):
    """Get real emerging artists from Spotify and enhance with simulated metrics"""
    logger.info(f"Fetching emerging artists from Spotify, limit: {limit}")
    
    sp = get_spotify_client()
    if not sp:
        logger.warning("Spotify client not available, using simulated data")
        return None
    
    try:
        # Use Spotify's browse API to get new releases
        logger.debug("Fetching new releases from Spotify")
        new_releases = sp.new_releases(limit=20)
        logger.debug(f"Found {len(new_releases['albums']['items'])} new releases")
        
        # Get artists from new releases
        artists_set = set()
        for album in new_releases['albums']['items']:
            for artist in album['artists']:
                artists_set.add(artist['id'])
        
        logger.debug(f"Found {len(artists_set)} unique artists from new releases")
        
        # Get full artist data for each artist
        artists_data = []
        for artist_id in list(artists_set)[:limit*2]:  # Get more than needed to filter
            try:
                logger.debug(f"Fetching artist data for ID: {artist_id}")
                artist = sp.artist(artist_id)
                
                # Filter for emerging artists (not too popular, not too unknown)
                if 30 <= artist['popularity'] <= 70:
                    logger.debug(f"Artist {artist['name']} has popularity {artist['popularity']}, fetching additional data")
                    # Get artist's top tracks
                    top_tracks = sp.artist_top_tracks(artist['id'])
                    
                    # Get playlists featuring the artist
                    playlists_results = sp.search(q=artist['name'], type='playlist', limit=5)
                    playlists = playlists_results['playlists']['items']
                    
                    # Format the data
                    formatted_artist = {
                        'id': artist['id'],
                        'name': artist['name'],
                        'popularity': artist['popularity'],
                        'followers': artist['followers']['total'],
                        'genres': artist['genres'],
                        'image_url': artist['images'][0]['url'] if artist['images'] else None
                    }
                    
                    formatted_tracks = []
                    for track in top_tracks['tracks']:
                        formatted_tracks.append({
                            'id': track['id'],
                            'name': track['name'],
                            'popularity': track['popularity'],
                            'album': track['album']['name'],
                            'release_date': track['album']['release_date'],
                            'preview_url': track['preview_url']
                        })
                    
                    formatted_playlists = []
                    for playlist in playlists:
                        formatted_playlists.append({
                            'id': playlist['id'],
                            'name': playlist['name'],
                            'owner': playlist['owner']['display_name'],
                            'tracks_total': playlist['tracks']['total'],
                            'image_url': playlist['images'][0]['url'] if playlist['images'] else None
                        })
                    
                    # Create Spotify data structure
                    spotify_data = {
                        'artist': formatted_artist,
                        'tracks': formatted_tracks,
                        'playlists': formatted_playlists
                    }
                    
                    # Calculate and simulate additional metrics
                    logger.debug(f"Calculating metrics for artist {artist['name']}")
                    metrics = calculate_metrics(spotify_data)
                    
                    # Combine all data
                    complete_data = {
                        'artist': spotify_data['artist'],
                        'momentum_score': metrics['momentum_score'],
                        'streaming_growth': metrics['streaming_growth'],
                        'social_growth': metrics['social_growth'],
                        'playlist_score': metrics['playlist_score'],
                        'viral_score': metrics['viral_score'],
                        'insights': metrics['insights'],
                        'raw_data': {
                            'artist': spotify_data['artist'],
                            'tracks': spotify_data['tracks'],
                            'playlists': spotify_data['playlists'],
                            'streaming_history': metrics['streaming_history'],
                            'tiktok_engagement': metrics['tiktok_engagement'],
                            'trending_hashtags': metrics['trending_hashtags'],
                            'viral_content': metrics['viral_content'],
                            'timestamp': metrics['timestamp']
                        }
                    }
                    
                    artists_data.append(complete_data)
                    logger.debug(f"Added artist {artist['name']} to results")
                    
                    # If we have enough artists, stop
                    if len(artists_data) >= limit:
                        break
                else:
                    logger.debug(f"Skipping artist {artist['name']} with popularity {artist['popularity']}")
            except Exception as e:
                logger.error(f"Error processing artist {artist_id}: {e}")
                continue
        
        # If we don't have enough artists, try to get more from related artists
        if len(artists_data) < limit:
            logger.debug(f"Only found {len(artists_data)} artists, trying to get more from related artists")
            # Get related artists for the ones we already have
            related_artist_ids = set()
            for artist_data in artists_data:
                try:
                    related = sp.artist_related_artists(artist_data['artist']['id'])
                    for related_artist in related['artists']:
                        related_artist_ids.add(related_artist['id'])
                except Exception as e:
                    logger.error(f"Error getting related artists: {e}")
                    continue
            
            logger.debug(f"Found {len(related_artist_ids)} related artists")
            
            # Process related artists
            for artist_id in related_artist_ids:
                if len(artists_data) >= limit:
                    break
                    
                try:
                    logger.debug(f"Fetching related artist data for ID: {artist_id}")
                    artist = sp.artist(artist_id)
                    
                    # Filter for emerging artists
                    if 30 <= artist['popularity'] <= 70:
                        logger.debug(f"Related artist {artist['name']} has popularity {artist['popularity']}, fetching additional data")
                        # Get artist's top tracks
                        top_tracks = sp.artist_top_tracks(artist['id'])
                        
                        # Get playlists featuring the artist
                        playlists_results = sp.search(q=artist['name'], type='playlist', limit=5)
                        playlists = playlists_results['playlists']['items']
                        
                        # Format the data
                        formatted_artist = {
                            'id': artist['id'],
                            'name': artist['name'],
                            'popularity': artist['popularity'],
                            'followers': artist['followers']['total'],
                            'genres': artist['genres'],
                            'image_url': artist['images'][0]['url'] if artist['images'] else None
                        }
                        
                        formatted_tracks = []
                        for track in top_tracks['tracks']:
                            formatted_tracks.append({
                                'id': track['id'],
                                'name': track['name'],
                                'popularity': track['popularity'],
                                'album': track['album']['name'],
                                'release_date': track['album']['release_date'],
                                'preview_url': track['preview_url']
                            })
                        
                        formatted_playlists = []
                        for playlist in playlists:
                            formatted_playlists.append({
                                'id': playlist['id'],
                                'name': playlist['name'],
                                'owner': playlist['owner']['display_name'],
                                'tracks_total': playlist['tracks']['total'],
                                'image_url': playlist['images'][0]['url'] if playlist['images'] else None
                            })
                        
                        # Create Spotify data structure
                        spotify_data = {
                            'artist': formatted_artist,
                            'tracks': formatted_tracks,
                            'playlists': formatted_playlists
                        }
                        
                        # Calculate and simulate additional metrics
                        logger.debug(f"Calculating metrics for related artist {artist['name']}")
                        metrics = calculate_metrics(spotify_data)
                        
                        # Combine all data
                        complete_data = {
                            'artist': spotify_data['artist'],
                            'momentum_score': metrics['momentum_score'],
                            'streaming_growth': metrics['streaming_growth'],
                            'social_growth': metrics['social_growth'],
                            'playlist_score': metrics['playlist_score'],
                            'viral_score': metrics['viral_score'],
                            'insights': metrics['insights'],
                            'raw_data': {
                                'artist': spotify_data['artist'],
                                'tracks': spotify_data['tracks'],
                                'playlists': spotify_data['playlists'],
                                'streaming_history': metrics['streaming_history'],
                                'tiktok_engagement': metrics['tiktok_engagement'],
                                'trending_hashtags': metrics['trending_hashtags'],
                                'viral_content': metrics['viral_content'],
                                'timestamp': metrics['timestamp']
                            }
                        }
                        
                        artists_data.append(complete_data)
                        logger.debug(f"Added related artist {artist['name']} to results")
                    else:
                        logger.debug(f"Skipping related artist {artist['name']} with popularity {artist['popularity']}")
                except Exception as e:
                    logger.error(f"Error processing related artist {artist_id}: {e}")
                    continue
        
        # Sort by momentum score
        artists_data.sort(key=lambda x: x['momentum_score'], reverse=True)
        
        # Limit to requested number
        artists_data = artists_data[:limit]
        
        logger.info(f"Successfully fetched {len(artists_data)} emerging artists from Spotify")
        return artists_data
    
    except Exception as e:
        logger.error(f"Error fetching emerging artists from Spotify: {e}")
        return None

def get_simple_spotify_artists(limit=10):
    """Get real artists from Spotify with minimal processing"""
    logger.info(f"Fetching simple artists from Spotify, limit: {limit}")
    
    sp = get_spotify_client()
    if not sp:
        logger.warning("Spotify client not available, using simulated data")
        return None
    
    try:
        # Use Spotify's browse API to get new releases
        logger.debug("Fetching new releases from Spotify")
        new_releases = sp.new_releases(limit=20)
        logger.debug(f"Found {len(new_releases['albums']['items'])} new releases")
        
        # Get artists from new releases
        artists_set = set()
        for album in new_releases['albums']['items']:
            for artist in album['artists']:
                artists_set.add(artist['id'])
        
        logger.debug(f"Found {len(artists_set)} unique artists from new releases")
        
        # Get full artist data for each artist
        artists_data = []
        for artist_id in list(artists_set)[:limit*2]:  # Get more than needed to filter
            try:
                logger.debug(f"Fetching artist data for ID: {artist_id}")
                artist = sp.artist(artist_id)
                
                # Get artist's top tracks
                top_tracks = sp.artist_top_tracks(artist['id'])
                
                # Format the data
                formatted_artist = {
                    'id': artist['id'],
                    'name': artist['name'],
                    'popularity': artist['popularity'],
                    'followers': artist['followers']['total'],
                    'genres': artist['genres'],
                    'image_url': artist['images'][0]['url'] if artist['images'] else None
                }
                
                formatted_tracks = []
                for track in top_tracks['tracks'][:5]:  # Limit to 5 tracks
                    formatted_tracks.append({
                        'id': track['id'],
                        'name': track['name'],
                        'popularity': track['popularity'],
                        'album': track['album']['name'],
                        'release_date': track['album']['release_date'],
                        'preview_url': track['preview_url']
                    })
                
                # Create Spotify data structure
                spotify_data = {
                    'artist': formatted_artist,
                    'tracks': formatted_tracks,
                    'playlists': []
                }
                
                # Calculate and simulate additional metrics
                logger.debug(f"Calculating metrics for artist {artist['name']}")
                metrics = calculate_metrics(spotify_data)
                
                # Combine all data
                complete_data = {
                    'artist': spotify_data['artist'],
                    'momentum_score': metrics['momentum_score'],
                    'streaming_growth': metrics['streaming_growth'],
                    'social_growth': metrics['social_growth'],
                    'playlist_score': metrics['playlist_score'],
                    'viral_score': metrics['viral_score'],
                    'insights': metrics['insights'],
                    'raw_data': {
                        'artist': spotify_data['artist'],
                        'tracks': spotify_data['tracks'],
                        'playlists': spotify_data['playlists'],
                        'streaming_history': metrics['streaming_history'],
                        'tiktok_engagement': metrics['tiktok_engagement'],
                        'trending_hashtags': metrics['trending_hashtags'],
                        'viral_content': metrics['viral_content'],
                        'timestamp': metrics['timestamp']
                    }
                }
                
                artists_data.append(complete_data)
                logger.debug(f"Added artist {artist['name']} to results")
                
                # If we have enough artists, stop
                if len(artists_data) >= limit:
                    break
            except Exception as e:
                logger.error(f"Error processing artist {artist_id}: {e}")
                continue
        
        # Sort by momentum score
        artists_data.sort(key=lambda x: x['momentum_score'], reverse=True)
        
        # Limit to requested number
        artists_data = artists_data[:limit]
        
        logger.info(f"Successfully fetched {len(artists_data)} artists from Spotify")
        return artists_data
    
    except Exception as e:
        logger.error(f"Error fetching artists from Spotify: {e}")
        return None 