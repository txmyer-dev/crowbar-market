// cb install <slug> [--force]
// cb install --profile <name> [--force]

import { getPlugin } from '../lib/registry';
import { isInstalled } from '../lib/manifest';
import { installPlugin } from '../lib/installer';
import { loadProfile } from '../lib/profiles';

export async function install(args: string[]): Promise<void> {
  const force = args.includes('--force');
  const profileIdx = args.indexOf('--profile');

  // Profile install mode
  if (profileIdx !== -1) {
    const profileName = args[profileIdx + 1];
    if (!profileName || profileName.startsWith('-')) {
      console.error('Usage: cb install --profile <name>');
      process.exit(1);
    }

    let profile;
    try {
      profile = loadProfile(profileName);
    } catch (err: any) {
      console.error(err.message);
      process.exit(1);
    }

    console.log(`Installing profile: ${profile.name}`);
    console.log(`  ${profile.description}`);
    console.log(`  ${profile.skills.length} skills\n`);

    let installed = 0;
    let skipped = 0;
    const errors: string[] = [];

    for (const slug of profile.skills) {
      const plugin = getPlugin(slug);
      if (!plugin) {
        errors.push(`${slug}: not found in registry (run 'cb sync' to update)`);
        continue;
      }

      if (isInstalled(slug) && !force) {
        skipped++;
        continue;
      }

      try {
        await installPlugin(plugin, { force });
        installed++;
      } catch (err: any) {
        errors.push(`${slug}: ${err.message}`);
      }
    }

    console.log(`\nProfile "${profile.name}" complete:`);
    console.log(`  ✓ ${installed} installed, ${skipped} already present`);
    if (errors.length > 0) {
      console.error(`  ✗ ${errors.length} failed:`);
      errors.forEach((e) => console.error(`    ${e}`));
    }
    return;
  }

  // Single plugin mode
  const slug = args.find((a) => !a.startsWith('-'));

  if (!slug) {
    console.error('Usage: cb install <slug> [--force]\n       cb install --profile <name> [--force]');
    process.exit(1);
  }

  const plugin = getPlugin(slug);
  if (!plugin) {
    console.error(`Plugin "${slug}" not found in registry. Run 'cb sync' to update.`);
    process.exit(1);
  }

  if (isInstalled(slug) && !force) {
    console.error(`Plugin "${slug}" already installed. Use --force to reinstall.`);
    process.exit(1);
  }

  try {
    await installPlugin(plugin, { force });
  } catch (err: any) {
    console.error(`Install failed: ${err.message}`);
    process.exit(1);
  }
}
