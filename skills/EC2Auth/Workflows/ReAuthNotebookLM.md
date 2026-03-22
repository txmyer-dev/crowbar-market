# ReAuthNotebookLM — Re-authenticate notebooklm-py on EC2

## When to Use

`notebooklm` returns auth errors, expired cookies, or CSRF token failures.

## How NotebookLM Auth Works

notebooklm-py uses **Playwright browser session cookies** (not API keys or service accounts). Auth is stored at `~/.notebooklm/storage_state.json`. The `notebooklm login` command opens Chromium via Playwright to capture Google session cookies.

## Steps

### 1. Start VNC Server on EC2

```bash
ssh -i ~/Downloads/ossh_lenovo.pem ubuntu@13.59.113.143 'bash -s' << 'REMOTE'
if pgrep -f "x11vnc.*5900" > /dev/null; then
  echo "VNC already running"
else
  Xvfb :1 -screen 0 1280x720x24 &>/dev/null &
  sleep 1
  x11vnc -display :1 -nopw -listen 0.0.0.0 -rfbport 5900 -forever -shared &>/dev/null &
  sleep 2
  echo "VNC started on :1, port 5900"
fi
REMOTE
```

### 2. Open SSH Tunnel

```bash
ssh -i ~/Downloads/ossh_lenovo.pem -L 5900:localhost:5900 -N -f ubuntu@13.59.113.143
```

### 3. Tell User to Connect VNC

Tell the user: **"Connect your VNC client to `localhost:5900` (no password). Let me know when you're connected."**

### 4. Run notebooklm login on VNC Display

```bash
cat << 'EOF' | ssh -i ~/Downloads/ossh_lenovo.pem ubuntu@13.59.113.143 "bash"
export DISPLAY=:1
export PATH=$PATH:/home/ubuntu/.local/bin
notebooklm login &
disown
echo "Login launched on VNC display"
EOF
```

Unlike gws, `notebooklm login` uses Playwright which opens its OWN Chromium browser on the display. No need to capture a URL and launch Firefox separately.

### 5. User Completes OAuth

Tell the user: **"A Chromium window should appear in your VNC client. Sign into Google there."**

### 6. Verify Auth Works

```bash
cat << 'EOF' | ssh -i ~/Downloads/ossh_lenovo.pem ubuntu@13.59.113.143 "bash"
export PATH=$PATH:/home/ubuntu/.local/bin
notebooklm list 2>&1 | head -15
EOF
```

If notebooks are listed, auth is successful.

## Key Differences from gws

| Aspect | gws | notebooklm |
|--------|-----|------------|
| Auth method | OAuth2 redirect flow | Playwright browser cookies |
| Browser needed | External (Firefox) | Built-in (Playwright Chromium) |
| URL capture | Yes, `--no-browser` flag | No, Playwright opens its own browser |
| Storage | `~/.config/gws/credentials.enc` | `~/.notebooklm/storage_state.json` |
| Env var override | `GOOGLE_WORKSPACE_CLI_TOKEN` | `NOTEBOOKLM_AUTH_JSON` |

## Alternative: Copy Local Auth

If VNC is unavailable, copy auth from local machine:

```bash
scp -i ~/Downloads/ossh_lenovo.pem ~/.notebooklm/storage_state.json ubuntu@13.59.113.143:~/.notebooklm/storage_state.json
```

This works because the storage_state.json contains Google session cookies that aren't machine-specific. However, cookies expire — this is a temporary fix.
