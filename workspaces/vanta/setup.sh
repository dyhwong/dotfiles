#!/usr/bin/env zsh

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

echo -n "Symlinking Vanta workspace scripts to ~/.local/bin..."
mkdir -p ~/.local/bin
ln -sf "$SCRIPT_DIR/ensure-obsidian-pr-guard-disabled.sh" ~/.local/bin/ensure-obsidian-pr-guard-disabled.sh
echo "DONE"

echo -n "Setting up agents repo..."
if [ -d ~/agents ]; then
  echo "ALREADY PRESENT"
else
  git clone -q https://github.com/dyhwong/agents.git ~/agents && echo "DONE" || echo "FAILED — clone ~/agents manually"
fi

echo -n "Setting up Vanta Claude local config..."
ln -sf "$SCRIPT_DIR/CLAUDE.md" /workspaces/obsidian/CLAUDE.local.md
echo "DONE"
