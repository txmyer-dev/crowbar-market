// cb publish <skill-name|--all> [--no-push]
// Push local skill(s) from ~/.claude/skills/ back to crowbar-market as source of truth

import { existsSync, readdirSync, statSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { paiPath } from '../lib/paths';

const PRIVATE_DIRS = new Set(['USER', '.git', '__pycache__', 'node_modules']);

function getMarketPath(): string {
  const envPath = process.env.CROWBAR_MARKET_DIR;
  if (envPath && existsSync(envPath)) return envPath;

  // Try common locations
  const home = process.env.HOME || process.env.USERPROFILE || '';
  const candidates = [
    join(home, 'crowbar-market'),
    join(home, 'projects', 'crowbar-market'),
    join(home, 'dev', 'crowbar-market'),
    join(home, 'SNAP', 'crowbar-market'),
  ];

  for (const c of candidates) {
    if (existsSync(join(c, 'registry.json'))) return c;
  }

  throw new Error(
    'crowbar-market repo not found.\n' +
    'Set CROWBAR_MARKET_DIR or clone it:\n' +
    '  git clone https://github.com/txmyer-dev/crowbar-market ~/crowbar-market\n' +
    '  export CROWBAR_MARKET_DIR=~/crowbar-market'
  );
}

function copyDirSync(src: string, dest: string): number {
  let count = 0;
  mkdirSync(dest, { recursive: true });
  const entries = readdirSync(src);

  for (const entry of entries) {
    if (PRIVATE_DIRS.has(entry)) continue;
    const srcPath = join(src, entry);
    const destPath = join(dest, entry);
    const stat = statSync(srcPath);

    if (stat.isDirectory()) {
      count += copyDirSync(srcPath, destPath);
    } else {
      writeFileSync(destPath, readFileSync(srcPath));
      count++;
    }
  }
  return count;
}

function gitExec(repoPath: string, args: string[]): { ok: boolean; out: string; err: string } {
  const result = Bun.spawnSync({ cmd: ['git', '-C', repoPath, ...args], stdout: 'pipe', stderr: 'pipe' });
  return {
    ok: result.exitCode === 0,
    out: result.stdout.toString().trim(),
    err: result.stderr.toString().trim(),
  };
}

export async function publish(args: string[]): Promise<void> {
  const all = args.includes('--all');
  const noPush = args.includes('--no-push');
  const skillName = args.find((a) => !a.startsWith('-'));

  if (!all && !skillName) {
    console.error('Usage: cb publish <skill-name> [--no-push]\n       cb publish --all [--no-push]');
    process.exit(1);
  }

  const marketPath = getMarketPath();
  console.log(`Market path: ${marketPath}`);

  // Build list of skills to publish
  const skillsToPublish: string[] = [];

  if (all) {
    const skillsDir = paiPath('skills');
    for (const entry of readdirSync(skillsDir)) {
      const full = join(skillsDir, entry);
      if (statSync(full).isDirectory() && existsSync(join(full, 'SKILL.md'))) {
        skillsToPublish.push(entry);
      }
    }
    console.log(`Publishing ${skillsToPublish.length} skills...\n`);
  } else {
    skillsToPublish.push(skillName!);
  }

  let published = 0;
  let totalFiles = 0;
  const errors: string[] = [];

  for (const name of skillsToPublish) {
    const srcDir = paiPath('skills', name);
    const destDir = join(marketPath, 'plugins', 'skills', name);

    if (!existsSync(srcDir)) {
      errors.push(`"${name}" not found at ${srcDir}`);
      continue;
    }

    try {
      const files = copyDirSync(srcDir, destDir);
      totalFiles += files;
      published++;
      if (!all) {
        console.log(`✓ ${name} — ${files} file(s) → plugins/skills/${name}`);
      } else {
        process.stdout.write('.');
      }
    } catch (err: any) {
      errors.push(`${name}: ${err.message}`);
    }
  }

  if (all) process.stdout.write('\n');

  if (errors.length > 0) {
    console.error('\nErrors:');
    errors.forEach((e) => console.error(`  ✗ ${e}`));
  }

  if (published === 0) {
    console.error('Nothing published.');
    process.exit(1);
  }

  console.log(`\n✓ Published ${published} skill(s), ${totalFiles} total files`);

  if (noPush) {
    console.log(`Skipped push (--no-push). cd ${marketPath} && git push`);
    return;
  }

  // Check if there are changes
  const status = gitExec(marketPath, ['status', '--porcelain']);
  if (!status.out) {
    console.log('Nothing to commit — all skills already up to date.');
    return;
  }

  // Commit and push
  const message = all
    ? `publish: sync ${published} skills from SNAP`
    : `publish: update ${skillsToPublish[0]} skill`;

  const add = gitExec(marketPath, ['add', 'plugins/skills/']);
  if (!add.ok) {
    console.error(`git add failed: ${add.err}`);
    process.exit(1);
  }

  const commit = gitExec(marketPath, ['commit', '-m', message]);
  if (!commit.ok && !commit.out.includes('nothing to commit')) {
    console.error(`git commit failed: ${commit.err}`);
    process.exit(1);
  }

  const push = gitExec(marketPath, ['push']);
  if (!push.ok) {
    console.error(`git push failed: ${push.err}`);
    console.log(`Files committed locally. Push manually: cd ${marketPath} && git push`);
    process.exit(1);
  }

  console.log('✓ Pushed to crowbar-market');
}
