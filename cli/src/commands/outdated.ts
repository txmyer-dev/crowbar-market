// cb outdated — compare installed versions to registry

import { loadManifest } from '../lib/manifest';
import { loadRegistry } from '../lib/registry';
import { displayOutdated } from '../lib/display';

export async function outdated(_args: string[]): Promise<void> {
  const manifest = loadManifest();
  const registry = loadRegistry();

  const items: { slug: string; installed: string; latest: string }[] = [];

  for (const [slug, installed] of Object.entries(manifest.plugins)) {
    const registryPlugin = registry.plugins[slug];
    if (registryPlugin && registryPlugin.version !== installed.version) {
      items.push({
        slug,
        installed: installed.version,
        latest: registryPlugin.version,
      });
    }
  }

  displayOutdated(items);
}
