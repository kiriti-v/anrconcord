import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# API configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Dashboard configuration
DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "8501"))

# Cache directory for storing artist data
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "app", "data", "cache_new")
os.makedirs(CACHE_DIR, exist_ok=True)

# Default weights for scoring model
DEFAULT_WEIGHTS = {
    "streaming_growth": 0.3,
    "social_growth": 0.3,
    "playlist_score": 0.2,
    "viral_score": 0.2
} 