from dotenv import load_dotenv
import asyncio
from config import get_company_profile
from models import CompanyProfile
from utils import save_to_db
from database.core import engine

# Load environment variables from .env file
load_dotenv()


async def main():
    try:
        result = get_company_profile()
        await save_to_db(CompanyProfile, result)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
