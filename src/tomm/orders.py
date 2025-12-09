import itertools

_order_id_generator = itertools.count(1)

def generate_order_id() -> int:
    return next(_order_id_generator)

class Order:
    def __init__(self, side: str, symbol: str, order_type: str, *, price: float | None = None, qty: int, src: str = 'indv'):
        side = side.upper()
        order_type = order_type.upper()
        symbol = symbol.upper()
        src = src.lower()

        if qty <= 0:
            raise ValueError('Quantity must be greater than 0.')
        if side not in {'BUY', 'SELL'}:
            raise ValueError('Side must be "BUY" or "SELL".')
        if order_type not in {'LIMIT', 'MARKET'}:
            raise ValueError('Order type must be "LIMIT" or "MARKET".')
        if order_type == 'LIMIT' and price is None:
            raise ValueError('Limit orders must include a price.')
        if order_type == 'MARKET' and price is not None:
            print('Warning: Market order received with a price. Ignoring it.')
            price = None

        self.side = side
        self.symbol = symbol
        self.order_type = order_type
        self.price = price
        self.qty = qty
        self.src = src
        self.id = generate_order_id()

    def __str__(self) -> str:
        symbol_tag = f'[{self.symbol}]'
        color_side = '\033[92m' if self.side == 'BUY' else '\033[91m'
        price_str = f'${self.price:<7.2f}' if self.price is not None else 'MKT     '
        return (
            f'\033[96m#{self.id:<4}\033[0m  '
            f'{color_side}{self.side:<5}\033[0m '
            f'\033[93m{self.qty:<5}\033[0m @ '
            f'\033[95m{price_str}\033[0m '
            f'\033[90m{symbol_tag:<8}\033[0m'
            f'\033[94m{self.src:<4}\033[0m  '
            f'\033[90m{self.order_type}\033[0m'
        )

if __name__ == '__main__':
    orders = [
        Order('BUY', 'AAPL', 'LIMIT', price=99.50, qty=500), Order('SELL', 'AAPL', 'MARKET', qty=300),
        Order('BUY', 'AAPL', 'LIMIT', price=100.00, qty=1000), Order('SELL', 'AAPL', 'LIMIT', price=100.05, qty=800),
        Order('BUY', 'AAPL', 'MARKET', qty=200), Order('SELL', 'AAPL', 'LIMIT', price=100.30, qty=150),
        Order('BUY', 'AAPL', 'MARKET', qty=750), Order('SELL', 'AAPL', 'LIMIT', price=99.85, qty=500),
        Order('BUY', 'AAPL', 'MARKET', qty=100), Order('SELL', 'AAPL', 'MARKET', qty=50),
    ]

    for o in orders:
        print(o)
