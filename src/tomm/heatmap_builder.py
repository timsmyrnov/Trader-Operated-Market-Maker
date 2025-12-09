import numpy as np
import pandas as pd
from xbbg import blp

class HeatmapBuilder:
    def __init__(self, assets: list[str]) -> None:
        self.assets = assets
        self._vol_cache = {}
        self._lq_cache = {}
        # self._sprd_cache = {}

    def compute_values(
        self,
        start_date: str,
        end_date: str,
        vol_anomaly_pct: float = 0.9,
        lq_anomaly_pct: float = 0.9,
        # sprd_anomaly_pct: float = 0.9
    ) -> pd.DataFrame:
        matrix = []
        for asset_a in self.assets:
            curr_row = []

            for asset_b in self.assets:
                if asset_a == asset_b:
                    curr_row.append(1)
                else:
                    vol_corr = self.get_vol_corr(asset_a, asset_b, start_date, end_date, vol_anomaly_pct)
                    lq_corr = self.get_lq_corr(asset_a, asset_b, start_date, end_date, lq_anomaly_pct)
                    # sprd_corr = self.get_sprd_corr(asset_a, asset_b, start_date, end_date, sprd_anomaly_pct)
                    valid = [corr for corr in [
                        vol_corr,
                        lq_corr,
                        # sprd_corr
                    ] if not np.isnan(corr)]
                    norm_corr = np.mean(valid) if valid else np.nan
                    curr_row.append(norm_corr)

            matrix.append(curr_row)

        return pd.DataFrame(matrix, index=self.assets, columns=self.assets)

    def get_vol(self, asset: str, start_date: str, end_date: str) -> pd.Series:
        key = (asset, start_date, end_date)
        if key in self._vol_cache:
            return self._vol_cache[key]

        prices = blp.bdh(tickers=asset, flds='PX_LAST', start_date=start_date, end_date=end_date)

        if isinstance(prices.columns, pd.MultiIndex):
            price_series = prices[asset]['PX_LAST']
        else:
            price_series = prices['PX_LAST'] if 'PX_LAST' in prices.columns else prices[asset]

        returns = price_series.pct_change()
        vol = returns.rolling(window=7).std() * np.sqrt(252)

        self._vol_cache[key] = vol
        return vol

    # Amihud illiquidity ratio (classic)
    def get_lq(self, asset: str, start_date: str, end_date: str) -> pd.Series:
        key = (asset, start_date, end_date)
        if key in self._lq_cache:
            return self._lq_cache[key]

        data = blp.bdh(tickers=asset, flds=['PX_LAST', 'PX_VOLUME'], start_date=start_date, end_date=end_date)

        if isinstance(data.columns, pd.MultiIndex):
            try:
                price = data[asset]['PX_LAST']
                volume = data[asset]['PX_VOLUME']
            except KeyError:
                print(f"Skipping illiquidity calculation for {asset}: PX_VOLUME not available.")
                self._lq_cache[key] = pd.Series(dtype=float)
                return self._lq_cache[key]
        else:
            if 'PX_VOLUME' not in data.columns:
                print(f"Skipping illiquidity calculation for {asset}: PX_VOLUME not available.")
                self._lq_cache[key] = pd.Series(dtype=float)
                return self._lq_cache[key]
            price = data['PX_LAST']
            volume = data['PX_VOLUME']

        volume = volume.replace(0, np.nan)
        returns = price.pct_change().abs()
        illiq = returns / volume
        illiq = illiq.rolling(window=7).mean()

        self._lq_cache[key] = illiq
        return illiq

    # def get_sprd(self, asset: str, start_date: str, end_date: str) -> pd.Series:
    #     key = (asset, start_date, end_date)
    #     if key in self._sprd_cache:
    #         return self._sprd_cache[key]

    #     data = blp.bdh(tickers=asset, flds=['BID', 'ASK'], start_date=start_date, end_date=end_date)

    #     if isinstance(data.columns, pd.MultiIndex):
    #         try:
    #             bid = data[asset]['BID']
    #             ask = data[asset]['ASK']
    #         except KeyError:
    #             print(f"Skipping spread calculation for {asset}: data is not available.")
    #             self._sprd_cache[key] = pd.Series(dtype=float)
    #             return self._sprd_cache[key]
    #     else:
    #         if 'BID' not in data.columns or 'ASK' not in data.columns:
    #             print(f"Skipping spread calculation for {asset}: data is not available.")
    #             self._sprd_cache[key] = pd.Series(dtype=float)
    #             return self._sprd_cache[key]
    #         bid = data['BID']
    #         ask = data['ASK']

    #     bid = bid.replace(0, np.nan)
    #     ask = ask.replace(0, np.nan)
    #     sprd = ask - bid

    #     self._sprd_cache[key] = sprd
    #     return sprd

    def _get_cond_corr(
        self,
        series_a: pd.Series,
        series_b: pd.Series,
        anomaly_pct: float,
        label_a: str = 'a',
        label_b: str = 'b'
    ) -> float:
        threshold = series_a.quantile(anomaly_pct)
        anomaly_dates = pd.to_datetime(series_a[series_a > threshold].dropna().index)

        series_a_adjusted = series_a.reindex(anomaly_dates)
        series_b_adjusted = series_b.reindex(anomaly_dates)

        aligned = pd.concat([series_a_adjusted, series_b_adjusted], axis=1).dropna()
        aligned.columns = [label_a, label_b]

        if aligned.empty:
            print(f"Warning: No aligned data for {label_a} vs {label_b} on anomaly dates")
            return np.nan

        return aligned[label_a].corr(aligned[label_b])

    def get_vol_corr(self, asset_a: str, asset_b: str, start_date: str, end_date: str, anomaly_pct: float) -> float:
        vol_a = self.get_vol(asset_a, start_date, end_date)
        vol_b = self.get_vol(asset_b, start_date, end_date)

        return self._get_cond_corr(vol_a, vol_b, anomaly_pct, label_a='vol_a', label_b='vol_b')

    def get_lq_corr(self, asset_a: str, asset_b: str, start_date: str, end_date: str, anomaly_pct: float) -> float:
        lq_a = self.get_lq(asset_a, start_date, end_date)
        lq_b = self.get_lq(asset_b, start_date, end_date)

        return self._get_cond_corr(lq_a, lq_b, anomaly_pct, label_a='lq_a', label_b='lq_b')

    # def get_sprd_corr(self, asset_a: str, asset_b: str, start_date: str, end_date: str, anomaly_pct: float) -> float:
    #     sprd_a = self.get_sprd(asset_a, start_date, end_date)
    #     sprd_b = self.get_sprd(asset_b, start_date, end_date)

    #     return self._get_cond_corr(sprd_a, sprd_b, anomaly_pct, label_a='sprd_a', label_b='sprd_b')

    def _is_valid_series(self, series: pd.Series) -> bool:
        return isinstance(series, pd.Series) and not series.dropna().empty

    def clear_cache(self) -> None:
        self._vol_cache.clear()
        self._lq_cache.clear()
        # self._sprd_cache.clear()

if __name__ == '__main__':
    assets = [
        'SPY US Equity', 'QQQ US Equity', 'DIA US Equity', 'IWM US Equity',
        'LQD US Equity', 'HYG US Equity', 'TLT US Equity', 'SHY US Equity',
        'GLD US Equity', 'SLV US Equity', 'USO US Equity', 'UNG US Equity',
        'XLF US Equity', 'XLK US Equity', 'XLE US Equity', 'XLY US Equity',
        'JNJ US Equity', 'JPM US Equity', 'MS US Equity', 'AAPL US Equity'
    ]

    hb = HeatmapBuilder(assets)

    print(hb.compute_values('2024-01-01', '2024-12-01'))
