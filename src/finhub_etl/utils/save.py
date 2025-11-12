import json
from pathlib import Path
from typing import Any, Union ,TypeVar
from sqlmodel import SQLModel


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

