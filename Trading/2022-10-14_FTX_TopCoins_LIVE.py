import requests
import pandas as pd

r = requests.get('https://ftx.com/api/markets')

df = pd.DataFrame(r.json()['result'])

# Clean the data to filter out what we don't need.
df.index = df.name
spot_df = df[df.type == 'spot']
spot_df = spot_df[spot_df.tokenizedEquity.isna()]
spot_df = spot_df[spot_df.isEtfMarket == False]
spot_df = spot_df[spot_df.quoteCurrency == 'USD']

Tradable_crypto_list = spot_df.index.tolist()
Tradable_crypto_list


# See how well the markets are doing over 24 and 1 hours.
# historical data over 1 - 24 hours
best_worst_24h = pd.DataFrame(spot_df.change24h.sort_values(ascending=False))
best_24h.head(10).plot(kind='bar')

best_worst_1h = pd.DataFrame(spot_df.change1h.sort_values(ascending=False))
best_1h.head(10).plot()

# What are the realtime movements over the last 1 - 10 minutes
# which one is moving the fastest and compare
# build web socket stream of multi coins, store and track performance (how we do binance is the same thing.)


df1 = GetMinuteData(symbol, '1m', interval)
sincebuy1 = df1.loc[df1.index > pd.to_datetime(
    order1['transactTime'], unit='ms')]  # convert timestamp

# Sell if asset rises by more than 0.15% (This is minimum as otherwise fees get us) OR falls again by 0.15%

if len(sincebuy1) > 0:
    sincebuy_returns1 = (sincebuy1.Open.pct_change() + 1).cumprod() - 1
    try:
        if sincebuy_returns1[-1] > 0.0003:
            print('YES')
    except:
        print('NO')
