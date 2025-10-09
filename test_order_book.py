from orders import Order
from quotes import Quote
from order_book import OrderBook

def print_state(book: OrderBook, title: str):
    print(book, '\n', title)
    print(f"TOB: {book.get_tob()}")

def test_order_matching():
    book = OrderBook()

    print("\n--- Test 1: Adding initial resting orders ---")
    book.handle_order(Order('SELL', 'AAPL', 'LIMIT', price=101.00, qty=100, src='mm'))
    book.handle_order(Order('BUY',  'AAPL', 'LIMIT', price=100.50, qty=100, src='indv'))
    print_state(book, "Initial book")

    print("\n--- Test 2: Aggressive BUY crosses the best ask ---")
    buy_order = Order('BUY', 'AAPL', 'LIMIT', price=101.00, qty=60, src='hft')
    book.handle_order(buy_order)
    print_state(book, "After aggressive buy @101.00 x60")

    print("\n--- Test 3: Partial fill and remainder resting ---")
    buy_order = Order('BUY', 'AAPL', 'LIMIT', price=101.00, qty=100, src='indv')
    book.handle_order(buy_order)
    print_state(book, "After partial fill buy @101.00 x100")

    print("\n--- Test 4: Aggressive SELL eats multiple bid levels ---")
    sell_order = Order('SELL', 'AAPL', 'LIMIT', price=100.40, qty=150, src='mm')
    book.handle_order(sell_order)
    print_state(book, "After aggressive sell @100.40 x150")

    print("\n--- Test 5: Adding quotes ---")
    q = Quote(100.60, 100.85, 500, 300, 'AAPL')
    book.handle_quote(q)
    print_state(book, "After quote injection (100.60 / 100.85)")

    print("\n--- Test 6: Non-crossing BUY should rest ---")
    book.handle_order(Order('BUY', 'AAPL', 'LIMIT', price=100.70, qty=50, src='indv'))
    print_state(book, "After resting buy @100.70 x50")

if __name__ == "__main__":
    test_order_matching()