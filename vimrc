" --- VUNDLE SETUP ---

" Vundle required
set nocompatible
filetype off
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

Plugin 'VundleVim/Vundle.vim'           " Let Vundle manage Vundle

" Text editing
Plugin 'ntpeters/vim-better-whitespace' " Better Whitespace removal/highlighting
Plugin 'tpope/vim-surround'             " Add, edit, remove tags like ', \", (, {
Plugin 'vim-scripts/tComment'           " Shortcut to toggle comments
Plugin 'jiangmiao/auto-pairs'           " Auto pairing of tags
Plugin 'ervandew/supertab'              " Autocomplete

" zsh integration
Plugin 'tpope/vim-dispatch'             " Run commands asynchronously

" Code linting
Plugin 'sbdchd/neoformat'               " Autoformatter

" File navigation
Plugin 'junegunn/fzf'
Plugin 'junegunn/fzf.vim'               " Fuzzy search for files
Plugin 'scrooloose/nerdtree'            " Sidebar for file directory
Plugin 'pbrisbin/vim-mkdir'             " Make directories automatically

" Syntax highlighting
Plugin 'leafgarland/typescript-vim'     " Typescript
Plugin 'ianks/vim-tsx'                  " TSX
Plugin 'cakebaker/scss-syntax.vim'      " SCSS

" Git helpers
Plugin 'tpope/vim-fugitive'             " Helpful git stuff

" TODO: add more packages

call vundle#end()
filetype plugin indent on

" --- PLUGIN SETUP ---

" Neoformat
" Only use Neoformat for Typescript and Javascript files
augroup fmt
  autocmd!
  autocmd BufWritePre *.tsx,*.jsx,*.ts,*.js undojoin | Neoformat
augroup END

" --- VIM SETUP ---

" Return to last edit position when opening files
autocmd BufReadPost *
\ if line("'\"") > 0 && line("'\"") <= line("$") |
\ exe "normal! g`\"" |
\ endif

" Set utf8 as standard encoding and en_US as the standard language
set encoding=utf-8

" Turn backup off, since most stuff is in git anyways
set nobackup
set nowb
set noswapfile

"Show line numbers
set number

" Enable mouse
set mouse=a

" Set terminal title
set title

" Allow multiple buffers
set hidden

" Enable Elite mode, no arrows
let g:elite_mode=1

" Search settings
set incsearch       " Find the next match as we type the search
set hlsearch        " Highlight searches by default
set ignorecase      " Smart searching
set smartcase

" Move to next displayed line instead of actual line
noremap j gj
noremap k gk

" cf opens editable command history
map <C-f> q:i

set tabstop=2
set softtabstop=2
set shiftwidth=2
set expandtab
autocmd FileType python setlocal shiftwidth=4 tabstop=4

" Configure backspace so it acts as it should
set backspace=eol,start,indent
set whichwrap+=<,>,h,l

" Show matching brackets when text indicator is over them
set showmatch
set mat=2      " How many tenths of a second to blink when matching

" Make pasting better
set pastetoggle=<leader>q

" Line wrapping, but don't insert newlines
set wrap
set textwidth=0 wrapmargin=0

" Show 3 lines above/below cursor
set scrolloff=3

" Pane splitting
set splitbelow
set splitright

" Syntax highlighting on
syntax enable

" Set shell to zsh
set shell=zsh

" Set colorscheme to oceanic
" colorscheme slate
