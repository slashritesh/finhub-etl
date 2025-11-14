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


def get_symbols_by_exchange(exchange: str, file_path: str = DIR) -> List[str]:
    """
    Read stock symbols from a CSV file filtered by exchange and return them as a list.

    Args:
        exchange: The exchange code to filter by (e.g., 'NASDAQ', 'NYSE').
        file_path: Path to the CSV file containing stock symbols.
                   Defaults to DIR constant.

    Returns:
        List of stock symbols as strings for the specified exchange.

    Raises:
        FileNotFoundError: If the CSV file doesn't exist.
        ValueError: If the CSV file is empty or has no valid symbols for the exchange.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    symbols = []

    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        # Try common column names for exchange
        exchange_columns = ['exchange', 'Exchange', 'EXCHANGE', 'mic', 'MIC']

        for row in reader:
            # Find which column contains the exchange
            exchange_value = None
            for col in exchange_columns:
                if col in row and row[col]:
                    exchange_value = row[col].strip()
                    break

            # If exchange matches, extract the symbol
            if exchange_value and exchange_value.upper() == exchange.upper():
                # Try common column names for stock symbols
                symbol_columns = ['symbol', 'Symbol', 'SYMBOL', 'ticker', 'Ticker']
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
        raise ValueError(f"No symbols found for exchange '{exchange}' in CSV file: {file_path}")

    print(f"Stocks Available for {exchange} - {len(symbols)}")

    return symbols



