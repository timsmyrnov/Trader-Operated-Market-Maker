class Inventory:
    def __init__(self) -> None:
        self.positions = {}

    def update(self, asset: str, qty: int) -> None:
        if asset not in self.positions:
            self.positions[asset] = 0
        self.positions[asset] += qty

    def get_position(self, asset: str) -> int:
        return self.positions.get(asset, 0)

    def net_exposure(self, prices: dict) -> float:
        exposure = 0.0
        for asset, qty in self.positions.items():
            price = prices.get(asset, 0.0)
            exposure += qty * price
        return exposure

    def __str__(self) -> str:
        return f"Inventory: {self.positions}"
