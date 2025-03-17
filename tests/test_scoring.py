import sys
import os
import unittest
import json
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.scoring import MomentumScorer

class TestMomentumScorer(unittest.TestCase):
    """Test cases for the MomentumScorer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scorer = MomentumScorer()
        
        # Create sample streaming history data
        self.streaming_history = []
        base_streams = 1000
        end_date = datetime.now()
        
        for i in range(30):
            date = end_date - timedelta(days=29-i)
            # Increasing trend
            streams = base_streams + (i * 100)
            self.streaming_history.append({
                'date': date.strftime('%Y-%m-%d'),
                'streams': streams
            })
        
        # Create sample social data
        self.social_data = []
        base_likes = 500
        base_shares = 50
        base_comments = 20
        
        for i in range(30):
            date = end_date - timedelta(days=29-i)
            # Increasing trend
            likes = base_likes + (i * 50)
            shares = base_shares + (i * 5)
            comments = base_comments + (i * 2)
            self.social_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'likes': likes,
                'shares': shares,
                'comments': comments,
                'views': likes * 5,
                'mentions': int(likes / 10),
                'engagement_ratio': (likes + shares + comments) / (likes * 5)
            })
        
        # Create sample playlists
        self.playlists = [
            {'id': 'playlist1', 'name': 'Playlist 1', 'owner': 'User 1', 'tracks_total': 50},
            {'id': 'playlist2', 'name': 'Playlist 2', 'owner': 'User 2', 'tracks_total': 100},
            {'id': 'playlist3', 'name': 'Playlist 3', 'owner': 'User 3', 'tracks_total': 75}
        ]
        
        # Create sample viral content
        self.viral_content = [
            {
                'id': 'content1',
                'content_type': 'dance',
                'title': 'Viral Dance',
                'creator': 'Creator 1',
                'likes': 500000,
                'shares': 100000,
                'comments': 50000,
                'views': 2000000,
                'created_at': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            }
        ]
        
        # Create sample artist data
        self.artist_data = {
            'artist': {
                'id': 'artist1',
                'name': 'Test Artist',
                'popularity': 70,
                'followers': 50000,
                'genres': ['pop', 'dance']
            },
            'streaming_history': self.streaming_history,
            'tiktok_engagement': self.social_data,
            'playlists': self.playlists,
            'viral_content': self.viral_content
        }
    
    def test_calculate_streaming_growth(self):
        """Test streaming growth calculation"""
        growth = self.scorer.calculate_streaming_growth(self.streaming_history)
        self.assertGreater(growth, 0)
    
    def test_calculate_social_growth(self):
        """Test social growth calculation"""
        growth = self.scorer.calculate_social_growth(self.social_data)
        self.assertGreater(growth, 0)
    
    def test_calculate_playlist_score(self):
        """Test playlist score calculation"""
        score = self.scorer.calculate_playlist_score(self.playlists)
        self.assertEqual(score, 0.3)  # 3 playlists / 10
    
    def test_calculate_viral_score(self):
        """Test viral score calculation"""
        score = self.scorer.calculate_viral_score(self.viral_content)
        self.assertGreater(score, 0)
        self.assertLessEqual(score, 1.0)
    
    def test_calculate_momentum_score(self):
        """Test momentum score calculation"""
        scores = self.scorer.calculate_momentum_score(self.artist_data)
        self.assertIn('momentum_score', scores)
        self.assertIn('streaming_growth', scores)
        self.assertIn('social_growth', scores)
        self.assertIn('playlist_score', scores)
        self.assertIn('viral_score', scores)
        self.assertIn('insights', scores)
        
        # Momentum score should be positive
        self.assertGreater(scores['momentum_score'], 0)
        
        # Insights should not be empty
        self.assertGreater(len(scores['insights']), 0)

if __name__ == '__main__':
    unittest.main() 