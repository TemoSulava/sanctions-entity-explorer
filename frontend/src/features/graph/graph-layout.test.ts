import { describe, expect, it } from "vitest";

import type { EntityType, GraphEdge, GraphNode, GraphResponse } from "../../types";
import { type GraphLayout, layoutGraph, type PositionedNode } from "./graph-layout";

function makeNode(id: string, isCenter: boolean, type: EntityType = "organization"): GraphNode {
  return { id, name: id, type, is_center: isCenter };
}

function makeGraph(nodes: GraphNode[], edges: GraphEdge[] = []): GraphResponse {
  // `center` is unused by the layout; a placeholder summary keeps the shape valid.
  return {
    center: { id: "center", name: "center", type: "organization", primary_country: null },
    nodes,
    edges,
  };
}

function nodeById(layout: GraphLayout, id: string): PositionedNode {
  const found = layout.nodes.find((node) => node.id === id);
  if (!found) {
    throw new Error(`positioned node "${id}" not found`);
  }
  return found;
}

// Defaults from layoutGraph: width 760, height 560 -> center (380, 280), radius 184.
const CX = 380;
const CY = 280;
const R = 184;

describe("layoutGraph", () => {
  it("places a center-only graph at the middle with no edges (n=0)", () => {
    const layout = layoutGraph(makeGraph([makeNode("c", true)]));

    expect(layout.nodes).toHaveLength(1);
    expect(layout.edges).toHaveLength(0);
    const center = nodeById(layout, "c");
    expect(center.x).toBeCloseTo(CX, 3);
    expect(center.y).toBeCloseTo(CY, 3);
    expect(center.is_center).toBe(true);
  });

  it("places a single neighbor at the top, 12 o'clock (n=1)", () => {
    const layout = layoutGraph(makeGraph([makeNode("c", true), makeNode("n0", false)]));

    const neighbor = nodeById(layout, "n0");
    expect(neighbor.x).toBeCloseTo(CX, 3);
    expect(neighbor.y).toBeCloseTo(CY - R, 3);
  });

  it("distributes four neighbors at top, right, bottom, left (n=4)", () => {
    const layout = layoutGraph(
      makeGraph([
        makeNode("c", true),
        makeNode("n0", false),
        makeNode("n1", false),
        makeNode("n2", false),
        makeNode("n3", false),
      ]),
    );

    expect(nodeById(layout, "n0").x).toBeCloseTo(CX, 3);
    expect(nodeById(layout, "n0").y).toBeCloseTo(CY - R, 3); // top
    expect(nodeById(layout, "n1").x).toBeCloseTo(CX + R, 3); // right
    expect(nodeById(layout, "n1").y).toBeCloseTo(CY, 3);
    expect(nodeById(layout, "n2").x).toBeCloseTo(CX, 3); // bottom
    expect(nodeById(layout, "n2").y).toBeCloseTo(CY + R, 3);
    expect(nodeById(layout, "n3").x).toBeCloseTo(CX - R, 3); // left
    expect(nodeById(layout, "n3").y).toBeCloseTo(CY, 3);
  });

  it("resolves an edge to its endpoints and midpoint", () => {
    const layout = layoutGraph(
      makeGraph(
        [makeNode("c", true), makeNode("n0", false)],
        [{ source: "c", target: "n0", type: "operates", note: null }],
      ),
    );

    expect(layout.edges).toHaveLength(1);
    const [edge] = layout.edges;
    expect(edge?.x1).toBeCloseTo(CX, 3);
    expect(edge?.y1).toBeCloseTo(CY, 3);
    expect(edge?.x2).toBeCloseTo(CX, 3);
    expect(edge?.y2).toBeCloseTo(CY - R, 3);
    expect(edge?.midX).toBeCloseTo(CX, 3);
    expect(edge?.midY).toBeCloseTo(CY - R / 2, 3);
  });

  it("drops edges whose endpoints are not in the node set", () => {
    const layout = layoutGraph(
      makeGraph(
        [makeNode("c", true), makeNode("n0", false)],
        [
          { source: "c", target: "n0", type: "operates", note: null },
          { source: "c", target: "ghost", type: "dangling", note: null },
        ],
      ),
    );

    expect(layout.edges).toHaveLength(1);
    expect(layout.edges[0]?.target).toBe("n0");
  });

  it("honors width/height/radius overrides", () => {
    const layout = layoutGraph(makeGraph([makeNode("c", true), makeNode("n0", false)]), {
      width: 200,
      height: 200,
      radius: 50,
    });

    expect(layout.width).toBe(200);
    expect(layout.height).toBe(200);
    const center = nodeById(layout, "c");
    expect(center.x).toBeCloseTo(100, 3);
    expect(center.y).toBeCloseTo(100, 3);
    const neighbor = nodeById(layout, "n0");
    expect(neighbor.x).toBeCloseTo(100, 3);
    expect(neighbor.y).toBeCloseTo(50, 3); // 100 - radius
  });
});
