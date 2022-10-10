# live Binance data and storing into SQL database.
# Part 1
# From: https://www.youtube.com/watch?v=rc_Y6rdBqXM

# My API backup key from Binance = QRUDQ3HMSYTOSDXN
import os
import time
import pandas as pd
import sqlalchemy
from binance import Client
from binance import BinanceSocketManager



api_key = 'ktVeNaWZwqJSQadqieUCKhZvIlgNco4eu0tF9OOhCit6n4h48WdYEZJznFPFwnDQ'
api_secret = 'iMXWqiiYZPL1drhDHcinqVdO5QtRYIXAHMlvff6K3tW0l8YkVjpLX1oUJlrRymqw'

# set the key we have copied from Binance Account
client = Client(api_key, api_secret)
bsm = BinanceSocketManager(client)
socket = bsm.trade_socket('ETHGBP')


# Test if the account is reachable
client.get_account()

# can also use datatream via websocket - we are not doing this in this one.

# Get the price data from a set period of time ago
# - can use this to train a bot to predict future trends?
pd.DataFrame(client.get_historical_klines('BTCUSDT', '1m', '30 min ago UTC') )

# function to get minute data on ANY COIN building on from above.
def GetMinuteData(symbol, interval, lookback):
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback+' min ago UTC'))
    frame = frame.iloc[:,:6] # arbitrary cutting off at col 6
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = frame.set_index('Time')
    # transform the unix timestamp to a readable one.
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    return frame

# call the new function to get minute data on any coin! try it out for ETH BTC and ADA
# - in minutes.
btc = GetMinuteData('BTCGBP', '1m', '30m')
eth = GetMinuteData('ETHGBP', '1m', '30m')
ada = GetMinuteData('ADAGBP', '1m', '30m')

# visualize the data for the length of time.
btc.Open.plot(title='BTC')
eth.Open.plot(title='ETH')
ada.Open.plot(title='ADA')

# Define the strategy
# - Buy if the asset fell by more than 0.2% (this is x, find this to adjust) within last 30 mins
# - Sell if asset rises by more than 0.15% (This is minimum as otherwise fees get us) OR falls again by 0.15%

df = GetMinuteData('ETHGBP', '1m', '60m')
df


def StratTest(symbol, qty, entried=False):
    df = GetMinuteData(symbol, '1m', '30')
    performance = (df.Open.pct_change() +1).cumprod() - 1
    print(performance[-1])
    # Buying condition
    if not entried:
        if performance[-1] < -0.001: # if last entry is below 0.2%, then place order
            order = client.create_order(symbol=symbol, side='BUY',
                                        type='MARKET',
                                        quantity=float(qty) )
            print(order)
            entried=True
        else:
            print('No Trade Executed')
    # Selling condition
    if entried:
        while True:
            df = GetMinuteData(symbol, '1m', '30')
            sincebuy = df.loc[df.index > pd.to_datetime(
            order['transactTime'], unit='ms')]
            if len(sincebuy) > 0:
                sincebuy_returns = (sincebuy.Open.pct_change() +1).cumprod() - 1
                # Sell if asset rises by more than 0.15% (This is minimum as otherwise fees get us) OR falls again by 0.15%
                if sincebuy_returns[-1] > 0.001 or sincebuy_returns[-1] < -0.001:
                    order = client.create_order(symbol=symbol, side='SELL',
                                                type='MARKET', quantity=qty)
                    print(order)
                    break

# Call the StratTest function and buy crypto using real money
# - qty of 0.001 ETH is aroughly £1.19 on the ETH/GBP market as of 2022-10-10
#time.time()

StratTest('ETHGBP', 0.001)
