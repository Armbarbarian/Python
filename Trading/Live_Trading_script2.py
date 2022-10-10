import time
import pandas as pd
import sqlalchemy
from binance import Client
from binance import BinanceSocketManager

api_key = 'ktVeNaWZwqJSQadqieUCKhZvIlgNco4eu0tF9OOhCit6n4h48WdYEZJznFPFwnDQ'
api_secret = 'iMXWqiiYZPL1drhDHcinqVdO5QtRYIXAHMlvff6K3tW0l8YkVjpLX1oUJlrRymqw'

# set the key we have copied from Binance Account
client = Client(api_key, api_secret)

engine = sqlalchemy.create_engine('sqlite:///BTCUSDTstream.db')

# read in the SQP dataframe (needs to be continuously running in the background to trade this way.)
# - Read using the SQL engine built from previous
df = pd.read_sql('BTCUSDT', engine)
df
df.Price.plot(title='Most recent BTC / USD')


# Trend Following Strategy
# - If the crypto was rising by x % then Buy
# - Sell when profit is above 0.15% or loss is crossing -0.15%
def Strategy(entry, lookback, qty, entried=False):
    while True:
        df = pd.read_sql('BTCUSDT', engine)
        lookback_period = df.iloc[-lookback:]
        cumret = (lookback_period.Price.pct_change() +1).cumprod() - 1
        # Buying conditions
        if not entried:
            if cumret[cumret.last_valid_index()] > entry:
                buyorder = client.create_order(symbol='BTCUSDT',
                                            side='BUY',
                                            type='MARKET',
                                            quantity=qty)
                entried=True
                print(buyorder)
                break
        # Selling conditions
        if entried:
            while True:
                df = pd.read_sql('BTCUSDT', engine)
                sincebuy = df.loc[df.Time >
                                    pd.to_datetime(buyorder['transactTime'],
                                    unit='ms')]
                if len(sincebuy) > 1:
                    sincebuy_return = (sincebuy.Price.pct_change() +1).cumprod() - 1
                    last_entry = sincebuy_return[sincebuy_return.last_valid_index()]
                    if last_entry > 0.0001 or last_entry < -0.0001:
                        sellorder = client.create_order(symbol='BTCUSDT',
                                                    side='SELL',
                                                    type='MARKET',
                                                    quantity=qty)
                        print(sellorder)
                        break

# Call Strategy and place trade!
Strategy(0.001, 60, 0.001)
