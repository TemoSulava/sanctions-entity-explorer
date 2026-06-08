// Mirrors the backend response schemas (app/schemas.py) exactly.

export type EntityType = "organization" | "person" | "vessel";
export type MatchedOn = "name" | "alias";

export interface SearchResult {
  id: string;
  name: string;
  type: EntityType;
  primary_country: string | null;
  programs: string[];
  score: number;
  matched_on: MatchedOn;
}

export interface SearchResponse {
  query: string;
  results: SearchResult[];
}

export interface EntitySummary {
  id: string;
  name: string;
  type: EntityType;
  primary_country: string | null;
}

export interface GraphNode {
  id: string;
  name: string;
  type: EntityType;
  is_center: boolean;
}

export interface GraphEdge {
  source: string;
  target: string;
  type: string;
  note: string | null;
}

export interface GraphResponse {
  center: EntitySummary;
  nodes: GraphNode[];
  edges: GraphEdge[];
}
