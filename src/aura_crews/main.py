"""
AURA v7.0 Crews — FastAPI Entry Point
Service 2: CrewAI Multi-Agent Service
Connected to: Aura-V.1 Gateway (Service 1)
"""
import os
import time
import psutil
from datetime import datetime, timezone
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# ═══ Import Crew Routers ═══
from src.aura_crews.crews.chat_crew.crew import router as chat_router
from src.aura_crews.crews.content_crew.crew import router as content_router
from src.aura_crews.crews.research_crew.crew import router as research_router
from src.aura_crews.crews.image_crew.crew import router as image_router
from src.aura_crews.crews.finance_crew.crew import router as finance_router

# ═══ App Setup ═══
app = FastAPI(
    title="AURA v7.0 Crews",
    description="CrewAI Multi-Agent Service by Matrol",
    version="7.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STARTUP_TIME = time.time()

CREWS = {
    "chat":     {"agents": 1, "endpoint": "/crew/chat",     "status": "active"},
    "content":  {"agents": 2, "endpoint": "/crew/content",  "status": "active"},
    "research": {"agents": 2, "endpoint": "/crew/research", "status": "active"},
    "image":    {"agents": 1, "endpoint": "/crew/image",    "status": "active"},
    "finance":  {"agents": 2, "endpoint": "/crew/finance",  "status": "active"},
}

# ═══ Include Routers ═══
app.include_router(chat_router, tags=["Chat"])
app.include_router(content_router, tags=["Content"])
app.include_router(research_router, tags=["Research"])
app.include_router(image_router, tags=["Image"])
app.include_router(finance_router, tags=["Finance"])


@app.get("/")
async def root():
    """Health check — basic."""
    return {
        "service": "AURA v7.0 Crews",
        "version": "7.0.0",
        "status": "online",
        "crews": list(CREWS.keys()),
        "total_agents": sum(c["agents"] for c in CREWS.values()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/health")
async def health():
    """Health check — detailed."""
    process = psutil.Process(os.getpid())
    uptime = round(time.time() - STARTUP_TIME)
    return {
        "service": "AURA v7.0 Crews",
        "version": "7.0.0",
        "status": "healthy",
        "uptime_seconds": uptime,
        "uptime_human": f"{uptime // 3600}h {(uptime % 3600) // 60}m {uptime % 60}s",
        "memory_mb": round(process.memory_info().rss / 1024 / 1024, 1),
        "cpu_percent": process.cpu_percent(),
        "crews": CREWS,
        "llm_model": os.getenv("DEFAULT_MODEL", "not set"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.on_event("startup")
async def startup():
    """Log startup info."""
    print("=" * 50)
    print("=== AURA v7.0 CREWS ONLINE ===")
    print(f"Port: {os.getenv('PORT', 8000)}")
    print(f"Crews: {len(CREWS)} active")
    print(f"Total Agents: {sum(c['agents'] for c in CREWS.values())}")
    print(f"LLM: {os.getenv('DEFAULT_MODEL', 'not set')}")
    print("=" * 50)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
