// cb pull-vps <skill-name|--all> [--host <user@host>] [--no-push] [--no-seed] [--dry-run]
// Pull skill(s) from VPS /root/.claude/skills/ to crowbar-market as source of truth

import { existsSync } from 'fs';
import { join } from 'path';

const PRIVATE_DIRS = new Set(['USER', '.git', '__pycache__', 'node_modules']);
const DEFAULT_HOST = 'root@76.13.98.215';

function getMarketPath(): string {
  const envPath = process.env.CROWBAR_MARKET_DIR;
  if (envPath && existsSync(envPath)) return envPath;

  const home = process.env.HOME || process.env.USERPROFILE || '';
  const candidates = [
    join(home, 'crowbar-market'),
    join(home, 'projects', 'crowbar-market'),
    join(home, 'Projects', 'crowbar-market'),
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

function gitExec(repoPath: string, args: string[]): { ok: boolean; out: string; err: string } {
  const result = Bun.spawnSync({ cmd: ['git', '-C', repoPath, ...args], stdout: 'pipe', stderr: 'pipe' });
  return {
    ok: result.exitCode === 0,
    out: result.stdout.toString().trim(),
    err: result.stderr.toString().trim(),
  };
}

function sshCheck(host: string): void {
  const result = Bun.spawnSync({
    cmd: ['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=5', host, 'echo ok'],
    stdout: 'pipe',
    stderr: 'pipe',
  });
  if (result.exitCode !== 0) {
    throw new Error(
      `Cannot connect to ${host}\n` +
      `Check SSH key auth and host reachability.\n` +
      `SSH error: ${result.stderr.toString().trim()}`
    );
  }
}

function listVpsSkills(host: string): string[] {
  const result = Bun.spawnSync({
    cmd: ['ssh', '-o', 'BatchMode=yes', host, 'ls /root/.claude/skills/'],
    stdout: 'pipe',
    stderr: 'pipe',
  });
  if (result.exitCode !== 0) {
    throw new Error(`Failed to list VPS skills: ${result.stderr.toString().trim()}`);
  }
  return result.stdout
    .toString()
    .trim()
    .split('\n')
    .map((s) => s.trim())
    .filter((s) => s && !PRIVATE_DIRS.has(s));
}

function checkVpsSkillExists(host: string, skillName: string): void {
  const result = Bun.spawnSync({
    cmd: ['ssh', '-o', 'BatchMode=yes', host, `test -d /root/.claude/skills/${skillName}`],
    stdout: 'pipe',
    stderr: 'pipe',
  });
  if (result.exitCode !== 0) {
    throw new Error(`"${skillName}" not found at ${host}:/root/.claude/skills/`);
  }
}

function pullSkill(host: string, skillName: string, destDir: string, dryRun: boolean): void {
  if (dryRun) {
    console.log(`  [dry-run] would pull ${skillName} from ${host}`);
    return;
  }

  // SSH produces tar bytes → pipe directly into tar extract
  const sshResult = Bun.spawnSync({
    cmd: ['ssh', '-o', 'BatchMode=yes', host, `tar czf - -C /root/.claude/skills ${skillName}`],
    stdout: 'pipe',
    stderr: 'pipe',
  });

  if (sshResult.exitCode !== 0) {
    throw new Error(
      `tar on VPS failed for ${skillName}: ${sshResult.stderr.toString().trim()}`
    );
  }

  const extractResult = Bun.spawnSync({
    cmd: ['tar', 'xzf', '-', '-C', destDir],
    stdin: sshResult.stdout as Uint8Array,
    stdout: 'pipe',
    stderr: 'pipe',
  });

  if (extractResult.exitCode !== 0) {
    throw new Error(
      `tar extract failed for ${skillName}: ${extractResult.stderr.toString().trim()}`
    );
  }
}

export async function pullVps(args: string[]): Promise<void> {
  const all = args.includes('--all');
  const noPush = args.includes('--no-push');
  const noSeed = args.includes('--no-seed');
  const dryRun = args.includes('--dry-run');

  const hostIdx = args.indexOf('--host');
  const host = hostIdx !== -1 && args[hostIdx + 1]
    ? args[hostIdx + 1]
    : (process.env.VPS_HOST || DEFAULT_HOST);

  const skillName = args.find((a) => !a.startsWith('-'));

  if (!all && !skillName) {
    console.error('Usage: cb pull-vps <skill-name> [--host <user@host>] [--no-push] [--no-seed] [--dry-run]\n' +
                  '       cb pull-vps --all [--host <user@host>] [--no-push] [--no-seed] [--dry-run]');
    process.exit(1);
  }

  const marketPath = getMarketPath();
  console.log(`Market path: ${marketPath}`);
  console.log(`VPS host:    ${host}`);

  if (dryRun) console.log('[dry-run mode — no files will be written]\n');

  // Verify SSH connectivity
  console.log('Checking SSH connectivity...');
  sshCheck(host);
  console.log('✓ SSH connection OK\n');

  // Build list of skills to fetch
  const skillsToFetch: string[] = [];

  if (all) {
    console.log('Listing skills on VPS...');
    const vpsSkills = listVpsSkills(host);
    skillsToFetch.push(...vpsSkills);
    console.log(`Found ${skillsToFetch.length} skills on VPS\n`);
  } else {
    checkVpsSkillExists(host, skillName!);
    skillsToFetch.push(skillName!);
  }

  const destDir = join(marketPath, 'plugins', 'skills');
  let pulled = 0;
  const errors: string[] = [];

  for (const name of skillsToFetch) {
    try {
      pullSkill(host, name, destDir, dryRun);
      pulled++;
      if (!all) {
        if (!dryRun) console.log(`✓ ${name} → plugins/skills/${name}`);
      } else {
        process.stdout.write('.');
      }
    } catch (err: any) {
      errors.push(`${name}: ${err.message}`);
      process.stdout.write('✗');
    }
  }

  if (all) process.stdout.write('\n');

  if (errors.length > 0) {
    console.error('\nErrors:');
    errors.forEach((e) => console.error(`  ✗ ${e}`));
  }

  if (pulled === 0 && !dryRun) {
    console.error('Nothing pulled.');
    process.exit(1);
  }

  if (!dryRun) {
    console.log(`\n✓ Pulled ${pulled} skill(s) from ${host}`);
  } else {
    console.log(`\n[dry-run] Would pull ${skillsToFetch.length} skill(s) from ${host}`);
    return;
  }

  // Re-seed registry
  if (!noSeed) {
    console.log('Seeding registry...');
    const seedResult = Bun.spawnSync({
      cmd: ['bun', 'scripts/seed-registry.ts'],
      cwd: marketPath,
      stdout: 'pipe',
      stderr: 'pipe',
    });
    if (seedResult.exitCode !== 0) {
      console.warn(`⚠ seed-registry failed (files are safe on disk):\n  ${seedResult.stderr.toString().trim()}`);
      console.warn(`  Run manually: cd ${marketPath} && bun run seed`);
    } else {
      console.log('✓ Registry reseeded');
    }
  }

  if (noPush) {
    console.log(`Skipped push (--no-push). Run: cd ${marketPath} && git push`);
    return;
  }

  // Check if there are changes to commit
  const status = gitExec(marketPath, ['status', '--porcelain']);
  if (!status.out) {
    console.log('Nothing to commit — all skills already up to date.');
    return;
  }

  const message = all
    ? `pull-vps: sync ${pulled} skills from ${host}`
    : `pull-vps: update ${skillsToFetch[0]} from ${host}`;

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
