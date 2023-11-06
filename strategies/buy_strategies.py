def bubz_strategy_buy(tf, dict_df):
    cond_buy = []
    for x in tf:
        try:
            if x in ['15T', '60T', '120T', '195T']:
                df = dict_df[x]
                df['buy'] = (df['ttm'] > 0) & (df['macd'] > df['signal']) & (
                    df['macd'] > df['macd'].shift(1))
                dict_df[x] = df
                cond_buy.append(df['buy'].iloc[-1])
            elif x in ['30T']:
                df = dict_df[x]
                df['buy'] = (df['ttm'] > 0) & (df['macd'] > df['signal']) & (
                    df['macd'] > df['macd'].shift(1)) & (df['MFI'] < 90)
                dict_df[x] = df
                cond_buy.append(df['buy'].iloc[-1])
            elif x in ['W']:
                df = dict_df[x]
                df['buy'] = (df['rsi'] > df['rsi_avg'])
                dict_df[x] = df
                cond_buy.append(df['buy'].iloc[-1])
            elif x in ['D']:
                df = dict_df[x]
                df['buy'] = (df['ttm'] > 0) & (df['ppo'] > df['ppo_signal']) & (
                    df['close'] < df['upper_BB'])
                dict_df[x] = df
                cond_buy.append(df['buy'].iloc[-1])
        except Exception:
            continue
    return all(cond_buy)


def bubz01(tf, dict_df):
    cond_buy = []
    for x in tf:
        try:
            if x in ['60T', '120T']:
                df = dict_df[x]
                df['buy'] = (df['ttm'] > 0) & (df['macd'] > df['signal'])
                dict_df[x] = df
                cond_buy.append(df['buy'].iloc[-1])
            elif x in ['15', '30T', '195T']:
                df = dict_df[x]
                df['buy'] = (df['ttm'] > 0) & (df['MFI'] < 90)
                dict_df[x] = df
                cond_buy.append(df['buy'].iloc[-1])
            elif x in ['D']:
                df = dict_df[x]
                df['buy'] = (df['ttm'] > 0) & (
                    df['close'] > df['open']) & (df['obv'])
                dict_df[x] = df
                cond_buy.append(df['buy'].iloc[-1])
        except Exception:
            continue
    return all(cond_buy)
