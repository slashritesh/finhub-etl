import csv
from pathlib import Path
from typing import List


DIR = "data/matched_stocks.csv"


def get_symbols_list(file_path: str = DIR) -> List[str]:
    """
    Read stock symbols from a CSV file and return them as a list.

    Args:
        file_path: Path to the CSV file containing stock symbols.
                   Defaults to DIR constant.

    Returns:
        List of stock symbols as strings.

    Raises:
        FileNotFoundError: If the CSV file doesn't exist.
        ValueError: If the CSV file is empty or has no valid symbols.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    symbols = []

    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        # Try common column names for stock symbols
        symbol_columns = ['symbol']

        for row in reader:
            # Find which column contains the symbol
            for col in symbol_columns:
                if col in row and row[col]:
                    symbols.append(row[col].strip())
                    break
            else:
                # If no matching column name, use the first column
                if row:
                    first_value = list(row.values())[0]
                    if first_value:
                        symbols.append(first_value.strip())

    if not symbols:
        raise ValueError(f"No symbols found in CSV file: {file_path}")
    
    print("Stocks Available in DB and CSV Dump - ",len(symbols))

    return symbols



symbols = get_symbols_list()

print(len(symbols))