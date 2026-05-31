"""Centralized configuration for AURA Crews."""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "openrouter/google/gemini-2.0-flash-001")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Server
PORT = int(os.getenv("PORT", 8000))
CREW_VERBOSE = os.getenv("CREW_VERBOSE", "false").lower() == "true"

# Database
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")

# External
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")
