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
x = client.get_asset_balance(asset='BTC')


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

# Define the strategy
# - Buy if the asset fell by more than 0.2% (this is x, find this to adjust) within last 30 mins
# - Sell if asset rises by more than 0.15% (This is minimum as otherwise fees get us) OR falls again by 0.15%

# df
# df.plot()
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

while True:
    try:
        SellOnly('ETHGBP', 0.0199, '10')
        time.sleep(5)
    except:
        print('No more coin...')
        break


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

# STRAT 4 is simply buy right away and hold until the price rises by x
# This seems full proof.


##################################################################

# Plotting the current trend under the current strat.
# Place Trades Based off the Vis function plot. If they look good then run it manually.

def Strat4(symbol_list, interval, entried=False):
    trend_data1 = []
    trend_data2 = []
    trend_data3 = []
    end_time = time.time() + 60*1  # How many minutes to build up the data for before starting to trade.
    while True:
        # Read in the data
        df1 = GetMinuteData(symbol_list[0], '1m', interval)
        #df2 = GetMinuteData(symbol_list[1], '1m', interval)
        #df3 = GetMinuteData(symbol_list[2], '1m', interval)
        performance1 = (df1.Open.pct_change() + 1).cumprod() - 1
        #performance2 = (df2.Open.pct_change() + 1).cumprod() - 1
        #performance3 = (df3.Open.pct_change() + 1).cumprod() - 1
        trend1 = (df1.Open.tail(5))
        #trend2 = (df2.Open.tail(5))
        #trend3 = (df3.Open.tail(5))
        diff1 = trend1[-1] / trend1[0]
        #diff2 = trend2[-1] / trend2[0]
        #diff3 = trend3[-1] / trend3[0]
        trend_data1.append(diff1)
        # trend_data2.append(diff2)
        # trend_data3.append(diff3)
        # print(pd.DataFrame(trend_data))
        # Buying condition
        if entried == False:
            print(performance1[-1])
            if performance1[-1] > 0.0023:  # if last entry is below 0.1%, then place order
                order1 = client.order_market_buy(symbol=symbol_list[0],
                                                 quantity=0.01)
                # order2 = client.order_market_buy(symbol=symbol_list[1],quantity = 0.001)
                # order3 = client.order_market_buy(symbol=symbol_list[2], quantity=0.1)
                print('Buy Order Filled!')
                print(order1)
                # print(order2)
                # print(order3)
                entried = True
                time.sleep(2)
                print('Transfering to Sales Department...')
            else:
                print('Chose not to buy. You are welcome.')
                time.sleep(2)
        if entried == True:
            while True:
                df1 = GetMinuteData(symbol_list[0], '1m', interval)
                # df2 = GetMinuteData(symbol_list[1], '1m', interval)
                # df3 = GetMinuteData(symbol_list[2], '1m', interval)

                sincebuy1 = df1.loc[df1.index > pd.to_datetime(
                    order1['transactTime'], unit='ms')]
                '''
                sincebuy2 = df2.loc[df2.index > pd.to_datetime(
                    order2['transactTime'], unit='ms')]
                sincebuy3 = df3.loc[df3.index > pd.to_datetime(
                    order3['transactTime'], unit='ms')]
                    '''
                # Sell if asset rises by more than 0.15% (This is minimum as otherwise fees get us) OR falls again by 0.15%
                if len(sincebuy1) > 0:
                    sincebuy_returns1 = (sincebuy1.Open.pct_change() + 1).cumprod() - 1
                    try:
                        if sincebuy_returns1[-1] > 0.0003 or sincebuy_returns1[-1] < -0.003:
                            sell1 = client.order_market_sell(symbol=symbol_list[0], quantity=0.01)
                            print('SOLD' + symbol_list[0])
                            print(sell1)
                            entried = False
                            break
                    except:
                        continue
                        print(sincebuy_returns1[-1])

                    '''
                if len(sincebuy2) > 0:
                    sincebuy_returns2 = (sincebuy2.Open.pct_change() + 1).cumprod() - 1
                    try:
                        print(sincebuy_returns2[-1])
                        if sincebuy_returns2[-1] > 0.0003 or sincebuy_returns2[-1] < -0.0015:
                            sell2 = client.order_market_sell(symbol=symbol_list[1], quantity=0.001)
                            print('SOLD' + symbol_list[1])
                            print(sell2)
                            break
                    except:
                        continue
                    '''


'''
                if len(sincebuy3) > 0:
                    sincebuy_returns3 = (sincebuy3.Open.pct_change() + 1).cumprod() - 1
                    try:
                        print(sincebuy_returns3[-1])
                        if sincebuy_returns3[-1] > 0.0003 or sincebuy_returns1[-1] < -0.0015:
                            sell3 = client.order_market_sell(symbol=symbol_list[2], quantity=0.1)
                            print('SOLD' + symbol_list[2])
                            print(sell3)
                            break
                    except:
                        continue
'''

######################################### MAIN CURRENT STRATEGY 2022-10-11 #######################################################
# Run a strategry for 1 hours over and over tracking start GBP and END to see how much we make or loose with this strat.
Start_GBP = client.get_asset_balance(asset='GBP')
Start_ETH = client.get_asset_balance(asset='ETH')
print(Start_ETH)
print(Start_GBP)

