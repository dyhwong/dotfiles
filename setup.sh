#!/usr/bin/env zsh

if [ ! -d $ZSH ]; then
  echo -n "Installing oh-my-zsh..."
  sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
  echo "DONE"
fi

antigen_path=~/.antigen.zsh
if [ ! -f $antigen_path ]; then
  echo -n "Installing antigen..."
  curl -L git.io/antigen > $antigen_path
  echo "DONE"
fi

[ -f ~/.aliases ] && rm ~/.aliases
[ -f ~/.vimrc ] && rm ~/.vimrc
[ -f ~/.zshrc ] && rm ~/.zshrc
echo -n "Symlinking dotfiles to the home directory..."
ln -s "$PWD/.aliases" ~/.aliases
ln -s "$PWD/.vimrc" ~/.vimrc
ln -s "$PWD/.zshrc" ~/.zshrc
echo "DONE"

echo -n "Symlinking bin scripts to ~/.local/bin..."
mkdir -p ~/.local/bin
for script in "$PWD"/bin/*; do
  target=~/.local/bin/$(basename "$script")
  [ -e "$target" ] && rm "$target"
  ln -s "$script" "$target"
done
echo "DONE"

source ~/.zshrc

vundle_path=~/.vim/bundle/Vundle.vim
if [ ! -d $vundle_path ]; then
  echo -n "Installing vundle..."
  git clone https://github.com/VundleVim/Vundle.vim.git $vundle_path
  echo "DONE"
fi

echo -n "Installing vim plugins..."
vim +PluginInstall +qall
echo "DONE"

echo -n "Setting up tmux..."
tmux_conf_path=~/.tmux.conf
[ -x "$(command -v tmux)" ] && tmux start-server
[ -f $tmux_conf_path ] && rm $tmux_conf_path
ln -s "$PWD/.tmux.conf" $tmux_conf_path
echo "DONE"

echo -n "Setting up git config..."
git config --global include.path "$PWD/.gitconfig"
echo "DONE"

echo -n "Setting up Claude Code config..."
mkdir -p ~/.claude
claude_md_path=~/.claude/CLAUDE.md
[ -f $claude_md_path ] && rm $claude_md_path
ln -s "$PWD/CLAUDE.md" $claude_md_path
echo "DONE"

echo -n "Installing git-absorb..."
absorb_version="0.9.0"
if command -v git-absorb >/dev/null 2>&1; then
  echo "ALREADY INSTALLED"
elif [ "$(uname)" = "Darwin" ]; then
  brew install git-absorb && echo "DONE" || echo "FAILED"
else
  target="x86_64-unknown-linux-musl"
  tmp=$(mktemp -d)
  tarball="git-absorb-${absorb_version}-${target}.tar.gz"
  curl -fsSL -o "$tmp/$tarball" "https://github.com/tummychow/git-absorb/releases/download/${absorb_version}/${tarball}" \
    && tar -xzf "$tmp/$tarball" -C "$tmp" \
    && mv "$tmp/git-absorb-${absorb_version}-${target}/git-absorb" ~/.local/bin/git-absorb \
    && echo "DONE" \
    || echo "FAILED"
  rm -rf "$tmp"
fi
