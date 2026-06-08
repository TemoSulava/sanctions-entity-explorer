import { useState } from "react";

import { StatusMessage } from "../../components/StatusMessage";
import { useSearch } from "../../hooks/useSearch";
import { ResultsTable } from "./ResultsTable";
import styles from "./SearchView.module.css";

export default function SearchView() {
  const [query, setQuery] = useState("");
  const { status, results, error } = useSearch(query);

  let body;
  if (status === "idle") {
    body = (
      <StatusMessage
        variant="idle"
        title="Start typing to search"
        detail="Results rank by match strength across names and aliases."
      />
    );
  } else if (status === "loading") {
    body = <StatusMessage variant="loading" title="Scanning watchlist…" />;
  } else if (status === "error") {
    body = <StatusMessage variant="error" title="Search failed" detail={error ?? undefined} />;
  } else if (results.length === 0) {
    body = (
      <StatusMessage
        variant="empty"
        title="No matching entities"
        detail="Try a partial name or a known alias."
      />
    );
  } else {
    body = <ResultsTable results={results} />;
  }

  return (
    <main className={styles.page}>
      <div className={styles.shell}>
        <header className={styles.masthead}>
          <p className={styles.eyebrow}>OFAC · SDN · Consolidated Watchlist</p>
          <h1 className={styles.title}>Sanctions Entity Explorer</h1>
          <p className={styles.lede}>
            Screen organizations, individuals, and vessels by name or alias, then trace their
            network of relations.
          </p>
        </header>

        <div className={styles.searchBar}>
          <span className={styles.searchGlyph} aria-hidden="true">
            ⌕
          </span>
          <input
            className={styles.input}
            type="search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="search by name or alias…"
            spellCheck={false}
            autoComplete="off"
            autoFocus
            aria-label="Search sanctions entities"
          />
          {status === "success" ? (
            <span className={styles.count}>
              {results.length} {results.length === 1 ? "match" : "matches"}
            </span>
          ) : null}
        </div>

        <section className={styles.results}>{body}</section>
      </div>
    </main>
  );
}
