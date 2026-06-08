# Sanctions Entity Explorer

A small fullstack slice of a compliance-investigation workflow: **search** sanctions
entities by name or alias (ranked fuzzy matches), then **visualize** a chosen entity's
relationships as a static radial graph.

- **Backend** — FastAPI (Python 3.14+), a read-only REST API over `data/sdn_sample.json`.
- **Frontend** — React 19 + TypeScript + Vite, two views (search + graph).

---

## Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| [uv](https://docs.astral.sh/uv/) | latest | Manages Python; **fetches CPython 3.14 automatically** — no system Python 3.14 needed. Must be on your `PATH`. |
| Node.js | ≥ 20 | |
| [pnpm](https://pnpm.io/) | ≥ 9 | `corepack enable` is the easiest way to get it. |

> The data fixture (`data/sdn_sample.json`) is the source of truth and is loaded once on
> backend startup. Do not modify it.

---

## Quick start (one command from the repo root)

```bash
pnpm install   # bootstraps BOTH apps: runs `uv sync` for the backend and `pnpm install` for the frontend
pnpm dev       # starts the API (:8000) and the web app (:5173) together
```

Then open **http://localhost:5173**.

`pnpm install` runs a `postinstall` that installs both apps, so you never have to `cd` into
`backend/` and `frontend/` separately. `pnpm dev` runs both processes with one command (via
[`concurrently`](https://www.npmjs.com/package/concurrently)); `Ctrl-C` stops both.

### Other root commands

```bash
pnpm test    # backend pytest + frontend vitest
pnpm check   # full gate: ruff + pytest + typecheck + vitest + production build
pnpm setup   # re-install both apps' dependencies
```

### Running an app on its own

You rarely need to, but each app is self-contained — see
[`backend/README.md`](backend/README.md) and [`frontend/README.md`](frontend/README.md).

---

## How it fits together

- The frontend calls **relative `/api/...`** paths. In dev, Vite proxies `/api` → `http://localhost:8000`
  (`frontend/vite.config.ts`), so the app is single-origin with no hardcoded host; a same-origin
  production deploy works identically. Backend CORS stays configured for `localhost:5173` as a safety net.

### API

| Method & path | Purpose |
|---|---|
| `GET /api/health` | Liveness check. |
| `GET /api/search?q={str}&limit={1–25}` | Ranked fuzzy matches over name + aliases. `q` and `limit` (default 10) are optional; empty/whitespace `q` → `{results: []}`. |
| `GET /api/entities/{id}` | Single entity summary. `404` if unknown. |
| `GET /api/entities/{id}/graph` | Center + neighbor nodes + edges, shaped for direct rendering. `404` if unknown. |

Interactive docs at **http://localhost:8000/docs** when the backend is running.

---

## Design decisions

The guiding principle is **proportionality** — clean, interview-defensible architecture with
zero anti-patterns and zero over-engineering for a small, fixed dataset.

**Backend**
- **One dependency that serves the requirement:** `rapidfuzz`. Its `WRatio` (with
  `default_process`) tolerates word reordering, partial names, and variant spellings — exactly
  what an investigator types. Scores are normalized to 0–1 and tagged with `matched_on`
  (`"name"` | `"alias"`) so the UI can show *why* and *how strongly* a record matched.
- **Pure, testable service cores:** `scoring`, `search`, and `graph` are pure functions over a
  repository — no I/O, no framework. Tests assert behavior, not plumbing.
- **Thin routes → services → repository.** The fixture is parsed through Pydantic models on
  startup (modern `lifespan`, not `on_event`) so any shape drift **fails loud** immediately.
  A single `EntityNotFound` → `404` exception handler keeps routes free of error plumbing.
- **Ranking:** top-N by score (then name), with **no hard threshold** — at 32 records, hiding
  plausible candidates is worse than showing weak ones. A floor would be added at scale.
- **Graph payload is shaped for the consumer:** `source`/`target`/`type` edges + `is_center`
  nodes are exactly what a renderer needs (and match the d3 / React-Flow convention).

**Frontend**
- **Hand-rolled data layer over a query library.** `useSearch` and `useEntityGraph` own
  debouncing, request cancellation (`AbortController`), and React 19 StrictMode safety directly —
  proportionate for two endpoints, and it makes the race/cancellation handling explicit.
- **Hand-rolled SVG radial graph over a graph library.** A pure `graph-layout.ts` (trig only,
  unit-tested) feeds a plain non-interactive SVG — matching the "static rendering" requirement
  without a heavy dependency.
- **`react-router-dom`** for deep-linkable `/entity/:id`, **CSS Modules + design tokens** for
  scoped styling with zero new build tooling.

**Testing**
- Backend: `pytest` over scoring/search/graph + a `TestClient` smoke suite (shapes, 404s, limit
  bounds, CORS). Frontend: `vitest` on the pure `graph-layout`.

---

## Project layout

```
.
├── package.json              # root runner (pnpm dev / test / check)
├── data/sdn_sample.json      # provided fixture — do not modify
├── backend/                  # FastAPI app + pytest suite (uv)
│   └── app/{api,services,…}  # thin routes → pure services → repository
└── frontend/                 # React + TS + Vite (pnpm)
    └── src/{api,hooks,features,components,styles}
```

---

**Approximate time spent:** ~2.5 hours.
