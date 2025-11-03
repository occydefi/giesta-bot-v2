"""
Script de teste para verificar se todas as APIs estão funcionando
Execute: python test_apis.py
"""

from indicators import IndicatorCollector
from scoring import GiestaScoring
from datetime import datetime
import sys


def test_indicator(name, func, *args):
    """Testa um indicador específico"""
    try:
        print(f"🔍 Testando {name}...", end=" ")
        result = func(*args)
        print(f"✅ OK - Valor: {result}")
        return True, result
    except Exception as e:
        print(f"❌ ERRO - {str(e)}")
        return False, None


def main():
    """Executa todos os testes"""
    print("═" * 60)
    print("  🧪 TESTE DE APIs - GIESTA BOT v2.7")
    print("═" * 60)
    print()
    
    collector = IndicatorCollector()
    scorer = GiestaScoring()
    
    results = {}
    
    # Teste 1: Preço BTC
    results['btc_price'] = test_indicator(
        "Preço BTC",
        collector.get_btc_price
    )
    
    # Teste 2: RSI Semanal
    results['rsi'] = test_indicator(
        "RSI Semanal",
        collector.get_rsi_weekly
    )
    
    # Teste 3: Funding Rate
    results['funding'] = test_indicator(
        "Funding Rate",
        collector.get_funding_rate
    )
    
    # Teste 4: MVRV Z-Score
    results['mvrv'] = test_indicator(
        "MVRV Z-Score",
        collector.get_mvrv_zscore
    )
    
    # Teste 5: ETH/BTC Ratio
    results['ethbtc'] = test_indicator(
        "ETH/BTC Ratio",
        collector.get_eth_btc_ratio
    )
    
    # Teste 6: Fear & Greed
    results['fg'] = test_indicator(
        "Fear & Greed",
        collector.get_fear_greed
    )
    
    # Teste 7: BTC Dominance
    results['dominance'] = test_indicator(
        "BTC Dominance",
        collector.get_btc_dominance
    )
    
    # Teste 8: ETF Flows
    results['etf'] = test_indicator(
        "ETF Flows",
        collector.get_etf_flows
    )
    
    # Teste 9: Puell Multiple
    results['puell'] = test_indicator(
        "Puell Multiple",
        collector.get_puell_multiple
    )
    
    # Teste 10: DXY
    results['dxy'] = test_indicator(
        "DXY",
        collector.get_dxy
    )
    
    # Teste 11: VIX
    results['vix'] = test_indicator(
        "VIX",
        collector.get_vix
    )
    
    print()
    print("─" * 60)
    
    # Contar sucessos
    total = len(results)
    success = sum(1 for ok, _ in results.values() if ok)
    
    print(f"\n📊 RESULTADO: {success}/{total} APIs funcionando")
    
    if success == total:
        print("✅ TUDO OK! Todas as APIs estão respondendo.")
    elif success >= 7:
        print("⚠️  Algumas APIs falharam, mas o bot pode funcionar.")
        print("   Considere usar APIs pagas para melhor precisão.")
    else:
        print("❌ ATENÇÃO! Muitas APIs falharam.")
        print("   Verifique sua conexão com internet.")
        return
    
    # Teste completo de score
    print("\n" + "═" * 60)
    print("  🎯 TESTE DE SCORE COMPLETO")
    print("═" * 60)
    print()
    print("⏳ Coletando todos os indicadores...")
    print("   (isso pode levar 10-20 segundos)")
    print()
    
    try:
        # Coletar todos os indicadores
        indicators = collector.get_all_indicators()
        
        # Calcular score
        score, breakdown = scorer.calculate_score(indicators)
        phase = scorer.get_phase(score)
        phase_info = scorer.get_phase_info(phase)
        
        print("✅ Score calculado com sucesso!")
        print()
        print("─" * 60)
        print(f"📊 GIESTA SCORE: {score:.1f}/100")
        print(f"🎯 FASE: {phase} - {phase_info['name']}")
        print(f"💰 BTC: ${indicators['btc_price']:,.0f}")
        print()
        print("📈 Indicadores:")
        for name, data in breakdown.items():
            zone_emoji = "🔴" if data['zone'] == 0 else "🟡" if data['zone'] == 0.5 else "🟢"
            print(f"  {zone_emoji} {name}: {data['points']:.1f} pts")
        
        print()
        print("─" * 60)
        print("🎯 AÇÕES SUGERIDAS:")
        print(f"   BTC: {phase_info['actions']['btc']}")
        print(f"   Alts: {phase_info['actions']['alts']}")
        print("─" * 60)
        
        # Verificar Failsafe
        failsafe_active, failsafe_msg = scorer.check_failsafe(indicators, score)
        if failsafe_active:
            print()
            print("🚨 FAILSAFE ATIVADO!")
            print("   Condições de reentrada detectadas.")
        else:
            print()
            print("✅ Failsafe não ativado")
        
        print()
        print("═" * 60)
        print("✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        print("═" * 60)
        print()
        print("🚀 Seu bot está pronto para uso!")
        print()
        print("📱 Próximos passos:")
        print("   1. Execute: python bot.py")
        print("   2. No Telegram, procure seu bot")
        print("   3. Envie: /start")
        print()
        
    except Exception as e:
        print(f"❌ Erro ao calcular score: {e}")
        print()
        print("⚠️  Isso pode indicar problemas com as APIs.")
        print("   Tente novamente em alguns minutos.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Teste interrompido pelo usuário.")
        sys.exit(0)
