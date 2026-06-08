import { useEffect, useState } from "react";

import { ApiError } from "../api/client";
import { searchEntities } from "../api/entities";
import type { SearchResult } from "../types";
import { useDebouncedValue } from "./useDebouncedValue";

export type SearchStatus = "idle" | "loading" | "success" | "error";

export interface SearchState {
  status: SearchStatus;
  query: string;
  results: SearchResult[];
  error: string | null;
}

const IDLE: SearchState = { status: "idle", query: "", results: [], error: null };

/**
 * Debounced entity search. Each query change cancels the in-flight request via
 * an AbortController, so stale responses never clobber newer ones and React 19
 * StrictMode's double-invoked effect is safe (the aborted run never setStates).
 */
export function useSearch(query: string, limit?: number): SearchState {
  const debouncedQuery = useDebouncedValue(query, 300);
  const [state, setState] = useState<SearchState>(IDLE);

  useEffect(() => {
    const trimmed = debouncedQuery.trim();
    if (!trimmed) {
      setState(IDLE);
      return;
    }

    const controller = new AbortController();
    setState({ status: "loading", query: trimmed, results: [], error: null });

    searchEntities(trimmed, limit, controller.signal)
      .then((response) => {
        // A response that resolved just before its abort propagated must not
        // clobber a newer request's state.
        if (controller.signal.aborted) {
          return;
        }
        setState({
          status: "success",
          query: response.query,
          results: response.results,
          error: null,
        });
      })
      .catch((error: unknown) => {
        // Aborted (stale request or StrictMode cleanup) — drop it silently.
        if (controller.signal.aborted) {
          return;
        }
        const message =
          error instanceof ApiError ? error.message : "Search failed. Please try again.";
        setState({ status: "error", query: trimmed, results: [], error: message });
      });

    return () => controller.abort();
  }, [debouncedQuery, limit]);

  return state;
}
