import { Link, useParams } from "react-router-dom";

import { StatusMessage } from "../../components/StatusMessage";
import { useEntityGraph } from "../../hooks/useEntityGraph";
import type { EntityType } from "../../types";
import { RadialGraph } from "./RadialGraph";
import styles from "./GraphView.module.css";

const LEGEND: { type: EntityType; label: string }[] = [
  { type: "organization", label: "organization" },
  { type: "person", label: "person" },
  { type: "vessel", label: "vessel" },
];

export default function GraphView() {
  const { id } = useParams<{ id: string }>();
  const state = useEntityGraph(id);

  return (
    <main className={styles.page}>
      <div className={styles.shell}>
        <Link to="/" className={styles.back}>
          ← Back to search
        </Link>

        {state.status === "loading" ? (
          <StatusMessage variant="loading" title="Loading graph…" />
        ) : null}

        {state.status === "error" ? (
          <StatusMessage variant="error" title="Could not load graph" detail={state.error} />
        ) : null}

        {state.status === "success" ? (
          <>
            <header className={styles.header}>
              <span className={styles.badge} data-type={state.data.center.type}>
                {state.data.center.type}
              </span>
              <h1 className={styles.title}>{state.data.center.name}</h1>
              <p className={styles.meta}>
                <span className={styles.id}>{state.data.center.id}</span>
                {state.data.center.primary_country ? (
                  <span>· {state.data.center.primary_country}</span>
                ) : null}
                <span>
                  · {state.data.edges.length}{" "}
                  {state.data.edges.length === 1 ? "relation" : "relations"}
                </span>
              </p>
            </header>

            {state.data.edges.length > 0 ? (
              <figure className={styles.canvas}>
                <RadialGraph graph={state.data} />
                <figcaption className={styles.legend}>
                  {LEGEND.map((item) => (
                    <span key={item.type} className={styles.legendItem}>
                      <span className={styles.swatch} data-type={item.type} aria-hidden="true" />
                      {item.label}
                    </span>
                  ))}
                </figcaption>
              </figure>
            ) : (
              <StatusMessage
                variant="empty"
                title="No known relations"
                detail="This entity has no connected entities in the dataset."
              />
            )}
          </>
        ) : null}
      </div>
    </main>
  );
}
