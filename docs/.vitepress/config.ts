import { readdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { defineConfig, type DefaultTheme } from "vitepress";

const __dirname = dirname(fileURLToPath(import.meta.url));
const DOCS_ROOT = resolve(__dirname, "..");

const ACRONYMS: Record<string, string> = {
  adr: "ADR",
  api: "API",
  ci: "CI",
  cors: "CORS",
  dx: "DX",
  e2e: "E2E",
  fastapi: "FastAPI",
  gitea: "Gitea",
  github: "GitHub",
  http: "HTTP",
  json: "JSON",
  openapi: "OpenAPI",
  postgresql: "PostgreSQL",
  redis: "Redis",
  sbom: "SBOM",
  sql: "SQL",
  taskiq: "Taskiq",
  testcontainers: "Testcontainers",
  ui: "UI",
};

function titleCase(rawSegment: string): string {
  return rawSegment
    .split("-")
    .map((part) => {
      const lower = part.toLowerCase();
      if (ACRONYMS[lower]) {
        return ACRONYMS[lower];
      }
      return part.charAt(0).toUpperCase() + part.slice(1);
    })
    .join(" ");
}

function fileLabel(filename: string): string {
  const stem = filename.replace(/\.md$/u, "");
  if (stem === "README") {
    return "Overview";
  }
  if (stem === "INDEX") {
    return "Reading Map";
  }

  const numbered = stem.match(/^(\d{4})-(.+)$/u);
  if (numbered) {
    return `ADR-${numbered[1]} ${titleCase(numbered[2])}`;
  }

  return titleCase(stem);
}

function markdownFiles(relativeDir: string): string[] {
  return readdirSync(resolve(DOCS_ROOT, relativeDir))
    .filter((entry) => entry.endsWith(".md"))
    .sort((left, right) => left.localeCompare(right));
}

function linkFor(relativeDir: string, filename: string): string {
  return `/${relativeDir}/${filename.replace(/\.md$/u, "")}`;
}

function buildItems(relativeDir: string): DefaultTheme.SidebarItem[] {
  return markdownFiles(relativeDir).map((filename) => ({
    text: fileLabel(filename),
    link: linkFor(relativeDir, filename),
  }));
}

function buildAdrSidebar(): DefaultTheme.SidebarItem[] {
  return [
    {
      text: "Start Here",
      items: [
        { text: "ADR Root", link: "/adr/README" },
        { text: "ADR Reading Map", link: "/adr/INDEX" },
      ],
    },
    {
      text: "Architecture ADRs",
      items: buildItems("adr/architecture"),
    },
    {
      text: "Engineering ADRs",
      items: buildItems("adr/engineering"),
    },
    {
      text: "Reference Product ADRs",
      items: buildItems("adr/product"),
    },
  ];
}

export default defineConfig({
  title: "Fullstack Template",
  description:
    "Opinionated FastAPI + Vue fullstack template with contract parity checks, ADR-driven governance, and observability baseline.",
  base: "/fullstack-template/",
  cleanUrls: true,
  lastUpdated: true,
  appearance: false,
  head: [
    ["meta", { name: "theme-color", content: "#08111d" }],
    ["meta", { property: "og:title", content: "Fullstack Template" }],
    [
      "meta",
      {
        property: "og:description",
        content:
          "Opinionated FastAPI + Vue fullstack template with contract parity checks, ADR-driven governance, and observability baseline.",
      },
    ],
  ],
  markdown: {
    theme: {
      light: "github-dark",
      dark: "github-dark",
    },
  },
  vite: {
    server: {
      host: "0.0.0.0",
      port: 4173,
    },
  },
  themeConfig: {
    logo: { text: "FT" },
    nav: [
      { text: "Overview", link: "/overview" },
      { text: "Get Started", link: "/getting-started" },
      { text: "Philosophy", link: "/template/PHILOSOPHY" },
      { text: "ADR Map", link: "/adr/INDEX" },
      { text: "UI Layer", link: "/frontend/ui-layer" },
      { text: "GitHub", link: "https://github.com/Mesteriis/fullstack-template" },
    ],
    search: {
      provider: "local",
    },
    socialLinks: [
      { icon: "github", link: "https://github.com/Mesteriis/fullstack-template" },
    ],
    outline: {
      level: [2, 3],
    },
    editLink: {
      pattern: "https://github.com/Mesteriis/fullstack-template/edit/main/docs/:path",
      text: "Edit this page on GitHub",
    },
    sidebar: {
      "/adr/": buildAdrSidebar(),
      "/frontend/": [
        {
          text: "Frontend",
          items: [{ text: "UI Layer", link: "/frontend/ui-layer" }],
        },
      ],
      "/template/": [
        {
          text: "Template",
          items: [{ text: "Philosophy", link: "/template/PHILOSOPHY" }],
        },
      ],
      "/": [
        {
          text: "Start Here",
          items: [
            { text: "Home", link: "/" },
            { text: "Template Overview", link: "/overview" },
            { text: "Getting Started", link: "/getting-started" },
            { text: "Template Philosophy", link: "/template/PHILOSOPHY" },
            { text: "Frontend UI Layer", link: "/frontend/ui-layer" },
          ],
        },
        ...buildAdrSidebar(),
      ],
    },
    footer: {
      message: "Fullstack Template documentation portal",
      copyright: "Released as a reusable engineering baseline.",
    },
  },
});
