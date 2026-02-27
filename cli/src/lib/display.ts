// Display helpers for CLI output

import type { Plugin, InstalledPlugin } from '../types';

const TYPE_COLORS: Record<string, string> = {
  'skill': '\x1b[36m',       // cyan
  'hook': '\x1b[33m',        // yellow
  'agent': '\x1b[35m',       // magenta
  'fabric-pattern': '\x1b[32m', // green
  'mcp-server': '\x1b[34m',  // blue
  'claude-plugin': '\x1b[31m', // red
};
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';
const DIM = '\x1b[2m';

/** Format a type badge */
export function typeBadge(type: string): string {
  const color = TYPE_COLORS[type] || '';
  return `${color}[${type}]${RESET}`;
}

/** Display a plugin card (search/info result) */
export function displayPluginCard(plugin: Plugin, verbose = false): void {
  console.log(`${BOLD}${plugin.name}${RESET} ${typeBadge(plugin.type)} ${DIM}v${plugin.version}${RESET}`);
  console.log(`  ${plugin.description}`);
  console.log(`  ${DIM}cb install ${plugin.slug}${RESET}`);
  if (plugin.tags.length > 0) {
    console.log(`  ${DIM}tags: ${plugin.tags.join(', ')}${RESET}`);
  }
  if (verbose) {
    console.log(`  ${DIM}source: ${plugin.source.type === 'github' ? `${plugin.source.repo}/${plugin.source.path}` : 'local'}${RESET}`);
    if (plugin.installTarget) console.log(`  ${DIM}target: ${plugin.installTarget}${RESET}`);
  }
  console.log();
}

/** Display installed plugins as table */
export function displayInstalledTable(plugins: [string, InstalledPlugin][], typeFilter?: string): void {
  if (plugins.length === 0) {
    console.log('No plugins installed.');
    return;
  }

  console.log(`${BOLD}Installed plugins${typeFilter ? ` (type: ${typeFilter})` : ''}:${RESET}\n`);

  const maxSlug = Math.max(...plugins.map(([slug]) => slug.length), 4);
  const maxVer = Math.max(...plugins.map(([, p]) => p.version.length), 7);

  console.log(`  ${'SLUG'.padEnd(maxSlug)}  ${'VERSION'.padEnd(maxVer)}  INSTALLED`);
  console.log(`  ${'-'.repeat(maxSlug)}  ${'-'.repeat(maxVer)}  ${'----------'}`);

  for (const [slug, installed] of plugins) {
    const date = installed.installedAt.split('T')[0];
    console.log(`  ${slug.padEnd(maxSlug)}  ${installed.version.padEnd(maxVer)}  ${date}`);
  }

  console.log(`\n  ${DIM}${plugins.length} plugin(s)${RESET}`);
}

/** Display outdated plugins */
export function displayOutdated(items: { slug: string; installed: string; latest: string }[]): void {
  if (items.length === 0) {
    console.log('All plugins are up to date.');
    return;
  }

  console.log(`${BOLD}Outdated plugins:${RESET}\n`);

  const maxSlug = Math.max(...items.map((i) => i.slug.length), 4);
  console.log(`  ${'SLUG'.padEnd(maxSlug)}  INSTALLED  LATEST`);
  console.log(`  ${'-'.repeat(maxSlug)}  ---------  ------`);

  for (const item of items) {
    console.log(`  ${item.slug.padEnd(maxSlug)}  ${item.installed.padEnd(9)}  ${item.latest}`);
  }

  console.log(`\n  ${DIM}Run \`cb update <slug>\` to update${RESET}`);
}
