import json
from pathlib import Path
from typing import Any, Union, List, Type, TypeVar
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from database.core import engine

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


async def save_to_db(
    model: Type[T],
    data: Union[dict, List[dict]],
) -> Union[T, List[T]]:
    """
    Save data to database using SQLModel.

    Args:
        model: SQLModel class to instantiate
        data: Dictionary or list of dictionaries to save

    Returns:
        Created model instance(s)

    Example:
        from src.models.company import CompanyProfile
        company = await save_to_db(CompanyProfile, company_data)

        # Batch insert
        companies = await save_to_db(CompanyProfile, [data1, data2, data3])
    """

    async with AsyncSession(engine) as session:
        if isinstance(data, list):
            instances = [model(**item) for item in data]
            session.add_all(instances)
            await session.commit()
            for instance in instances:
                await session.refresh(instance)
            return instances
        else:
            instance = model(**data)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            session.close()
            return instance
