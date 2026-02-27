// cb update [slug] — re-install newer version (remove + install)

import { loadManifest } from '../lib/manifest';
import { loadRegistry } from '../lib/registry';
import { uninstallPlugin } from '../lib/uninstaller';
import { installPlugin } from '../lib/installer';

export async function update(args: string[]): Promise<void> {
  const slug = args.find((a) => !a.startsWith('-'));
  const manifest = loadManifest();
  const registry = loadRegistry();

  const toUpdate: string[] = [];

  if (slug) {
    if (!manifest.plugins[slug]) {
      console.error(`Plugin "${slug}" is not installed.`);
      process.exit(1);
    }
    toUpdate.push(slug);
  } else {
    // Update all outdated
    for (const [s, installed] of Object.entries(manifest.plugins)) {
      const reg = registry.plugins[s];
      if (reg && reg.version !== installed.version) {
        toUpdate.push(s);
      }
    }
  }

  if (toUpdate.length === 0) {
    console.log('All plugins are up to date.');
    return;
  }

  for (const s of toUpdate) {
    const plugin = registry.plugins[s];
    if (!plugin) continue;

    console.log(`Updating ${s}...`);
    try {
      await uninstallPlugin(plugin);
      await installPlugin(plugin, { force: true });
    } catch (err: any) {
      console.error(`  Failed to update ${s}: ${err.message}`);
    }
  }
}
