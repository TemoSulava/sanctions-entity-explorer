import type { GraphResponse, SearchResponse } from "../types";
import { apiFetch } from "./client";

export function searchEntities(
  query: string,
  limit?: number,
  signal?: AbortSignal,
): Promise<SearchResponse> {
  const params = new URLSearchParams({ q: query });
  if (limit !== undefined) {
    params.set("limit", String(limit));
  }
  return apiFetch<SearchResponse>(`/api/search?${params.toString()}`, { signal });
}

export function getEntityGraph(id: string, signal?: AbortSignal): Promise<GraphResponse> {
  return apiFetch<GraphResponse>(`/api/entities/${encodeURIComponent(id)}/graph`, { signal });
}
