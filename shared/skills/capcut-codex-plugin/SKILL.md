---
name: install-capcut-plugin
description: Install, reinstall, or update the CapCut Codex plugin from its hosted bundle on macOS or Windows, then guide account authorization.
metadata:
  plugin-version: "0.2.0"
---

# Install CapCut Plugin

## Execution Contract

- Read this entire file before taking action, then perform the installation instead of summarizing the instructions or only returning commands.
- Treat this document as a standalone runbook fetched by the user's bootstrap prompt. Do not install or persist it; if a local copy is required for reading, keep it only in the unique temporary directory used for this run. Do not look for sibling scripts, references, or metadata.
- Use only the plugin bundle URL embedded below as the plugin source. Do not discover or substitute another build. The `ifconfig.co` and `ipinfo.io` URLs named in the authorization workflow are allowed only for the mandatory pre-authorization country check, never as bundle sources.
- Request approval for network access, writes outside the workspace, removal of the old installation, and browser launch when required.
- Preserve the current working installation until the replacement bundle has been downloaded, extracted, and staged successfully.
- Do not run any `codex plugin` inventory or mutation command until every step under **Prepare** succeeds. CLI discovery may run only the selected executable's `--version` before then.
- Use the language of the user's installation request for every user-facing update, approval request, error summary, and final instruction. If the request mixes languages, use the language of the user's latest message. Do not default to English because this runbook is written in English. Keep commands, identifiers, paths, versions, URLs, and safe verbatim CLI errors unchanged.
- Treat plugin installation and OAuth authorization as separate phases. Installation ends when verification in step 8 under **Replace and Install** succeeds. From that point onward, always describe the plugin as installed even when authorization is pending, cancelled, timed out, or unsuccessful.
- Record whether `CapCut@CapCut` was already installed before replacement and retain that fact through the authorization phase.
- Keep every downloaded file, extracted file, generated helper, and log for this run inside one unique operating-system temporary directory. The only installer artifacts outside it may be the sibling staging directory and managed-directory backup explicitly described below. Never create installer artifacts in the current working directory or user workspace.
- Execute the workflow with short host-native commands instead of designing a reusable or general-purpose installer program. Do not create ZIP inspection or validation helpers. Do not edit, test, or refactor installer code in the user's workspace.

## Published Version

`metadata.plugin-version` is the semantic version of the plugin distributed by the bundle below, not the ZIP filename revision. Keep it equal to `codex/.codex-plugin/plugin.json` in that bundle when publishing both artifacts. Version checks may read this metadata without executing this installation runbook. An upgrade discovered during MCP login recovery requires the user's explicit agreement before starting **Prepare** or changing the installation.

## Bundle Source

Download this bundle without asking the user for another URL:

```text
https://sf16-sg.tiktokcdn.com/obj/eden-sg/962370eh7nupenuhbo/capcut_codex_plugin/plugins_v20.zip
```

## Platform Setup

Detect the host OS before running commands.

- On macOS, use the native zsh/bash environment.
- On Windows, use native PowerShell on the same Windows host as Codex Desktop, not WSL. Prefer PowerShell 7 while remaining compatible with Windows PowerShell 5.1. Pass values as arguments, use `-LiteralPath` for filesystem operations, avoid shell aliases, `Invoke-Expression`, and `&&`, and check `$LASTEXITCODE` after every Codex CLI command.
- Treat the download URL as an opaque argument so query characters, spaces, or PowerShell metacharacters are never evaluated as code.
- If a native Codex CLI belonging to the active Codex host cannot be found, stop and report that prerequisite instead of installing another CLI or changing configuration in a different host environment.

| Operation | macOS | Windows PowerShell |
| --- | --- | --- |
| Temporary directory | `mktemp -d` | Create a GUID-named directory below `[IO.Path]::GetTempPath()` |
| Download | `curl -fL --proto '=https' --proto-redir '=https'` | `Invoke-WebRequest`; add `-UseBasicParsing` only on Windows PowerShell 5.1 |
| Extract | Use `ditto -x -k` or `unzip` directly | Use `Expand-Archive` directly |
| Find Codex CLI | Prefer the executable bundled with the active desktop app, including `/Applications/ChatGPT.app/Contents/Resources/codex` or `/Applications/Codex.app/Contents/Resources/codex`; otherwise use `command -v codex` | Prefer the executable bundled with the active Codex desktop host when exposed; otherwise use `Get-Command codex` in native PowerShell |

Resolve one absolute CLI path as `<codex-cli>` before changing anything and use that exact executable for every plugin and MCP command in this run; never switch later to a bare PATH-resolved `codex`. Prefer the active desktop app's bundled CLI so its version matches the host. If only a PATH CLI is available, confirm that it belongs to the same native host; never use a WSL CLI for a Windows-hosted app. If this cannot be established, stop instead of installing with an ambiguous CLI.

