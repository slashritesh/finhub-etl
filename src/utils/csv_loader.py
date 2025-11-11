import csv
from pathlib import Path
from typing import Union, List
from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from database.core import engine
from models import MatchedStock


async def load_matched_stocks_csv(
    csv_path: Union[str, Path],
    batch_size: int = 1000,
) -> int:
    """
    Load matched stocks from CSV file into database.

    Args:
        csv_path: Path to the CSV file
        batch_size: Number of records to insert per batch (default: 1000)

    Returns:
        Total number of records inserted

    Example:
        count = await load_matched_stocks_csv("matched_stocks.csv")
        print(f"Inserted {count} records")
    """
    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    total_inserted = 0
    batch: List[MatchedStock] = []

    async with AsyncSession(engine) as session:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                # Convert empty strings and 'NULL' to None
                cleaned_row = {
                    k: None if v in ("", "NULL") else v
                    for k, v in row.items()
                }

                # Parse datetime fields
                for date_field in ["created_at", "updated_at"]:
                    if cleaned_row.get(date_field):
                        try:
                            # Parse format: "2024-11-27 06:26:48.606"
                            cleaned_row[date_field] = datetime.strptime(
                                cleaned_row[date_field].split('.')[0],
                                "%Y-%m-%d %H:%M:%S"
                            )
                        except (ValueError, AttributeError):
                            cleaned_row[date_field] = None

                # Convert numeric fields
                for numeric_field in [
                    "is_active", "is_deleted", "last_price", "change",
                    "changePercent", "market_cap", "min_order_size"
                ]:
                    if cleaned_row.get(numeric_field):
                        try:
                            if numeric_field in ["is_active", "is_deleted"]:
                                cleaned_row[numeric_field] = int(cleaned_row[numeric_field])
                            else:
                                cleaned_row[numeric_field] = float(cleaned_row[numeric_field])
                        except (ValueError, TypeError):
                            cleaned_row[numeric_field] = None

                # Create model instance
                try:
                    stock = MatchedStock(**cleaned_row)
                    batch.append(stock)
                except Exception as e:
                    print(f"Error creating MatchedStock from row: {e}")
                    print(f"Row data: {cleaned_row}")
                    continue

                # Insert batch when it reaches batch_size
                if len(batch) >= batch_size:
                    session.add_all(batch)
                    await session.commit()
                    total_inserted += len(batch)
                    print(f"Inserted {total_inserted} records...")
                    batch = []

            # Insert remaining records
            if batch:
                session.add_all(batch)
                await session.commit()
                total_inserted += len(batch)

    print(f"✓ Successfully loaded {total_inserted} matched stocks into database")
    return total_inserted


async def clear_matched_stocks_table() -> int:
    """
    Clear all records from the matched_stocks table.

    Returns:
        Number of records deleted

    Example:
        count = await clear_matched_stocks_table()
        print(f"Deleted {count} records")
    """
    from sqlmodel import select

    async with AsyncSession(engine) as session:
        # Get count before deletion
        result = await session.execute(select(MatchedStock))
        records = result.scalars().all()
        count = len(records)

        # Delete all records
        for record in records:
            await session.delete(record)

        await session.commit()
        print(f"✓ Cleared {count} records from matched_stocks table")
        return count
