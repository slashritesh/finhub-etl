import httpx
import os
from dotenv import load_dotenv

load_dotenv()

# Get the API key safely
api_key = os.getenv("FINHUB_API_KEY")

# Check if key exists
if not api_key:
    raise ValueError("❌ FINHUB_API_KEY not found in environment variables!")

# Base URL for Finnhub API
BASE_URL = "https://finnhub.io/api/v1"


class FinnhubAPIClient:
    """Async HTTP client for Finnhub REST API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = BASE_URL
        self.headers = {"X-Finnhub-Token": api_key}

    async def get(self, endpoint: str, params: dict = None) -> dict:
        """Make GET request to Finnhub API.

        Args:
            endpoint (str): API endpoint (e.g., '/stock/profile2')
            params (dict): Query parameters

        Returns:
            dict: JSON response from API
        """
        url = f"{self.base_url}{endpoint}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()


# Initialize API client
api_client = FinnhubAPIClient(api_key=api_key)