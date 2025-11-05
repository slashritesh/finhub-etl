from .finhub import finnhub_client as client

def get_stocks_symbols():
    return client.symbol_lookup("US")


def get_company_profile():
    return client.company_profile(symbol="AAPL")
