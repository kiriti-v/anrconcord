from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import os
import json
from datetime import datetime, timedelta
import random

from app.data.spotify_collector import get_complete_artist_data, get_spotify_client, get_emerging_artists_from_spotify, get_simple_spotify_artists
from app.utils.logger import logger
from app.utils.config import CACHE_DIR

router = APIRouter()

# Create cache directory if it doesn't exist
os.makedirs(CACHE_DIR, exist_ok=True)

@router.get("/emerging")
async def get_emerging_artists(limit: int = 10, days: int = 30):
    """
    Get a list of emerging artists based on momentum score
    """
    try:
        # Use these seed genres to find emerging artists
        seed_genres = [
            "indie", "alt-pop", "bedroom pop", "indie pop", "indie rock",
            "underground hip hop", "lo-fi", "future bass", "experimental",
            "alternative r&b", "electropop", "new wave", "indie folk"
        ]
        
        # Shuffle the genres to get different results each time
        random.shuffle(seed_genres)
        
        # Get data for emerging artists
        artists_data = []
        
        # Generate simulated emerging artists for each genre
        for i, genre in enumerate(seed_genres[:limit]):
            # Create a simulated emerging artist for this genre
            artist_data = create_emerging_artist_for_genre(genre, i)
            artists_data.append(artist_data)
            
            # Stop if we have enough artists
            if len(artists_data) >= limit:
                break
        
        # Sort by momentum score and limit to requested number
        artists_data.sort(key=lambda x: x['momentum_score'], reverse=True)
        artists_data = artists_data[:limit]
        
        return {"artists": artists_data}
    
    except Exception as e:
        logger.error(f"Error getting emerging artists: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/emerging-new")
async def get_new_emerging_artists(limit: int = 10, days: int = 30):
    """
    Get a list of newly generated emerging artists based on momentum score
    """
    try:
        # Use these seed genres to find emerging artists
        seed_genres = [
            "indie", "alt-pop", "bedroom pop", "indie pop", "indie rock",
            "underground hip hop", "lo-fi", "future bass", "experimental",
            "alternative r&b", "electropop", "new wave", "indie folk"
        ]
        
        # Shuffle the genres to get different results each time
        random.shuffle(seed_genres)
        
        # Get data for emerging artists
        artists_data = []
        
        # Generate simulated emerging artists for each genre
        for i, genre in enumerate(seed_genres[:limit]):
            # Create a somewhat realistic artist name based on genre
            name_prefixes = ["The", "Young", "Little", "Midnight", "Summer", "Winter", "Crystal", "Neon", "Electric", "Cosmic"]
            name_suffixes = ["Band", "Collective", "Project", "Sound", "Wave", "Echo", "Pulse", "Beat", "Vibe", "Groove"]
            
            if random.random() > 0.5:
                # Use format: "The Something"
                artist_name = f"{random.choice(name_prefixes)} {genre.title()}"
            else:
                # Use format: "Something Something"
                artist_name = f"{genre.title()} {random.choice(name_suffixes)}"
                
            # Add a random modifier to make names unique
            if random.random() > 0.7:
                artist_name = f"{artist_name} {chr(65 + i)}"
            
            logger.info(f"Generated artist name: {artist_name}")
            
            # Create a simulated emerging artist for this genre with the custom name
            artist_data = create_emerging_artist_for_genre(genre, i)
            
            # Update the artist name in both places
            artist_data['artist']['name'] = artist_name
            artist_data['raw_data']['artist']['name'] = artist_name
            
            # Update artist ID to match the name
            artist_id = f"sim_{artist_name.replace(' ', '').lower()}"
            artist_data['artist']['id'] = artist_id
            artist_data['raw_data']['artist']['id'] = artist_id
            
            # Update hashtags to use the new name
            for hashtag in artist_data['raw_data']['trending_hashtags']:
                if 'emerging-new' in hashtag['hashtag']:
                    hashtag['hashtag'] = hashtag['hashtag'].replace('emerging-new', artist_name.replace(' ', ''))
            
            # Update viral content titles to use the new name
            for content in artist_data['raw_data']['viral_content']:
                if 'emerging-new' in content['title']:
                    content['title'] = content['title'].replace('emerging-new', artist_name)
            
            logger.info(f"Final artist name: {artist_data['artist']['name']}")
            
            artists_data.append(artist_data)
            
            # Stop if we have enough artists
            if len(artists_data) >= limit:
                break
        
        # Sort by momentum score and limit to requested number
        artists_data.sort(key=lambda x: x['momentum_score'], reverse=True)
        artists_data = artists_data[:limit]
        
        return {"artists": artists_data}
    
    except Exception as e:
        logger.error(f"Error getting emerging artists: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/emerging-artists")
