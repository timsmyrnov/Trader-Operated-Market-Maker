import keyboard

class HeadTrader:
    def __init__(self):
        self.spread_multiplier = 1.0
        self.bias = 0

        keyboard.add_hotkey('s', self.increase_spread)
        keyboard.add_hotkey('d', self.decrease_spread)
        keyboard.add_hotkey('1', lambda: self.set_bias(-1))
        keyboard.add_hotkey('2', lambda: self.set_bias(0))
        keyboard.add_hotkey('3', lambda: self.set_bias(1))

    def increase_spread(self):
        self.spread_multiplier += 0.1
        print(f"[HeadTrader] Spread increased → {self.spread_multiplier:.2f}")

    def decrease_spread(self):
        self.spread_multiplier = max(0.1, self.spread_multiplier - 0.1)
        print(f"[HeadTrader] Spread decreased → {self.spread_multiplier:.2f}")

    def set_bias(self, val):
        self.bias = val
        print(f"[HeadTrader] Bias set → {val}")

    def get_instructions(self):
        return {
            "spread_multiplier": self.spread_multiplier,
            "bias": self.bias,
        }
