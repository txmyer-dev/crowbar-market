# ReAuthGWS — Re-authenticate gws CLI on EC2

## When to Use

`gws` returns `401`, `invalid_grant`, or `Token has been expired or revoked`.

## Steps

### 1. Start VNC Server on EC2

```bash
ssh -i ~/Downloads/ossh_lenovo.pem ubuntu@13.59.113.143 'bash -s' << 'REMOTE'
# Check if already running
if pgrep -f "x11vnc.*5900" > /dev/null; then
  echo "VNC already running"
else
  Xvfb :1 -screen 0 1280x720x24 &>/dev/null &
  sleep 1
  x11vnc -display :1 -nopw -listen 0.0.0.0 -rfbport 5900 -forever -shared &>/dev/null &
  sleep 2
  echo "VNC started on :1, port 5900"
fi
ps aux | grep -E "Xvfb|x11vnc" | grep -v grep
REMOTE
```

### 2. Open SSH Tunnel

```bash
ssh -i ~/Downloads/ossh_lenovo.pem -L 5900:localhost:5900 -N -f ubuntu@13.59.113.143
```

### 3. Tell User to Connect VNC

Tell the user: **"Connect your VNC client to `localhost:5900` (no password). Let me know when you're connected."**

Wait for user confirmation before proceeding.

### 4. Run gws auth login (Capture URL)

```bash
cat << 'EOF' | ssh -i ~/Downloads/ossh_lenovo.pem ubuntu@13.59.113.143 "cat > /tmp/gws-reauth.sh && chmod +x /tmp/gws-reauth.sh && bash /tmp/gws-reauth.sh"
#!/bin/bash
pkill -f "gws auth" 2>/dev/null
sleep 1
export PATH=$PATH:/home/ubuntu/.local/bin
nohup gws auth login --no-browser > /tmp/gws-auth-output.txt 2>&1 &
sleep 5
cat /tmp/gws-auth-output.txt
EOF
```

This outputs the OAuth URL. The `gws auth` process stays running in background waiting for the callback.

### 5. Launch Firefox with Auth URL on VNC Display

Extract the URL from step 4 output and launch Firefox:

```bash
cat << EOF | ssh -i ~/Downloads/ossh_lenovo.pem ubuntu@13.59.113.143 "bash"
export DISPLAY=:1
firefox "<THE_AUTH_URL>" &
disown
echo "Firefox launched"
EOF
```

**IMPORTANT**: The URL contains special characters. Pass it inside double quotes.

### 6. User Completes OAuth

Tell the user: **"Firefox is open in your VNC client with the Google sign-in page. Complete the OAuth flow there."**

Wait for user confirmation.

### 7. Verify Auth Works

```bash
cat << 'EOF' | ssh -i ~/Downloads/ossh_lenovo.pem ubuntu@13.59.113.143 "bash"
export PATH=$PATH:/home/ubuntu/.local/bin
gws drive files list --params '{"pageSize": 3}' --format table 2>&1
EOF
```

If this returns files, auth is successful.

### 8. Cleanup (Optional)

Kill the VNC server if no longer needed:

```bash
ssh -i ~/Downloads/ossh_lenovo.pem ubuntu@13.59.113.143 'pkill x11vnc; pkill -f "Xvfb :1"'
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Firefox doesn't open in VNC | Ensure `DISPLAY=:1` is set |
| "xterm command not found" | `sudo apt-get install -y xterm` |
| No browser installed | `sudo apt-get install -y firefox` |
| SSH tunnel port conflict | Kill old tunnels: `pkill -f "5900.*13.59"` |
| gws auth URL not captured | Check `/tmp/gws-auth-output.txt` on EC2 |
| Ctrl+C/right-click don't work in xterm | Don't use xterm for auth. Capture URL via script (step 4), launch Firefox directly (step 5) |
