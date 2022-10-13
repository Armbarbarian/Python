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

api_key = 'ktVeNaWZwqJSQadqieUCKhZvIlgNco4eu0tF9OOhCit6n4h48WdYEZJznFPFwnDQ'
api_secret = 'iMXWqiiYZPL1drhDHcinqVdO5QtRYIXAHMlvff6K3tW0l8YkVjpLX1oUJlrRymqw'

# set the key we have copied from Binance Account
client = Client(api_key, api_secret)
bsm = BinanceSocketManager(client)
socket = bsm.trade_socket('ETHGBP')


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


btc = GetMinuteData('BTCGBP', '1m', '30m')
btc.Open.plot(title='BTCGBP')

eth = GetMinuteData('ETHGBP', '1m', '30m')
eth.Open.plot(title='ETH')

btc = GetMinuteData('BNBGBP', '1m', '20m')
btc.Close.plot(title='BNB / GBP')

ada = GetMinuteData('ADAGBP', '1m', '30m')
ada.Open.plot(title='ADA')


# Min needed for the trade to even take place
info = client.get_symbol_info('ETHGBP')
print(info['filters'][2]['minQty'])


# Define the strategy
# - Buy if the asset fell by more than 0.2% (this is x, find this to adjust) within last 30 mins
# - Sell if asset rises by more than 0.15% (This is minimum as otherwise fees get us) OR falls again by 0.15%
df = GetMinuteData('ETHGBP', '1m', '60 min')
# df
# df.plot()

'''
# Previous function - works as of 2022-10-10 and took roughly 2 minutes to complete a sell.
def StratTest(symbol, qty, interval, entried=False):
    df = GetMinuteData(symbol, '1m', interval)
    performance = (df.Open.pct_change() + 1).cumprod() - 1
    print(performance[-1])
    # Buying condition
    if entried == False:
        if performance[-1] < -0.001:  # if last entry is below 0.1%, then place order
            order = client.order_market_buy(symbol=symbol,
                                            quantity=qty)
            print('BOUGHT: ' + symbol)
            print(order)
            entried = True
        else:
            print('No Trade Executed')
    # Selling condition
    if entried == True:
        while True:
            df = GetMinuteData(symbol, '1m', interval)
            sincebuy = df.loc[df.index > pd.to_datetime(
                order['transactTime'], unit='ms')]
            if len(sincebuy) > 0:
                sincebuy_returns = (sincebuy.Open.pct_change() + 1).cumprod() - 1
                # Sell if asset rises by more than 0.15% (This is minimum as otherwise fees get us) OR falls again by 0.15%
                if sincebuy_returns[-1] > 0.0015 or sincebuy_returns[-1] < -0.0015:
                    order = client.order_market_sell(symbol=symbol, quantity=qty)
                    print('SOLD: ' + symbol)
                    print(order)
                    break
'''
# call the function to start the trading loop.


# Simple trading using one condition

# SELLONLY

#########################################################
# Testing algorithm
# Selling condition
def SellOnly(symbol, qty, interval):
    while True:
        df = GetMinuteData(symbol, '1m', interval)
        trend = (df.Close.tail(5))
        trend_data = []
        diff = trend[-1] / trend[0]
        trend_data.append(diff)
        print(trend_data)

        # trend.plot()
        # Conditions to Sell:
        print(diff)
        if trend_data[-1] > 1:
            print('Sell Order Placed!')
            order = client.order_market_sell(symbol=symbol,
                                             quantity=qty)
            print(order)
        else:
            print('Chose not to sell. You are welcome.')
            # difference = trend[0] / trend[-1]

        break


# SELL EVERYTHING of one coin
'''
while True:
    SellOnly('ETHGBP', x, '10')
    time.sleep(5)
'''

# keep appending the database for 5 minutes before executing any trades
'''
time_end = time.time() + 60*5 # 5 minutes of data before starting the actual trading.
while time.time() < time_end:
    trend_data.append(diff)
    time.sleep(10)
'''


