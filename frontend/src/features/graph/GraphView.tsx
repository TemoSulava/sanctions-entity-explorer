import { useParams } from "react-router-dom";

// Placeholder — the graph UI is built in Phase 7.
export default function GraphView() {
  const { id } = useParams<{ id: string }>();
  return (
    <main style={{ padding: "2rem", fontFamily: "var(--font-mono)" }}>
      <p>Graph for {id}</p>
    </main>
  );
}
