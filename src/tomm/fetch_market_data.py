from datetime import datetime
import yfinance as yf
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(exist_ok=True)

def download_latest_data(symbols: list) -> dict:
    if isinstance(symbols, str):
        symbols = [symbols]

    latest_prices = {}

    for sym in symbols:
        try:
            ticker = yf.Ticker(sym)
            data = ticker.history(period="1d")
            if not data.empty:
                latest_prices[sym] = float(data["Close"].iloc[-1])
            else:
                latest_prices[sym] = None
        except Exception:
            latest_prices[sym] = None

    return latest_prices

def download_all_time_single_stock_data(symbol: str, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.reset_index()

    data['Symbol'] = symbol
    data = data[['Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume']]

    numerical_columns = ['Open', 'High', 'Low', 'Close']
    data[numerical_columns] = data[numerical_columns].round(2)

    data.to_csv(f'{symbol}_market_data.csv', index=False)

def download_all_time_data():
    symbols = [
        "NVDA", "HTZ", "F", "INTC", "PLTR", "TSLA", "ABEV", "LCID", "BTG", "PFE",
        "AAL", "AAPL", "SXTC", "BAC", "SOFI", "RIG", "AMZN", "JBLU", "AGNC", "SMX",
        "MSGM", "APLD", "AMD", "NU", "GOOGL", "PBR", "NVO", "SNAP", "WBD", "HBAN",
        "AMCR", "VRN", "BBAI", "UNH", "TSM", "SMCI", "VALE", "ERIC", "BBD", "T",
        "LYG", "HOOD", "NGD", "NIO", "KMI", "KVUE", "AVGO", "HPE", "AGL", "UBER",
        "CMCSA", "CSX", "MRK", "WMT", "CLSK", "ITUB", "MSFT", "UUUU", "ACHR", "RIOT",
        "WOLF", "KO", "INFY", "MU", "QXO", "MP", "CNH", "GOLD", "KGC", "GOOG", "MARA",
        "FNA", "SCHW", "KEY", "WFC", "NKE", "TGL", "RF", "PTEN", "HIMS", "STLA",
        "SBSW", "HAL", "IAG", "XOM", "BABA", "AG", "GRAB"
    ]

    start_date = '2000-01-01'
    end_date = datetime.now().strftime('%Y-%m-%d')

    data = yf.download(symbols, start=start_date, end=end_date, group_by='symbol')
    combined_data = pd.DataFrame()

    for sym in symbols:
        temp_df = data[sym].reset_index()
        temp_df['Symbol'] = sym
        temp_df = temp_df[['Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume']]
        combined_data = pd.concat([combined_data, temp_df], ignore_index=True)

    numerical_columns = ['Open', 'High', 'Low', 'Close']
    combined_data[numerical_columns] = combined_data[numerical_columns].round(2)

    combined_data.to_csv(DATA_DIR / "market_data.csv", index=False)

if __name__ == '__main__':
    download_all_time_data()
