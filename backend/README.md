# Backend — Sanctions Entity Explorer

A read-only FastAPI service (Python 3.14+) over `../data/sdn_sample.json`: ranked fuzzy
search and an entity relations graph.

> To run the backend **and** frontend together with one command, see the root
> [`README.md`](../README.md). The steps below run the backend on its own.

## Setup

With [uv](https://docs.astral.sh/uv/) (recommended):

```bash
cd backend
uv sync
```

Or with pip:

```bash
cd backend
python3.14 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Run

```bash
uv run uvicorn app.main:app --reload --port 8000
# or, with the venv activated:
uvicorn app.main:app --reload --port 8000
```

API at http://localhost:8000. OpenAPI UI at http://localhost:8000/docs.

## Notes

- The fixture lives at `../data/sdn_sample.json`. Treat it as read-only — load it once on startup.
- CORS is preconfigured for `http://localhost:5173` (Vite default). Adjust if you change ports.
