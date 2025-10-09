import matplotlib.pyplot as plt
import market_behavior as mb

def simulate_path(start_prices: dict, steps: int) -> list:
    prices = start_prices.copy()
    path = []

    for _ in range(steps):
        prices = mb.generate_market_tick(prices)
        path.append(prices['AAPL'])

    return path

init_price = {'AAPL': 201.00}
steps = 365
paths = [simulate_path(init_price, steps) for _ in range(50)]

x = range(steps)
for path in paths:
    plt.plot(x, path)

plt.xlabel("Tick")
plt.ylabel("AAPL Price")
plt.title("Simulated AAPL Price Fluctuation")
plt.show()