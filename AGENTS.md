# AURA v7.0 Crews — Coding Agent Instructions

## For Cline / GitHub Copilot / Cursor

### Project Type
CrewAI **Flow** project with FastAPI HTTP wrapper.

### Key Rules
1. ALL agent definitions → `config/agents.yaml` (NEVER hardcode in Python)
2. ALL task definitions → `config/tasks.yaml` (NEVER hardcode in Python)
3. ALL crew classes MUST use `@CrewBase` decorator
4. Flows orchestrate Crews — Crews do NOT call other Crews directly
5. Use `output_pydantic` for structured outputs where needed
6. Skills inject domain expertise via `SKILL.md` files
7. Final task in each crew should have `guardrail=hallucination_guardrail`

### Adding a New Crew
1. Create folder: `src/aura_crews/crews/new_crew/`
2. Add `__init__.py`, `crew.py`, `config/agents.yaml`, `config/tasks.yaml`
3. Register router in `src/aura_crews/main.py`
4. Add `@listen` handler in `src/aura_crews/flows/aura_flow.py`

### LLM Config
- Default: `openrouter/google/gemini-2.0-flash-001`
- Set via `OPENROUTER_API_KEY` env var
- Override per-agent in `agents.yaml` via `llm:` field

### Testing
```bash
curl -X POST http://localhost:8000/crew/chat \
  -H "Content-Type: application/json" \
  -d '{"task": "hello AURA", "context": {"userName": "Boss"}}'
```