'''
# Min needed for the trade to even take place
info1 = client.get_symbol_info('ETHGBP')
print(info1['filters'][2]['minQty'])
info2 = client.get_symbol_info('BTCGBP')
print(info2['filters'][2]['minQty'])
info3 = client.get_symbol_info('BNBGBP')
print(info3['filters'][2]['minQty'])'''


'''
# EXECUTE SCHEME
final_time = time.time() + 60*60
while time.time() < final_time:
    Strat4(symbol_list=['ETHGBP'], interval='20m')
'''
# Only run after the Hour is complete.
End_GBP = client.get_asset_balance(asset='GBP')
End_ETH = client.get_asset_balance(asset='ETH')
print(End_ETH)
print(End_GBP)


######################################################


# strat 5
# SIMPLY LOOK AT PRICE
temp_list = []
try:
    for i in range(5):
        last_datapoint = GetMinuteData('ETHGBP', '1m', '1m')
        temp_list.append(last_datapoint)
        print(pd.DtataFrame(temp_list))
        time.sleep(15)
except:
    print(temp_list)
    'Finished'


print(df1.loc[df1.Open > 1097])
for i in df1:
    if df1.Open > 1090:
        print('Up')
    else:
        print('Low')


##################################################################

# Plotting the current trend under the current strat.
# Place Trades Based off the Vis function plot. If they look good then run it manually.

def Strat5(symbol_list, interval, entried=False):
    trend_data1 = []
    trend_data2 = []
    trend_data3 = []
    end_time = time.time() + 60*1  # How many minutes to build up the data for before starting to trade.
    while True:
        # Read in the data
        df1 = GetMinuteData(symbol_list[0], '1m', interval)
        #df2 = GetMinuteData(symbol_list[1], '1m', interval)
        #df3 = GetMinuteData(symbol_list[2], '1m', interval)
        performance1 = (df1.Open.pct_change() + 1).cumprod() - 1
        #performance2 = (df2.Open.pct_change() + 1).cumprod() - 1
        #performance3 = (df3.Open.pct_change() + 1).cumprod() - 1
        trend1 = (df1.Open.tail(5))
        #trend2 = (df2.Open.tail(5))
        #trend3 = (df3.Open.tail(5))
        diff1 = trend1[-1] / trend1[0]
        #diff2 = trend2[-1] / trend2[0]
        #diff3 = trend3[-1] / trend3[0]
        trend_data1.append(diff1)
        # trend_data2.append(diff2)
        # trend_data3.append(diff3)
        # print(pd.DataFrame(trend_data))
        # Buying condition
        if entried == False:
            print(performance1[-1])
            if performance1[-1] > 0.0023:  # if last entry is below 0.1%, then place order
                order1 = client.order_market_buy(symbol=symbol_list[0],
                                                 quantity=0.01)
                # order2 = client.order_market_buy(symbol=symbol_list[1],quantity = 0.001)
                # order3 = client.order_market_buy(symbol=symbol_list[2], quantity=0.1)
                print('Buy Order Filled!')
                print(order1)
                # print(order2)
                # print(order3)
                entried = True
                time.sleep(2)
                print('Transfering to Sales Department...')
            else:
                print('Chose not to buy. You are welcome.')
                time.sleep(2)
        if entried == True:
            while True:
                df1 = GetMinuteData(symbol_list[0], '1m', interval)
                # df2 = GetMinuteData(symbol_list[1], '1m', interval)
                # df3 = GetMinuteData(symbol_list[2], '1m', interval)

                sincebuy1 = df1.loc[df1.index > pd.to_datetime(
                    order1['transactTime'], unit='ms')]
                '''
                sincebuy2 = df2.loc[df2.index > pd.to_datetime(
                    order2['transactTime'], unit='ms')]
                sincebuy3 = df3.loc[df3.index > pd.to_datetime(
                    order3['transactTime'], unit='ms')]
                    '''
                # Sell if asset rises by more than 0.15% (This is minimum as otherwise fees get us) OR falls again by 0.15%
                if len(sincebuy1) > 0:
                    sincebuy_returns1 = (sincebuy1.Open.pct_change() + 1).cumprod() - 1
                    try:
                        if sincebuy_returns1[-1] > 0.0003 or sincebuy_returns1[-1] < -0.003:
                            sell1 = client.order_market_sell(symbol=symbol_list[0], quantity=0.01)
                            print('SOLD' + symbol_list[0])
                            print(sell1)
                            entried = False
                            break
                    except:
                        continue
                        print(sincebuy_returns1[-1])

                    '''
                if len(sincebuy2) > 0:
                    sincebuy_returns2 = (sincebuy2.Open.pct_change() + 1).cumprod() - 1
                    try:
                        print(sincebuy_returns2[-1])
                        if sincebuy_returns2[-1] > 0.0003 or sincebuy_returns2[-1] < -0.0015:
                            sell2 = client.order_market_sell(symbol=symbol_list[1], quantity=0.001)
                            print('SOLD' + symbol_list[1])
                            print(sell2)
                            break
                    except:
                        continue
                    '''


'''
                if len(sincebuy3) > 0:
                    sincebuy_returns3 = (sincebuy3.Open.pct_change() + 1).cumprod() - 1
                    try:
                        print(sincebuy_returns3[-1])
                        if sincebuy_returns3[-1] > 0.0003 or sincebuy_returns1[-1] < -0.0015:
                            sell3 = client.order_market_sell(symbol=symbol_list[2], quantity=0.1)
                            print('SOLD' + symbol_list[2])
                            print(sell3)
                            break
                    except:
                        continue
'''
