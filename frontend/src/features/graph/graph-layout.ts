import type { GraphNode, GraphResponse } from "../../types";

export interface PositionedNode extends GraphNode {
  x: number;
  y: number;
}

export interface PositionedEdge {
  source: string;
  target: string;
  type: string;
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  midX: number;
  midY: number;
}

export interface GraphLayout {
  width: number;
  height: number;
  nodes: PositionedNode[];
  edges: PositionedEdge[];
}

export interface LayoutOptions {
  width?: number;
  height?: number;
  /** Distance from center to each neighbor; defaults to fit the viewport. */
  radius?: number;
}

/**
 * Pure radial layout: the center node sits at the middle and each of the `n`
 * neighbors is placed on a circle at angle `2π·i/n` (starting at 12 o'clock).
 * No DOM, no React — trivially unit-testable.
 */
export function layoutGraph(graph: GraphResponse, options: LayoutOptions = {}): GraphLayout {
  const width = options.width ?? 760;
  const height = options.height ?? 560;
  const cx = width / 2;
  const cy = height / 2;
  // Inset so the outermost node circle and its label stay inside the viewport.
  const radius = options.radius ?? Math.min(width, height) / 2 - 96;

  const positioned = new Map<string, PositionedNode>();
  // The backend emits exactly one center node per graph.
  const center = graph.nodes.find((node) => node.is_center);
  const neighbors = graph.nodes.filter((node) => !node.is_center);

  if (center) {
    positioned.set(center.id, { ...center, x: cx, y: cy });
  }

  neighbors.forEach((node, index) => {
    // Start at the top (-90°) and distribute evenly clockwise.
    const angle = (2 * Math.PI * index) / neighbors.length - Math.PI / 2;
    positioned.set(node.id, {
      ...node,
      x: cx + radius * Math.cos(angle),
      y: cy + radius * Math.sin(angle),
    });
  });

  const nodes = graph.nodes
    .map((node) => positioned.get(node.id))
    .filter((node): node is PositionedNode => node !== undefined);

  const edges = graph.edges
    .map((edge): PositionedEdge | null => {
      const source = positioned.get(edge.source);
      const target = positioned.get(edge.target);
      if (!source || !target) {
        return null;
      }
      return {
        source: edge.source,
        target: edge.target,
        type: edge.type,
        x1: source.x,
        y1: source.y,
        x2: target.x,
        y2: target.y,
        midX: (source.x + target.x) / 2,
        midY: (source.y + target.y) / 2,
      };
    })
    .filter((edge): edge is PositionedEdge => edge !== null);

  return { width, height, nodes, edges };
}
