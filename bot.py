"""GIESTA MASTER STRATEGY v2.7"""
import os
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
from indicators import IndicatorCollector
from scoring import GiestaScoring
from config import CHECK_INTERVAL
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
collector = IndicatorCollector()
scorer = GiestaScoring()
bot_state = {'monitoring': False, 'last_phase': None, 'last_score': None, 'last_check': None}
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""🤖 GIESTA v2.7

Bot com Override ATH

📋 COMANDOS:
/status - Status rápido
/score - Análise completa
/alerta - Monitoramento 24/7
/help - Ajuda

🎯 FASES:
G0: Acúmulo
G1: Aproximação ATH
G2: Rompimento
G3: Altseason
G4: Euforia""")
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Coletando...")
    try:
        ind = collector.get_all_indicators()
        score, _ = scorer.calculate_score(ind)
        phase = scorer.get_phase(score, ind['btc_price'])
        pi = scorer.get_phase_info(phase)
        await update.message.reply_text(f"""🟢 STATUS

💵 BTC: ${ind['btc_price']:,.0f}
📊 RSI: {ind['rsi_weekly']:.2f}
💸 Funding: {ind['funding_rate']:.4f}%
📈 Dom: {ind['btc_dominance']:.2f}%
😱 F&G: {ind['fear_greed']}

🎯 {phase} - {pi['name']}
📊 Score: {score:.1f}/100""")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {e}")
async def score_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Calculando...\nAguarde 10-20s...")
    try:
        ind = collector.get_all_indicators()
        score, bd = scorer.calculate_score(ind)
        phase = scorer.get_phase(score, ind['btc_price'])
        fs = scorer.check_failsafe(ind, score)
        report = scorer.format_report(score, phase, bd, ind, fs)
        await update.message.reply_text(report)
        bot_state['last_phase'] = phase
        bot_state['last_score'] = score
        bot_state['last_check'] = datetime.now()
    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {e}")
async def alerta_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if bot_state['monitoring']:
        await update.message.reply_text("⚠️ Já ativo!")
        return
    bot_state['monitoring'] = True
    await update.message.reply_text("""🔔 ATIVADO

Checando a cada 1h
/stop para parar""")
    context.job_queue.run_repeating(monitoring_loop, interval=CHECK_INTERVAL, first=10, chat_id=update.effective_chat.id, name=str(update.effective_chat.id))
async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not bot_state['monitoring']:
        await update.message.reply_text("ℹ️ Não ativo")
        return
    bot_state['monitoring'] = False
    jobs = context.job_queue.get_jobs_by_name(str(update.effective_chat.id))
    for j in jobs:
        j.schedule_removal()
    await update.message.reply_text("🔕 Desativado")
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)
async def monitoring_loop(context: ContextTypes.DEFAULT_TYPE):
    try:
        ind = collector.get_all_indicators()
        score, _ = scorer.calculate_score(ind)
        phase = scorer.get_phase(score, ind['btc_price'])
        if bot_state['last_phase'] and phase != bot_state['last_phase']:
            await context.bot.send_message(chat_id=context.job.chat_id, text=f"""🚨 MUDANÇA!

{bot_state['last_phase']} → {phase}

/score para detalhes""")
        elif bot_state['last_score'] and abs(score - bot_state['last_score']) >= 5:
            emoji = "📈" if score > bot_state['last_score'] else "📉"
            await context.bot.send_message(chat_id=context.job.chat_id, text=f"""{emoji} VARIAÇÃO

Score: {bot_state['last_score']:.1f} → {score:.1f}
Fase: {phase}""")
        bot_state['last_phase'] = phase
        bot_state['last_score'] = score
        bot_state['last_check'] = datetime.now()
    except Exception as e:
        print(f"❌ {e}")
def main():
    print("🤖 GIESTA Bot v2.7...")
    if not TOKEN:
        print("❌ Token não encontrado")
        return
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("score", score_command))
    app.add_handler(CommandHandler("alerta", alerta_command))
    app.add_handler(CommandHandler("stop", stop_command))
    app.add_handler(CommandHandler("help", help_command))
    print("✅ Bot pronto!")
    print(f"📱 {CHAT_ID}\n")
    app.run_polling()
if __name__ == "__main__":
    main()
