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
socket = bsm.trade_socket('BTCGBP')

# Test if the account is reachable
client.get_account()

# Price data
await socket.__aenter__()
msg = await socket.recv()

# dataframe of the price data to append to a df
def CreateFrame(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:,['s','E','p']]
    df.columns = ['symbol','Time','Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')
    return df

CreateFrame(msg)

# Append the live data to SQL database using sqlalchemy
engine = sqlalchemy.create_engine('sqlite:///BTCGBPstream.db')

while True:
    await socket.__aenter__()
    new_msg = await socket.recv()
    new_frame = CreateFrame(new_msg)
    new_frame.to_sql('BTCGBP', engine, if_exists='append', index=False)
    #print(frame)
