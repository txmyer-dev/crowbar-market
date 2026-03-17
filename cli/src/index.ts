#!/usr/bin/env bun
// Crowbar Market CLI — Plugin marketplace for SNAP

const VERSION = '1.1.0';
const HELP = `
\x1b[1mCrowbar Market\x1b[0m v${VERSION} — Plugin marketplace for SNAP

\x1b[1mUsage:\x1b[0m cb <command> [options]

\x1b[1mCommands:\x1b[0m
  install <slug> [--force]         Install a plugin from the registry
  install --profile <name>         Install a curated skill set
  publish <skill> [--no-push]      Push a local skill to crowbar-market
  publish --all [--no-push]        Sync all local skills to crowbar-market
  remove <slug>                    Uninstall a plugin
  list [--type <type>]             List installed plugins
  search <query> [--type]          Search the registry
  info <slug>                      Show plugin details
  outdated                         Check for newer versions
  update [slug]                    Update plugin(s)
  sync                             Pull latest registry from remote
  build-site [outdir]              Generate static catalog site

\x1b[1mProfiles:\x1b[0m
  vps-headless       Minimal set for headless VPS deployments
  paperclip-builder  Skills for the Paperclip Builder agent

\x1b[1mPlugin types:\x1b[0m skill, hook, agent, fabric-pattern, mcp-server, claude-plugin

\x1b[1mEnv vars:\x1b[0m
  CROWBAR_MARKET_DIR   Path to local crowbar-market clone (required for publish)
  PAI_DIR              SNAP installation dir (default: ~/.claude)
`;

const [command, ...args] = process.argv.slice(2);

if (!command || command === '--help' || command === '-h') {
  console.log(HELP);
  process.exit(0);
}

if (command === '--version' || command === '-v') {
  console.log(VERSION);
  process.exit(0);
}

const commands: Record<string, () => Promise<void>> = {
  install: () => import('./commands/install').then((m) => m.install(args)),
  publish: () => import('./commands/publish').then((m) => m.publish(args)),
  remove: () => import('./commands/remove').then((m) => m.remove(args)),
  list: () => import('./commands/list').then((m) => m.list(args)),
  search: () => import('./commands/search').then((m) => m.search(args)),
  info: () => import('./commands/info').then((m) => m.info(args)),
  outdated: () => import('./commands/outdated').then((m) => m.outdated(args)),
  update: () => import('./commands/update').then((m) => m.update(args)),
  sync: () => import('./commands/sync').then((m) => m.sync(args)),
  'build-site': () => import('./commands/build-site').then((m) => m.buildSite(args)),
};

const handler = commands[command];
if (!handler) {
  console.error(`Unknown command: ${command}\nRun 'cb --help' for usage.`);
  process.exit(1);
}

handler().catch((err) => {
  console.error(err.message || err);
  process.exit(1);
});
