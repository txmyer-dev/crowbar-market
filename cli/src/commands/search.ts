// cb search <query> [--type <type>]

import { searchPlugins } from '../lib/registry';
import { displayPluginCard } from '../lib/display';

export async function search(args: string[]): Promise<void> {
  const typeIdx = args.indexOf('--type');
  const typeFilter = typeIdx !== -1 ? args[typeIdx + 1] : undefined;
  const query = args.filter((a, i) => !a.startsWith('-') && (typeIdx === -1 || i !== typeIdx + 1)).join(' ');

  if (!query) {
    console.error('Usage: cb search <query> [--type <type>]');
    process.exit(1);
  }

  const results = searchPlugins(query, typeFilter);

  if (results.length === 0) {
    console.log(`No plugins found matching "${query}".`);
    return;
  }

  console.log(`Found ${results.length} plugin(s):\n`);
  for (const plugin of results) {
    displayPluginCard(plugin);
  }
}
