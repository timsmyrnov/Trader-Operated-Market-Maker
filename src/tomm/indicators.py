import pandas as pd

def compute_sma(data: pd.DataFrame, interval: int) -> list:
    # Compute initial sum based on window size (interval)
    price_sum = sum(data['Close'].iloc[:interval])

    sma_list = []

    for i in range(interval, len(data)):
        sma_list.append(round(float(price_sum / interval), 2))

        u_bound = data['Close'].iloc[i]
        l_bound = data['Close'].iloc[i - interval]

        price_sum = price_sum + u_bound - l_bound

    return sma_list

def compute_rsi(data: pd.DataFrame, interval: int) -> list:
    gain_pct = []
    loss_pct = []

    for i in range(1, interval + 1):
        pct_change = float((data['Close'].iloc[i] - data['Close'].iloc[i-1]) / data['Close'].iloc[i-1] * 100)

        gain_pct.append(pct_change if pct_change > 0 else 0)
        loss_pct.append(abs(pct_change) if pct_change < 0 else 0)

    avg_gain = sum(gain_pct) / interval
    avg_loss = sum(loss_pct) / interval

    rsi_list = [100] if avg_loss == 0 else [round(100 - 100 / (1 + avg_gain / avg_loss), 2)]

    for j in range(interval + 1, len(data)):
        curr_pct_change = float((data['Close'].iloc[j] - data['Close'].iloc[j-1]) / data['Close'].iloc[j-1] * 100)

        # Wilder's smoothing
        if curr_pct_change > 0:
            avg_gain = (avg_gain * (interval - 1) + curr_pct_change) / interval
            avg_loss = (avg_loss * (interval - 1) + 0) / interval

        elif curr_pct_change < 0:
            avg_loss = (avg_loss * (interval - 1) + abs(curr_pct_change)) / interval
            avg_gain = (avg_gain * (interval - 1) + 0) / interval

        rsi_list.append(100) if avg_loss == 0 else rsi_list.append(round(100 - 100 / (1 + avg_gain / avg_loss), 2))

    return rsi_list

def compute_atr(data: pd.DataFrame, interval: int) -> list:
    tr_sum = 0

    for i in range(1, interval + 1):
        tr = max(
            data['High'].iloc[i] - data['Low'].iloc[i],
            abs(data['High'].iloc[i] - data['Close'].iloc[i-1]),
            abs(data['Low'].iloc[i] - data['Close'].iloc[i-1])
        )
        tr_sum += tr

    atr = round(float(tr_sum / interval), 2)
    atr_list = [atr]

    for j in range(interval + 1, len(data)):
        curr_tr = max(
            data['High'].iloc[j] - data['Low'].iloc[j],
            abs(data['High'].iloc[j] - data['Close'].iloc[j-1]),
            abs(data['Low'].iloc[j] - data['Close'].iloc[j-1])
        )

        # Wilder's smoothing
        atr = round(float((atr * (interval - 1) + curr_tr) / interval), 2)
        atr_list.append(atr)

    return atr_list
