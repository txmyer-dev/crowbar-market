// Centralized path resolution — reuses pattern from ~/.claude/hooks/lib/paths.ts

import { homedir } from 'os';
import { join } from 'path';

/** Expand shell variables: $HOME, ${HOME}, ~ */
export function expandPath(path: string): string {
  const home = homedir();
  return path
    .replace(/^\$HOME(?=\/|$)/, home)
    .replace(/^\$\{HOME\}(?=\/|$)/, home)
    .replace(/^~(?=\/|$)/, home);
}

/** Get PAI directory. Priority: PAI_DIR env → ~/.claude */
export function getPaiDir(): string {
  const envPaiDir = process.env.PAI_DIR;
  if (envPaiDir) return expandPath(envPaiDir);
  return join(homedir(), '.claude');
}

/** Get path relative to PAI_DIR */
export function paiPath(...segments: string[]): string {
  return join(getPaiDir(), ...segments);
}

/** Crowbar local state directory */
export function getCrowbarDir(): string {
  return paiPath('crowbar');
}

/** Installed manifest path */
export function getManifestPath(): string {
  return join(getCrowbarDir(), 'installed.json');
}

/** Backups directory */
export function getBackupsDir(): string {
  return join(getCrowbarDir(), 'backups');
}

/** Local registry cache */
export function getRegistryCachePath(): string {
  return join(getCrowbarDir(), 'registry.json');
}
