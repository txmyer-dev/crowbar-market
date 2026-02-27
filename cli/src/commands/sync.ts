// cb sync — pull latest registry.json from remote

import { mkdirSync, existsSync, writeFileSync } from 'fs';
import { dirname } from 'path';
import { getRegistryCachePath } from '../lib/paths';

const REGISTRY_URL = 'https://raw.githubusercontent.com/txmyer-dev/crowbar-market/main/registry.json';

export async function sync(_args: string[]): Promise<void> {
  console.log('Syncing registry from remote...');

  try {
    const response = await fetch(REGISTRY_URL);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.text();
    // Validate JSON
    const parsed = JSON.parse(data);

    const cachePath = getRegistryCachePath();
    const dir = dirname(cachePath);
    if (!existsSync(dir)) mkdirSync(dir, { recursive: true });

    writeFileSync(cachePath, data);

    const count = Object.keys(parsed.plugins || {}).length;
    console.log(`Registry synced: ${count} plugins (v${parsed.version})`);
  } catch (err: any) {
    console.error(`Sync failed: ${err.message}`);
    process.exit(1);
  }
}
