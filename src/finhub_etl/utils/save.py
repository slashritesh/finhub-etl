# In file: finhub_etl/utils/save.py

import json
from pathlib import Path
from typing import Any, Union ,TypeVar, Type, List, Callable
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from ..database import engine

T = TypeVar("T", bound=SQLModel)


# Your save_json function is fine, no changes needed there.
def save_json(
    data: Any, file_path: Union[str, Path], indent: int = 2, ensure_ascii: bool = False
) -> None:
    # ... (this function remains the same)
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)
    print(f"Data saved to {file_path}")


async def fetch_and_store_data(
    handler: Callable[..., Any],
    model: Type[T],
    **params
) -> Union[List[T], None]:
    """
    Fetch data from an API handler and store it in the database.

    This version correctly handles:
    1. Nested API responses (e.g., {"data": [...]})
    2. Enriching records with parameters like 'symbol' for composite keys.

    Args:
        handler: Function to fetch data from API.
        model: SQLModel class where data will be stored.
        **params: Parameters to pass to the handler.

    Returns:
        A list of saved records or None if no data was stored.
    """
    async with AsyncSession(engine) as session:
        try:
            # 1️⃣ Fetch data from the handler
            raw_response = await handler(**params)
            if not raw_response:
                print(f"No data returned by handler for {model.__name__}")
                return None

            # 2️⃣ Normalize the data into a list of records
            #    This is the key change to handle different API response shapes.
            records_list = []
            if isinstance(raw_response, dict) and 'data' in raw_response:
                # Handles {"data": [...]} structure
                records_list = raw_response['data']
            elif isinstance(raw_response, list):
                # Handles [...] structure
                records_list = raw_response
            else:
                # Handles a single object response
                records_list = [raw_response]

            if not records_list:
                print(f"No records to process for {model.__name__}")
                return None

            # 3️⃣ Convert dicts to model instances, enriching them first
            model_instances = []
            symbol = params.get("symbol") # Get symbol from original request

            for record in records_list:
                # CRITICAL FIX: Add the symbol to the record if it's not there.
                # This is necessary for models with composite primary keys.
                if 'symbol' not in record and symbol:
                    record['symbol'] = symbol
                
                model_instances.append(model(**record))

            # 4️⃣ Store in DB
            session.add_all(model_instances)
            await session.commit()

            print(f"✅ Stored {len(model_instances)} records in {model.__name__}")
            # Always return a list for consistency
            return model_instances

        except IntegrityError as e:
            await session.rollback()
            # The str(e) gives a much more useful error message
            print(f"⚠️ Integrity error saving {model.__name__}: {str(e)}")
        except Exception as e:
            await session.rollback()
            print(f"❌ Failed to fetch/store {model.__name__}: {e}")

        return None