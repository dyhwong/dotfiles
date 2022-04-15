# Setup Instructions

## Set up Zsh

### Install Zsh
```
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

### Install Antigen
```
curl -L git.io/antigen > dotfiles/antigen.zsh
```

### Symlink `.zshrc`
```
ln -s dotfiles/zshrc ~/.zshrc
source ~/.zshrc
```

## Set up Vim

### Symlink `.vimrc`
```
ln -s dotfiles/vimrc ~/.vimrc
```

### Install Vundle
```
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
```

### Install Plugins
```
vim +PluginInstall +qall
```

## Set up FZF

### Install FZF
```
brew install fzf
```

### Install Key Bindings
```
$(brew --prefix)/opt/fzf/install
```

## Set up Tmux

```
tmux start-server
ln -s dotfiles/tmux.conf ~/.tmux.conf
```

## Install `tldr` and `tree`
```
brew install tldr
brew install tree
source ~/.zshrc
```
