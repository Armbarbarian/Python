# live Binance data and storing into SQL database.
# Part 1
# From: https://www.youtube.com/watch?v=rc_Y6rdBqXM
#
# My API backup key from Binance = QRUDQ3HMSYTOSDXN
import os
import time
import datetime
import pandas as pd
import sqlalchemy
from binance import Client
from binance import BinanceSocketManager
import matplotlib.pyplot as plt

api_key = 'ktVeNaWZwqJSQadqieUCKhZvIlgNco4eu0tF9OOhCit6n4h48WdYEZJznFPFwnDQ'
api_secret = 'iMXWqiiYZPL1drhDHcinqVdO5QtRYIXAHMlvff6K3tW0l8YkVjpLX1oUJlrRymqw'

# set the key we have copied from Binance Account
client = Client(api_key, api_secret)
bsm = BinanceSocketManager(client)
# socket = bsm.trade_socket('ETHGBP')


# Test if the account is reachable
# client.get_account()

# get balance for a specific asset only one coin
print(client.get_asset_balance(asset='BTC'))
print(client.get_asset_balance(asset='ETH'))
print(client.get_asset_balance(asset='ADA'))
print(client.get_asset_balance(asset='BNB'))
print(client.get_asset_balance(asset='GBP'))
# can also use datatream via websocket - we are not doing this in this one.

# Get the price data from a set period of time ago
# - can use this to train a bot to predict future trends?

# function to get minute data on ANY COIN building on from above.


def GetMinuteData(symbol, interval, lookback):
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback+' min ago UTC'))
    frame = frame.iloc[:, :6]  # arbitrary cutting off at col 6
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = frame.set_index('Time')
    # transform the unix timestamp to a readable one.
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    return frame

# call the new function to get minute data on any coin! try it out for ETH BTC and ADA
# - in minutes.
# Check how the markets look before trading and figure out which time frame gives us an increasing trends


'''
btc = GetMinuteData('BTCGBP', '1m', '30m')
btc.Open.plot(title='BTCGBP')
'''


# Define the strategy
# - Buy if the asset fell by more than 0.2% (this is x, find this to adjust) within last 30 mins
# - Sell if asset rises by more than 0.15% (This is minimum as otherwise fees get us) OR falls again by 0.15%

# df
# df.plot()


def Strat4_Vis(symbol_list, qty, interval, entried=False):
    trend_data1 = []
    trend_data2 = []
    trend_data3 = []
    end_time = time.time() + 60*1  # How many minutes to build up the data for before starting to trade.
    while True:
        # Read in the data
        df1 = GetMinuteData(symbol_list[0], '1m', interval)
        df2 = GetMinuteData(symbol_list[1], '1m', interval)
        df3 = GetMinuteData(symbol_list[2], '1m', interval)
        performance1 = (df1.Open.pct_change() + 1).cumprod() - 1
        performance2 = (df2.Open.pct_change() + 1).cumprod() - 1
        performance3 = (df3.Open.pct_change() + 1).cumprod() - 1
        print(performance1[-1])
        print(performance2[-1])
        print(performance3[-1])
        trend1 = (df1.Open.tail(5))
        trend2 = (df2.Open.tail(5))
        trend3 = (df3.Open.tail(5))
        diff1 = trend1[-1] / trend1[0]
        diff2 = trend2[-1] / trend2[0]
        diff3 = trend3[-1] / trend3[0]
        trend_data1.append(diff1)
        trend_data2.append(diff2)
        trend_data3.append(diff3)
        '''
        print(symbol_list[0] + 'Data')
        print(pd.DataFrame(trend_data1))
        print(symbol_list[1] + 'Data')
        print(pd.DataFrame(trend_data2))
        print(symbol_list[2] + 'Data')
        print(pd.DataFrame(trend_data3))
        '''
        # pd.DataFrame(trend_data1).plot(title=symbol_list[0])
        # pd.DataFrame(trend_data2).plot(title=symbol_list[1])
        # pd.DataFrame(trend_data3).plot(title=symbol_list[2])

        # Initialise the subplot function using number of rows and columns
        figure, axis = plt.subplots(2, 2)
        # plot for coin 1
        axis[0, 0].plot(pd.DataFrame(trend_data1))
        axis[0, 0].set_title(symbol_list[0])
        # plot for coin 2
        axis[0, 1].plot(pd.DataFrame(trend_data2))
        axis[0, 1].set_title(symbol_list[1])
        # plot for coin 3
        axis[1, 0].plot(pd.DataFrame(trend_data3))
        axis[1, 0].set_title(symbol_list[2])
        # Combine all the operations and display
        plt.show()
        time.sleep(5)


# JUST VISUALISE
Strat4_Vis(symbol_list=['ETHGBP', 'BTCGBP', 'BNBGBP'], qty=0.001, interval='10')
