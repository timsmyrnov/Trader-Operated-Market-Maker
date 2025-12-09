# TOMM – Trader Operated Market Maker

TOMM is a limit‐order–book (LOB) and market-microstructure framework. It provides:

- A price–time–priority **limit order book**
- A parametric **market maker** quoting around a mid price
- Stochastic **order-flow models** for investors
- Stylised **macro shocks** applied to an asset universe
- Utilities for:
  - Historical data acquisition (via `yfinance`)
  - Technical indicator computation (SMA, RSI, ATR, with EMA to be implemented)
  - Cross-asset conditional correlation / “heatmap” construction (via `xbbg`)
  - Simple price-path and book visualization

The intent is to have a compact codebase suitable for experimentation, teaching, and prototyping of LOB-level ideas.

---

## Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/timsmyrnov/Trader-Operated-Market-Maker.git
cd Trader-Operated-Market-Maker
pip install -r requirements.txt
pip install -e .
```

### Example: `run.py` in action

The screenshot below shows a short extract of the main simulation loop:

- colored **MM quotes** hitting the book on every tick  
- **investor market orders** interacting with those quotes  
- a generated **macro event** (“Favorable Policy Announcement”) with an impact
  magnitude  
- the post-event **repricing** of the whole symbol universe

[![Terminal snapshot of TOMM run loop with quotes, retail orders, and a macro event](https://i.postimg.cc/kMKYzyBt/Screenshot-2025-12-09-at-00-20-35.png)](https://postimg.cc/Z0YLypPT)


## Repository Layout

Top-level structure:

```text
/
├── .gitignore
├── pyproject.toml
├── README.md
├── requirements.txt
└── src/
    ├── tests/
    │   └── test_order_book.py
    └── tomm/
        ├── fetch_market_data.py
        ├── head_trader.py
        ├── heatmap_builder.py
        ├── indicators.py
        ├── inventory.py
        ├── investor_behavior.py
        ├── macro_events.py
        ├── market_behavior.py
        ├── market_maker.py
        ├── order_book_viz.py
        ├── order_book.py
        ├── orders.py
        ├── price_paths_viz.py
        ├── quotes.py
        └── run.py