async def get_emerging_artists_new(limit: int = 10, days: int = 30):
    """
    Get a list of newly generated emerging artists based on momentum score
    """
    try:
        # Use these seed genres to find emerging artists
        seed_genres = [
            "indie", "alt-pop", "bedroom pop", "indie pop", "indie rock",
            "underground hip hop", "lo-fi", "future bass", "experimental",
            "alternative r&b", "electropop", "new wave", "indie folk"
        ]
        
        # Shuffle the genres to get different results each time
        random.shuffle(seed_genres)
        
        # Get data for emerging artists
        artists_data = []
        
        # Generate simulated emerging artists for each genre
        for i, genre in enumerate(seed_genres[:limit]):
            # Generate artist name based on genre
            name_prefixes = ["The", "Young", "Little", "Midnight", "Summer", "Winter", "Crystal", "Neon", "Electric", "Cosmic"]
            name_suffixes = ["Band", "Collective", "Project", "Sound", "Wave", "Echo", "Pulse", "Beat", "Vibe", "Groove"]
            
            # Create a somewhat realistic artist name based on genre
            if random.random() > 0.5:
                # Use format: "The Something"
                artist_name = f"{random.choice(name_prefixes)} {genre.title()}"
            else:
                # Use format: "Something Something"
                artist_name = f"{genre.title()} {random.choice(name_suffixes)}"
                
            # Add a random modifier to make names unique
            if random.random() > 0.7:
                artist_name = f"{artist_name} {chr(65 + i)}"
            
            # Create artist data structure
            artist_id = f"sim_{artist_name.replace(' ', '').lower()}"
            popularity = random.randint(30, 65)  # Lower popularity for emerging artists
            followers = random.randint(1000, 50000)  # Fewer followers
            
            # Create artist object
            artist = {
                'id': artist_id,
                'name': artist_name,
                'popularity': popularity,
                'followers': followers,
                'genres': [genre] + random.sample(['indie', 'alternative', 'pop', 'electronic'], k=random.randint(0, 2)),
                'image_url': None
            }
            
            # Create tracks
            tracks = []
            for j in range(5):
                tracks.append({
                    'id': f"{artist_id}_track_{j}",
                    'name': f"Track {j+1}",
                    'popularity': random.randint(30, 70),
                    'album': f"Album {j//2 + 1}",
                    'release_date': f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                    'preview_url': None
                })
            
            # Create playlists
            playlists = []
            for j in range(3):
                playlists.append({
                    'id': f"{artist_id}_playlist_{j}",
                    'name': f"Playlist {j+1}",
                    'owner': f"User {j+1}",
                    'tracks_total': random.randint(20, 100),
                    'image_url': None
                })
            
            # Simulate streaming history
            streaming_history = []
            base_streams = popularity * 100  # Higher popularity = more streams
            
            for j in range(days):
                date = (datetime.now() - timedelta(days=days-j)).strftime("%Y-%m-%d")
                
                # Add some randomness but maintain a trend based on popularity
                daily_variance = random.uniform(0.7, 1.3)
                # Add a slight upward trend for more popular artists
                trend_factor = 1 + (0.01 * j * (popularity / 100))
                
                streams = int(base_streams * daily_variance * trend_factor)
                streaming_history.append({
                    'date': date,
                    'streams': streams
                })
            
            # Simulate social engagement
            tiktok_engagement = []
            
            # Base metrics scaled by popularity
            base_likes = popularity * 10
            base_shares = popularity * 1.5
            base_comments = popularity * 1
            base_views = popularity * 100
            base_mentions = popularity * 0.5
            
            for j in range(days):
                date = (datetime.now() - timedelta(days=days-j)).strftime("%Y-%m-%d")
                
                # Regular engagement with random variance
                variance = random.uniform(0.8, 1.2)
                
                # Simulate a viral spike in the last week for some artists
                viral_factor = 1.0
                if j >= days - 7 and popularity > 50 and random.random() > 0.7:
                    viral_factor = random.uniform(2.5, 5.0)
                
                likes = int(base_likes * variance * viral_factor)
                shares = int(base_shares * variance * viral_factor)
                comments = int(base_comments * variance * viral_factor)
                views = int(base_views * variance * viral_factor)
                mentions = int(base_mentions * variance * viral_factor)
                
                # Calculate engagement ratio
                engagement_ratio = round((likes + shares + comments) / views, 4) if views > 0 else 0
                
                tiktok_engagement.append({
                    'date': date,
                    'likes': likes,
                    'shares': shares,
                    'comments': comments,
                    'views': views,
                    'mentions': mentions,
                    'engagement_ratio': engagement_ratio
                })
            
            # Simulate trending hashtags
            trending_hashtags = []
            
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
            for j, hashtag in enumerate(patterns):
                # More popular artists have more posts
                post_count = int(popularity * 1000 * random.uniform(0.5, 1.5))
                
                # First few hashtags are more likely to be trending
                is_trending = (j < 3 and popularity > 40) or (random.random() > 0.8 and popularity > 50)
                
                trending_hashtags.append({
                    'hashtag': hashtag,
                    'post_count': post_count,
                    'is_trending': is_trending
                })
            
            # Simulate viral content
            viral_content = []
            if popularity > 40:
                # Number of viral content pieces based on popularity
                count = min(2, max(1, int(popularity / 40)))
                
                content_types = ["fan edit", "reaction", "lip sync", "cover", "dance challenge"]
                
                for j in range(count):
                    content_type = random.choice(content_types)
                    
                    # More popular artists get more engagement
                    base_engagement = popularity * 1000
                    variance = random.uniform(0.5, 2.0)
                    
                    likes = int(base_engagement * variance * random.uniform(0.8, 1.2))
                    shares = int(likes * random.uniform(0.1, 0.3))
                    comments = int(likes * random.uniform(0.05, 0.15))
                    views = int(likes * random.uniform(3, 8))
                    
                    # Date within last 30 days
                    days_ago = random.randint(1, 30)
                    created_at = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
                    
                    viral_content.append({
                        "id": f"{artist_id}_content_{j}",
                        "content_type": content_type,
                        "title": f"{artist_name} {content_type} - viral TikTok #{j+1}",
                        "creator": f"Creator {j+1}",
                        "likes": likes,
                        "shares": shares,
                        "comments": comments,
                        "views": views,
                        "created_at": created_at
                    })
            
            # Calculate metrics
            # Calculate streaming growth (last 7 days vs previous 7 days)
            recent_streams = sum(day['streams'] for day in streaming_history[-7:])
            previous_streams = sum(day['streams'] for day in streaming_history[-14:-7])
            streaming_growth = (recent_streams - previous_streams) / previous_streams if previous_streams > 0 else 0
            
            # Calculate social growth (last 7 days vs previous 7 days)
            recent_engagement = sum(day['likes'] + day['shares'] + day['comments'] for day in tiktok_engagement[-7:])
            previous_engagement = sum(day['likes'] + day['shares'] + day['comments'] for day in tiktok_engagement[-14:-7])
            social_growth = (recent_engagement - previous_engagement) / previous_engagement if previous_engagement > 0 else 0
            
            # Calculate playlist score (0-1 based on number of playlists)
            playlist_score = min(1.0, len(playlists) / 10)
            
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
            if streaming_growth > 0.1:
                insights.append(f"{int(streaming_growth*100)}% increase in streaming")
            if social_growth > 0.2:
                insights.append(f"{int(social_growth*100)}% growth in social engagement")
            if random.random() > 0.5:
                insights.append("Featured in editorial playlists")
            if random.random() > 0.7:
                insights.append("Viral content on TikTok")
            if random.random() > 0.8:
                insights.append("Strong local fanbase")
            
            # Combine all data
            artist_data = {
                'artist': artist,
                'momentum_score': momentum_score,
                'streaming_growth': streaming_growth,
                'social_growth': social_growth,
                'playlist_score': playlist_score,
                'viral_score': viral_score,
                'insights': insights,
                'raw_data': {
                    'artist': artist,
                    'tracks': tracks,
                    'playlists': playlists,
                    'streaming_history': streaming_history,
                    'tiktok_engagement': tiktok_engagement,
                    'trending_hashtags': trending_hashtags,
                    'viral_content': viral_content,
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            artists_data.append(artist_data)
            
            # Stop if we have enough artists
            if len(artists_data) >= limit:
                break
        
        # Sort by momentum score and limit to requested number
        artists_data.sort(key=lambda x: x['momentum_score'], reverse=True)
        artists_data = artists_data[:limit]
        
        return {"artists": artists_data}
    
    except Exception as e:
        logger.error(f"Error getting emerging artists: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def create_emerging_artist_for_genre(genre, index):
    """Create a realistic emerging artist for a specific genre"""
    # Generate artist name based on genre
    name_prefixes = ["The", "Young", "Little", "Midnight", "Summer", "Winter", "Crystal", "Neon", "Electric", "Cosmic"]
    name_suffixes = ["Band", "Collective", "Project", "Sound", "Wave", "Echo", "Pulse", "Beat", "Vibe", "Groove"]
    
    # Create a somewhat realistic artist name based on genre
    if random.random() > 0.5:
        # Use format: "The Something"
        artist_name = f"{random.choice(name_prefixes)} {genre.title()}"
    else:
        # Use format: "Something Something"
        artist_name = f"{genre.title()} {random.choice(name_suffixes)}"
        
    # Add a random modifier to make names unique
    if random.random() > 0.7:
        artist_name = f"{artist_name} {chr(65 + index)}"
    
    # Create artist data structure
    artist_id = f"sim_{artist_name.replace(' ', '').lower()}"
    popularity = random.randint(30, 65)  # Lower popularity for emerging artists
    followers = random.randint(1000, 50000)  # Fewer followers
    
    # Create artist object
    artist = {
        'id': artist_id,
        'name': artist_name,
        'popularity': popularity,
        'followers': followers,
        'genres': [genre] + random.sample(['indie', 'alternative', 'pop', 'electronic'], k=random.randint(0, 2)),
        'image_url': None
    }
    
    # Create tracks
    tracks = []
    for i in range(5):
        tracks.append({
            'id': f"{artist_id}_track_{i}",
            'name': f"Track {i+1}",
            'popularity': random.randint(30, 70),
            'album': f"Album {i//2 + 1}",
            'release_date': f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            'preview_url': None
        })
    
    # Create playlists
    playlists = []
    for i in range(3):
        playlists.append({
            'id': f"{artist_id}_playlist_{i}",
            'name': f"Playlist {i+1}",
            'owner': f"User {i+1}",
            'tracks_total': random.randint(20, 100),
            'image_url': None
        })
    
    # Simulate streaming history
    streaming_history = []
    base_streams = popularity * 100  # Higher popularity = more streams
    
    for i in range(days):
        date = (datetime.now() - timedelta(days=days-i)).strftime("%Y-%m-%d")
        
        # Add some randomness but maintain a trend based on popularity
        daily_variance = random.uniform(0.7, 1.3)
        # Add a slight upward trend for more popular artists
        trend_factor = 1 + (0.01 * i * (popularity / 100))
        
        streams = int(base_streams * daily_variance * trend_factor)
        streaming_history.append({
            'date': date,
            'streams': streams
        })
    
    # Simulate social engagement
    tiktok_engagement = []
    
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
        
        tiktok_engagement.append({
            'date': date,
            'likes': likes,
            'shares': shares,
            'comments': comments,
            'views': views,
            'mentions': mentions,
            'engagement_ratio': engagement_ratio
        })
    
    # Simulate trending hashtags
    trending_hashtags = []
    
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
        post_count = int(popularity * 1000 * random.uniform(0.5, 1.5))
        
        # First few hashtags are more likely to be trending
        is_trending = (i < 3 and popularity > 40) or (random.random() > 0.8 and popularity > 50)
        
        trending_hashtags.append({
            'hashtag': hashtag,
            'post_count': post_count,
            'is_trending': is_trending
        })
    
    # Simulate viral content
    viral_content = []
    if popularity > 40:
        # Number of viral content pieces based on popularity
        count = min(2, max(1, int(popularity / 40)))
        
        content_types = ["fan edit", "reaction", "lip sync", "cover", "dance challenge"]
        
        for i in range(count):
            content_type = random.choice(content_types)
            
            # More popular artists get more engagement
            base_engagement = popularity * 1000
            variance = random.uniform(0.5, 2.0)
            
            likes = int(base_engagement * variance * random.uniform(0.8, 1.2))
            shares = int(likes * random.uniform(0.1, 0.3))
            comments = int(likes * random.uniform(0.05, 0.15))
            views = int(likes * random.uniform(3, 8))
            
            # Date within last 30 days
            days_ago = random.randint(1, 30)
            created_at = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            
            viral_content.append({
                "id": f"{artist_id}_content_{i}",
                "content_type": content_type,
                "title": f"{artist_name} {content_type} - viral TikTok #{i+1}",
                "creator": f"Creator {i+1}",
                "likes": likes,
                "shares": shares,
                "comments": comments,
                "views": views,
                "created_at": created_at
            })
    
    # Calculate metrics
    # Calculate streaming growth (last 7 days vs previous 7 days)
    recent_streams = sum(day['streams'] for day in streaming_history[-7:])
    previous_streams = sum(day['streams'] for day in streaming_history[-14:-7])
    streaming_growth = (recent_streams - previous_streams) / previous_streams if previous_streams > 0 else 0
    
    # Calculate social growth (last 7 days vs previous 7 days)
    recent_engagement = sum(day['likes'] + day['shares'] + day['comments'] for day in tiktok_engagement[-7:])
    previous_engagement = sum(day['likes'] + day['shares'] + day['comments'] for day in tiktok_engagement[-14:-7])
    social_growth = (recent_engagement - previous_engagement) / previous_engagement if previous_engagement > 0 else 0
    
    # Calculate playlist score (0-1 based on number of playlists)
    playlist_score = min(1.0, len(playlists) / 10)
    
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
    if streaming_growth > 0.1:
        insights.append(f"{int(streaming_growth*100)}% increase in streaming")
    if social_growth > 0.2:
        insights.append(f"{int(social_growth*100)}% growth in social engagement")
    if random.random() > 0.5:
        insights.append("Featured in editorial playlists")
    if random.random() > 0.7:
        insights.append("Viral content on TikTok")
    if random.random() > 0.8:
        insights.append("Strong local fanbase")
    
    # Combine all data
    return {
        'artist': artist,
        'momentum_score': momentum_score,
        'streaming_growth': streaming_growth,
        'social_growth': social_growth,
        'playlist_score': playlist_score,
        'viral_score': viral_score,
        'insights': insights,
        'raw_data': {
            'artist': artist,
            'tracks': tracks,
            'playlists': playlists,
            'streaming_history': streaming_history,
            'tiktok_engagement': tiktok_engagement,
            'trending_hashtags': trending_hashtags,
            'viral_content': viral_content,
            'timestamp': datetime.now().isoformat()
        }
    }

@router.get("/spotify-emerging")
async def get_spotify_emerging_artists(limit: int = 10, days: int = 30, force_refresh: bool = False):
    """
    Get a list of real emerging artists from Spotify API
    """
    try:
        # Check if we have cached data
        cache_file = os.path.join(CACHE_DIR, f"spotify_emerging_artists_{limit}.json")
        
        # If cache exists and is recent (less than 24 hours old) and not forcing refresh
        if os.path.exists(cache_file) and not force_refresh:
            file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(cache_file))
            if file_age < timedelta(hours=24):
                logger.info(f"Using cached Spotify emerging artists data from {cache_file}")
                with open(cache_file, 'r') as f:
                    return json.load(f)
        
        # Get real artists from Spotify using the simpler function
        logger.info("Fetching real artists from Spotify using simple function")
        artists_data = get_simple_spotify_artists(limit=limit)
        
        # If we couldn't get data from Spotify, fall back to simulated data
        if not artists_data:
            logger.warning("Could not get real artists from Spotify, falling back to simulated data")
            return await get_emerging_artists(limit=limit, days=days)
        
        # Cache the results
        with open(cache_file, 'w') as f:
            json.dump({"artists": artists_data}, f)
        
        return {"artists": artists_data}
    
    except Exception as e:
        logger.error(f"Error getting Spotify emerging artists: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
async def search_artists(query: str, limit: int = 10):
    """
    Search for artists by name
    """
    try:
        # Try to get real artist data from Spotify
        artist_data = get_complete_artist_data(query)
        
        # If we couldn't get data from Spotify, fall back to simulated data
        if not artist_data:
            logger.warning(f"Could not find artist '{query}' on Spotify, falling back to simulated data")
            # For testing, create a simulated emerging artist based on the query
            genre = query.lower()
            artist_data = create_emerging_artist_for_genre(genre, 0)
        
        return {"artists": [artist_data]}
    
    except Exception as e:
        logger.error(f"Error searching artists: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{artist_name}")
async def get_artist_details(artist_name: str):
    """
    Get detailed information about a specific artist
    """
    try:
        # Try to get real artist data from Spotify
        artist_data = get_complete_artist_data(artist_name)
        
        # If we couldn't get data from Spotify, fall back to simulated data
        if not artist_data:
            logger.warning(f"Could not find artist '{artist_name}' on Spotify, falling back to simulated data")
            # Create a simulated emerging artist based on the artist name
            genre = artist_name.split()[0].lower() if ' ' in artist_name else artist_name.lower()
            artist_data = create_emerging_artist_for_genre(genre, 0)
            artist_data['artist']['name'] = artist_name  # Use the exact name from the request
        
        return artist_data
    
    except Exception as e:
        logger.error(f"Error getting artist details: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 