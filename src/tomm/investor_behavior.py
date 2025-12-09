import random
import time
from orders import Order

def order(symbol: str, data: dict) -> Order:
    min_qty = 100
    max_qty = 1000

    side = random.choice(['BUY', 'SELL'])
    qty = random.randint(min_qty, max_qty)

    return Order(side, symbol, order_type='MARKET', qty=qty)

if __name__ == '__main__':
    print(order('MSFT', {'AAPL': 101, 'MSFT': 201}))
