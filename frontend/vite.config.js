import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { fileURLToPath } from "node:url";

const rootDir = fileURLToPath(new URL("../", import.meta.url));

console.log("ROOT ENV DIR:", rootDir);

export default defineConfig({
  plugins: [react()],
  envDir: rootDir,
});