Resolve the absolute Codex data directory from the existing `CODEX_HOME` value, falling back to the current user's `.codex` directory on the same host. Never overwrite `HOME`, `USERPROFILE`, or `CODEX_HOME`. Use `<codex-data>/plugin-marketplaces/CapCut` as the installer-managed marketplace directory. In every command below, replace `codex` with the resolved `<codex-cli>` absolute path.

## Local Execution Permissions

Before each local command, compare its required access with the current sandbox policy. Download and country-check commands need outbound HTTPS; staging, replacement, rollback, and plugin CLI mutations need writes under `<codex-data>`. The login helper starts a child App Server that also needs writable SQLite state under `<codex-data>`, host credential-store access, outbound HTTPS, and a local callback listener. Check that login can obtain this access before logging out an existing account session.

When the sandbox restricts the command's required access, use the execution tool's supported approval mechanism to run that command outside the sandbox on its first attempt. For tools exposing `sandbox_permissions`, use `require_escalated` with a specific justification; for login, apply it to the whole Node.js helper command so the child inherits the required access. Do not deliberately run in a known-incompatible sandbox first. Keep approval scoped to the exact command, never a blanket shell or CLI prefix.

If the session already has unrestricted access, run normally without escalation parameters. If the current policy prohibits approval requests (for example, `approval_policy=never`), do not request escalation; use existing permissions only. When those permissions are insufficient or approval is unavailable or denied, stop the affected phase and report the required access, preserving completed installation status. Do not use `sudo`, change home directories, rewrite sandbox settings, or add bypass flags to the child CLI.

A SQLite state initialization error with `Operation not permitted` or `Permission denied` is a local startup/access failure, not a CapCut OAuth rejection. The helper suppresses raw App Server stderr; a generic early exit alone does not establish a sandbox cause. Unexpected explicit permission failures during login follow Authenticate step 10; inspect the current registration state before resuming an interrupted installation mutation, rather than blindly replaying it.

## Prepare

1. Download the archive into the new temporary directory. Require redirects and the final response to remain on HTTPS. Treat any failed or incomplete download as terminal and leave the current installation unchanged. Do not execute scripts or binaries from the archive.
2. Extract the archive directly into the unique temporary directory without inspecting archive entries, paths, sizes, links, hashes, signatures, or manifest contents.
3. Locate `.agents/plugins/marketplace.json`, allowing outer wrapper directories, and treat the directory containing `.agents` as the extracted marketplace root. If it cannot be found, report that the bundle layout is unusable and leave the current installation unchanged.
4. Copy that extracted root, including hidden files, to a new sibling staging directory below `<codex-data>/plugin-marketplaces`. Keep the current installation untouched through this step.

## Replace and Install

1. Inspect the installer-owned registration with `codex plugin list --marketplace CapCut --available --json`, and record whether exact plugin ID `CapCut@CapCut` was installed as `was-already-installed`. The `name` values from `codex plugin marketplace list --json` are manifest display identities and may repeat across differently keyed registrations; never stop merely because multiple rows display `CapCut`.
2. Classify the exact configured key `CapCut` as one of these states, comparing normalized absolute paths with host-appropriate case semantics:
   - **Managed:** Its `marketplaceSource.source` is `<codex-data>/plugin-marketplaces/CapCut` and its local plugin source is `<codex-data>/plugin-marketplaces/CapCut/codex`.
   - **Migratable local:** Its marketplace source is an existing local directory outside the managed path and the `CapCut@CapCut` plugin source is inside that directory. Record that source exactly for rollback. This includes an older development or test registration using the key `CapCut`.
   - **Absent:** No configured key `CapCut` resolves.
   Stop before changing anything for a malformed entry, a non-local foreign source, multiple scoped `CapCut@CapCut` entries, or paths that do not fit either accepted state.
3. Ignore and preserve every registration under a different configured key, even when its manifest also displays `CapCut`. Never remove, rename, edit, or copy from those sources.
4. Handle the recorded registration state without removing the installed plugin yet:
   - **Managed:** Keep the existing marketplace registration. Refuse to replace the managed path when it is a symlink or Windows reparse point. Require it to be a normal directory, rename it to a unique backup, then rename the staging directory to `CapCut`.
   - **Migratable local:** Require the managed path not to exist. Run `codex plugin marketplace remove CapCut --json` for that exact configured key and require success with the returned marketplace name exactly `CapCut`; then re-query the exact key and require that it no longer resolves. This unregisters the old source; never delete, rename, or modify the external source directory itself. Then rename the staging directory to `CapCut`.
   - **Absent:** Require the managed path not to exist, then rename the staging directory to `CapCut`.
