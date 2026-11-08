// Rewrites the "Latest from my GitHub" block of README.md with the newest public repos.
// Usage: GITHUB_TOKEN=... node scripts/update-latest-repos.mjs [username]
import { readFile, writeFile } from "node:fs/promises";

const USER = process.argv[2] || process.env.GITHUB_REPOSITORY_OWNER || "JuanMora1945";
const LIMIT = 6;
const START = "<!-- LATEST-REPOS:START -->";
const END = "<!-- LATEST-REPOS:END -->";
const EMPTY = '<p align="center"><sub>New projects are on the way. This list updates itself every day.</sub></p>';

const escape = (s) =>
  String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

const formatDate = (iso) =>
  new Date(iso).toLocaleDateString("en-US", { month: "short", year: "numeric", timeZone: "UTC" });

export function renderBlock(repos) {
  if (repos.length === 0) return EMPTY;
  const cells = repos.map((r) => {
    const lang = r.language ? ` · ${escape(r.language)}` : "";
    const desc = r.description ? escape(r.description) : "No description yet";
    const demo = r.homepage ? ` · <a href="${escape(r.homepage)}">live demo</a>` : "";
    return (
      `<td width="50%" valign="top"><a href="${escape(r.html_url)}"><b>${escape(r.name)}</b></a><br/>` +
      `<sub>${desc}</sub><br/><sub>Updated ${formatDate(r.pushed_at)}${lang}${demo}</sub></td>`
    );
  });
  const rows = [];
  for (let i = 0; i < cells.length; i += 2) rows.push(`  <tr>\n    ${cells.slice(i, i + 2).join("\n    ")}\n  </tr>`);
  return `<table>\n${rows.join("\n")}\n</table>`;
}

export function replaceBlock(readme, block) {
  const s = readme.indexOf(START);
  const e = readme.indexOf(END);
  if (s === -1 || e === -1 || e < s) throw new Error("README markers not found");
  return `${readme.slice(0, s + START.length)}\n${block}\n${readme.slice(e)}`;
}

async function fetchRepos() {
  const headers = { Accept: "application/vnd.github+json", "User-Agent": "profile-readme-updater" };
  if (process.env.GITHUB_TOKEN) headers.Authorization = `Bearer ${process.env.GITHUB_TOKEN}`;
  const res = await fetch(`https://api.github.com/users/${USER}/repos?type=owner&sort=pushed&per_page=100`, { headers });
  if (!res.ok) throw new Error(`GitHub API ${res.status}: ${await res.text()}`);
  const all = await res.json();
  return all
    .filter((r) => !r.fork && !r.private && !r.archived && r.name.toLowerCase() !== USER.toLowerCase())
    .slice(0, LIMIT);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const repos = await fetchRepos();
  const readme = await readFile("README.md", "utf8");
  const next = replaceBlock(readme, renderBlock(repos));
  if (next !== readme) {
    await writeFile("README.md", next);
    console.log(`README updated with ${repos.length} repo(s).`);
  } else {
    console.log("README already up to date.");
  }
}
