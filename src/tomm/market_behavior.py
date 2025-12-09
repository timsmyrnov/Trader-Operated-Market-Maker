import random
import tomm.macro_events as me

def generate_market_tick(curr_prices: dict, mu=0.0001, sigma=0.003):
    new_prices = curr_prices.copy()

    for sym in new_prices:
        # Geometric Brownian motion
        new_prices[sym] *= (1 + random.gauss(mu, sigma))

    return new_prices

def generate_market_fluctuation(curr_prices: dict, event: tuple):
    event_name, magnitude = event
    sign = 1 if event_name in me.positive_events else -1
    base_move = 0.05
    spread = 0.2

    print(
        f"\n"
        f"\033[92m" if sign == 1 else f"\033[91m",
        end=""
    )
    print()
    print(f"--- MARKET EVENT: {event_name.replace('_', ' ').title()} ---")
    print(f"Impact Magnitude: {sign * magnitude:+.2f}\033[0m\n")

    new_prices = {}

    for sym, price in curr_prices.items():
        pct_change = sign * magnitude * random.uniform(1 - spread, 1 + spread) * base_move
        new_price = price * (1 + pct_change)
        new_prices[sym] = new_price
        print(f"{sym}: {price:.2f} → {new_price:.2f} ({pct_change * 100:+.2f}%)")

    return new_prices
