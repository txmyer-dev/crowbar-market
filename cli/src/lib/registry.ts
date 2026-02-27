// Registry loading and searching

import { existsSync, readFileSync } from 'fs';
import { join, dirname } from 'path';
import { getRegistryCachePath } from './paths';
import type { Registry, Plugin } from '../types';

/** Load registry from local cache or bundled fallback */
export function loadRegistry(): Registry {
  const cachePath = getRegistryCachePath();
  if (existsSync(cachePath)) {
    return JSON.parse(readFileSync(cachePath, 'utf-8'));
  }

  // Fallback: bundled registry in repo root
  const bundledPath = join(dirname(dirname(dirname(dirname(__dirname)))), 'registry.json');
  if (existsSync(bundledPath)) {
    return JSON.parse(readFileSync(bundledPath, 'utf-8'));
  }

  // Try CWD
  const cwdPath = join(process.cwd(), 'registry.json');
  if (existsSync(cwdPath)) {
    return JSON.parse(readFileSync(cwdPath, 'utf-8'));
  }

  console.error('No registry found. Run `cb sync` to fetch the latest registry.');
  process.exit(1);
}

/** Get plugin by slug */
export function getPlugin(slug: string): Plugin | undefined {
  const registry = loadRegistry();
  return registry.plugins[slug];
}

/** Search plugins by query string against name, description, tags */
export function searchPlugins(query: string, typeFilter?: string): Plugin[] {
  const registry = loadRegistry();
  const q = query.toLowerCase();
  return Object.values(registry.plugins).filter((p) => {
    if (typeFilter && p.type !== typeFilter) return false;
    return (
      p.name.toLowerCase().includes(q) ||
      p.slug.toLowerCase().includes(q) ||
      p.description.toLowerCase().includes(q) ||
      p.tags.some((t) => t.toLowerCase().includes(q))
    );
  });
}
