import finnhub
import os
from dotenv import load_dotenv

load_dotenv()

# Get the API key safely
api_key = os.getenv("FINHUB_API_KEY")

# Check if key exists
if not api_key:
    raise ValueError("❌ FINHUB_API_KEY not found in environment variables!")

# Initialize client
finnhub_client = finnhub.Client(api_key=api_key)