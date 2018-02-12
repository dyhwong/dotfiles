" --- VUNDLE SETUP ---
set nocompatible
filetype off
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

Plugin 'VundleVim/Vundle.vim'       " Let Vundle manage Vundle
" TODO: add more packages

call vundle#end()
filetype plugin indent on

" --- VIM SETUP ---
" Return to last edit position when opening files
autocmd BufReadPost *
\ if line("'\"") > 0 && line("'\"") <= line("$") |
\ exe "normal! g`\"" |
\ endif

" Move to next displayed line instead of actual line
nnoremap j gj
nnoremap k gk

" cf opens editable command history
map <C-f> q:i

set number
set mouse=a
colorscheme slate
syntax on

set tabstop=2
set softtabstop=2
set shiftwidth=2
set expandtab
autocmd FileType make set noexpandtab softtabstop=8
