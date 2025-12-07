import { build } from "vite";
import { build as esbuild } from "esbuild";
import { fileURLToPath } from "url";
import { dirname, resolve } from "path";
import fs from "fs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const rootDir = resolve(__dirname, "..");

async function buildClient() {
  console.log("Building client...");

  await build({
    root: resolve(rootDir, "client"),
    build: {
      outDir: resolve(rootDir, "dist/public"),
      emptyOutDir: true,
    },
  });

  console.log("Client build complete!");
}

async function buildServer() {
  console.log("Building server...");

  // Ensure dist directory exists
  const distDir = resolve(rootDir, "dist");
  if (!fs.existsSync(distDir)) {
    fs.mkdirSync(distDir, { recursive: true });
  }

  await esbuild({
    entryPoints: [resolve(rootDir, "server/index.ts")],
    bundle: true,
    platform: "node",
    target: "node18",
    format: "cjs",
    outfile: resolve(rootDir, "dist/index.cjs"),
    external: [
      // Don't bundle node_modules that have native dependencies
      "better-sqlite3",
      "pg-native",
      "bcrypt",
      "sharp",
      "@neondatabase/serverless",
      "ws",
    ],
    sourcemap: true,
    minify: false,
  });

  console.log("Server build complete!");
}

async function main() {
  try {
    await buildClient();
    await buildServer();
    console.log("\nBuild successful! 🎉");
  } catch (error) {
    console.error("Build failed:", error);
    process.exit(1);
  }
}

main();
