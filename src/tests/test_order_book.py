import unittest

from tomm.orders import Order
from tomm.quotes import Quote
from tomm.order_book import OrderBook

class TestOrderBookMatching(unittest.TestCase):
    def setUp(self) -> None:
        self.book = OrderBook()

    def _side_levels(self, side: str) -> dict[float, int]:
        if side not in {"bid", "ask"}:
            raise ValueError("side must be 'bid' or 'ask'")
        levels = self.book.bids if side == "bid" else self.book.asks
        return {price: sum(o.qty for o in dq) for price, dq in levels.items()}

    def assertBookSideEqual(self, side: str, expected: dict[float, int]) -> None:
        self.assertEqual(self._side_levels(side), expected, msg=f"Mismatch on {side} side")

    def test_order_matching_scenario(self):
        self.book.handle_order(Order("SELL", "AAPL", "LIMIT", price=101.00, qty=100, src="mm"))
        self.book.handle_order(Order("BUY", "AAPL", "LIMIT", price=100.50, qty=100, src="indv"))
        self.assertBookSideEqual("bid", {100.50: 100})
        self.assertBookSideEqual("ask", {101.00: 100})

        buy_order = Order("BUY", "AAPL", "LIMIT", price=101.00, qty=60, src="hft")
        self.book.handle_order(buy_order)
        self.assertBookSideEqual("bid", {100.50: 100})
        self.assertBookSideEqual("ask", {101.00: 40})

        buy_order = Order("BUY", "AAPL", "LIMIT", price=101.00, qty=100, src="indv")
        self.book.handle_order(buy_order)
        self.assertBookSideEqual("bid", {101.00: 60, 100.50: 100})
        self.assertBookSideEqual("ask", {})

        sell_order = Order("SELL", "AAPL", "LIMIT", price=100.40, qty=150, src="mm")
        self.book.handle_order(sell_order)
        self.assertBookSideEqual("bid", {100.50: 10})
        self.assertBookSideEqual("ask", {})

        q = Quote(100.60, 100.85, 500, 300, "AAPL")
        self.book.handle_quote(q)
        self.assertBookSideEqual("bid", {100.60: 500, 100.50: 10})
        self.assertBookSideEqual("ask", {100.85: 300})

        self.book.handle_order(Order("BUY", "AAPL", "LIMIT", price=100.70, qty=50, src="indv"))
        self.assertBookSideEqual("bid", {100.70: 50, 100.60: 500, 100.50: 10})
        self.assertBookSideEqual("ask", {100.85: 300})


if __name__ == "__main__":
    unittest.main()
