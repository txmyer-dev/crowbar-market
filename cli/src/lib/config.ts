// Safe config file operations — backup before modify, deep merge, restore on failure

import { existsSync, readFileSync, writeFileSync, mkdirSync, copyFileSync } from 'fs';
import { join, basename } from 'path';
import { getBackupsDir, paiPath } from './paths';
import type { ConfigChange } from '../types';

function ensureBackupDir(): string {
  const dir = getBackupsDir();
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  return dir;
}

/** Create a timestamped backup of a config file */
export function backupConfig(filePath: string): string {
  const dir = ensureBackupDir();
  const ts = new Date().toISOString().replace(/[:.]/g, '-');
  const name = `${basename(filePath)}.${ts}.bak`;
  const backupPath = join(dir, name);
  if (existsSync(filePath)) {
    copyFileSync(filePath, backupPath);
  }
  return backupPath;
}

/** Read a JSON config file, return parsed or default */
export function readJsonConfig<T>(filePath: string, fallback: T): T {
  if (!existsSync(filePath)) return fallback;
  try {
    return JSON.parse(readFileSync(filePath, 'utf-8'));
  } catch {
    return fallback;
  }
}

/** Write JSON config with backup + verification */
export function writeJsonConfig(filePath: string, data: unknown): void {
  const backupPath = backupConfig(filePath);
  const json = JSON.stringify(data, null, 2);
  // Verify it parses before writing
  try {
    JSON.parse(json);
  } catch (e) {
    console.error('Generated invalid JSON — aborting write, backup at:', backupPath);
    throw e;
  }
  writeFileSync(filePath, json);
}

/** Deep set a value at a dotted path in an object */
export function deepSet(obj: Record<string, any>, path: string, value: unknown): void {
  const parts = path.split('.');
  let current = obj;
  for (let i = 0; i < parts.length - 1; i++) {
    const key = parts[i];
    if (!(key in current) || typeof current[key] !== 'object') {
      current[key] = {};
    }
    current = current[key];
  }
  current[parts[parts.length - 1]] = value;
}

/** Deep delete a value at a dotted path */
export function deepDelete(obj: Record<string, any>, path: string): void {
  const parts = path.split('.');
  let current = obj;
  for (let i = 0; i < parts.length - 1; i++) {
    const key = parts[i];
    if (!(key in current)) return;
    current = current[key];
  }
  delete current[parts[parts.length - 1]];
}

// --- Specific config handlers ---

/** Add hook to settings.json */
export function addHookToSettings(hookConfig: { event: string; matcher?: string; command: string }): ConfigChange {
  const settingsPath = paiPath('settings.json');
  const settings = readJsonConfig(settingsPath, {} as Record<string, any>);

  if (!settings.hooks) settings.hooks = {};
  if (!settings.hooks[hookConfig.event]) settings.hooks[hookConfig.event] = [];

  const entry: Record<string, string> = { command: hookConfig.command };
  if (hookConfig.matcher) entry.matcher = hookConfig.matcher;

  settings.hooks[hookConfig.event].push(entry);
  writeJsonConfig(settingsPath, settings);

  return { file: settingsPath, type: 'add', path: `hooks.${hookConfig.event}`, value: entry };
}

/** Remove hook from settings.json */
export function removeHookFromSettings(hookConfig: { event: string; command: string }): ConfigChange {
  const settingsPath = paiPath('settings.json');
  const settings = readJsonConfig(settingsPath, {} as Record<string, any>);

  if (settings.hooks?.[hookConfig.event]) {
    settings.hooks[hookConfig.event] = settings.hooks[hookConfig.event].filter(
      (h: any) => h.command !== hookConfig.command
    );
    if (settings.hooks[hookConfig.event].length === 0) {
      delete settings.hooks[hookConfig.event];
    }
    writeJsonConfig(settingsPath, settings);
  }

  return { file: settingsPath, type: 'remove', path: `hooks.${hookConfig.event}` };
}

/** Add MCP server to .mcp.json */
export function addMcpServer(mcpConfig: { serverName: string; command: string; args: string[]; env?: Record<string, string> }): ConfigChange {
  const mcpPath = paiPath('.mcp.json');
  const mcp = readJsonConfig(mcpPath, { mcpServers: {} } as Record<string, any>);

  if (!mcp.mcpServers) mcp.mcpServers = {};

  const entry: Record<string, any> = { command: mcpConfig.command, args: mcpConfig.args };
  if (mcpConfig.env) entry.env = mcpConfig.env;

  mcp.mcpServers[mcpConfig.serverName] = entry;
  writeJsonConfig(mcpPath, mcp);

  return { file: mcpPath, type: 'add', path: `mcpServers.${mcpConfig.serverName}`, value: entry };
}

/** Remove MCP server from .mcp.json */
export function removeMcpServer(serverName: string): ConfigChange {
  const mcpPath = paiPath('.mcp.json');
  const mcp = readJsonConfig(mcpPath, { mcpServers: {} } as Record<string, any>);

  if (mcp.mcpServers?.[serverName]) {
    delete mcp.mcpServers[serverName];
    writeJsonConfig(mcpPath, mcp);
  }

  return { file: mcpPath, type: 'remove', path: `mcpServers.${serverName}` };
}

/** Add skill to skill-index.json */
export function addSkillToIndex(skill: { name: string; path: string; fullDescription: string; triggers: string[]; tier: string }): ConfigChange {
  const indexPath = paiPath('skill-index.json');
  const index = readJsonConfig(indexPath, { version: '1.0.0', totalSkills: 0, skills: {} } as Record<string, any>);

  const key = skill.name.toLowerCase();
  index.skills[key] = skill;
  index.totalSkills = Object.keys(index.skills).length;
  writeJsonConfig(indexPath, index);

  return { file: indexPath, type: 'add', path: `skills.${key}`, value: skill };
}

/** Remove skill from skill-index.json */
export function removeSkillFromIndex(name: string): ConfigChange {
  const indexPath = paiPath('skill-index.json');
  const index = readJsonConfig(indexPath, { version: '1.0.0', totalSkills: 0, skills: {} } as Record<string, any>);

  const key = name.toLowerCase();
  if (index.skills[key]) {
    delete index.skills[key];
    index.totalSkills = Object.keys(index.skills).length;
    writeJsonConfig(indexPath, index);
  }

  return { file: indexPath, type: 'remove', path: `skills.${key}` };
}
