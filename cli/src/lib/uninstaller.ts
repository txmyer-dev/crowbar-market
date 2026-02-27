// Plugin uninstaller — reverse of installer, using manifest

import { existsSync, rmSync, statSync } from 'fs';
import { removeRecord, getInstalled } from './manifest';
import { removeHookFromSettings, removeMcpServer, removeSkillFromIndex } from './config';
import type { Plugin } from '../types';

/** Uninstall a plugin — remove files and clean config entries */
export async function uninstallPlugin(plugin: Plugin): Promise<void> {
  const record = getInstalled(plugin.slug);
  if (!record) {
    console.error(`Plugin ${plugin.slug} is not installed.`);
    process.exit(1);
  }

  // Remove files
  for (const filePath of record.files) {
    if (existsSync(filePath)) {
      const stat = statSync(filePath);
      if (stat.isDirectory()) {
        rmSync(filePath, { recursive: true, force: true });
      } else {
        rmSync(filePath);
      }
      console.log(`  Removed: ${filePath}`);
    }
  }

  // Reverse config changes
  for (const change of record.configChanges) {
    if (change.type === 'add') {
      // Reverse an add by removing
      if (change.path.startsWith('hooks.')) {
        const event = change.path.replace('hooks.', '');
        if (change.value && typeof change.value === 'object' && 'command' in (change.value as any)) {
          removeHookFromSettings({ event, command: (change.value as any).command });
        }
      } else if (change.path.startsWith('mcpServers.')) {
        const serverName = change.path.replace('mcpServers.', '');
        removeMcpServer(serverName);
      } else if (change.path.startsWith('skills.')) {
        removeSkillFromIndex(plugin.name);
      }
    }
  }

  // Remove from manifest
  removeRecord(plugin.slug);
  console.log(`Uninstalled ${plugin.name} (${plugin.type})`);
}