# actual orders that worrks instantly! BE Careful as there are no conditions.
'''
# BUY
order = client.order_market_buy(
    symbol='ETHGBP',
    quantity=0.01)

# SELL
order = client.order_market_sell(
    symbol='ETHGBP',
    quantity=0.0001)'''


# BUY AND SELL


# BUY
'''
# BTC
StratTest(symbol='BTCGBP', qty=0.0008, interval='30')
# ETH
StratTest(symbol='ETHGBP', qty=0.001, interval='30')
# ADA
StratTest(symbol='ADAGBP', qty=0.1, interval='30')
# BNB
StratTest(symbol='BNBGBP', qty=0.00100000, interval='30')
'''
# Call the StratTest function and buy crypto using real money
# - qty of 0.001 ETH is aroughly £1.19 on the ETH/GBP market as of 2022-10-10
# time.time()


###############################################################
######################################################################
symbol = ['ETC', 'BTC', 'BNB']
symbol[2]

# STRAT 4 is simply buy right away and hold until the price rises by x
# This seems full proof.


##################################################################


# Plotting the current trend under the current strat.


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
        pd.DataFrame(trend_data1)
        pd.DataFrame(trend_data2)
        pd.DataFrame(trend_data3)
        # pd.DataFrame(trend_data1).plot(title=symbol_list[0])
        # pd.DataFrame(trend_data2).plot(title=symbol_list[1])
        # pd.DataFrame(trend_data3).plot(title=symbol_list[2])
        time.sleep(5)


# Place Trades Based off the Vis function plot. If they look good then run it manually.


def Strat4(symbol_list, qty, interval, entried=False):
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
        # print(pd.DataFrame(trend_data))
        # Buying condition
        if entried == False:
            # if performance[-1] < -0.001:  # if last entry is below 0.1%, then place order
            order1 = client.order_market_buy(symbol=symbol[0],
                                             quantity=qty)
            order2 = client.order_market_buy(symbol=symbol[1],
                                             quantity=qty)
            order3 = client.order_market_buy(symbol=symbol[2],
                                             quantity=qty)
            print('Buy Order Filled!')
            print(order)
            entried = True
            time.sleep(2)
            print('Transfering to Sales Department...')
            # else:
            # print('Chose not to buy. You are welcome.')
            # time.sleep(2)
        if entried == True:
            while True:
                df = GetMinuteData(symbol, '1m', interval)
                sincebuy = df.loc[df.index > pd.to_datetime(
                    order['transactTime'], unit='ms')]
                if len(sincebuy) > 0:
                    sincebuy_returns = (sincebuy.Open.pct_change() + 1).cumprod() - 1
                    # Sell if asset rises by more than 0.15% (This is minimum as otherwise fees get us) OR falls again by 0.15%
                    try:
                        print(sincebuy_returns[-1])
                        if sincebuy_returns[-1] > 0.0003 or sincebuy_returns[-1] < -0.0015:
                            order = client.order_market_sell(symbol=symbol, quantity=qty)
                            print('SOLD ETH!')
                            print(order)
                            break
                    except:
                        continue


# JUST VISUALISE
Strat4_Vis(symbol_list=['ETHGBP', 'BTCGBP', 'BNBGBP'], qty=0.01, interval='10')

######################################### MAIN CURRENT STRATEGY 2022-10-11 #######################################################
# Run a strategry for 1 hours over and over tracking start GBP and END to see how much we make or loose with this strat.
Start_GBP = client.get_asset_balance(asset='GBP')
Start_ETH = client.get_asset_balance(asset='ETH')
print(Start_ETH)
print(Start_GBP)
final_time = time.time() + 60*60
while time.time() < final_time:
    Strat4(symbol=['ETHGBP', 'BTCGBP', 'BNBGBP'], qty=0.01, interval='10')
# Only run after the Hour is complete.
End_GBP = client.get_asset_balance(asset='GBP')
End_ETH = client.get_asset_balance(asset='ETH')
print(End_ETH)
print(End_GBP)
