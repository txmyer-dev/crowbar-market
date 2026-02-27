// Git operations for fetching plugin sources

import { existsSync, mkdirSync, rmSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';

/** Download a directory from a GitHub repo using git sparse checkout */
export async function fetchFromGithub(
  repo: string,
  path: string,
  ref: string,
  destDir: string
): Promise<void> {
  const tmpDir = join(tmpdir(), `crowbar-${Date.now()}`);

  try {
    mkdirSync(tmpDir, { recursive: true });

    // Clone with sparse checkout
    const cloneResult = Bun.spawnSync({
      cmd: ['git', 'clone', '--depth', '1', '--filter=blob:none', '--sparse', '--branch', ref, `https://github.com/${repo}.git`, tmpDir],
      stderr: 'pipe',
    });

    if (cloneResult.exitCode !== 0) {
      throw new Error(`Git clone failed: ${cloneResult.stderr.toString()}`);
    }

    // Set sparse checkout
    const sparseResult = Bun.spawnSync({
      cmd: ['git', '-C', tmpDir, 'sparse-checkout', 'set', path],
      stderr: 'pipe',
    });

    if (sparseResult.exitCode !== 0) {
      throw new Error(`Sparse checkout failed: ${sparseResult.stderr.toString()}`);
    }

    // Copy from tmp to destination
    const srcPath = join(tmpDir, path);
    if (!existsSync(srcPath)) {
      throw new Error(`Source path ${path} not found in repository ${repo}`);
    }

    mkdirSync(destDir, { recursive: true });
    copyDirRecursive(srcPath, destDir);
  } finally {
    // Cleanup tmp
    if (existsSync(tmpDir)) {
      rmSync(tmpDir, { recursive: true, force: true });
    }
  }
}

/** Download a single file from GitHub via raw URL */
export async function fetchFileFromGithub(
  repo: string,
  path: string,
  ref: string,
  destFile: string
): Promise<void> {
  const url = `https://raw.githubusercontent.com/${repo}/${ref}/${path}`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch ${url}: ${response.status}`);
  }
  const content = await response.text();
  const { dirname } = await import('path');
  mkdirSync(dirname(destFile), { recursive: true });
  const { writeFileSync } = await import('fs');
  writeFileSync(destFile, content);
}

/** Recursively copy directory contents */
function copyDirRecursive(src: string, dest: string): void {
  const { readdirSync, statSync, readFileSync, writeFileSync, mkdirSync } = require('fs');
  const { join } = require('path');

  mkdirSync(dest, { recursive: true });
  const entries = readdirSync(src);

  for (const entry of entries) {
    const srcPath = join(src, entry);
    const destPath = join(dest, entry);
    const stat = statSync(srcPath);

    if (stat.isDirectory()) {
      copyDirRecursive(srcPath, destPath);
    } else {
      writeFileSync(destPath, readFileSync(srcPath));
    }
  }
}
