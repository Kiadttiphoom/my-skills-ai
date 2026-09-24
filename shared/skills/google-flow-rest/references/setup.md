# Setup and installation

## Install the skill

Copy the entire `google-flow-rest` folder into the receiving user's Codex skills directory:

```bash
mkdir -p "$HOME/.codex/skills"
cp -R google-flow-rest "$HOME/.codex/skills/google-flow-rest"
```

Restart Codex after installation. Invoke the skill as `$google-flow-rest`.

For Claude Code personal installation, copy the same folder to:

```bash
mkdir -p "$HOME/.claude/skills"
cp -R google-flow-rest "$HOME/.claude/skills/google-flow-rest"
```

For project-only use, install it at `.claude/skills/google-flow-rest`. Claude Code can invoke it automatically or directly as `/google-flow-rest`. If the top-level skills directory was created during an active session, restart Claude Code once.

## Connect useapi.net and Google Flow

1. Subscribe to useapi.net and obtain an API token.
2. Use a dedicated Google account rather than a personal primary account.
3. Connect the Google Flow account using <https://useapi.net/docs/start-here/setup-google-flow>.
4. In the project directory, copy `assets/.env.example` to `.env` and fill it locally.
5. Run `chmod 600 .env` and ensure `.env` is ignored by version control.
6. Verify the connection with `accounts` before generation.

Never place a real token or Google session cookie inside the skill folder, a Git repository, a shared archive, or chat.

## CSV batch format

Start from `assets/batch.example.csv`. Required columns are `id`, `status`, and `prompt`. Only `Ready` rows are submitted. Multiple reference images use absolute paths separated by semicolons in `reference_images`.

Preview first:

```bash
python3 /path/to/google-flow-rest/scripts/google_flow_rest.py batch reviewed.csv
```

After explicit approval:

```bash
python3 /path/to/google-flow-rest/scripts/google_flow_rest.py batch reviewed.csv --confirm-spend
```

The script writes each accepted job ID back to the CSV immediately, preventing duplicate submission on rerun.

## Provider boundary

useapi.net is a third-party wrapper around a connected Google Flow session. It is separate from Gemini API and Vertex AI billing. Provider endpoints, model support, prices, and session behavior can change; consult <https://useapi.net/docs/api-google-flow-v1> when a newly supported setting is rejected locally.
