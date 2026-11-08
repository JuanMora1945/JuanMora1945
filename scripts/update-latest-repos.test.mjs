import { test } from "node:test";
import assert from "node:assert/strict";
import { renderBlock, replaceBlock } from "./update-latest-repos.mjs";

const repo = (name, extra = {}) => ({
  name,
  html_url: `https://github.com/JuanMora1945/${name}`,
  description: "A small demo",
  language: "JavaScript",
  homepage: "",
  pushed_at: "2026-11-07T12:00:00Z",
  ...extra,
});

test("shows a friendly placeholder when there are no repos", () => {
  assert.match(renderBlock([]), /New projects are on the way/);
});

test("renders two repos per row with link, description, date and language", () => {
  const html = renderBlock([repo("one"), repo("two"), repo("three")]);
  assert.equal((html.match(/<tr>/g) || []).length, 2);
  assert.match(html, /href="https:\/\/github.com\/JuanMora1945\/one"><b>one<\/b>/);
  assert.match(html, /Updated Nov 2026 · JavaScript/);
});

test("adds a live demo link only when the repo has a homepage", () => {
  assert.match(renderBlock([repo("site", { homepage: "https://example.com" })]), /live demo/);
  assert.doesNotMatch(renderBlock([repo("plain")]), /live demo/);
});

test("escapes HTML in repo descriptions", () => {
  assert.match(renderBlock([repo("x", { description: "<script>" })]), /&lt;script&gt;/);
});

test("replaces only the content between the markers", () => {
  const readme = "top\n<!-- LATEST-REPOS:START -->\nold\n<!-- LATEST-REPOS:END -->\nbottom";
  assert.equal(
    replaceBlock(readme, "new"),
    "top\n<!-- LATEST-REPOS:START -->\nnew\n<!-- LATEST-REPOS:END -->\nbottom",
  );
});

test("fails loudly when the markers are missing", () => {
  assert.throws(() => replaceBlock("no markers", "x"), /markers not found/);
});
