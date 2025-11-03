# 📋 CHANGELOG & ROADMAP - GIESTA Bot v2.7

## 🆕 v2.7 (Outubro 2025) - ATUAL

### ✨ Novidades

#### Sistema de Scoring Completo
- ✅ 9 indicadores implementados com pesos
- ✅ RSI Semanal (20%)
- ✅ Funding Rate (20%)
- ✅ MVRV Z-Score (15%)
- ✅ ETH/BTC Ratio (10%)
- ✅ Fear & Greed Index (10%)
- ✅ BTC Dominance (5%)
- ✅ ETF Flows (10%)
- ✅ Puell Multiple (5%)
- ✅ Macro - DXY/VIX (5%)

#### Detecção de Fases
- ✅ 5 fases do ciclo (G0 a G4)
- ✅ Score de 0-100
- ✅ Ações específicas por fase
- ✅ Alertas automáticos de mudança de fase

#### Sistema Failsafe
- ✅ Detecção de condições de reentrada
- ✅ Regras de stop loss
- ✅ Alertas de proteção

#### Bot Telegram
- ✅ Comandos completos (/start, /status, /score, /alerta)
- ✅ Monitoramento automático (1h)
- ✅ Alertas em tempo real
- ✅ Interface amigável

---

## 🚀 ROADMAP - Próximas Versões

### v2.8 (Previsto: Novembro 2025)

#### 🎨 Dashboard Web
- [ ] Interface web com gráficos interativos
- [ ] Histórico de scores e fases
- [ ] Visualização de breakdown por indicador
- [ ] Gráficos de linha temporal

#### 📊 Google Sheets Integration
- [ ] Exportação automática para planilha
- [ ] Dashboard ao vivo no Sheets
- [ ] Histórico de trades
- [ ] Cálculo de performance

#### 🔔 Notificações Avançadas
- [ ] Alertas por email
- [ ] Webhook para Discord
- [ ] Push notifications
- [ ] SMS (opcional, via Twilio)

### v2.9 (Previsto: Dezembro 2025)

#### 📈 APIs Pagas (Opcionais)
- [ ] CoinGlass API completa
  - MVRV Z-Score preciso
  - Long/Short Ratio
  - Liquidation heatmap
- [ ] Glassnode API
  - On-chain detalhado
  - Exchange flows
  - Whale movements
- [ ] Farside Investors
  - ETF flows em tempo real

#### 🤖 Automação
- [ ] Integração com exchanges (view-only)
- [ ] Cálculo automático de % a vender
- [ ] Sugestão de preços de entrada/saída
- [ ] Tracking de portfolio

#### 📚 Backtesting
- [ ] Simulação de estratégia em dados históricos
- [ ] Comparação com buy & hold
- [ ] Otimização de pesos
- [ ] Relatório de performance

### v3.0 (Previsto: Janeiro 2026)

#### 🧠 Machine Learning
- [ ] Predição de próxima fase
- [ ] Otimização dinâmica de pesos
- [ ] Detecção de padrões
- [ ] Score ajustado por contexto

#### 📱 App Mobile
- [ ] App nativo iOS/Android
- [ ] Notificações push nativas
- [ ] Widgets
- [ ] Sincronização multi-device

#### 👥 Multi-usuário
- [ ] Cadastro de usuários
- [ ] Portfolios individuais
- [ ] Compartilhamento de setups
- [ ] Ranking de performance

---

## 🐛 BUGS CONHECIDOS

### v2.7

#### Indicadores
- ⚠️ MVRV Z-Score usa aproximação (sem API paga)
- ⚠️ ETF Flows estimado por volume (não é preciso)
- ⚠️ Puell Multiple calculado, não em tempo real
- ⚠️ Algumas APIs podem ter rate limits

#### Bot
- ⚠️ Monitoramento para quando o terminal fecha
- ⚠️ Sem persistência de dados entre reinícios
- ⚠️ Falhas de API não fazem retry automático

### Soluções Temporárias

**MVRV/Puell/ETF não precisos:**
→ Considere assinar CoinGlass (~$50/mês) ou Glassnode (~$30/mês)
→ O bot ainda funciona bem com aproximações

**Bot offline quando terminal fecha:**
→ Use `screen` (Linux/Mac) ou `nohup`
→ Ou rode em servidor/VPS 24/7

**Rate limits:**
→ Aguarde alguns minutos e tente novamente
→ O intervalo de 1h ajuda a evitar limites

---

## 💡 IDEIAS FUTURAS

### Indicadores Adicionais
- [ ] NVT Ratio
- [ ] SOPR (Spent Output Profit Ratio)
- [ ] Exchange Reserve
- [ ] Stablecoin Supply
- [ ] Google Trends BTC
- [ ] Social sentiment (Twitter/Reddit)

### Features Avançadas
- [ ] Multi-timeframe analysis
- [ ] Correlação entre indicadores
- [ ] Detecção de divergências
- [ ] Zonas de acumulação/distribuição
- [ ] Pattern recognition

### Integrações
- [ ] TradingView alerts
- [ ] CoinGecko portfolio
- [ ] Binance/Bybit API (trading)
- [ ] Tax reporting
- [ ] Notion/Obsidian export

---

## 📝 NOTAS DE DESENVOLVIMENTO

### Tecnologias Usadas
- Python 3.10+
- python-telegram-bot 20.7
- requests
- pandas/numpy (futuro)

### Arquitetura
```
bot.py          → Controller (Telegram)
indicators.py   → Model (Data collection)
scoring.py      → Business logic (Scoring)
config.py       → Configuration
```

### APIs Gratuitas Utilizadas
- Binance API (preço, RSI, funding, ETH/BTC)
- Alternative.me (Fear & Greed)
- CoinMarketCap (Dominance)
- Yahoo Finance (DXY, VIX)

### Melhorias de Performance
- [ ] Cache de indicadores (evitar chamadas repetidas)
- [ ] Async requests (paralelizar coleta)
- [ ] Database para histórico (SQLite)
- [ ] Rate limiting inteligente

---

## 🤝 CONTRIBUIÇÕES

Quer contribuir? Áreas que precisam de ajuda:

1. **Scraping ETF Flows** do Farside Investors
2. **Parser HTML** para dados do CoinGlass (free tier)
3. **Dashboard web** em React/Vue
4. **Testes unitários** para indicadores
5. **Documentação** de casos de uso

---

## 📞 SUPORTE

- 📧 Email: (adicionar)
- 💬 Telegram: (adicionar grupo)
- 🐛 Issues: (adicionar link GitHub)

---

**Última atualização:** 26/10/2025  
**Versão atual:** v2.7  
**Próxima release:** v2.8 (Nov/2025)
