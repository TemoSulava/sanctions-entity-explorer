import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // Single origin in dev: the SPA calls relative /api, proxied to the backend.
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
});
