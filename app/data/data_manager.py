import os
import json
from datetime import datetime
import random

from app.data.spotify_collector import get_artist_data, get_complete_artist_data
from app.utils.logger import logger
from app.utils.config import CACHE_DIR

class DataManager:
    """Class to manage data collection and caching"""
    
    def __init__(self):
        """Initialize data manager"""
        # Create cache directory if it doesn't exist
        os.makedirs(CACHE_DIR, exist_ok=True)
        logger.info(f"Data manager initialized with cache directory: {CACHE_DIR}")
    
    def get_emerging_artists(self, limit=10, days=30):
        """
        Get a list of emerging artists based on momentum score
        """
        # For demo purposes, we'll use a predefined list of artists
        demo_artists = [
            "Taylor Swift",
            "Drake",
            "Billie Eilish",
            "The Weeknd",
            "Dua Lipa",
            "Post Malone",
            "Ariana Grande",
            "Bad Bunny",
            "Justin Bieber",
            "BTS"
        ]
        
        # Shuffle the list to get different results each time
        random.shuffle(demo_artists)
        
        # Get data for each artist
        artists_data = []
        for artist_name in demo_artists[:limit]:
            # Check if we have cached data
            cache_file = os.path.join(CACHE_DIR, f"{artist_name.replace(' ', '_')}.json")
            
            if os.path.exists(cache_file):
                # Use cached data
                with open(cache_file, 'r') as f:
                    artist_data = json.load(f)
                logger.info(f"Using cached data for {artist_name}")
            else:
                # Get fresh data
                artist_data = get_complete_artist_data(artist_name)
                if artist_data:
                    # Cache the data
                    with open(cache_file, 'w') as f:
                        json.dump(artist_data, f)
                    logger.info(f"Cached data for {artist_name}")
                else:
                    logger.warning(f"Failed to get data for {artist_name}")
                    continue
            
            artists_data.append(artist_data)
        
        # Sort by momentum score
        artists_data.sort(key=lambda x: x['momentum_score'], reverse=True)
        
        return artists_data
    
    def get_artist_data(self, artist_name, days=30, force_refresh=False):
        """
        Get detailed information about a specific artist
        """
        # Check if we have cached data and not forcing refresh
        cache_file = os.path.join(CACHE_DIR, f"{artist_name.replace(' ', '_')}.json")
        
        if os.path.exists(cache_file) and not force_refresh:
            # Use cached data
            with open(cache_file, 'r') as f:
                artist_data = json.load(f)
            logger.info(f"Using cached data for {artist_name}")
            return artist_data
        
        # Get fresh data
        artist_data = get_complete_artist_data(artist_name)
        if artist_data:
            # Cache the data
            with open(cache_file, 'w') as f:
                json.dump(artist_data, f)
            logger.info(f"Cached data for {artist_name}")
            return artist_data
        
        logger.warning(f"Failed to get data for {artist_name}")
        return None 