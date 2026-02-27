#!/usr/bin/env bun
// Crowbar Market CLI — Plugin marketplace for PAI

const VERSION = '1.0.0';
const HELP = `
\x1b[1mCrowbar Market\x1b[0m v${VERSION} — Plugin marketplace for PAI

\x1b[1mUsage:\x1b[0m cb <command> [options]

\x1b[1mCommands:\x1b[0m
  install <slug> [--force]   Install a plugin from the registry
  remove <slug>              Uninstall a plugin
  list [--type <type>]       List installed plugins
  search <query> [--type]    Search the registry
  info <slug>                Show plugin details
  outdated                   Check for newer versions
  update [slug]              Update plugin(s)
  sync                       Pull latest registry from remote
  build-site [outdir]        Generate static catalog site

\x1b[1mPlugin types:\x1b[0m skill, hook, agent, fabric-pattern, mcp-server, claude-plugin
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
