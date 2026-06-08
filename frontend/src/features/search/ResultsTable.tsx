import { useNavigate } from "react-router-dom";

import type { SearchResult } from "../../types";
import styles from "./ResultsTable.module.css";

interface ResultsTableProps {
  results: SearchResult[];
}

function formatScore(score: number): string {
  return `${Math.round(score * 100)}%`;
}

export function ResultsTable({ results }: ResultsTableProps) {
  const navigate = useNavigate();

  const open = (id: string) => navigate(`/entity/${encodeURIComponent(id)}`);

  return (
    <div className={styles.table}>
      <div className={styles.head} aria-hidden="true">
        <span>Entity</span>
        <span>Type</span>
        <span>Country</span>
        <span>Programs</span>
        <span>Match</span>
      </div>

      {results.map((result) => {
        const formattedScore = formatScore(result.score);
        return (
          <div
            key={result.id}
            className={styles.row}
            role="button"
            tabIndex={0}
            aria-label={`Open ${result.name}, ${result.type}, match ${formattedScore}`}
            onClick={() => open(result.id)}
            onKeyDown={(event) => {
              if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                open(result.id);
              }
            }}
          >
            <span className={styles.entity}>
              <span className={styles.name}>{result.name}</span>
              <span className={styles.id}>
                {result.id}
                {result.matched_on === "alias" ? (
                  <span className={styles.via}> · via alias</span>
                ) : null}
              </span>
            </span>

            <span className={styles.type}>
              <span className={styles.badge} data-type={result.type}>
                {result.type}
              </span>
            </span>

            <span className={styles.country}>{result.primary_country ?? "—"}</span>

            <span className={styles.programs}>
              {result.programs.length > 0 ? (
                result.programs.map((program) => (
                  <span key={program} className={styles.program}>
                    {program}
                  </span>
                ))
              ) : (
                <span className={styles.dim}>—</span>
              )}
            </span>

            <span className={styles.match}>
              <span className={styles.meter} aria-hidden="true">
                <span className={styles.meterFill} style={{ width: formattedScore }} />
              </span>
              <span className={styles.score}>{formattedScore}</span>
            </span>
          </div>
        );
      })}
    </div>
  );
}
