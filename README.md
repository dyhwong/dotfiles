# Setup Instructions

## Install Brew
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## Install tmux
```
brew install tmux
```

## Run the setup script
```
./setup.sh
```

## Optional Setup
### Set up FZF

#### Install FZF
```
brew install fzf
```

#### Install Key Bindings for `zsh`
##### Mac OS
```
$(brew --prefix)/opt/fzf/install
```

##### Linux
```
. /usr/share/doc/fzf/examples/key-bindings.zsh
```

### Install `tldr` and `tree`
```
brew install tldr
brew install tree
source ~/.zshrc
```

---

## Repo layout

| Path | Purpose |
|------|---------|
| `setup.sh` | Main installer — symlinks dotfiles, installs tools |
| `bin/` | Personal utility scripts; `setup.sh` symlinks all of them to `~/.local/bin/` |
| `.aliases` | Shell aliases |
| `.zshrc` | Zsh config (plugins via antigen, env vars, sourcing `.aliases`) |
| `.gitconfig` | Git config (included globally by `setup.sh`) |
| `.vimrc` | Vim config (plugins via Vundle) |
| `.tmux.conf` | tmux config |
| `CLAUDE.md` | Global Claude Code instructions — symlinked to `~/.claude/CLAUDE.md` |
| `claude-settings.json` | Claude Code settings — symlinked to `~/.claude/settings.json` |

## Adding a new tool

Add an install block to `setup.sh`. Follow the existing pattern: check if already installed, then branch on Mac vs Linux:

```bash
echo -n "Installing <tool>..."
if command -v <tool> >/dev/null 2>&1; then
  echo "ALREADY INSTALLED"
elif [ "$(uname)" = "Darwin" ]; then
  brew install <tool> && echo "DONE" || echo "FAILED"
else
  # Linux: download from GitHub releases or use apt/curl
  echo "DONE"
fi
```

## Adding a utility script

Drop the script in `bin/`. `setup.sh` auto-symlinks everything in `bin/` to `~/.local/bin/`, so no further changes are needed. Mark it executable.

## Where config changes go

- New aliases → `.aliases`
- New env vars, PATH entries, plugin declarations → `.zshrc`
- Git aliases or config → `.gitconfig`
- Editor settings → `.vimrc`
- Terminal multiplexer settings → `.tmux.conf`
- Claude Code behavior → `CLAUDE.md` (symlinked globally — change carefully)
- Claude Code hooks, permissions, plugins → `claude-settings.json`

## setup.sh conventions

- All steps print `echo -n "Doing X..."` before work and `echo "DONE"` after.
- Steps are idempotent: guard with existence checks before symlinking or installing.
- Symlink steps remove the old target before creating the new one.
- Cross-platform: Mac uses `brew`, Linux uses package managers or direct downloads from GitHub releases.
- Machine-specific logic is fine — check for a path or condition before applying it.
