import pyupbit
import time
import datetime

access = "24KELbDjvwobesALxayW27PAUD7uEyGfqbZXlB4X"         
secret = "Jax4hRuExWgxWWUHbbFUpYGNfO7EBYxxySRoExT2"          

upbit = pyupbit.Upbit(access, secret)
print("autotrade start")


def get_target_price(ticker):
    df = pyupbit.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target

def get_yesterday_ma5(ticker):
    df = pyupbit.get_ohlcv(ticker)
    close = df['close']
    ma5 = close.rolling(window=5).mean()
    return ma5[-2]

def buy_crypto_currency(ticker):
    krw = upbit.get_balance(ticker)[2]
    orderbook = pyupbit.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']
    unit = krw/float(sell_price)
    upbit.buy_market_order(ticker, unit)

def sell_crypto_currency(ticker):
    unit = upbit.get_balance(ticker)[0]
    upbit.sell_market_order(ticker, unit)
    
now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
ma5 = get_yesterday_ma5("KRW-DOGE")
target_price = get_target_price("KRW-DOGE")


while True:
    now = datetime.datetime.now()
    if mid < now < mid + datetime.delta(second=10):
        target_price = get_target_price("KRW-DOGE")
        mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        ma5 = get_yesterday_ma5("KRW-DOGE")
        sell_crypto_currency("KRW-DOGE")

    currnet_price = pyupbit.get_current_price("KRW-DOGE")
    if (currnet_price > target_price) and (currnet_price > ma5):
        buy_crypto_currency("KRW-DOGE")
    
    time.sleep(1)