5. Run with the absolute persistent path, never the temporary extraction path. For **Migratable local** or **Absent**, run:

   ```text
   codex plugin marketplace add <codex-data>/plugin-marketplaces/CapCut --json
   ```

   Require success with the returned marketplace name exactly `CapCut`. For **Managed**, do not run marketplace add or remove. Re-query with `codex plugin list --marketplace CapCut --available --json` and require exactly one `CapCut@CapCut` whose marketplace and plugin sources are the two managed paths before proceeding.
6. Only after the managed marketplace is ready, run `codex plugin remove CapCut@CapCut --json` when `was-already-installed` is true. This supported command removes its configuration and cache. Never clear the whole plugin cache, remove same-named plugins from other marketplace keys, or use wildcard deletion. Then always run:

   ```text
   codex plugin add CapCut@CapCut --json
   ```

7. Record the version returned by `codex plugin add` and require it to equal this document's `metadata.plugin-version`. A mismatch means the document and bundle were published inconsistently; treat it as verification failure and apply step 9.
8. Confirm from `codex plugin list --marketplace CapCut --available --json` that `CapCut@CapCut` is installed, enabled, has the recorded version, and resolves to the two managed paths. Run `codex mcp get capcut_creation --json` and require `enabled` to be `true` and the transport URL to be exactly `https://www.capcut.com/api/external_mcp`. Do not parse human-readable CLI output or add a duplicate MCP server manually.
9. Track separately whether the old registration was removed, the new registration was created, and the old plugin was removed. If replacement or verification fails, remove only an incomplete new `CapCut@CapCut`. Remove the new `CapCut` marketplace registration only when this run created it and a fresh scoped query confirms it points to the managed path. Move any replacement managed directory and sibling staging directory back into this run's temporary area before restoring prior state, unless the supported marketplace removal already removed that exact managed directory. For **Managed**, restore the backed-up managed directory while keeping its registration. For **Migratable local**, re-add the exact recorded external source only when the old registration was successfully removed and the exact key is currently absent; never modify that external directory. For **Absent**, leave the exact key absent. Reinstall the prior `CapCut@CapCut` only when `was-already-installed` is true, the old plugin was actually removed, and its original registration has been restored. If failure occurred before old-plugin removal, preserve the existing plugin configuration and cache instead of reinstalling it. Report any rollback failure explicitly and never alter registrations under other keys. Remove a managed backup only after the new plugin passes verification.

## Present Capabilities

Immediately after installation verification succeeds, and before any logout or login command, explicitly tell the user in their language that the CapCut plugin installation is complete and state the installed version. Then show:

- **Template search:** Search CapCut templates and editing inspiration from natural language, images, or videos.
- **AI video editing:** Turn uploaded footage into a finished video with cuts, pacing, captions, transitions, and music.

Clearly label the next action as a separate authorization phase. Explain that the plugin is already installed, Codex will first check whether authorization is available from the current network, and the CapCut authorization page will open only when that check does not identify US egress. Credentials must remain in the browser.

## Authenticate

1. Before any account logout or login, tell the user in their language that plugin installation is complete and Codex is checking whether account authorization is available from the current network. Run the primary check as its own command: on macOS use `curl -fsS --connect-timeout 5 --max-time 10 https://ifconfig.co/country-iso`; on Windows use the same command with `curl.exe`. Do not append `|| true`, replace failure with success, run providers in parallel, or substitute another endpoint. Accept the result only when the command succeeds and its complete trimmed, case-normalized response is exactly two ASCII letters.
   - If the primary command fails or its response is empty or malformed, run the fallback once as a separate command: `curl -fsS --connect-timeout 5 --max-time 10 https://ipinfo.io/country`, using `curl.exe` on Windows. Apply the same exit-status and exact two-letter validation. Never describe a failed or malformed response as a passed check.
   - If the first valid result is exactly `US`, record `us-network-unsupported`, state that the plugin remains installed but authorization is unavailable because the current network egress appears to be in the United States, and skip every remaining authentication step. Do not run account logout or login.
   - If the first valid result is another two-letter country code, continue without calling another provider. Do not persist or log the response, and never claim that region availability is guaranteed or that the check "passed."
   - If neither provider returns a valid country code, state that the network region could not be verified and OAuth will still be attempted, then continue the authorization workflow. Never call this outcome a passed, successful, available, or non-US region check. Do not choose another provider or repeat either check in this run.
