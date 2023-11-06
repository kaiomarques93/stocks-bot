from screener.finviz_scanner import FinvizScanner
from django.utils import timezone
import ta
from kaiostocks import data_treatment
from strategies.buy_strategies import bubz_strategy_buy, bubz01
import datetime
import pytz
import pandas as pd
from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
import alpaca_trade_api as tradeapi
import contextlib
import warnings
warnings.filterwarnings("ignore")


API_KEY = 'PKK6ZVM86CAK72CBMLSO'
API_SECRET = 'YodQAQtpneaDWjZzdUi7fJmjrXNTRfeu2IvjhKaP'
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v2')

list_stratetiges = [bubz_strategy_buy, bubz01]
strategy_index = 1
chosen_strategy = list_stratetiges[strategy_index]


def get_symbols():
    url = 'https://finviz.com/screener.ashx?v=111&f=sh_curvol_o200,sh_float_u50,sh_price_u20,sh_relvol_o1,ta_change_u,ta_changeopen_u,ta_perf_1wup&ft=4&o=-change'
    finviz = FinvizScanner(url)
    df_finviz = finviz.get_tables()
    df_finviz = df_finviz[(df_finviz['Change'] >= 1) &
                          (df_finviz['Volume'] > 200000)]
    return df_finviz['Ticker'].to_list()


def modified_dict_resampled(tf, dict_df):

    for x in tf:
        df = dict_df[x]
        ppo = ta.momentum.PercentagePriceOscillator(df['close'])
        macd = ta.trend.MACD(df['close'], window_slow=10, window_fast=3)
        df['ppo'] = ppo.ppo()
        df['ppo_signal'] = ppo.ppo_signal()
        df['macd'] = macd.macd()
        df['signal'] = macd.macd_signal()
        df['diff'] = macd.macd_diff()
        df['MFI'] = ta.volume.money_flow_index(
            df['high'], df['low'], df['close'], df['volume'])
        df.dropna(inplace=True)
        dict_df[x] = df

    return dict_df


def get_dates(days):
    # Get current time minus 20 minutes
    current_time = datetime.datetime.now()
    past_time = current_time - datetime.timedelta(minutes=16)
    past_time_str = past_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    # Subtract `minutes` from past_time
    delta = datetime.timedelta(days=days)
    past_date = past_time - delta
    past_date_str = past_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return past_time_str, past_date_str


def shares_qty(close, equity, percentage_per_stock=0.1):
    return int((equity*percentage_per_stock)/close)


def run():
    tf = ['15T', '30T', '60T', '120T', '195T', 'D']
    clock = api.get_clock()
    list_positions = api.list_positions()
    portfolio_value = float(api.get_account().portfolio_value)
    symbols_to_buy = _extracted_from_run_10(
        list_positions, tf, portfolio_value)
    return {"res": symbols_to_buy}

# TODO Rename this here and in `run`


def _extracted_from_run_10(list_positions, tf, portfolio_value):
    try:
        symbols = get_symbols()
    except Exception:
        symbols = ['AAPL', 'AMZN']
    today, past_date = get_dates(140)
    positions = [x.symbol for x in list_positions]
    symbols = list(set(positions+symbols))
    bars = api.get_bars(symbols, TimeFrame(
        15, TimeFrameUnit.Minute), past_date, today, adjustment='raw').df
    ks = data_treatment()
    symbols_to_buy = []
    mfi_dict = {}
    for symbol in symbols:
        df = bars[bars['symbol'] == symbol]
        dict_df = ks.resampled_data_ind(tf, df)
        dict_df = modified_dict_resampled(tf, dict_df)
        try:
            buy_condition = chosen_strategy(tf, dict_df)
            close = df['close'].iloc[-1]
            mfi_dict[symbol] = dict_df['30T']['MFI'].iloc[-1]
            qty = shares_qty(close, portfolio_value)
            if buy_condition:
                symbols_to_buy.append(symbol)
                # buy_ticker(symbol, qty, close, positions)
        except Exception:
            continue

    return symbols_to_buy
