"""Static configuration constants.

Plain module-level constants — no settings library needed for a fixture-backed,
single-environment take-home.
"""

from pathlib import Path

# Resolve the fixture relative to this file so `uv run ...` works from any CWD.
# config.py -> app/ -> backend/ -> repo root -> data/sdn_sample.json
DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "sdn_sample.json"

# Frontend dev origin (Vite). The Vite dev proxy is the primary wiring; CORS is a
# safety net for when the SPA hits the API cross-origin.
CORS_ORIGINS = ["http://localhost:5173"]
