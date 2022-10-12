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
x = time.time()
Todays_date = datetime.datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S')

api_key = 'ktVeNaWZwqJSQadqieUCKhZvIlgNco4eu0tF9OOhCit6n4h48WdYEZJznFPFwnDQ'
api_secret = 'iMXWqiiYZPL1drhDHcinqVdO5QtRYIXAHMlvff6K3tW0l8YkVjpLX1oUJlrRymqw'

# set the key we have copied from Binance Account
client = Client(api_key, api_secret)
bsm = BinanceSocketManager(client)
# socket = bsm.trade_socket('ETHGBP')

# Test if the account is reachable
# client.get_account()

# get balance for a specific asset only one coin
client.get_account()
# get balance for a specific asset only one coin
print(client.get_asset_balance(asset='BTC'))
print(client.get_asset_balance(asset='ETH'))
print(client.get_asset_balance(asset='ADA'))
print(client.get_asset_balance(asset='BNB'))
print(client.get_asset_balance(asset='GBP'))
# can also use datatream via websocket - we are not doing this in this one.

# Get the price data from a set period of time ago
# - can use this to train a bot to predict future trends?

pd.DataFrame(client.get_historical_klines('BTCUSDT', '1m', '30 min ago UTC'))

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

eth = GetMinuteData('ETHGBP', '1m', '30m')
eth.Open.plot(title='ETH')

btc = GetMinuteData('BNBGBP', '1m', '20m')
btc.Close.plot(title='BNB / GBP')

ada = GetMinuteData('ADAGBP', '1m', '30m')
ada.Open.plot(title='ADA')

mdx = GetMinuteData('MDXBUSD', '1m', '30m')
mdx.Open.plot(title='MDX / USD')
'''

# Min needed for the trade to even take place
info = client.get_symbol_info('ETHGBP')
print(info['filters'][2]['minQty'])


# Define the strategy
# - Buy if the asset fell by more than 0.2% (this is x, find this to adjust) within last 30 mins
# - Sell if asset rises by more than 0.15% (This is minimum as otherwise fees get us) OR falls again by 0.15%
df = GetMinuteData('ETHGBP', '1m', '60 min')
# df
# df.plot()

df
# df.plot()


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

        if performance[-1] < -0.001:  # if last entry is below 0.2%, then place order
            order = client.order_market_buy(symbol=symbol,
                                            quantity=qty)
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


# call the function to start the trading loop.


# Simple trading using one condition

# Call the StratTest function and buy crypto using real money
# - qty of 0.001 ETH is aroughly £1.19 on the ETH/GBP market as of 2022-10-10
# time.time()

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


# SELL
while True:
    SellOnly('BTCGBP', 0.0008, '10')
    time.sleep(10)


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

# BTC
StratTest(symbol='BTCGBP', qty=0.0008, interval='30')
# ETH
StratTest(symbol='ETHGBP', qty=0.001, interval='30')
# ADA
StratTest(symbol='ADAGBP', qty=0.1, interval='30')
# BNB
StratTest(symbol='BNBGBP', qty=0.00100000, interval='30')

# Call the StratTest function and buy crypto using real money
# - qty of 0.001 ETH is aroughly £1.19 on the ETH/GBP market as of 2022-10-10
# time.time()


###############################################################


# 2022-10-11 New Strategy taking into account monitoring of the current health of a market.
# Principle is simple, buy if the average is below 0.999 and sell if it is above 1.005
# Working Strat
# Previous function - works as of 2022-10-10 and took roughly 2 minutes to complete a sell.
def Strat1(symbol, qty, interval, entried=False):
    trend_data = []
    end_time = time.time() + 60*1  # How many minutes to build up the data for before starting to trade.
    while time.time() < end_time:
        # Read in the data
        df = GetMinuteData(symbol, '1m', interval)
        performance = (df.Close.pct_change() + 1).cumprod() - 1
        trend = (df.Close.tail(5))
        diff = trend[-1] / trend[0]
        trend_data.append(diff)
        # print(pd.DataFrame(trend_data))
        time.sleep(10)

    # Buying condition
    if entried == False:
        average_trend = (trend_data[-1] + trend_data[-2] + trend_data[-3]) / 3
        print(len(trend_data))
        print(average_trend)
        print(performance[-1])

        if average_trend < 1.000:  # Change this value to alter the threshold
            order = client.order_market_buy(symbol=symbol,
                                            quantity=qty)
            print(order)
            entried = True
        else:
            print('No order placed.')

        # Place multiple orders per loop! Start with 1 first.
        '''
        if performance[-1] > 0.001: # Change this value to alter the threshold
            order = client.order_market_buy(symbol=symbol,
                                        quantity=qty)
            print(order)
            entried=True
        else:
            print('No order placed.')
'''

    # Selling condition
    if entried == True:
        while True:
            df = GetMinuteData(symbol, '1m', interval)
            sincebuy = df.loc[df.index > pd.to_datetime(
                order['transactTime'], unit='ms')]
            if len(sincebuy) > 0:
                sincebuy_returns = (sincebuy.Close.pct_change() + 1).cumprod() - 1
                # Sell if asset rises by more than 0.15% (This is minimum as otherwise fees get us) OR falls again by 0.15%
                if sincebuy_returns[-1] > 0.0015 or sincebuy_returns[-1] < -0.0015:
                    order = client.order_market_sell(symbol=symbol, quantity=qty)
                    print(order)
                    break
        print('Algorithm Complete. Thank you for choosing Goodall Logistics Ltd.')

    # Selling condition
# Testing algorithm
# Selling condition


# Buy sell single run.
Strat1(symbol='BTCGBP', qty=0.001, interval='30')
Strat1(symbol='ETHGBP', qty=0.01, interval='30')
Strat1(symbol='ADAGBP', qty=0.1, interval='30')


######################################### MAIN CURRENT STRATEGY 2022-10-11 #######################################################
# Run a strategry for 1 hours over and over tracking start GBP and END to see how much we make or loose with this strat.
Start_GBP = client.get_asset_balance(asset='GBP')
Start_BTC = client.get_asset_balance(asset='BTC')
print(Start_GBP)
print(Start_BTC)
final_time = time.time() + 60*60
while time.time() < final_time:
    Strat1(symbol='BTCGBP', qty=0.0008, interval='60')
# Only run after the Hour is complete.
End_GBP = client.get_asset_balance(asset='GBP')
End_BTC = client.get_asset_balance(asset='BTC')
print(End_GBP)
print(End_BTC)
###############################################################
