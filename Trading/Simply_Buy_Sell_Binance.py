# https://algotrading101.com/learn/binance-python-api-guide/
import os
import time
import pandas as pd
import sqlalchemy
from binance import Client
from binance import BinanceSocketManager
from time import sleep
from binance import ThreadedWebsocketManager
import csv
from binance.enums import *
import btalib
####
# STANDALONE BY ORDER NO CCONDITIONS
buyorder = client.create_order(symbol='BTCUSDT',
                            side='BUY',
                            type='MARKET',
                            quantity=0.0001)


####






api_key = 'ktVeNaWZwqJSQadqieUCKhZvIlgNco4eu0tF9OOhCit6n4h48WdYEZJznFPFwnDQ'
api_secret = 'iMXWqiiYZPL1drhDHcinqVdO5QtRYIXAHMlvff6K3tW0l8YkVjpLX1oUJlrRymqw'

# set the key we have copied from Binance Account
client = Client(api_key, api_secret)

## get balance for a specific asset only one coin
print(client.get_asset_balance(asset='BTC'))
print(client.get_asset_balance(asset='ETH'))
print(client.get_asset_balance(asset='ADA'))
print(client.get_asset_balance(asset='GBP'))

# get latest price from Binance API
btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
# print full output (dictionary)
print(btc_price)
print(btc_price["price"])

btc_price = {'error':False}

# Next we will create a dictionary that will hold our latest price data
def btc_trade_history(msg):
    ''' define how to process incoming WebSocket messages '''
    if msg['e'] != 'error':
    	print(msg['c'])
    	btc_price['last'] = msg['c']
    	btc_price['bid'] = msg['b']
    	btc_price['last'] = msg['a']
    	btc_price['error'] = False
    else:
        btc_price['error'] = True


# init and start the WebSocket
bsm = ThreadedWebsocketManager()
bsm.start()

# subscribe to a stream
bsm.start_symbol_ticker_socket(callback=btc_trade_history, symbol='BTCUSDT')
bsm.start_symbol_ticker_socket(callback=btc_trade_history, symbol='ETHUSDT')
#help(ThreadedWebsocketManager)


# Periodic BTC data in csv
# valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
# get timestamp of earliest date data is available
timestamp = client._get_earliest_valid_timestamp('BTCUSDT', '1d')
print(timestamp)

# request historical candle (or klines) data
bars = client.get_historical_klines('BTCUSDT', '1d', timestamp, limit=1000)

# option 1 - save to file using json method
'''with open('btc_bars.json', 'w') as e:
    json.dump(bars, e)'''
# option 2 - save as CSV file using the csv writer library
with open('btc_bars.csv', 'w', newline='') as f:
    wr = csv.writer(f)
    for line in bars:
        wr.writerow(line)
btc_df = pd.read_csv('btc_bars.csv')
btc_df

# access your open orders
client.get_open_orders


# BUY TEST
buy_order = client.create_test_order(symbol='ETHUSDT', side='BUY', type='MARKET', quantity=0.001)
buy_order_limit = client.create_test_order(
    symbol='ETHUSDT',
    side='BUY',
    type='LIMIT',
    timeInForce='GTC',
    quantity=100,
    price=200)
# create a real order if the test orders did not raise an exception
try:
    buy_limit = client.create_order(
        symbol='ETHUSDT',
        side='BUY',
        type='MARKET',
        quantity=0.0001)
except:
    print('FAIL')

except BinanceAPIException as e:
    # error handling goes here
    print(e)
except BinanceOrderException as e:
    # error handling goes here
    print(e)

# SELL





# stop websocket
bsm.stop()
