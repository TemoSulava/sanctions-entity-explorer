import { useEffect, useState } from "react";

import { ApiError } from "../api/client";
import { getEntityGraph } from "../api/entities";
import type { GraphResponse } from "../types";

export type GraphStatus = "loading" | "success" | "error";

export interface GraphState {
  status: GraphStatus;
  data: GraphResponse | null;
  error: string | null;
}

/**
 * Fetches one entity's relation graph. Aborts the in-flight request when `id`
 * changes or the view unmounts, with the same abort-guarding as useSearch so
 * stale responses and StrictMode's double-invoke can't leak state.
 */
export function useEntityGraph(id: string | undefined): GraphState {
  const [state, setState] = useState<GraphState>({ status: "loading", data: null, error: null });

  useEffect(() => {
    if (!id) {
      setState({ status: "error", data: null, error: "No entity was specified." });
      return;
    }

    const controller = new AbortController();
    setState({ status: "loading", data: null, error: null });

    getEntityGraph(id, controller.signal)
      .then((graph) => {
        if (controller.signal.aborted) {
          return;
        }
        setState({ status: "success", data: graph, error: null });
      })
      .catch((error: unknown) => {
        if (controller.signal.aborted) {
          return;
        }
        const message =
          error instanceof ApiError ? error.message : "Could not load the relationship graph.";
        setState({ status: "error", data: null, error: message });
      });

    return () => controller.abort();
  }, [id]);

  return state;
}
