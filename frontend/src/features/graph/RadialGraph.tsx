import type { GraphResponse } from "../../types";
import { layoutGraph } from "./graph-layout";
import styles from "./RadialGraph.module.css";

const NEIGHBOR_RADIUS = 9;
const CENTER_RADIUS = 14;

function formatRelation(type: string): string {
  return type.replace(/_/g, " ");
}

export function RadialGraph({ graph }: { graph: GraphResponse }) {
  const { width, height, nodes, edges } = layoutGraph(graph);

  return (
    <svg
      className={styles.svg}
      viewBox={`0 0 ${width} ${height}`}
      role="img"
      aria-label={`Relationship graph for ${graph.center.name}`}
    >
      <defs>
        <filter id="node-glow" x="-60%" y="-60%" width="220%" height="220%">
          <feGaussianBlur stdDeviation="3.2" result="blur" />
          <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      <g>
        {edges.map((edge, index) => (
          <g key={`${edge.source}-${edge.target}-${edge.type}-${index}`}>
            <line
              className={styles.edge}
              x1={edge.x1}
              y1={edge.y1}
              x2={edge.x2}
              y2={edge.y2}
            />
            <text className={styles.edgeLabel} x={edge.midX} y={edge.midY}>
              {formatRelation(edge.type)}
            </text>
          </g>
        ))}
      </g>

      <g>
        {nodes.map((node) => {
          const r = node.is_center ? CENTER_RADIUS : NEIGHBOR_RADIUS;
          return (
            <g key={node.id} transform={`translate(${node.x}, ${node.y})`}>
              {node.is_center ? <circle className={styles.halo} r={r + 9} /> : null}
              <circle
                className={styles.node}
                r={r}
                data-type={node.type}
                data-center={node.is_center}
                filter={node.is_center ? "url(#node-glow)" : undefined}
              />
              <text className={styles.nodeLabel} y={r + 16} data-center={node.is_center}>
                {node.name}
              </text>
            </g>
          );
        })}
      </g>
    </svg>
  );
}
