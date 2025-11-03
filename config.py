"""
GIESTA MASTER STRATEGY v2.7 - Configurações
"""

# Indicadores e seus pesos (%)
INDICATOR_WEIGHTS = {
    'rsi_weekly': 20,
    'funding_rate': 20,
    'mvrv_zscore': 15,
    'eth_btc_ratio': 10,
    'fear_greed': 10,
    'btc_dominance': 5,
    'etf_flows': 10,
    'onchain': 5,  # Puell Multiple + Whales
    'macro': 5     # DXY + VIX
}

# Zonas de cada indicador (Baixa=0, Neutra=0.5, Alta=1)
INDICATOR_ZONES = {
    'rsi_weekly': {
        'low': 45,      # <45 = 0
        'high': 70      # >70 = 1, entre = 0.5
    },
    'funding_rate': {
        'low': 0,       # <0 = 0
        'high': 0.03    # >0.03 = 1, entre = 0.5
    },
    'mvrv_zscore': {
        'low': 1.2,     # <1.2 = 0
        'high': 6       # >6 = 1, entre = 0.5
    },
    'eth_btc_ratio': {
        'threshold': 5  # ±5% da MM50
    },
    'fear_greed': {
        'low': 30,      # <30 = 0
        'high': 80      # >80 = 1, entre = 0.5
    },
    'btc_dominance': {
        'low': 44,      # <44 = 1 (alta para alts)
        'high': 50      # >50 = 0 (baixa para alts)
    },
    'etf_flows': {
        'low': 0,       # <0 = 0
        'high': 1000    # >1B = 1, entre = 0.5 (em milhões)
    },
    'puell_multiple': {
        'low': 0.5,     # <0.5 = 0
        'high': 3       # >3 = 1, entre = 0.5
    },
    'dxy': {
        'low': 100,     # <100 = 1 (bom para cripto)
        'high': 105     # >105 = 0 (ruim para cripto)
    },
    'vix': {
        'low': 15,      # <15 = 1 (baixo risco)
        'high': 20      # >20 = 0 (alto risco)
    }
}

# Fases do ciclo
CYCLE_PHASES = {
    'G0': {'min': 0, 'max': 39, 'name': 'Acúmulo'},
    'G1': {'min': 40, 'max': 59, 'name': 'Rompimento ATH'},
    'G2': {'min': 60, 'max': 69, 'name': 'Rotação ETH'},
    'G3': {'min': 70, 'max': 84, 'name': 'Altseason'},
    'G4': {'min': 85, 'max': 100, 'name': 'Euforia Final'}
}

# Ações por fase
PHASE_ACTIONS = {
    'G0': {
        'btc': 'Comprar / Hold',
        'alts': 'Acumular seletivamente'
    },
    'G1': {
        'btc': 'Vender 30%',
        'alts': 'Vender 20-30%'
    },
    'G2': {
        'btc': 'Vender 25%',
        'alts': 'Vender 30%'
    },
    'G3': {
        'btc': 'Vender 25%',
        'alts': 'Vender 40-50%'
    },
    'G4': {
        'btc': 'Zerar 80-100%',
        'alts': 'Zerar (moonbag máx 5%)'
    }
}

# Condições Failsafe
FAILSAFE_CONDITIONS = {
    'score': 40,
    'rsi': 45,
    'mvrv': 1.2,
    'funding': 0,
    'fear_greed': 30
}

# APIs e URLs
APIS = {
    'binance': 'https://api.binance.com/api/v3',
    'alternative_me': 'https://api.alternative.me/fng/',
    'coinglass': 'https://open-api.coinglass.com/public/v2',
    'coinmarketcap': 'https://api.coinmarketcap.com/data-api/v3/global-metrics',
    'tradingview': 'https://scanner.tradingview.com',
    'yahoo_finance': 'https://query1.finance.yahoo.com/v8/finance/chart'
}

# Timeframes
CHECK_INTERVAL = 3600  # 1 hora em segundos
WEEKLY_CANDLE_HOURS = 168  # 7 dias
