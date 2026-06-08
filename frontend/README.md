# Frontend — Sanctions Entity Explorer

React 19 + TypeScript + Vite. Strict TS, `noUncheckedIndexedAccess` on. Search view +
non-interactive radial graph view.

> To run the frontend **and** backend together with one command, see the root
> [`README.md`](../README.md). The steps below run the frontend on its own.
> It expects the API at http://localhost:8000 (proxied via `/api`).

## Setup

```bash
cd frontend
pnpm install   # or: npm install / yarn install
```

## Run

```bash
pnpm dev
```

App at http://localhost:5173. Backend expected at http://localhost:8000.

## Build

```bash
pnpm build
```

## Type-check

```bash
pnpm typecheck
```

## Test

```bash
pnpm test   # vitest: pure graph-layout unit tests
```
