"""
This module simulates TikTok data for the MVP.
In a production environment, this would be replaced with actual TikTok API integration.
"""

import random
from datetime import datetime, timedelta

def simulate_social_engagement(artist_name, popularity=50, days=30):
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

def simulate_trending_hashtags(artist_name, popularity=50):
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

def simulate_viral_content(artist_name, popularity=50):
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