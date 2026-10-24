import os
try:
    import streamlit as st
    _s = dict(st.secrets)
except Exception:
    _s = {}
def get(k, d=None): return os.getenv(k) or _s.get(k, d)

ANTHROPIC_API_KEY = get("ANTHROPIC_API_KEY")
VOYAGE_API_KEY    = get("VOYAGE_API_KEY")
QDRANT_URL        = get("QDRANT_URL")        # Qdrant Cloud cluster URL
QDRANT_API_KEY    = get("QDRANT_API_KEY")
LLM_MODEL   = get("LLM_MODEL", "claude-haiku-5-5")   # cheapest Claude tier = fewest cost/tokens
EMBED_MODEL = get("EMBED_MODEL", "voyage-3.5-lite")  # 1024-dim
COLLECTION  = "college_docs"
DIM, CHUNK, OVERLAP = 1024, 800, 120
TOP_K, MIN_SCORE, MAX_OUT = 4, 0.35, 300
NOT_FOUND = "Information not found in the available documents."
