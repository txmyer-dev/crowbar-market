// Plugin installer — dispatches to type-specific handlers

import { existsSync, mkdirSync } from 'fs';
import { join, basename } from 'path';
import { paiPath } from './paths';
import { recordInstall } from './manifest';
import { addHookToSettings, addMcpServer, addSkillToIndex, backupConfig } from './config';
import { fetchFromGithub, fetchFileFromGithub } from './git';
import type { Plugin, InstalledPlugin, ConfigChange } from '../types';

interface InstallOptions {
  force?: boolean;
}

/** Install a plugin by dispatching to the correct type handler */
export async function installPlugin(plugin: Plugin, opts: InstallOptions = {}): Promise<void> {
  const handler = handlers[plugin.type];
  if (!handler) {
    console.error(`Unknown plugin type: ${plugin.type}`);
    process.exit(1);
  }

  const result = await handler(plugin, opts);

  recordInstall({
    slug: plugin.slug,
    version: plugin.version,
    installedAt: new Date().toISOString(),
    files: result.files,
    configChanges: result.configChanges,
  });

  console.log(`Installed ${plugin.name} (${plugin.type}) v${plugin.version}`);
}

interface InstallResult {
  files: string[];
  configChanges: ConfigChange[];
}

const handlers: Record<string, (plugin: Plugin, opts: InstallOptions) => Promise<InstallResult>> = {
  'skill': installSkill,
  'hook': installHook,
  'agent': installAgent,
  'fabric-pattern': installFabricPattern,
  'mcp-server': installMcpServer,
  'claude-plugin': installClaudePlugin,
};

async function installSkill(plugin: Plugin, opts: InstallOptions): Promise<InstallResult> {
  const target = paiPath('skills', plugin.name);
  if (existsSync(target) && !opts.force) {
    throw new Error(`Skill ${plugin.name} already exists at ${target}. Use --force to overwrite.`);
  }

  const files: string[] = [];
  const configChanges: ConfigChange[] = [];

  if (plugin.source.type === 'github' && plugin.source.repo && plugin.source.path) {
    await fetchFromGithub(plugin.source.repo, plugin.source.path, plugin.source.ref || 'main', target);
    files.push(target);
  }

  // Register in skill-index.json
  if (plugin.triggers && plugin.tier) {
    const change = addSkillToIndex({
      name: plugin.name,
      path: `${plugin.name}/SKILL.md`,
      fullDescription: plugin.description,
      triggers: plugin.triggers,
      tier: plugin.tier,
    });
    configChanges.push(change);
  }

  return { files, configChanges };
}

async function installHook(plugin: Plugin, opts: InstallOptions): Promise<InstallResult> {
  const hookFile = `${plugin.name}.hook.ts`;
  const target = paiPath('hooks', hookFile);
  if (existsSync(target) && !opts.force) {
    throw new Error(`Hook ${hookFile} already exists. Use --force to overwrite.`);
  }

  const files: string[] = [];
  const configChanges: ConfigChange[] = [];

  if (plugin.source.type === 'github' && plugin.source.repo && plugin.source.path) {
    await fetchFileFromGithub(plugin.source.repo, plugin.source.path, plugin.source.ref || 'main', target);
    files.push(target);
  }

  // Register in settings.json hooks
  if (plugin.hookConfig) {
    const change = addHookToSettings(plugin.hookConfig);
    configChanges.push(change);
  }

  return { files, configChanges };
}

async function installAgent(plugin: Plugin, opts: InstallOptions): Promise<InstallResult> {
  const target = paiPath('agents', `${plugin.name}.md`);
  if (existsSync(target) && !opts.force) {
    throw new Error(`Agent ${plugin.name}.md already exists. Use --force to overwrite.`);
  }

  if (plugin.source.type === 'github' && plugin.source.repo && plugin.source.path) {
    await fetchFileFromGithub(plugin.source.repo, plugin.source.path, plugin.source.ref || 'main', target);
  }

  return { files: [target], configChanges: [] };
}

async function installFabricPattern(plugin: Plugin, opts: InstallOptions): Promise<InstallResult> {
  const patternName = plugin.slug.split('/').pop() || plugin.name;
  const target = paiPath('skills', 'Fabric', 'Patterns', patternName);
  if (existsSync(target) && !opts.force) {
    throw new Error(`Pattern ${patternName} already exists. Use --force to overwrite.`);
  }

  if (plugin.source.type === 'github' && plugin.source.repo && plugin.source.path) {
    await fetchFromGithub(plugin.source.repo, plugin.source.path, plugin.source.ref || 'main', target);
  }

  return { files: [target], configChanges: [] };
}

async function installMcpServer(plugin: Plugin, opts: InstallOptions): Promise<InstallResult> {
  if (!plugin.mcpConfig) {
    throw new Error(`MCP server ${plugin.name} missing mcpConfig`);
  }

  const change = addMcpServer(plugin.mcpConfig);
  return { files: [], configChanges: [change] };
}

async function installClaudePlugin(plugin: Plugin, _opts: InstallOptions): Promise<InstallResult> {
  // Pass-through to claude plugins install
  console.log(`Installing Claude plugin via: claude plugins install ${plugin.name}`);
  const result = Bun.spawnSync({
    cmd: ['claude', 'plugins', 'install', plugin.name],
    stdout: 'inherit',
    stderr: 'inherit',
  });

  if (result.exitCode !== 0) {
    throw new Error(`Claude plugin install failed for ${plugin.name}`);
  }

  return { files: [], configChanges: [] };
}
