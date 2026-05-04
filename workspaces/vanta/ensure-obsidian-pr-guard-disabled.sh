#!/usr/bin/env bash
# Disables the obsidian pr-template-guard plugin in the current checkout by
# merging an entry into .claude/settings.local.json. Idempotent — no-op when
# already disabled, no-op when not in an obsidian checkout.
#
# Wired in via a SessionStart hook in ~/.claude/settings.json.

set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
PLUGIN_DIR="$PROJECT_DIR/.claude/plugins/pr-template-guard"
LOCAL_SETTINGS="$PROJECT_DIR/.claude/settings.local.json"
PLUGIN_KEY="pr-template-guard@obsidian-local"

[[ -d "$PLUGIN_DIR" ]] || exit 0

if [[ -f "$LOCAL_SETTINGS" ]] && jq -e --arg k "$PLUGIN_KEY" \
    '.enabledPlugins[$k] == false' "$LOCAL_SETTINGS" >/dev/null 2>&1; then
  exit 0
fi

mkdir -p "$(dirname "$LOCAL_SETTINGS")"
TMP="$(mktemp)"
if [[ -f "$LOCAL_SETTINGS" ]]; then
  jq --arg k "$PLUGIN_KEY" '.enabledPlugins[$k] = false' "$LOCAL_SETTINGS" > "$TMP"
else
  jq -n --arg k "$PLUGIN_KEY" '{enabledPlugins: {($k): false}}' > "$TMP"
fi
mv "$TMP" "$LOCAL_SETTINGS"
