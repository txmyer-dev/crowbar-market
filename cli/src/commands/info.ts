// cb info <slug>

import { getPlugin } from '../lib/registry';
import { isInstalled, getInstalled } from '../lib/manifest';
import { displayPluginCard } from '../lib/display';

export async function info(args: string[]): Promise<void> {
  const slug = args.find((a) => !a.startsWith('-'));

  if (!slug) {
    console.error('Usage: cb info <slug>');
    process.exit(1);
  }

  const plugin = getPlugin(slug);
  if (!plugin) {
    console.error(`Plugin "${slug}" not found in registry.`);
    process.exit(1);
  }

  displayPluginCard(plugin, true);

  if (isInstalled(slug)) {
    const installed = getInstalled(slug);
    if (installed) {
      console.log(`  \x1b[32mInstalled\x1b[0m v${installed.version} (${installed.installedAt.split('T')[0]})`);
      if (installed.files.length > 0) {
        console.log(`  Files: ${installed.files.join(', ')}`);
      }
    }
  } else {
    console.log(`  \x1b[2mNot installed\x1b[0m`);
  }
}
