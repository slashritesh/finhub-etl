from dotenv import load_dotenv
import asyncio
from config import get_ipo_calendar
from models import IpoCalendar
from utils import save_to_db
from database.core import engine

# Load environment variables from .env file
load_dotenv()


async def main():
    try:
        result = get_ipo_calendar(from_date="2020-05-01", to="2020-06-01")
        await save_to_db(IpoCalendar, result)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
