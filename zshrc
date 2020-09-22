###################
## ZSH THEME
###################

# Set name of the theme to load. Optionally, if you set this to "random"
# it'll load a random theme each time that oh-my-zsh is loaded.
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="simple"

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion. Case
# sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# ssh
# export SSH_KEY_PATH="~/.ssh/rsa_id"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"

###################
## ZSH SETUP
###################
export ZSH=$HOME/.oh-my-zsh
source $ZSH/oh-my-zsh.sh

###################
## ANTIGEN SETUP
###################
# Set up antigen.
source $HOME/dotfiles/antigen.zsh

# Load the oh-my-zsh library.
antigen use oh-my-zsh

# Load gitfast bundle.
antigen bundle gitfast

# Load zsh syntax highlighting bundle.
antigen bundle zsh-users/zsh-syntax-highlighting

# Load shell completion suggestions bundle.
antigen bundle zsh-users/zsh-autosuggestions

# Load Tmux bundle.
antigen bundle tmux

antigen apply

###################
## VI MODE
###################
# Vi line-editing mode
bindkey -v

# Reduce mode transition delay to 0.1s
export KEYTIMEOUT=1

function zle-line-init zle-keymap-select {
    VIM_PROMPT="%{$fg_bold[yellow]%} [% COMMAND]%  %{$reset_color%}"
    RPS1="${${KEYMAP/vicmd/$VIM_PROMPT}/(main|viins)/} $EPS2"
    zle reset-prompt
}

zle -N zle-line-init
zle -N zle-keymap-select

# Use vim CLI mode
bindkey '^P' up-history
bindkey '^N' down-history

# Fix backspace after returning from command mode
bindkey '^?' backward-delete-char

# Add ctrl-w: remove word backwards
bindkey '^w' backward-kill-word

# Add ctrl-r: search history backward
bindkey '^r' history-incremental-search-backward

# Bind ctrl + space to autoaccept
bindkey '^ ' autosuggest-accept

# Save history
export HISTSIZE=130000
export HISTFILE=~/.zsh_history
export SAVEHIST=$HISTSIZE
setopt    hist_ignore_all_dups
setopt    appendhistory
setopt    sharehistory
setopt    incappendhistory

# Don't abort commands if glob-matching fails
setopt NO_NOMATCH

source ~/dotfiles/alias/main.alias
export PATH="/usr/local/sbin:$PATH"

source ~/.config/broot/launcher/bash/br

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=240'

###################
## NVM SETUP
###################
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
