from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_async_engine(DATABASE_URL)


async def get_session():
    async with AsyncSession(engine) as session:
        yield session

 