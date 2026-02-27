// cb list [--type <type>]

import { loadManifest } from '../lib/manifest';
import { loadRegistry } from '../lib/registry';
import { displayInstalledTable } from '../lib/display';

export async function list(args: string[]): Promise<void> {
  const typeIdx = args.indexOf('--type');
  const typeFilter = typeIdx !== -1 ? args[typeIdx + 1] : undefined;

  const manifest = loadManifest();
  const registry = loadRegistry();

  let entries = Object.entries(manifest.plugins);

  if (typeFilter) {
    entries = entries.filter(([slug]) => {
      const plugin = registry.plugins[slug];
      return plugin && plugin.type === typeFilter;
    });
  }

  entries.sort(([a], [b]) => a.localeCompare(b));
  displayInstalledTable(entries, typeFilter);
}
