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
