import itertools

_quote_id_generator = itertools.count(1)

def generate_quote_id() -> int:
    return next(_quote_id_generator)

class Quote:
    def __init__(self, bid: float, ask: float, bid_size: int, ask_size: int, symbol: str, src: str = 'mm') -> None:
        symbol = symbol.upper()
        src = src.lower()

        if bid >= ask:
            raise ValueError('Bid must be less than Ask.')
        if bid_size <= 0 or ask_size <= 0:
            raise ValueError('Bid size and Ask size must be greater than 0.')

        self.bid = bid
        self.ask = ask
        self.bid_size = bid_size
        self.ask_size = ask_size
        self.symbol = symbol
        self.src = src
        self.id = generate_quote_id()

    def spread(self) -> float:
        return self.ask - self.bid

    def mid_price(self) -> float:
        return (self.bid + self.ask) / 2

    def update(self, bid: float, ask: float, bid_size: int, ask_size: int) -> None:
        if bid >= ask:
            raise ValueError('Bid must be less than Ask.')
        if bid_size <= 0 or ask_size <= 0:
            raise ValueError('Bid size and Ask size must be greater than 0.')

        self.bid = bid
        self.ask = ask
        self.bid_size = bid_size
        self.ask_size = ask_size

    def __str__(self) -> str:
        return (
            f'\033[96m#{self.id:<4}\033[0m  '
            f'\033[91m{self.bid:<7.2f}\033[0m / '
            f'\033[94m{self.ask:<7.2f}\033[0m  '
            f'\033[95m{self.bid_size:<4}\033[0m x '
            f'\033[92m{self.ask_size:<4}\033[0m '
            f'\033[90m[{self.symbol}]\033[0m '
            f'\033[94m{self.src:<4}\033[0m'
        )

if __name__ == '__main__':
    quotes = [
        Quote(99.50, 99.55, 500, 300, 'AAPL'), Quote(100.00, 100.05, 1000, 800, 'AAPL'),
        Quote(100.20, 100.30, 200, 150, 'AAPL'), Quote(99.75, 99.85, 750, 500, 'AAPL'),
        Quote(101.10, 101.25, 100, 50, 'AAPL'), Quote(98.90, 99.10, 600, 700, 'AAPL'),
        Quote(100.45, 100.50, 350, 350, 'AAPL'), Quote(101.75, 101.80, 150, 120, 'AAPL'),
        Quote(102.00, 102.15, 90, 200, 'AAPL'),  Quote(99.00, 99.20, 1000, 1000, 'AAPL')
    ]

    for q in quotes:
        print(q)