2. Locate `<codex-data>/plugin-marketplaces/CapCut/codex/skills/mcp-auth/scripts/capcut-login.mjs`, resolve a native Node.js runtime, and confirm that an in-app browser tool is available before changing the account session. If a prerequisite is missing, leave the existing session intact, keep installation marked complete, and report authorization as incomplete. Otherwise explain that opening a fresh authorization page replaces any existing local CapCut MCP session, and request approval when required. Then run `codex mcp logout capcut_creation` once and tolerate only the no-existing-session result. Skip logout when the user explicitly asks to preserve an existing valid connection.
3. Never log in to or otherwise attach OAuth to `capcut_creation_resource`; it is identity-free.
4. Before starting login, tell the user in their language that plugin installation is complete and only authorization in Codex's in-app browser remains.
5. Run the installed helper under **Local Execution Permissions** with the same absolute CLI selected during **Platform Setup**:

   ```text
   node <codex-data>/plugin-marketplaces/CapCut/codex/skills/mcp-auth/scripts/capcut-login.mjs --codex-cli <codex-cli>
   ```

   Use a persistent shell execution session and a short initial wait. The helper starts `codex app-server` and requests `mcpServer/oauth/login`; it leaves callback handling, PKCE, and credential storage to Codex without opening a system browser. Do not run `codex mcp login capcut_creation` or use `BROWSER` overrides. When `event=authorization_required` arrives, pass the exact `authorization_url` to `mcp__codex_app__open_in_codex` with `target={"type":"browser","url":<authorization_url>}`. If only Computer Use is available, use `cua.createBrowserTab("iab", authorization_url, { visible: true })` under that tool's current instructions. Leave login and consent to the user. If opening the in-app browser fails, stop the helper and report authorization as incomplete; do not switch to a system browser.
6. Poll the same running helper with waits of at most 60 seconds, without starting another login. Treat a poll with no new output or a polling-tool timeout only as authorization still pending. It is not evidence of slow or failed installation, browser-launch failure, OAuth cancellation, or OAuth timeout. Every progress update during this wait must explicitly say that installation is complete and only browser authorization is pending. Never describe this phase as installation. If the user cancels, interrupt this helper to stop its App Server and callback listener.
7. Never construct, modify, or display an authorization URL as a chat link. Pass only the exact URL returned by this helper to the in-app browser. If no URL was emitted, do not invent one. Opening the page or receiving a URL does not prove authorization succeeded.
8. Never request or expose cookies, tokens, authorization codes, browser storage, or raw headers.
9. Report authentication as successful only when the helper emits `event=completed` with `success=true` for `capcut_creation` and exits with code 0. This event comes from Codex's `mcpServer/oauthLogin/completed` notification. Do not infer cancellation or OAuth timeout from silence or a polling-tool timeout. If an execution wrapper stops waiting before success, report authorization as pending or incomplete while continuing to report installation as complete.
10. If the login invocation definitively fails after plugin verification succeeded:
   - If that same login process's safe error explicitly identifies HTTP 502 or Bad Gateway from the MCP endpoint, do not retry it or repeat the country check. Retain the original safe 502 error and continue with the unresolved-failure handling below.
   - For an unexpected permission failure only: when the first invocation has definitively failed, either because the execution tool rejected it before launch or because the process exited, its error explicitly identifies a local sandbox or network-permission denial, and that invocation did not use the required permission, follow **Local Execution Permissions** to rerun the exact same command outside the sandbox once when policy permits. Poll that retried process under step 6's rules. Do not use this retry for DNS, TLS, timeout, HTTP, remote-service, or OAuth protocol or configuration failures, or a generic App Server early exit.
   - If approval is prohibited, unavailable or denied, or the single retry still fails, retain the specific safe error and stop further authorization attempts. Do not retry again, change endpoints, reinstall the plugin, or inspect credentials.
   - For any other definitive invocation failure, do not retry login or reinstall the plugin in this task. Retain the exact safe error and stop further authorization attempts; do not treat a local sandbox or network-permission denial as an OAuth configuration failure.
   - In every unresolved failure case, state that the plugin remains installed and mark authorization as incomplete. Tell the user to open a new Codex task and ask it to authorize the CapCut plugin; the new task should perform only the `capcut_creation` authorization flow, not installation. Apply this handoff especially when `was-already-installed` is true. Never log in to `capcut_creation_resource`.

## Finish

Clean up the unique temporary directory for this run and any successful-install backup, including on early failure.

Report two separate statuses:

- **Plugin installation:** Report whether installation completed and include the installed version when successful.
- **CapCut authorization:** Report `complete`, `pending`, or `incomplete`, with a concise safe reason when it is not complete.

Do not start a template search or video edit in this task. Choose the first matching final user-facing sentence from these branches and append nothing after it:

- If `us-network-unsupported` was recorded: use the localized equivalent of "CapCut plugin authorization is not currently available from the U.S. network detected for this device. Thanks for your understanding."
- If authorization failed or is incomplete after successful plugin verification: use the localized equivalent of "Open a new Codex task and ask Codex to authorize the CapCut plugin."
- If authorization succeeded: use the localized equivalent of "Open a new Codex task."
