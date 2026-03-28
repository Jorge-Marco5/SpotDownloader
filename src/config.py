import os
from dotenv import load_dotenv

# Load environment variables once at module level
load_dotenv()

class Config:
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    
    # YouTube / Audio settings
    YT_CODEC_AUDIO = os.getenv("YT_CODEC_AUDIO", "mp3")
    YT_CODEC_VIDEO = os.getenv("YT_CODEC_VIDEO", "mp4")
    YT_QUALITY_AUDIO = os.getenv("YT_QUALITY_AUDIO", "192")
    YT_QUALITY_VIDEO = os.getenv("YT_QUALITY_VIDEO", "best")

    @classmethod
    def validate(cls):
        """Check if essential environment variables are set."""
        if not cls.SPOTIFY_CLIENT_ID or not cls.SPOTIFY_CLIENT_SECRET:
            print("WARNING: SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET not found in environment.")
