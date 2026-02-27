// Installed plugins manifest — tracks what's installed and where

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { dirname } from 'path';
import { getManifestPath, getCrowbarDir } from './paths';
import type { InstalledManifest, InstalledPlugin } from '../types';

function ensureDir(): void {
  const dir = getCrowbarDir();
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
}

/** Load installed manifest */
export function loadManifest(): InstalledManifest {
  const path = getManifestPath();
  if (!existsSync(path)) {
    return { version: '1.0.0', plugins: {} };
  }
  return JSON.parse(readFileSync(path, 'utf-8'));
}

/** Save installed manifest */
export function saveManifest(manifest: InstalledManifest): void {
  ensureDir();
  writeFileSync(getManifestPath(), JSON.stringify(manifest, null, 2));
}

/** Record a plugin installation */
export function recordInstall(plugin: InstalledPlugin): void {
  const manifest = loadManifest();
  manifest.plugins[plugin.slug] = plugin;
  saveManifest(manifest);
}

/** Remove a plugin record */
export function removeRecord(slug: string): InstalledPlugin | undefined {
  const manifest = loadManifest();
  const record = manifest.plugins[slug];
  if (record) {
    delete manifest.plugins[slug];
    saveManifest(manifest);
  }
  return record;
}

/** Check if a plugin is installed */
export function isInstalled(slug: string): boolean {
  const manifest = loadManifest();
  return slug in manifest.plugins;
}

/** Get installed plugin record */
export function getInstalled(slug: string): InstalledPlugin | undefined {
  const manifest = loadManifest();
  return manifest.plugins[slug];
}
