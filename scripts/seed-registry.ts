#!/usr/bin/env bun
/**
 * Seed registry.json from live PAI installation
 * Reads: skill-index.json, hooks/, agents/, Fabric/Patterns/, .mcp.json
 * Writes: registry.json (READ-ONLY scan — never modifies PAI files)
 */

import { readFileSync, readdirSync, existsSync, statSync } from 'fs';
import { join, basename } from 'path';
import { homedir } from 'os';

const PAI_DIR = process.env.PAI_DIR || join(homedir(), '.claude');
const REPO = 'txmyer-dev/Ekko';
const AUTHOR = { name: 'Tony', github: 'txmyer-dev' };

interface Plugin {
  name: string;
  slug: string;
  type: string;
  version: string;
  description: string;
  author: typeof AUTHOR;
  source: { type: string; repo: string; path: string; ref: string };
  tags: string[];
  installTarget: string | null;
  configTarget: string | null;
  [key: string]: unknown;
}

const plugins: Record<string, Plugin> = {};

// --- 1. Skills from skill-index.json ---
console.log('Scanning skills...');
const skillIndexPath = join(PAI_DIR, 'skill-index.json');
if (existsSync(skillIndexPath)) {
  const skillIndex = JSON.parse(readFileSync(skillIndexPath, 'utf-8'));
  for (const [key, skill] of Object.entries(skillIndex.skills) as [string, any][]) {
    const slug = `crowbar/${key}`;
    plugins[slug] = {
      name: skill.name,
      slug,
      type: 'skill',
      version: '1.0.0',
      description: skill.fullDescription || `${skill.name} skill`,
      author: AUTHOR,
      source: { type: 'github', repo: REPO, path: `skills/${skill.name}`, ref: 'main' },
      tags: skill.triggers?.slice(0, 3) || [],
      installTarget: `~/.claude/skills/${skill.name}/`,
      configTarget: 'skill-index.json',
      tier: skill.tier,
      triggers: skill.triggers,
    };
  }
  console.log(`  Found ${Object.keys(skillIndex.skills).length} skills`);
}

// --- 2. Hooks ---
console.log('Scanning hooks...');
const hooksDir = join(PAI_DIR, 'hooks');
if (existsSync(hooksDir)) {
  const hookFiles = readdirSync(hooksDir).filter((f) => f.endsWith('.hook.ts'));
  for (const file of hookFiles) {
    const name = file.replace('.hook.ts', '');
    const slug = `crowbar/hook-${name.toLowerCase()}`;
    plugins[slug] = {
      name,
      slug,
      type: 'hook',
      version: '1.0.0',
      description: `${name} event hook`,
      author: AUTHOR,
      source: { type: 'github', repo: REPO, path: `hooks/${file}`, ref: 'main' },
      tags: ['hook', 'event'],
      installTarget: `~/.claude/hooks/${file}`,
      configTarget: 'settings.json',
    };
  }
  console.log(`  Found ${hookFiles.length} hooks`);
}

// --- 3. Agents ---
console.log('Scanning agents...');
const agentsDir = join(PAI_DIR, 'agents');
if (existsSync(agentsDir)) {
  const agentFiles = readdirSync(agentsDir).filter((f) => f.endsWith('.md') && f !== 'CLAUDE.md');
  for (const file of agentFiles) {
    const name = file.replace('.md', '');
    const slug = `crowbar/${name.toLowerCase()}`;
    plugins[slug] = {
      name,
      slug,
      type: 'agent',
      version: '1.0.0',
      description: `${name} agent definition`,
      author: AUTHOR,
      source: { type: 'github', repo: REPO, path: `agents/${file}`, ref: 'main' },
      tags: ['agent', name.toLowerCase()],
      installTarget: `~/.claude/agents/${file}`,
      configTarget: null,
    };
  }
  console.log(`  Found ${agentFiles.length} agents`);
}

// --- 4. Fabric Patterns ---
console.log('Scanning fabric patterns...');
const patternsDir = join(PAI_DIR, 'skills', 'Fabric', 'Patterns');
if (existsSync(patternsDir)) {
  const patternDirs = readdirSync(patternsDir).filter((f) => {
    const full = join(patternsDir, f);
    return existsSync(full) && statSync(full).isDirectory();
  });

  for (const dir of patternDirs) {
    const slug = `crowbar/pattern-${dir}`;
    // Try to read system.md for a description
    let description = `Fabric pattern: ${dir.replace(/_/g, ' ')}`;
    const systemMd = join(patternsDir, dir, 'system.md');
    if (existsSync(systemMd)) {
      const content = readFileSync(systemMd, 'utf-8');
      const firstLine = content.split('\n').find((l) => l.trim() && !l.startsWith('#'));
      if (firstLine) {
        description = firstLine.trim().slice(0, 120);
      }
    }

    // Generate tags from pattern name
    const nameParts = dir.split('_').filter((p) => p.length > 2);
    const tags = ['fabric', 'pattern', ...nameParts.slice(0, 2)];

    plugins[slug] = {
      name: dir,
      slug,
      type: 'fabric-pattern',
      version: '1.0.0',
      description,
      author: { name: 'Daniel Miessler', github: 'danielmiessler' },
      source: { type: 'github', repo: 'danielmiessler/fabric', path: `patterns/${dir}`, ref: 'main' },
      tags: [...new Set(tags)],
      installTarget: `~/.claude/skills/Fabric/Patterns/${dir}/`,
      configTarget: null,
    };
  }
  console.log(`  Found ${patternDirs.length} fabric patterns`);
}

// --- 5. MCP Servers ---
console.log('Scanning MCP servers...');
const mcpPath = join(PAI_DIR, '.mcp.json');
if (existsSync(mcpPath)) {
  const mcp = JSON.parse(readFileSync(mcpPath, 'utf-8'));
  for (const [name, config] of Object.entries(mcp.mcpServers || {}) as [string, any][]) {
    const slug = `crowbar/mcp-${name}`;
    plugins[slug] = {
      name,
      slug,
      type: 'mcp-server',
      version: '1.0.0',
      description: `MCP server: ${name}`,
      author: AUTHOR,
      source: { type: 'local', repo: '', path: '', ref: '' },
      tags: ['mcp', name],
      installTarget: null,
      configTarget: '.mcp.json',
      mcpConfig: {
        serverName: name,
        command: config.command,
        args: config.args || [],
        ...(config.env ? { env: config.env } : {}),
      },
    };
  }
  console.log(`  Found ${Object.keys(mcp.mcpServers || {}).length} MCP servers`);
}

// --- Write registry ---
const registry = {
  version: '1.0.0',
  plugins,
};

const outPath = join(process.cwd(), 'registry.json');
const { writeFileSync } = require('fs');
writeFileSync(outPath, JSON.stringify(registry, null, 2));

const counts: Record<string, number> = {};
for (const p of Object.values(plugins)) {
  counts[p.type] = (counts[p.type] || 0) + 1;
}

console.log(`\nRegistry written to ${outPath}`);
console.log(`Total: ${Object.keys(plugins).length} plugins`);
for (const [type, count] of Object.entries(counts).sort()) {
  console.log(`  ${type}: ${count}`);
}
