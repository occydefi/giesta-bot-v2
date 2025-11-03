# 🐍 Setup PythonAnywhere (Plano Gratuito)

## ⚠️ Limitações do Plano Gratuito

- ✅ Tarefas agendadas (1x por hora)
- ✅ Alertas automáticos quando muda de fase ou score varia
- ✅ Resumo diário
- ❌ NÃO responde comandos imediatos (`/status`, `/score`, etc)
- ❌ Bot NÃO fica online 24/7

**Para bot 24/7 respondendo comandos:** precisa do plano pago ($5/mês)

---

## 📋 Passo a Passo

### 1️⃣ Criar conta no PythonAnywhere

1. Acesse: https://www.pythonanywhere.com/registration/register/beginner/
2. Crie sua conta gratuita
3. Faça login

### 2️⃣ Abrir Console Bash

1. No dashboard, clique em **"Consoles"**
2. Clique em **"Bash"** (ou "$ Bash")

### 3️⃣ Clonar o repositório

No console bash, digite:

```bash
git clone https://github.com/occydefi/giesta-bot-v2.git
cd giesta-bot-v2
```

### 4️⃣ Criar virtualenv

```bash
mkvirtualenv --python=/usr/bin/python3.10 giesta-env
```

### 5️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 6️⃣ Configurar variáveis de ambiente

```bash
cp .env.example .env
nano .env
```

Adicione suas credenciais:
```
TELEGRAM_TOKEN=seu_token_aqui
CHAT_ID=seu_chat_id_aqui
```

**Salvar:** `Ctrl+O`, Enter, `Ctrl+X`

### 7️⃣ Testar o script

```bash
python check_scheduled.py
```

Se aparecer "✅ Check concluído!" e você receber uma mensagem no Telegram, está funcionando!

### 8️⃣ Configurar tarefa agendada

1. Volte ao dashboard do PythonAnywhere
2. Clique na aba **"Tasks"**
3. Em **"Scheduled tasks"**, configure:

**Command:**
```bash
cd /home/SEU_USERNAME/giesta-bot-v2 && /home/SEU_USERNAME/.virtualenvs/giesta-env/bin/python check_scheduled.py
```

**Substitua `SEU_USERNAME`** pelo seu username do PythonAnywhere!

**Horário:**
- Escolha a hora que quer que rode (ex: 12:00 UTC)
- No plano gratuito, só pode 1 tarefa por dia

**⚠️ IMPORTANTE:** No plano gratuito, só roda **1x por dia**, não a cada hora!

4. Clique em **"Create"**

### 9️⃣ Upgrade para mais tarefas (opcional)

Se quiser rodar **a cada hora** (não 1x por dia):
- Precisa do plano **"Hacker" ($5/mês)**
- Permite tarefas a cada hora

---

## 📊 O que vai acontecer

**Plano Gratuito (1x por dia):**
- Script roda 1x por dia no horário escolhido
- Envia alertas se:
  - Mudou de fase (G0→G1, etc)
  - Score variou ≥5 pontos
  - Failsafe ativado
  - Resumo diário

**Plano Pago ($5/mês - tarefas de hora em hora):**
- Script roda a cada 1 hora
- Mais responsivo a mudanças

---

## 🔧 Troubleshooting

### Erro: "No module named 'telegram'"

```bash
workon giesta-env
pip install -r requirements.txt
```

### Tarefa não roda

- Verifique se o caminho está correto
- Verifique se substituiu `SEU_USERNAME`
- Veja os logs na aba "Tasks" → "Log files"

### Bot não envia mensagens

- Verifique o `.env` (TELEGRAM_TOKEN e CHAT_ID corretos)
- Teste manualmente: `python check_scheduled.py`

---

## 📈 Melhorar a frequência

**Opções:**

1. **PythonAnywhere Hacker ($5/mês):**
   - Tarefas a cada hora
   - Mais confiável

2. **Railway/Fly.io (grátis/barato):**
   - Bot 24/7
   - Responde comandos imediatamente
   - Melhor opção se quiser interatividade

---

## 🔄 Atualizar o código

Quando fizer mudanças no GitHub:

```bash
cd ~/giesta-bot-v2
git pull
workon giesta-env
pip install -r requirements.txt
```

---

**✅ Pronto!** Seu bot vai enviar alertas automáticos no horário agendado!
