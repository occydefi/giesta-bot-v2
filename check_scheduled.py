"""
GIESTA Bot - Scheduled Check (PythonAnywhere Free)
Roda a cada hora e envia alertas se houver mudanças
"""
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from indicators import IndicatorCollector
from scoring import GiestaScoring

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
STATE_FILE = 'bot_state.json'

collector = IndicatorCollector()
scorer = GiestaScoring()

def load_state():
    """Carrega estado anterior"""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {'last_phase': None, 'last_score': None}

def save_state(state):
    """Salva estado atual"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def send_telegram(message):
    """Envia mensagem para o Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, data=data, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Erro ao enviar: {e}")
        return False

def main():
    print(f"🤖 GIESTA Check - {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    try:
        # Carrega estado anterior
        state = load_state()

        # Coleta indicadores
        print("📊 Coletando indicadores...")
        ind = collector.get_all_indicators()

        # Calcula score
        score, bd = scorer.calculate_score(ind)
        phase = scorer.get_phase(score, ind['btc_price'])
        fs = scorer.check_failsafe(ind, score)

        print(f"Score: {score:.1f} | Fase: {phase}")

        # Verifica mudanças
        send_alert = False
        message = ""

        # Mudança de fase
        if state['last_phase'] and phase != state['last_phase']:
            send_alert = True
            message = f"""🚨 <b>MUDANÇA DE FASE!</b>

{state['last_phase']} → <b>{phase}</b>

💵 BTC: ${ind['btc_price']:,.0f}
📊 Score: {score:.1f}/100

⏰ {datetime.now().strftime('%d/%m %H:%M')}"""

        # Variação de score >= 5
        elif state['last_score'] and abs(score - state['last_score']) >= 5:
            send_alert = True
            emoji = "📈" if score > state['last_score'] else "📉"
            message = f"""{emoji} <b>VARIAÇÃO DE SCORE</b>

Score: {state['last_score']:.1f} → <b>{score:.1f}</b>
Fase: {phase}

💵 BTC: ${ind['btc_price']:,.0f}

⏰ {datetime.now().strftime('%d/%m %H:%M')}"""

        # Failsafe ativo
        elif fs['active']:
            send_alert = True
            message = f"""🛡️ <b>FAILSAFE ATIVO</b>

Condições de reentrada detectadas!

📊 Score: {score:.1f}
💵 BTC: ${ind['btc_price']:,.0f}
📉 RSI: {ind['rsi_weekly']:.1f}
😱 F&G: {ind['fear_greed']}

⏰ {datetime.now().strftime('%d/%m %H:%M')}"""

        # Sem mudanças - envia resumo diário (opcional)
        else:
            # Envia resumo uma vez por dia (se for primeira checagem do dia)
            current_date = datetime.now().strftime('%Y-%m-%d')
            if state.get('last_daily_report') != current_date:
                send_alert = True
                pi = scorer.get_phase_info(phase)
                message = f"""📊 <b>RESUMO DIÁRIO</b>

🎯 {phase} - {pi['name']}
📊 Score: {score:.1f}/100

💵 BTC: ${ind['btc_price']:,.0f}
📈 RSI: {ind['rsi_weekly']:.1f}
💸 Funding: {ind['funding_rate']:.4f}%
😱 F&G: {ind['fear_greed']}
📊 Dom: {ind['btc_dominance']:.1f}%

⏰ {datetime.now().strftime('%d/%m %H:%M')}"""
                state['last_daily_report'] = current_date

        # Envia alerta se necessário
        if send_alert and message:
            print("📤 Enviando alerta...")
            if send_telegram(message):
                print("✅ Alerta enviado!")
            else:
                print("❌ Falha ao enviar")
        else:
            print("ℹ️ Sem mudanças significativas")

        # Salva novo estado
        state['last_phase'] = phase
        state['last_score'] = score
        save_state(state)

        print("✅ Check concluído!")

    except Exception as e:
        print(f"❌ Erro: {e}")
        # Tenta enviar erro para Telegram
        error_msg = f"❌ Erro no bot:\n{str(e)}\n\n⏰ {datetime.now().strftime('%d/%m %H:%M')}"
        send_telegram(error_msg)

if __name__ == "__main__":
    main()
