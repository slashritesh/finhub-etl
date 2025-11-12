import json
from pathlib import Path
from typing import Any, Union ,TypeVar
from sqlmodel import SQLModel
from typing import Type, List, Callable
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from ..database import engine

T = TypeVar("T", bound=SQLModel)


def save_json(
    data: Any, file_path: Union[str, Path], indent: int = 2, ensure_ascii: bool = False
) -> None:
    """
    Save data to a JSON file.

    Args:
        data: JSON-serializable data to save
        file_path: Path where the file should be saved
        indent: Number of spaces for indentation (default: 2)
        ensure_ascii: If True, escape non-ASCII characters (default: False)

    Raises:
        TypeError: If data is not JSON-serializable
        OSError: If file cannot be written
    """
    file_path = Path(file_path)

    # Create parent directories if they don't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Write JSON to file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)

    print(f"Data saved to {file_path}")



T = TypeVar("T", bound=SQLModel)


async def fetch_and_store_data(
    handler: Callable[..., Any],
    model: Type[T],
    **params
) -> Union[T, List[T], None]:
    """
    Fetch data from an API handler and store it in the database.

    Automatically manages the AsyncSession context.

    Args:
        handler: Function to fetch data from API (e.g. trading.get_dividends)
        model: SQLModel class where data will be stored
        **params: Parameters to pass to the handler (e.g. symbol, from_date, to_date)

    Returns:
        Saved record(s) or None if no data was returned
    """
    async with AsyncSession(engine) as session:
        try:
            # 1️⃣ Fetch data
            data = await handler(**params)
            if not data:
                print(f"No data returned for {model.__name__}")
                return None

            # 2️⃣ Normalize to list
            records = data if isinstance(data, list) else [data]

            # 3️⃣ Convert dicts → model instances
            model_instances = [model(**record) for record in records]

            # 4️⃣ Store in DB
            session.add_all(model_instances)
            await session.commit()

            print(f"✅ Stored {len(model_instances)} records in {model.__name__}")
            await session.close()
            return model_instances if len(model_instances) > 1 else model_instances[0]

        except IntegrityError as e:
            await session.rollback()
            print(f"⚠️ Integrity error saving {model.__name__}: {e}")
        except Exception as e:
            await session.rollback()
            print(f"❌ Failed to fetch/store {model.__name__}: {e}")

        return None