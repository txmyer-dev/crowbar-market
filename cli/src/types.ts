// Crowbar Market — Plugin type definitions

export type PluginType = 'skill' | 'hook' | 'agent' | 'fabric-pattern' | 'mcp-server' | 'claude-plugin';

export interface PluginAuthor {
  name: string;
  github: string;
}

export interface PluginSource {
  type: 'github' | 'local';
  repo?: string;
  path?: string;
  ref?: string;
  localPath?: string;
}

export interface HookConfig {
  event: string;
  matcher?: string;
  command: string;
}

export interface McpConfig {
  serverName: string;
  command: string;
  args: string[];
  env?: Record<string, string>;
}

export interface Plugin {
  name: string;
  slug: string;
  type: PluginType;
  version: string;
  description: string;
  author: PluginAuthor;
  source: PluginSource;
  tags: string[];
  installTarget: string | null;
  configTarget: string | null;
  // Type-specific
  hookConfig?: HookConfig;
  mcpConfig?: McpConfig;
  tier?: string;
  triggers?: string[];
}

export interface Registry {
  version: string;
  plugins: Record<string, Plugin>;
}

export interface InstalledPlugin {
  slug: string;
  version: string;
  installedAt: string;
  files: string[];
  configChanges: ConfigChange[];
}

export interface ConfigChange {
  file: string;
  type: 'add' | 'remove';
  path: string;
  value?: unknown;
}

export interface InstalledManifest {
  version: string;
  plugins: Record<string, InstalledPlugin>;
}
