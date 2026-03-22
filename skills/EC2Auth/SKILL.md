---
name: EC2Auth
description: Re-authenticate CLI tools on EC2 via VNC. USE WHEN gws auth expired, notebooklm auth expired, EC2 auth, re-auth, VNC auth, token expired, token revoked, headless auth.
---

# EC2Auth

Re-authenticate browser-based CLI tools (gws, notebooklm) on the headless EC2 instance using VNC.

## Prerequisites

- **EC2**: `ubuntu@13.59.113.143` via `~/Downloads/ossh_lenovo.pem`
- **Installed on EC2**: `x11vnc`, `Xvfb`, `xterm`, `firefox`
- **VNC client on local machine** (RealVNC, TightVNC, etc.)

## Workflow Routing

| Trigger | Workflow |
|---------|----------|
| "gws auth expired", "re-auth gws" | `Workflows/ReAuthGWS.md` |
| "notebooklm auth expired" | `Workflows/ReAuthNotebookLM.md` |

## Quick Reference

**The pattern is always the same:**
1. Start Xvfb + x11vnc on EC2
2. SSH tunnel port 5900 to localhost
3. User connects VNC client
4. Run auth command with `--no-browser`, capture URL
5. Launch Firefox on VNC display with that URL
6. User completes OAuth in VNC browser
7. Verify auth works
