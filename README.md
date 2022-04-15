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

#### Install Key Bindings
```
$(brew --prefix)/opt/fzf/install
```

### Install `tldr` and `tree`
```
brew install tldr
brew install tree
source ~/.zshrc
```
