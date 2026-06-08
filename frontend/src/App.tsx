import { Route, Routes } from "react-router-dom";

import GraphView from "./features/graph/GraphView";
import SearchView from "./features/search/SearchView";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<SearchView />} />
      <Route path="/entity/:id" element={<GraphView />} />
    </Routes>
  );
}
