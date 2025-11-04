
import finnhub
finnhub_client = finnhub.Client(api_key="d1qgq9hr01qo4qd75oe0d1qgq9hr01qo4qd75oeg")




def getSymbols():
    print(finnhub_client.symbol_lookup('US'))

# def getSymbolsByExchnage():
#     print(finnhub_client.symbol_lookup('',exchnage="US"))

getSymbols()