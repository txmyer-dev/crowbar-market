// cb remove <slug>

import { getPlugin } from '../lib/registry';
import { isInstalled } from '../lib/manifest';
import { uninstallPlugin } from '../lib/uninstaller';

export async function remove(args: string[]): Promise<void> {
  const slug = args.find((a) => !a.startsWith('-'));

  if (!slug) {
    console.error('Usage: cb remove <slug>');
    process.exit(1);
  }

  if (!isInstalled(slug)) {
    console.error(`Plugin "${slug}" is not installed.`);
    process.exit(1);
  }

  const plugin = getPlugin(slug);
  if (!plugin) {
    console.error(`Plugin "${slug}" not found in registry. Removing manifest entry only.`);
    const { removeRecord } = await import('../lib/manifest');
    removeRecord(slug);
    return;
  }

  try {
    await uninstallPlugin(plugin);
  } catch (err: any) {
    console.error(`Remove failed: ${err.message}`);
    process.exit(1);
  }
}
