"""Test handler data fetching and storage."""
import asyncio
import sys
import os
from pathlib import Path
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError

# Change to src directory to ensure consistent imports
src_dir = Path(__file__).parent.parent
os.chdir(src_dir)
sys.path.insert(0, str(src_dir))

from utils.mappings import HANDLER_MODEL_DICT
from database import engine


async def test_handler(key: str):
    """Fetch and store data for a given handler key."""
    cfg = HANDLER_MODEL_DICT.get(key)
    if not cfg:
        return print(f"Invalid key: {key}\nAvailable: {', '.join(HANDLER_MODEL_DICT)}")

    print(f"\n{'='*60}\nTesting: {cfg['name']}\n{'='*60}\nFetching...")

    data = await cfg["handler"](**cfg["params"])
    if not data:
        return print("No data returned")

    recs = (data if isinstance(data, list) else [data])[:cfg.get("limit", len(data))]
    print(f"Fetched {len(recs)} records. Storing...\n")

    stored = exist = errs = 0
    msgs = []

    async with AsyncSession(engine) as s:
        for r in recs:
            try:
                s.add(cfg["model"].model_validate(r))
                await s.commit()
                stored += 1
            except IntegrityError:
                await s.rollback()
                exist += 1
            except Exception as e:
                await s.rollback()
                errs += 1
                msgs.append(str(e)[:100])

    print(f"Stored: {stored} | Existing: {exist} | Errors: {errs}")
    for i, m in enumerate(msgs[:5], 1):
        print(f"{i}. {m}")
    if len(msgs) > 5:
        print(f"...and {len(msgs) - 5} more")
    print(f"{'='*60}\n")


async def main():
    TEST_KEY = "company_profile2"
    try:
        await test_handler(TEST_KEY)
    finally:
        await engine.dispose()
        print("Engine disposed.")


if __name__ == "__main__":
    asyncio.run(main())
