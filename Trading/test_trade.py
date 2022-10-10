from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import time
import pandas as pd
import sqlalchemy
from binance import Client
from binance import BinanceSocketManager
from binance.client import Client



api_key = 'ktVeNaWZwqJSQadqieUCKhZvIlgNco4eu0tF9OOhCit6n4h48WdYEZJznFPFwnDQ'
api_secret = 'iMXWqiiYZPL1drhDHcinqVdO5QtRYIXAHMlvff6K3tW0l8YkVjpLX1oUJlrRymqw'
client = Client(api_key, api_secret)

# get market depth
depth = client.get_order_book(symbol='ETHGBP')
depth
# recent trades
trades = client.get_recent_trades(symbol='ETHGBP')
trades

## get balance for a specific asset only one coin
print(client.get_asset_balance(asset='BTC'))
print(client.get_asset_balance(asset='ETH'))
print(client.get_asset_balance(asset='ADA'))
print(client.get_asset_balance(asset='GBP'))

# actual order
order = client.order_market_buy(
    symbol='ETHGBP',
    quantity=0.01)


order = client.order_market_sell(
    symbol='ETHGBP',
    quantity=0.01)
