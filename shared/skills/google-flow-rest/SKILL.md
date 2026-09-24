---
name: google-flow-rest
description: Connect and operate Google Flow through the third-party useapi.net REST API, including account checks, dry-run previews, reference uploads, single or CSV batch video submission, job polling, downloads, and media verification. Compatible with Codex and Claude Code Agent Skills. Use when a user asks for Google Flow REST, useapi.net Flow automation, or reusable Flow batch generation. Do not use for the official Gemini or Vertex AI Veo APIs.
---

# Google Flow REST

Use `scripts/google_flow_rest.py` for deterministic operations. This integration uses useapi.net and a connected Google Flow browser session; it is not an official Google API. Flow credits come from the connected Google Flow account, not Codex, Gemini API, Vertex AI, or Fuzion credits.

## Route the request

- For first-time setup or non-technical users, read
  `คู่มือแบบง่ายไม่ใช้โค้ด.md`. Operate the bundled script on the user's
  behalf and do not show terminal commands unless they ask.
- Use `คู่มือการติดตั้งและใช้งาน.md` or `references/setup.md` only when
  the user wants manual CLI instructions or troubleshooting details.
- For account health, run `accounts`.
- For one clip, preview `submit` without `--confirm-spend`, show the resolved settings, then obtain explicit approval and rerun with `--confirm-spend`.
- For multiple clips, use a reviewed CSV and `batch`. Preview first. Submit only rows whose `status` is exactly `Ready`.
- For a submitted job, use `status` or `wait --download` with the exact returned job ID.

## Safety invariants

- Never ask the user to paste API tokens, Google cookies, passwords, or recovery codes into chat.
- Never print `.env`, authorization headers, cookies, or signed upload/download URLs.
- Treat uploads and generation as external writes. Dry-run before submission and require explicit approval immediately before `--confirm-spend`.
- A batch approval covers only the displayed Ready-row count and settings. Reconfirm if model, resolution, duration, count, references, or eligible rows change.
- Persist the returned job ID before continuing. Never resubmit a row that already has a job ID.
- Do not automatically retry failed paid jobs. Report the provider error and request approval for a new attempt.
- `processing` is not delivery. Poll to terminal state, download successful media, and verify it with `ffprobe` before reporting completion.
- Use a dedicated Google account when possible. Account setup gives the third-party service control of that Flow session.

## No-code interaction

When the user asks Codex or Claude Code to handle setup or generation:

1. Inspect the installed skill and the user's chosen project directory.
2. Create a blank project-local `.env` from `assets/.env.example` and open
   it for the user. The user enters the token and email directly in that file;
   never ask them to paste secrets into chat.
3. Guide account connection in the browser, but let the user personally enter
   Google credentials and complete two-factor authentication.
4. Run account checks, previews, submissions, polling, downloads, and media
   verification on the user's behalf.
5. Explain only the result, cost-impacting settings, and any decision the user
   must make. Keep command syntax hidden unless requested.

## Typical commands

Run from the user's project directory:

```bash
python3 /path/to/google-flow-rest/scripts/google_flow_rest.py accounts
python3 /path/to/google-flow-rest/scripts/google_flow_rest.py submit --prompt "..." --model omni-flash --aspect-ratio portrait --resolution 720p --duration 10
python3 /path/to/google-flow-rest/scripts/google_flow_rest.py batch reviewed.csv
python3 /path/to/google-flow-rest/scripts/google_flow_rest.py wait JOB_ID --download --output-dir outputs
```

Only append `--confirm-spend` after the user approves the exact preview.

## Deliver results

Report the submitted count, exact settings, terminal success/failure counts, download paths, and verified duration/resolution/codecs. Keep job IDs in a saved log when a spoken list would be noisy. Clearly label provider-side dimensions when they differ from the advertised resolution.
