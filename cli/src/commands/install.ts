// cb install <slug> [--force]

import { getPlugin } from '../lib/registry';
import { isInstalled } from '../lib/manifest';
import { installPlugin } from '../lib/installer';

export async function install(args: string[]): Promise<void> {
  const force = args.includes('--force');
  const slug = args.find((a) => !a.startsWith('-'));

  if (!slug) {
    console.error('Usage: cb install <slug> [--force]');
    process.exit(1);
  }

  const plugin = getPlugin(slug);
  if (!plugin) {
    console.error(`Plugin "${slug}" not found in registry.`);
    process.exit(1);
  }

  if (isInstalled(slug) && !force) {
    console.error(`Plugin "${slug}" is already installed. Use --force to reinstall.`);
    process.exit(1);
  }

  try {
    await installPlugin(plugin, { force });
  } catch (err: any) {
    console.error(`Install failed: ${err.message}`);
    process.exit(1);
  }
}
