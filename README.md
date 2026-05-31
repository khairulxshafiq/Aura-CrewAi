# 🤖 AURA v7.0 Crews

**CrewAI Multi-Agent Service — Service 2 of AURA Microservices Architecture**

Built by **Matrol** | Merged with CrewAI Official Best Practices

---

## 🏗️ Architecture

```
User → Telegram
         │
         ▼
┌────────────────┐
│  Aura-V.1      │  ← Service 1 (Node.js Gateway)
│  Gateway       │     aura-v1.up.railway.app
└───────┬────────┘
        │ HTTP POST
        ▼
┌────────────────┐
│  Aura-V.1-     │  ← Service 2 (THIS) 🔥
│  Crews         │     Python + FastAPI + CrewAI
│  8 Agents      │     @CrewBase + YAML configs
│  5 Crews       │     Flow-first architecture
└────────────────┘
```

---

## 📁 File Structure

```
Aura-V.1-Crews/
├── pyproject.toml              ← CrewAI standard config
├── .env.example
├── .gitignore
├── AGENTS.md                   ← Instructions for coding agents
├── Procfile                    ← Railway start command
├── railway.json                ← Railway deploy config
│
├── src/aura_crews/
│   ├── main.py                 ← FastAPI entry point
│   │
│   ├── flows/
│   │   └── aura_flow.py        ← Flow-first routing
│   │
│   ├── crews/
│   │   ├── chat_crew/          → 1 agent  (Conversational AI)
│   │   ├── content_crew/       → 2 agents (Strategist + Writer)
│   │   ├── research_crew/      → 2 agents (Analyst + Report Writer)
│   │   ├── image_crew/         → 1 agent  (Visual Designer)
│   │   └── finance_crew/       → 2 agents (Analyst + Reporter)
│   │
│   ├── skills/                 ← Domain expertise (SKILL.md)
│   │   ├── aura_personality/
│   │   ├── sakluma_brand/
│   │   └── content_writing/
│   │
│   ├── knowledge/              ← RAG knowledge base
│   ├── tools/                  ← Custom tools (WebSearch, Airtable)
│   ├── guardrails/             ← Output validation
│   ├── schemas/                ← Pydantic models
│   └── config/                 ← Settings
│
└── tests/                      ← Unit tests
```

---

## 🚀 API Endpoints

| Method | Endpoint | Crew | Agents |
|--------|----------|------|--------|
| GET | `/` | — | Health check |
| GET | `/health` | — | Detailed health |
| POST | `/crew/chat` | Chat | 1 |
| POST | `/crew/content` | Content | 2 |
| POST | `/crew/research` | Research | 2 |
| POST | `/crew/image` | Image | 1 |
| POST | `/crew/finance` | Finance | 2 |

### Request Format
```json
{
    "task": "Write a post about Sakluma new menu",
    "context": {
        "userName": "Boss",
        "chatId": "123456"
    }
}
```

### Response Format
```json
{
    "success": true,
    "response": "...",
    "crew": "content",
    "duration": 3.45,
    "metadata": {}
}
```

---

## ⚡ Quick Setup

```bash
# 1. Clone
git clone https://github.com/khairulxshafiq/Aura-V.1-Crews.git
cd Aura-V.1-Crews

# 2. Install
pip install -e .

# 3. Configure
cp .env.example .env
# Edit .env — add OPENROUTER_API_KEY

# 4. Run
uvicorn src.aura_crews.main:app --reload --port 8000

# 5. Test
curl http://localhost:8000/
curl -X POST http://localhost:8000/crew/chat \
  -H "Content-Type: application/json" \
  -d '{"task": "hi AURA", "context": {"userName": "Boss"}}'
```

---

## 🚂 Railway Deployment

1. Create repo on GitHub: `Aura-V.1-Crews`
2. Push all files
3. Railway → New Service → Connect GitHub repo
4. Set env vars: `OPENROUTER_API_KEY`, `PORT=8000`
5. Deploy! 🚀

---

## ➕ Adding a New Crew

1. Create `src/aura_crews/crews/new_crew/`
2. Add `__init__.py`, `crew.py`, `config/agents.yaml`, `config/tasks.yaml`
3. Follow `@CrewBase` pattern (see existing crews)
4. Register router in `main.py`
5. Add `@listen` in `flows/aura_flow.py`

---

## 🔑 Key Features (CrewAI Best Practice)

- ✅ `@CrewBase` decorator on all crews
- ✅ YAML-first agent & task definitions
- ✅ Flow-first architecture (`@start`, `@router`, `@listen`)
- ✅ Hallucination guardrails on final tasks
- ✅ Structured Pydantic outputs
- ✅ Skills system (SKILL.md)
- ✅ Knowledge base for RAG
- ✅ Custom tools (WebSearch, Airtable)
- ✅ FastAPI HTTP wrapper for Gateway integration
- ✅ `pyproject.toml` with `[tool.crewai] type = "flow"`

---

**Built with 🔥 by Matrol — AURA v7.0 Microservices Architecture**
