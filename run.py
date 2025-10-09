import time
import random
import yfinance as yf
import fetch_market_data as fmd
import order_book as ob
import market_behavior as mb
import investor_behavior as ib
import market_maker as mm
import macro_events as me

orders_per_tick = 1
quotes_per_tick = 4
tick_rate = 0.2 # s
macro_event_rarity = 20 # 1/N

def run_simulation():
    AAPL_order_book = ob.OrderBook()
    market_maker = mm.MarketMaker()
    prices = fmd.download_latest_data(["AAPL", "MSFT", "GOOG", "NFLX", "TSLA"])
    ticker = "AAPL"

    while True:
        prices = mb.generate_market_tick(prices)

        if random.randint(1, macro_event_rarity) == 1:
            macro_event = random.choice([me.generate_positive_event, me.generate_negative_event])()
            prices = mb.generate_market_fluctuation(prices, macro_event)
            print()

        for _ in range(quotes_per_tick):
            new_quote = market_maker.quote(ticker, prices)
            AAPL_order_book.handle_quote(new_quote)
            print(new_quote)

        for _ in range(orders_per_tick):
            new_order = ib.order(ticker, prices)
            AAPL_order_book.handle_order(new_order)
            print(new_order)

        time.sleep(tick_rate)

if __name__ == "__main__":
    print(run_simulation())