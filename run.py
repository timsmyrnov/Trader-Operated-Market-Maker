import time
import random
import yfinance as yf
import fetch_market_data as fmd
import order_book as ob
import market_behavior as mb
import investor_behavior as ib
import market_maker as mm
import macro_events as me

def run_simulation():
    AAPL_order_book = ob.OrderBook()
    market_maker = mm.MarketMaker()
    prices = fmd.download_latest_data(["AAPL", "MSFT", "GOOG", "NFLX", "TSLA"])
    ticker = "AAPL"

    while True:
        # Generate quotes
        # Generate orders
        # Generate macro events
        # Generate stock price movement
        # Simulate mm behavior

        prices = mb.generate_market_tick(prices)

        if random.randint(1, 20) == 1:
            macro_event = random.choice([me.generate_positive_event, me.generate_negative_event])()
            prices = mb.generate_market_fluctuation(prices, macro_event)
            print()

        new_quote = market_maker.quote(ticker, prices)
        new_order = ib.order(ticker, prices)

        AAPL_order_book.handle_quote(new_quote)
        AAPL_order_book.handle_order(new_order)

        print(new_quote)
        print(new_order)

        time.sleep(0.2)

if __name__ == "__main__":
    print(run_simulation())