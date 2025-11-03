"""GIESTA v2.7 - Sistema de Scoring COM CORREÇÃO DE ATH"""
from typing import Dict, Tuple
from config import INDICATOR_WEIGHTS, INDICATOR_ZONES, CYCLE_PHASES, PHASE_ACTIONS, FAILSAFE_CONDITIONS

BTC_ATH = 124000

class GiestaScoring:
    def __init__(self):
        self.weights = INDICATOR_WEIGHTS
        self.zones = INDICATOR_ZONES
        self.phases = CYCLE_PHASES
    
    def classify_indicator(self, indicator: str, value: float, extra_data: Dict = None) -> float:
        if indicator == 'rsi_weekly':
            return 0 if value < 45 else (1 if value > 70 else 0.5)
        elif indicator == 'funding_rate':
            return 0 if value < 0 else (1 if value > 0.03 else 0.5)
        elif indicator == 'mvrv_zscore':
            return 0 if value < 1.2 else (1 if value > 6 else 0.5)
        elif indicator == 'eth_btc_ratio':
            if extra_data:
                dev = abs(extra_data.get('deviation', 0))
                return 0.5 if dev < 5 else (1 if extra_data.get('deviation', 0) > 0 else 0)
            return 0.5
        elif indicator == 'fear_greed':
            return 0 if value < 30 else (1 if value > 80 else 0.5)
        elif indicator == 'btc_dominance':
            return 0 if value > 50 else (1 if value < 44 else 0.5)
        elif indicator == 'etf_flows':
            return 0 if value < 0 else (1 if value > 1000 else 0.5)
        elif indicator == 'puell_multiple':
            return 0 if value < 0.5 else (1 if value > 3 else 0.5)
        elif indicator == 'macro':
            dxy = extra_data.get('dxy', 102)
            vix = extra_data.get('vix', 17)
            ds = 1 if dxy < 100 else (0 if dxy > 105 else 0.5)
            vs = 1 if vix < 15 else (0 if vix > 20 else 0.5)
            return (ds + vs) / 2
        return 0.5
    
    def calculate_score(self, indicators: Dict) -> Tuple[float, Dict]:
        total = 0
        bd = {}
        z = self.classify_indicator('rsi_weekly', indicators['rsi_weekly'])
        p = z * self.weights['rsi_weekly']
        total += p
        bd['RSI Semanal'] = {'value': indicators['rsi_weekly'], 'zone': z, 'points': p}
        z = self.classify_indicator('funding_rate', indicators['funding_rate'])
        p = z * self.weights['funding_rate']
        total += p
        bd['Funding Rate'] = {'value': indicators['funding_rate'], 'zone': z, 'points': p}
        z = self.classify_indicator('mvrv_zscore', indicators['mvrv_zscore'])
        p = z * self.weights['mvrv_zscore']
        total += p
        bd['MVRV Z-Score'] = {'value': indicators['mvrv_zscore'], 'zone': z, 'points': p}
        z = self.classify_indicator('eth_btc_ratio', indicators['eth_btc']['current'], indicators['eth_btc'])
        p = z * self.weights['eth_btc_ratio']
        total += p
        bd['ETH/BTC Ratio'] = {'value': indicators['eth_btc']['current'], 'deviation': indicators['eth_btc']['deviation'], 'zone': z, 'points': p}
        z = self.classify_indicator('fear_greed', indicators['fear_greed'])
        p = z * self.weights['fear_greed']
        total += p
        bd['Fear & Greed'] = {'value': indicators['fear_greed'], 'zone': z, 'points': p}
        z = self.classify_indicator('btc_dominance', indicators['btc_dominance'])
        p = z * self.weights['btc_dominance']
        total += p
        bd['BTC Dominance'] = {'value': indicators['btc_dominance'], 'zone': z, 'points': p}
        z = self.classify_indicator('etf_flows', indicators['etf_flows'])
        p = z * self.weights['etf_flows']
        total += p
        bd['ETF Flows'] = {'value': indicators['etf_flows'], 'zone': z, 'points': p}
        z = self.classify_indicator('puell_multiple', indicators['puell_multiple'])
        p = z * self.weights['onchain']
        total += p
        bd['Puell Multiple'] = {'value': indicators['puell_multiple'], 'zone': z, 'points': p}
        z = self.classify_indicator('macro', 0, {'dxy': indicators['dxy'], 'vix': indicators['vix']})
        p = z * self.weights['macro']
        total += p
        bd['Macro (DXY/VIX)'] = {'dxy': indicators['dxy'], 'vix': indicators['vix'], 'zone': z, 'points': p}
        return total, bd
    
    def get_phase(self, score: float, btc_price: float = None) -> str:
        if btc_price:
            dist_pct = ((btc_price - BTC_ATH) / BTC_ATH) * 100
            if dist_pct < -15:
                max_phase = 'G0'
            elif dist_pct < -5:
                max_phase = 'G0'
            elif dist_pct < 0:
                max_phase = 'G1'
            elif dist_pct < 10:
                max_phase = 'G2'
            else:
                max_phase = 'G4'
            score_phase = None
            for phase, limits in self.phases.items():
                if limits['min'] <= score <= limits['max']:
                    score_phase = phase
                    break
            if not score_phase:
                score_phase = 'G0'
            phase_order = ['G0', 'G1', 'G2', 'G3', 'G4']
            max_index = phase_order.index(max_phase)
            score_index = phase_order.index(score_phase)
            return phase_order[min(max_index, score_index)]
        for phase, limits in self.phases.items():
            if limits['min'] <= score <= limits['max']:
                return phase
        return 'G0'
    
    def get_phase_info(self, phase: str) -> Dict:
        return {'phase': phase, 'name': self.phases[phase]['name'], 'score_range': f"{self.phases[phase]['min']}-{self.phases[phase]['max']}", 'actions': PHASE_ACTIONS[phase]}
    
    def check_ath_status(self, btc_price: float) -> Dict:
        dist_pct = ((btc_price - BTC_ATH) / BTC_ATH) * 100
        if btc_price >= BTC_ATH:
            status = "🟢 NOVO ATH!"
            context = "Descoberta de preço"
        elif dist_pct >= -5:
            status = f"🟡 Próximo ({abs(dist_pct):.1f}% abaixo)"
            context = "Zona de rompimento"
        elif dist_pct >= -15:
            status = f"🟠 Abaixo ({abs(dist_pct):.1f}%)"
            context = "Consolidação alta"
        else:
            status = f"🔴 Longe ({abs(dist_pct):.1f}%)"
            context = "Zona de acumulação"
        return {'ath': BTC_ATH, 'current': btc_price, 'distance_pct': dist_pct, 'distance_usd': btc_price - BTC_ATH, 'status': status, 'context': context}
    
    def check_failsafe(self, indicators: Dict, score: float) -> Tuple[bool, str]:
        if score >= 40:
            return False, ""
        active = (indicators['rsi_weekly'] < 45 and indicators['mvrv_zscore'] < 1.2 and indicators['funding_rate'] < 0 and indicators['fear_greed'] < 30)
        if active:
            return True, "🚨 FAILSAFE ATIVADO\n\nRecomprar 10% a cada -10%"
        return False, ""
    
    def format_report(self, score: float, phase: str, breakdown: Dict, indicators: Dict, failsafe: Tuple[bool, str]) -> str:
        pi = self.get_phase_info(phase)
        ath = self.check_ath_status(indicators['btc_price'])
        score_would_be = None
        for p, limits in self.phases.items():
            if limits['min'] <= score <= limits['max']:
                score_would_be = p
                break
        override_msg = ""
        if score_would_be and score_would_be != phase:
            override_msg = f"\n⚠️ Override ATH: Score indicava {score_would_be}, ajustado para {phase}"
        report = f"""📊 GIESTA SCORE: {score:.1f}/100

🎯 {phase} - {pi['name']}
{ath['context']}{override_msg}

💵 BTC: ${indicators['btc_price']:,.0f}
{ath['status']}
ATH: ${ath['ath']:,.0f} ({ath['distance_pct']:.1f}%)

💰 AÇÕES:
BTC: {pi['actions']['btc']}
Alts: {pi['actions']['alts']}

━━━━━━━━━━━━━━━━━━
📈 INDICADORES:
"""
        for name, data in breakdown.items():
            emoji = "🔴" if data['zone'] == 0 else ("🟡" if data['zone'] == 0.5 else "🟢")
            if 'deviation' in data:
                report += f"\n{emoji} {name}: {data['deviation']:.1f}% → {data['points']:.1f} pts"
            elif name == 'Macro (DXY/VIX)':
                report += f"\n{emoji} {name}: {data['dxy']:.0f}/{data['vix']:.0f} → {data['points']:.1f} pts"
            else:
                report += f"\n{emoji} {name}: {data['value']:.2f} → {data['points']:.1f} pts"
        if failsafe[0]:
            report += f"\n\n{failsafe[1]}"
        return report
