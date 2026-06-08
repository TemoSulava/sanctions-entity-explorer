// Thin fetch wrapper. Calls relative /api paths so the Vite dev proxy (and a
// same-origin production deploy) route to the backend with no hardcoded host.

export class ApiError extends Error {
  readonly status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

interface ApiFetchOptions {
  signal?: AbortSignal;
}

function extractDetail(body: unknown, fallback: string): string {
  if (body && typeof body === "object" && "detail" in body) {
    const detail = (body as { detail: unknown }).detail;
    if (typeof detail === "string") {
      return detail;
    }
  }
  return fallback;
}

export async function apiFetch<T>(path: string, { signal }: ApiFetchOptions = {}): Promise<T> {
  const response = await fetch(path, {
    signal,
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    let body: unknown = null;
    try {
      body = await response.json();
    } catch {
      // Non-JSON error body — fall back to a generic message below.
    }
    throw new ApiError(response.status, extractDetail(body, `Request failed (${response.status})`));
  }

  // Trusted cast: the T types in types.ts mirror the backend Pydantic schemas
  // directly, so a runtime validation layer (e.g. zod) would be redundant here.
  return (await response.json()) as T;
}
