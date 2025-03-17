import numpy as np
from app.utils.logger import logger
from app.utils.config import DEFAULT_WEIGHTS

class MomentumScorer:
    """Class to calculate momentum scores for artists"""
    
    def __init__(self, weights=None):
        """Initialize with custom weights or defaults"""
        self.weights = weights or DEFAULT_WEIGHTS
        logger.info(f"MomentumScorer initialized with weights: {self.weights}")
    
    def calculate_streaming_growth(self, streaming_history, window_days=7):
        """Calculate streaming growth over time"""
        if not streaming_history or len(streaming_history) < window_days * 2:
            return 0.0
        
        # Get first and last window
        first_window = streaming_history[:window_days]
        last_window = streaming_history[-window_days:]
        
        # Calculate average streams for each window
        first_avg = sum(day['streams'] for day in first_window) / window_days
        last_avg = sum(day['streams'] for day in last_window) / window_days
        
        # Calculate growth rate
        if first_avg > 0:
            growth_rate = (last_avg - first_avg) / first_avg
        else:
            growth_rate = 1.0 if last_avg > 0 else 0.0
        
        return growth_rate
    
    def calculate_social_growth(self, social_data, window_days=7):
        """Calculate social engagement growth over time"""
        if not social_data or len(social_data) < window_days * 2:
            return 0.0
        
        # Get first and last window
        first_window = social_data[:window_days]
        last_window = social_data[-window_days:]
        
        # Calculate average engagement for each window
        first_avg = sum(day['likes'] + day['shares'] + day['comments'] for day in first_window) / window_days
        last_avg = sum(day['likes'] + day['shares'] + day['comments'] for day in last_window) / window_days
        
        # Calculate growth rate
        if first_avg > 0:
            growth_rate = (last_avg - first_avg) / first_avg
        else:
            growth_rate = 1.0 if last_avg > 0 else 0.0
        
        return growth_rate
    
    def calculate_playlist_score(self, playlists):
        """Calculate score based on playlist additions"""
        if not playlists:
            return 0.0
        
        # Simple score based on number of playlists
        # Could be enhanced with playlist follower counts, etc.
        return min(1.0, len(playlists) / 10)
    
    def calculate_viral_score(self, viral_content):
        """Calculate score based on viral content"""
        if not viral_content:
            return 0.0
        
        # Calculate score based on likes and shares
        total_likes = sum(content['likes'] for content in viral_content)
        total_shares = sum(content['shares'] for content in viral_content)
        
        # Normalize to 0-1 range
        likes_score = min(1.0, total_likes / 1000000)
        shares_score = min(1.0, total_shares / 500000)
        
        return (likes_score * 0.7 + shares_score * 0.3)
    
    def calculate_momentum_score(self, artist_data):
        """Calculate overall momentum score for an artist"""
        # Extract relevant data
        streaming_history = artist_data.get('streaming_history', [])
        social_data = artist_data.get('tiktok_engagement', [])
        playlists = artist_data.get('playlists', [])
        viral_content = artist_data.get('viral_content', [])
        
        # Calculate individual scores
        streaming_growth = self.calculate_streaming_growth(streaming_history)
        social_growth = self.calculate_social_growth(social_data)
        playlist_score = self.calculate_playlist_score(playlists)
        viral_score = self.calculate_viral_score(viral_content)
        
        # Apply weights to get final score
        momentum_score = (
            self.weights['streaming_growth'] * streaming_growth +
            self.weights['social_engagement'] * social_growth +
            self.weights['playlist_adds'] * playlist_score +
            self.weights['social_engagement'] * viral_score / 2  # Split social weight between growth and viral
        )
        
        # Generate insights
        insights = []
        
        if streaming_growth > 0.5:
            insights.append(f"{int(streaming_growth * 100)}% streaming growth")
        
        if social_growth > 1.0:
            insights.append(f"{int(social_growth * 100)}% increase in social engagement")
        
        if playlist_score > 0.5:
            insights.append(f"Added to {len(playlists)} playlists")
        
        if viral_score > 0.3:
            insights.append(f"Viral content with high engagement")
        
        if len(insights) == 0:
            insights.append("Steady growth across platforms")
        
        return {
            'momentum_score': momentum_score,
            'streaming_growth': streaming_growth,
            'social_growth': social_growth,
            'playlist_score': playlist_score,
            'viral_score': viral_score,
            'insights': insights
        }
    
    def rank_artists(self, artists_data):
        """Rank a list of artists by momentum score"""
        scored_artists = []
        
        for artist_data in artists_data:
            artist = artist_data.get('artist', {})
            scores = self.calculate_momentum_score(artist_data)
            
            scored_artists.append({
                'artist': artist,
                'momentum_score': scores['momentum_score'],
                'streaming_growth': scores['streaming_growth'],
                'social_growth': scores['social_growth'],
                'playlist_score': scores['playlist_score'],
                'viral_score': scores['viral_score'],
                'insights': scores['insights'],
                'raw_data': artist_data
            })
        
        # Sort by momentum score
        scored_artists.sort(key=lambda x: x['momentum_score'], reverse=True)
        
        return scored_artists 