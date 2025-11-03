# 🤖 GIESTA MASTER STRATEGY v2.7 - Telegram Bot

Bot de monitoramento automatizado do ciclo cripto baseado em **9 indicadores** técnicos, on-chain e macroeconômicos.

## 📊 Metodologia

Sistema de scoring quantitativo (0-100) que define **5 fases do ciclo**:

| Fase | Score | Contexto | Ação BTC | Ação Alts |
|------|-------|----------|----------|-----------|
| **G0** | 0-39 | Acúmulo / Bear | Comprar / Hold | Acumular seletivamente |
| **G1** | 40-59 | Rompimento ATH | Vender 30% | Vender 20-30% |
| **G2** | 60-69 | Rotação ETH | Vender 25% | Vender 30% |
| **G3** | 70-84 | Altseason | Vender 25% | Vender 40-50% |
| **G4** | 85-100 | Euforia Final | Zerar 80-100% | Zerar (moonbag 5%) |

## 🎯 Indicadores (9 no total)

| Indicador | Peso | Função |
|-----------|------|--------|
| RSI Semanal BTC | 20% | Momentum e exaustão |
| Funding Rate | 20% | Euforia de derivativos |
| MVRV Z-Score | 15% | Valorização on-chain |
| ETH/BTC Ratio | 10% | Rotação BTC→ETH→Alts |
| Fear & Greed | 10% | Sentimento de varejo |
| BTC Dominance | 5% | Confirmação estrutural |
| ETF Flows | 10% | Liquidez institucional |
| Puell Multiple | 5% | Pressão de mineração |
| Macro (DXY/VIX) | 5% | Risco sistêmico |

## 🚀 Instalação Rápida

### 1️⃣ Pré-requisitos

- Python 3.10 ou superior
- Conta no Telegram

### 2️⃣ Clone/Baixe o projeto

```bash
cd giesta-bot-v2
```

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure o bot

#### a) Criar bot no Telegram

1. Abra o Telegram e procure: `@BotFather`
2. Envie: `/newbot`
3. Escolha um nome (ex: "Giesta Strategy")
4. Escolha um username (ex: "giesta_strategy_bot")
5. **Copie o token** fornecido

#### b) Obter seu Chat ID

1. Procure no Telegram: `@userinfobot`
2. Envie: `/start`
3. **Copie o número** (seu Chat ID)

#### c) Configurar .env

```bash
cp .env.example .env
```

Edite o `.env` e adicione:

```env
TELEGRAM_TOKEN=1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
CHAT_ID=123456789
```

### 5️⃣ Execute o bot

```bash
python bot.py
```

Você verá:
```
🤖 Iniciando GIESTA Bot v2.7...
✅ Bot pronto! Aguardando comandos...
```

**Mantenha o terminal aberto!**

### 6️⃣ Teste no Telegram

1. No Telegram, procure seu bot: `@seu_bot_username`
2. Envie: `/start`
3. Pronto! 🎉

## 📱 Comandos

```
/start      - Iniciar bot e ver ajuda
/status     - Status rápido do mercado
/score      - Cálculo completo do GIESTA SCORE
/alerta     - Ativar monitoramento automático (1h)
/stop       - Desativar monitoramento
/fase       - Ver informações da fase atual
/failsafe   - Checar condições de reentrada
/help       - Mostrar ajuda
```

## 🔔 Monitoramento Automático

Ative com `/alerta` para receber alertas quando:

✅ Mudar de fase (G0→G1, G1→G2, etc)  
✅ Score variar mais de 5 pontos  
✅ Condições de Failsafe atingidas  
✅ Alertas críticos de risco  

O bot checa **a cada 1 hora** automaticamente.

## 🛡️ Sistema Failsafe

Ativa quando **TODAS** as condições são atingidas:

- Score < 40
- RSI Semanal < 45
- MVRV Z-Score < 1.2
- Funding Rate < 0
- Fear & Greed < 30

### Ações no Failsafe:

1. Recomprar 10% a cada -10% de queda do BTC
2. Reentrada total quando RSI > 50 e Funding neutro
3. Stop: BTC -15% em 24h → reduzir 50% posições

## 📂 Estrutura do Projeto

```
giesta-bot-v2/
├── bot.py              # Bot principal do Telegram
├── indicators.py       # Coleta de indicadores
├── scoring.py          # Sistema de scoring e fases
├── config.py           # Configurações e pesos
├── requirements.txt    # Dependências Python
├── .env.example        # Exemplo de configuração
└── README.md          # Este arquivo
```

## 🔧 APIs Utilizadas

### Gratuitas (já implementadas):

- Binance API - Preço, RSI, Funding, ETH/BTC
- Alternative.me - Fear & Greed Index
- CoinMarketCap - BTC Dominance
- Yahoo Finance - DXY e VIX

### Opcionais (melhoram precisão):

- CoinGlass API - MVRV Z-Score preciso
- Glassnode API - On-chain avançado
- Farside Investors - ETF Flows precisos

## ⚙️ Configurações Avançadas

### Ajustar intervalo de checagem:

No arquivo `.env`:

```env
CHECK_INTERVAL=1800  # 30 minutos
# ou
CHECK_INTERVAL=7200  # 2 horas
```

### Ativar modo debug:

```env
DEBUG=true
```

## 🐛 Troubleshooting

### Erro: "Token inválido"

✅ Verifique se copiou o token completo do @BotFather  
✅ Não deve ter espaços antes/depois  

### Bot não responde:

✅ Certifique-se que `bot.py` está rodando  
✅ Verifique se o CHAT_ID está correto  
✅ Tente enviar `/start` novamente  

### Erro ao coletar indicadores:

✅ Verifique sua conexão com internet  
✅ Algumas APIs podem ter rate limits  
✅ Aguarde 1 minuto e tente novamente  

## 📈 Exemplo de Uso

```python
# Cálculo manual (sem Telegram)
from indicators import IndicatorCollector
from scoring import GiestaScoring

collector = IndicatorCollector()
scorer = GiestaScoring()

# Coletar dados
indicators = collector.get_all_indicators()

# Calcular score
score, breakdown = scorer.calculate_score(indicators)
phase = scorer.get_phase(score)

print(f"Score: {score:.1f}")
print(f"Fase: {phase}")
```

## 📊 Dashboard (Futuro)

Em desenvolvimento:

- [ ] Dashboard web com histórico
- [ ] Gráficos interativos
- [ ] Integração com Google Sheets
- [ ] Notificações push
- [ ] Backtesting histórico

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas!

## ⚠️ Disclaimer

Este bot é uma ferramenta educacional e de análise. **Não é uma recomendação financeira**. Sempre faça sua própria pesquisa (DYOR) e consulte profissionais antes de investir.

## 📄 Licença

MIT License - Use livremente!

---

Desenvolvido com ❤️ baseado na metodologia GIESTA v2.7

**Última atualização:** Outubro 2025
