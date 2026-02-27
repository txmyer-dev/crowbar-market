// cb build-site — generate static HTML catalog from registry

import { writeFileSync, mkdirSync, existsSync, copyFileSync } from 'fs';
import { join } from 'path';
import { loadRegistry } from '../lib/registry';
import type { Plugin } from '../types';

export async function buildSite(args: string[]): Promise<void> {
  const outDir = args.find((a) => !a.startsWith('-')) || join(process.cwd(), 'site');
  const registry = loadRegistry();
  const plugins = Object.values(registry.plugins);

  mkdirSync(outDir, { recursive: true });

  const types = [...new Set(plugins.map((p) => p.type))].sort();
  const typeCounts = types.map((t) => ({ type: t, count: plugins.filter((p) => p.type === t).length }));

  const html = generateHTML(plugins, typeCounts, registry.version);
  writeFileSync(join(outDir, 'index.html'), html);

  console.log(`Site generated: ${outDir}/index.html`);
  console.log(`  ${plugins.length} plugins across ${types.length} types`);
}

function generateHTML(plugins: Plugin[], typeCounts: { type: string; count: number }[], version: string): string {
  const pluginCards = plugins
    .sort((a, b) => a.name.localeCompare(b.name))
    .map((p) => `
      <div class="card" data-type="${p.type}" data-search="${[p.name, p.description, ...p.tags].join(' ').toLowerCase()}">
        <div class="card-header">
          <span class="card-name">${escapeHtml(p.name)}</span>
          <span class="badge badge-${p.type}">${p.type}</span>
        </div>
        <p class="card-desc">${escapeHtml(p.description)}</p>
        <div class="card-footer">
          <code class="install-cmd">cb install ${escapeHtml(p.slug)}</code>
          <span class="version">v${escapeHtml(p.version)}</span>
        </div>
        ${p.tags.length > 0 ? `<div class="tags">${p.tags.map((t) => `<span class="tag">${escapeHtml(t)}</span>`).join('')}</div>` : ''}
      </div>`)
    .join('\n');

  const filterPills = typeCounts.map((tc) =>
    `<button class="pill" data-filter="${tc.type}">${tc.type} <span class="count">${tc.count}</span></button>`
  ).join('\n          ');

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Crowbar Market</title>
  <style>
    :root {
      --bg: #0d1117;
      --surface: #161b22;
      --border: #30363d;
      --text: #e6edf3;
      --text-dim: #8b949e;
      --accent: #3b82f6;
      --accent-hover: #60a5fa;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
    }

    .header {
      border-bottom: 1px solid var(--border);
      padding: 2rem 0;
      text-align: center;
    }

    .header h1 {
      font-size: 2rem;
      font-weight: 700;
      margin-bottom: 0.5rem;
    }

    .header h1 span { color: var(--accent); }

    .header p {
      color: var(--text-dim);
      font-size: 1.1rem;
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 2rem 1rem;
    }

    .controls {
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      margin-bottom: 2rem;
      align-items: center;
    }

    .search-box {
      flex: 1;
      min-width: 250px;
      padding: 0.75rem 1rem;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--text);
      font-size: 1rem;
      outline: none;
    }

    .search-box:focus { border-color: var(--accent); }
    .search-box::placeholder { color: var(--text-dim); }

    .pills {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
    }

    .pill {
      padding: 0.4rem 0.8rem;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 20px;
      color: var(--text-dim);
      cursor: pointer;
      font-size: 0.85rem;
      transition: all 0.15s;
    }

    .pill:hover { border-color: var(--accent); color: var(--text); }
    .pill.active { background: var(--accent); border-color: var(--accent); color: #fff; }
    .pill .count { opacity: 0.6; font-size: 0.8em; }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: 1rem;
    }

    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1.25rem;
      transition: border-color 0.15s;
    }

    .card:hover { border-color: var(--accent); }

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.5rem;
    }

    .card-name { font-weight: 600; font-size: 1.1rem; }

    .badge {
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
    }

    .badge-skill { background: #0d4f4f; color: #5eead4; }
    .badge-hook { background: #4a3600; color: #fbbf24; }
    .badge-agent { background: #3b1f5e; color: #c084fc; }
    .badge-fabric-pattern { background: #14532d; color: #4ade80; }
    .badge-mcp-server { background: #1e3a5f; color: #60a5fa; }
    .badge-claude-plugin { background: #5c1a1a; color: #f87171; }

    .card-desc {
      color: var(--text-dim);
      font-size: 0.9rem;
      margin-bottom: 0.75rem;
    }

    .card-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .install-cmd {
      background: var(--bg);
      padding: 0.3rem 0.6rem;
      border-radius: 4px;
      font-size: 0.8rem;
      color: var(--accent);
      cursor: pointer;
    }

    .install-cmd:hover { color: var(--accent-hover); }

    .version {
      color: var(--text-dim);
      font-size: 0.8rem;
    }

    .tags {
      display: flex;
      flex-wrap: wrap;
      gap: 0.3rem;
      margin-top: 0.5rem;
    }

    .tag {
      font-size: 0.7rem;
      color: var(--text-dim);
      background: var(--bg);
      padding: 0.15rem 0.4rem;
      border-radius: 3px;
    }

    .stats {
      text-align: center;
      color: var(--text-dim);
      margin-bottom: 1.5rem;
      font-size: 0.9rem;
    }

    .hidden { display: none !important; }
  </style>
</head>
<body>
  <div class="header">
    <h1><span>Crowbar</span> Market</h1>
    <p>Plugin marketplace for PAI &mdash; more leverage for your AI</p>
  </div>
  <div class="container">
    <div class="stats">${plugins.length} plugins &bull; Registry v${escapeHtml(version)}</div>
    <div class="controls">
      <input type="text" class="search-box" placeholder="Search plugins..." id="search">
      <div class="pills">
        <button class="pill active" data-filter="all">All</button>
        ${filterPills}
      </div>
    </div>
    <div class="grid" id="grid">
      ${pluginCards}
    </div>
  </div>
  <script>
    const search = document.getElementById('search');
    const grid = document.getElementById('grid');
    const pills = document.querySelectorAll('.pill');
    let activeFilter = 'all';

    function filterCards() {
      const q = search.value.toLowerCase();
      const cards = grid.querySelectorAll('.card');
      cards.forEach(card => {
        const matchType = activeFilter === 'all' || card.dataset.type === activeFilter;
        const matchSearch = !q || card.dataset.search.includes(q);
        card.classList.toggle('hidden', !(matchType && matchSearch));
      });
    }

    search.addEventListener('input', filterCards);

    pills.forEach(pill => {
      pill.addEventListener('click', () => {
        pills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        activeFilter = pill.dataset.filter;
        filterCards();
      });
    });

    // Click to copy install command
    grid.addEventListener('click', (e) => {
      if (e.target.classList.contains('install-cmd')) {
        navigator.clipboard.writeText(e.target.textContent);
        const orig = e.target.textContent;
        e.target.textContent = 'Copied!';
        setTimeout(() => e.target.textContent = orig, 1500);
      }
    });
  </script>
</body>
</html>`;
}

function escapeHtml(str: string): string {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
