# Setup Workflow

Install and authenticate notebooklm-py for first-time use.

Running the **Setup** workflow in the **NotebookLM** skill to authenticate...

## Step 1: Check Installation

```bash
notebooklm --version
```

If not installed:
```bash
pip install "notebooklm-py[browser]"
playwright install chromium
```

## Step 2: Authenticate

```bash
notebooklm login
```

This opens a browser window for Google OAuth. User logs in and authentication is stored locally.

## Step 3: Verify

```bash
notebooklm list
```

If this returns without error, setup is complete.

## Troubleshooting

- **Browser doesn't open:** Ensure `playwright install chromium` completed successfully
- **Auth fails:** Try `notebooklm login` again — sometimes the browser session expires
- **Rate limited:** Google throttles undocumented API usage. Wait and retry.
