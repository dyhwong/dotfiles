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

### Customize Terminal Prompt
In `~/.oh-my-zsh/themes/simple.zsh-theme`, update `PROMPT='%n@%m:%~%# '

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

### Symlink `.tmux.conf`
```
ln -s dotfiles/tmux.conf ~/.tmux.conf
source ~/.tmux.conf
```

## Install `tldr`, `broot`, and `tree`
```
brew install tldr
brew install broot
brew install tree
source ~/.zshrc
```
