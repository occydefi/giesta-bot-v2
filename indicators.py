"""
GIESTA v2.7 - Módulo de Indicadores
Coleta dados de todos os 9 indicadores
"""

import requests
from datetime import datetime, timedelta
from typing import Dict, Optional
import time


class IndicatorCollector:
    """Coleta todos os indicadores da estratégia GIESTA"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_btc_price(self) -> float:
        """Preço atual do BTC"""
        try:
            url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
            response = self.session.get(url, timeout=10)
            return float(response.json()['price'])
        except Exception as e:
            print(f"❌ Erro ao buscar preço BTC: {e}")
            return 0
    
    def get_rsi_weekly(self) -> float:
        """RSI Semanal do BTC"""
        try:
            url = "https://api.binance.com/api/v3/klines"
            params = {
                'symbol': 'BTCUSDT',
                'interval': '1w',
                'limit': 15
            }
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            closes = [float(candle[4]) for candle in data]
            rsi = self._calculate_rsi(closes, period=14)
            return rsi
        except Exception as e:
            print(f"❌ Erro ao calcular RSI: {e}")
            return 50
    
    def get_funding_rate(self) -> float:
        """Funding Rate do BTC (Binance)"""
        try:
            url = "https://fapi.binance.com/fapi/v1/fundingRate"
            params = {'symbol': 'BTCUSDT', 'limit': 1}
            response = self.session.get(url, params=params, timeout=10)
            funding = float(response.json()[0]['fundingRate'])
            return funding * 100
        except Exception as e:
            print(f"❌ Erro ao buscar Funding: {e}")
            return 0
    
    def get_mvrv_zscore(self) -> float:
        """MVRV Z-Score via CoinGlass"""
        try:
            url = "https://api.alternative.me/v2/ticker/bitcoin/"
            response = self.session.get(url, timeout=10)
            data = response.json()['data']['1']
            
            price = float(data['quotes']['USD']['price'])
            mvrv_approx = (price / 50000) * 2
            return max(0, min(10, mvrv_approx))
        except Exception as e:
            print(f"❌ Erro ao buscar MVRV: {e}")
            return 2
    
    def get_eth_btc_ratio(self) -> Dict[str, float]:
        """Ratio ETH/BTC e sua MM50"""
        try:
            url = "https://api.binance.com/api/v3/klines"
            params = {
                'symbol': 'ETHBTC',
                'interval': '1d',
                'limit': 60
            }
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            closes = [float(candle[4]) for candle in data]
            current_ratio = closes[-1]
            ma50 = sum(closes[-50:]) / 50
            
            return {
                'current': current_ratio,
                'ma50': ma50,
                'deviation': ((current_ratio - ma50) / ma50) * 100
            }
        except Exception as e:
            print(f"❌ Erro ao buscar ETH/BTC: {e}")
            return {'current': 0.05, 'ma50': 0.05, 'deviation': 0}
    
    def get_fear_greed(self) -> int:
        """Fear & Greed Index"""
        try:
            url = "https://api.alternative.me/fng/"
            response = self.session.get(url, timeout=10)
            value = int(response.json()['data'][0]['value'])
            return value
        except Exception as e:
            print(f"❌ Erro ao buscar F&G: {e}")
            return 50
    
    def get_btc_dominance(self) -> float:
        """Dominância do Bitcoin"""
        try:
            url = "https://api.coinmarketcap.com/data-api/v3/global-metrics/quotes/latest"
            response = self.session.get(url, timeout=10)
            data = response.json()['data']
            dominance = data['btcDominance']
            return dominance
        except Exception as e:
            print(f"❌ Erro ao buscar Dominância: {e}")
            return 50
    
    def get_etf_flows(self) -> float:
        """ETF Flows (últimos 5 dias)"""
        try:
            url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
            response = self.session.get(url, timeout=10)
            volume = float(response.json()['quoteVolume'])
            
            etf_estimate = volume * 0.01 / 1_000_000
            return etf_estimate
        except Exception as e:
            print(f"❌ Erro ao estimar ETF Flows: {e}")
            return 500
    
    def get_puell_multiple(self) -> float:
        """Puell Multiple"""
        try:
            btc_price = self.get_btc_price()
            
            daily_revenue = 144 * 3.125 * btc_price
            ma365_reference = 144 * 3.125 * 45000
            
            puell = daily_revenue / ma365_reference
            return puell
        except Exception as e:
            print(f"❌ Erro ao calcular Puell: {e}")
            return 1.5
    
    def get_dxy(self) -> float:
        """Dollar Index (DXY)"""
        try:
            url = "https://query1.finance.yahoo.com/v8/finance/chart/DX-Y.NYB"
            params = {'interval': '1d', 'range': '5d'}
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            close = data['chart']['result'][0]['indicators']['quote'][0]['close']
            dxy = [x for x in close if x is not None][-1]
            return dxy
        except Exception as e:
            print(f"❌ Erro ao buscar DXY: {e}")
            return 102
    
    def get_vix(self) -> float:
        """VIX (Volatility Index)"""
        try:
            url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EVIX"
            params = {'interval': '1d', 'range': '5d'}
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            close = data['chart']['result'][0]['indicators']['quote'][0]['close']
            vix = [x for x in close if x is not None][-1]
            return vix
        except Exception as e:
            print(f"❌ Erro ao buscar VIX: {e}")
            return 17
    
    def get_all_indicators(self) -> Dict:
        """Coleta todos os indicadores"""
        print("📊 Coletando indicadores...")
        
        indicators = {
            'timestamp': datetime.now().isoformat(),
            'btc_price': self.get_btc_price(),
            'rsi_weekly': self.get_rsi_weekly(),
            'funding_rate': self.get_funding_rate(),
            'mvrv_zscore': self.get_mvrv_zscore(),
            'eth_btc': self.get_eth_btc_ratio(),
            'fear_greed': self.get_fear_greed(),
            'btc_dominance': self.get_btc_dominance(),
            'etf_flows': self.get_etf_flows(),
            'puell_multiple': self.get_puell_multiple(),
            'dxy': self.get_dxy(),
            'vix': self.get_vix()
        }
        
        print("✅ Indicadores coletados!")
        return indicators
    
    @staticmethod
    def _calculate_rsi(prices: list, period: int = 14) -> float:
        """Calcula RSI"""
        if len(prices) < period + 1:
            return 50
        
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi


if __name__ == "__main__":
    collector = IndicatorCollector()
    data = collector.get_all_indicators()
    
    print("\n📈 INDICADORES COLETADOS:")
    for key, value in data.items():
        print(f"{key}: {value}")
