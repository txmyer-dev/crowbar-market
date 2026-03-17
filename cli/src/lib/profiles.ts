// Profile loader — curated skill sets for different deployment contexts
// No external yaml dependency — uses a simple line-by-line parser

import { existsSync, readFileSync, readdirSync } from 'fs';
import { join, dirname } from 'path';

function getProfilesDir(): string {
  // 1. Explicit env
  const marketDir = process.env.CROWBAR_MARKET_DIR;
  if (marketDir && existsSync(join(marketDir, 'profiles'))) {
    return join(marketDir, 'profiles');
  }

  // 2. Relative to this source file (dev mode)
  const srcRelative = join(dirname(new URL(import.meta.url).pathname), '../../../profiles');
  if (existsSync(srcRelative)) return srcRelative;

  // 3. Relative to cwd (run from repo root)
  const cwdRelative = join(process.cwd(), 'profiles');
  if (existsSync(cwdRelative)) return cwdRelative;

  throw new Error(
    'profiles/ directory not found.\n' +
    'Set CROWBAR_MARKET_DIR=/path/to/crowbar-market'
  );
}

export interface Profile {
  name: string;
  description: string;
  version: string;
  skills: string[];
  agents?: string[];
  hooks?: string[];
}

export function loadProfile(name: string): Profile {
  const profilesDir = getProfilesDir();
  const profilePath = join(profilesDir, `${name}.yaml`);

  if (!existsSync(profilePath)) {
    const available = existsSync(profilesDir)
      ? readdirSync(profilesDir)
          .filter((f) => f.endsWith('.yaml'))
          .map((f) => f.replace('.yaml', ''))
      : [];
    const hint = available.length > 0 ? `\nAvailable: ${available.join(', ')}` : '';
    throw new Error(`Profile "${name}" not found.${hint}`);
  }

  return parseYaml(readFileSync(profilePath, 'utf-8'));
}

function parseYaml(content: string): Profile {
  const result: any = { skills: [], agents: [], hooks: [] };
  let currentList: string | null = null;

  for (const rawLine of content.split('\n')) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#')) continue;

    // List item
    if (line.startsWith('- ')) {
      if (currentList) {
        result[currentList].push(line.slice(2).trim());
      }
      continue;
    }

    // Key: value or Key: (start of list)
    const colonIdx = line.indexOf(':');
    if (colonIdx === -1) continue;

    const key = line.slice(0, colonIdx).trim();
    const value = line.slice(colonIdx + 1).trim().replace(/^"|"$/g, '');

    if (value) {
      result[key] = value;
      currentList = null;
    } else {
      currentList = key;
    }
  }

  return result as Profile;
}
