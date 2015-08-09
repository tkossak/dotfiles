" ---------------------------------------------------------------------
" VUDNLE installation
" ---------------------------------------------------------------------

let s:uname = system("uname -s")
let s:hname = system("uname -n")

set nocompatible " be iMproved, required
filetype off " required

" set the runtime path to include Vundle and initialize
if has('gui_running') && ( has('win32') || has('win64') ) && isdirectory("D:\\Kossak\\progs\\gvim\\bundle\\Vundle.vim") " windows GVIM
    set rtp+=D:\Kossak\progs\gvim\bundle\Vundle.vim
    call vundle#begin("D:\\Kossak\\progs\\gvim\\_vim")
else
    set rtp+=~/.vim/bundle/Vundle.vim
    call vundle#begin()
endif

" let Vundle manage Vundle, required
Plugin 'gmarik/Vundle.vim'
" Plugin 'altercation/vim-colors-solarized'

" Plugin 'scrooloose/nerdtree'
" Plugin 'othree/eregex.vim'
Plugin 'gregsexton/MatchTag'  " match HTML tags
Plugin 'haya14busa/incsearch.vim'
Plugin 'kien/ctrlp.vim'
Bundle 'christoomey/vim-tmux-navigator'
" Plugin 'scrooloose/syntastic'
Plugin 'junegunn/fzf'
Plugin 'tpope/vim-commentary'
Plugin 'terryma/vim-expand-region'
Plugin 'tpope/vim-repeat'
Plugin 'bling/vim-airline'
Plugin 'EinfachToll/DidYouMean'
Plugin 'KabbAmine/zeavim.vim'
Plugin 'nanotech/jellybeans.vim' " color scheme

" if !has('gui_running') || !( has('win32') || has('win64') )
"     Bundle 'https://github.com/neilagabriel/vim-geeknote'
" endif

call vundle#end()            " required
filetype plugin indent on    " required

" ===================================================
" source .vimrc.local if it exists
" ===================================================
let $LOCALFILE=expand("~/.vimrc.local")
if filereadable($LOCALFILE)
    source $LOCALFILE
endif

" ===================================================
" = for plugins
" ===================================================

" " vim-airline
let g:airline_theme='jellybeans'
let g:airline_left_sep=''
let g:airline_right_sep=''
let g:airline_section_z=''

" statusline appears all the time:
set laststatus=2

" inc-search
map /  <Plug>(incsearch-forward)
map ?  <Plug>(incsearch-backward)
map g/ <Plug>(incsearch-stay)

" Geeknote
" nnoremap <F8> :Geeknote<cr>

" incsearch - automatic nohl
set hlsearch
let g:incsearch#auto_nohlsearch = 1
map n  <Plug>(incsearch-nohl-n)
map N  <Plug>(incsearch-nohl-N)
map *  <Plug>(incsearch-nohl-*)
map #  <Plug>(incsearch-nohl-#)
map g* <Plug>(incsearch-nohl-g*)
map g# <Plug>(incsearch-nohl-g#)

" Make a simple "search" text object.
" Type ys to copy the search hit.
" Type "+ys to copy the hit to the clipboard.
" Type cs to change the hit.
" Type gUs to convert the hit to uppercase.
" Type vs to visually select the hit. If you type another s you will extend the selection to the end of the next hit.
vnoremap <silent> s //e<C-r>=&selection=='exclusive'?'+1':''<CR><CR>
    \:<C-u>call histdel('search',-1)<Bar>let @/=histget('search',-1)<CR>gv
omap s :normal vs<CR>

" syntastic
set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

let g:syntastic_always_populate_loc_list = 1
let g:syntastic_auto_loc_list = 1
let g:syntastic_check_on_open = 1
let g:syntastic_check_on_wq = 0
let g:syntastic_python_python_exec = '/usr/bin/python3'

" vim-expand-region :: expand/shrink selection
vmap v <Plug>(expand_region_expand)
vmap <C-v> <Plug>(expand_region_shrink)

" ==================================================================
" .vimrc
" ==================================================================
set fileencodings=ucs-bom,utf-8,default,cp1250,ibm852,latin1,latin2
set showcmd
set showmode
set wildmode=longest,list " tab completion works as in shell

set incsearch " incremental search (show matches as you type)
set ignorecase " ignore case when searching
set smartcase " ignore case when all pattern is lowercase, CASE-SENSITIVE otherwise

set backspace=2 " backspace works on \n characters
set mouse=a " use mouse in all modes
set number " display line numbers
set hidden " allow to switch between modified buffers
set showmatch " when you insert closing bracket vim brifly jumps/highlights to opening bracket

set autoindent " for new line add the same indentation as previous line
set smartindent " triggered when starting new line according to current language
set expandtab " insert spaces instead of tabs
set softtabstop=4 " amount of spaces for pressing <tab>
set tabstop=4 " amount of spaces to visualize <tab> character
set shiftwidth=4 " number of spaces for each step of autoindent
set shiftround " round indent to multiple of 'shiftwidth'

set listchars=eol:$,tab:>-,trail:~,extends:>,precedes:<
" ↩ ↵ ↲ ␣ • … → » ∎ ¶ ▶ ▸ ▷ ▹
" set listchars=eol:↲,tab:▶▹,nbsp:␣,extends:…,trail:•

set nobackup " do not save backups of the files
" set nowritebackup " writes backup, before saving the file, then deletes backup (if saving was successful)
set noswapfile

set statusline=%t[%{strlen(&fenc)?&fenc:'none'},%{&ff}]%h%m%r%y%=%c,%l/%L\ %P

let mapleader = " "

" diff ignores whitespace
set diffopt+=iwhite
set diffexpr=""
nnoremap <leader>dd :diffthis<CR>
nnoremap <leader>do :diffoff<CR>
nnoremap <leader>ds :DiffSaved<CR>

nnoremap <Leader><BS> :let _s=@/<Bar>:%s/\s\+$//e<Bar>:let @/=_s<Bar>:nohl<CR>
" quickly repeat macro
nnoremap Q @q

noremap <up>    <C-W>+
noremap <down>  <C-W>-
noremap <left>  3<C-W>>
noremap <right> 3<C-W><

nnoremap ; :
nnoremap : ;
vnoremap ; :
vnoremap : ;
" pasting from clipboard without indeting
nnoremap <F10> :set invpaste paste?<CR>
set pastetoggle=<F10>

" copy from os clipboard
vnoremap <Leader>y "+y
nnoremap <Leader>p "+gp
nnoremap <Leader>P "+gP
vnoremap <Leader>p "+gp
vnoremap <Leader>P "+gP

" go to start/end of file
nnoremap <CR> G
nnoremap <BS> gg

" Move visual block
vnoremap J :m '>+1<CR>gv=gv
vnoremap K :m '<-2<CR>gv=gv

" save and run make command
nnoremap <F9> :w<CR>:make<CR>
inoremap <F9> <esc>:w<CR>:make<CR>

" color 80'th column
" set colorcolumn=80
" highlight ColorColumn ctermbg=233

" automatic reloading of .vimrc
autocmd! bufwritepost .vimrc source %

" Show whitespace
" MUST be inserted BEFORE the colorscheme command
autocmd ColorScheme * highlight ExtraWhitespace ctermbg=red guibg=red
au InsertLeave * match ExtraWhitespace /\s\+$/
" Syntax coloring
syntax on " syntax enable
" set t_Co=256
set background=dark
" colorscheme koehler
colorscheme jellybeans

" colorscheme solarized

" center screen after searching/moving:
" nnoremap n nzz
nnoremap } }zz
" nnoremap N Nzz
nnoremap { {zz

" clear search highlight
nnoremap <Leader>h :nohl<CR>

" " quick save
nnoremap <Leader>w :update<CR>
" noremap <C-x> :update<CR>
" vnoremap <C-x> <C-C>:update<CR>
" inoremap <C-x> <C-O>:update<CR>

" Quick quit command
nnoremap <Leader>e :quit<CR>
vnoremap <Leader>e :<BS><BS><BS><BS><BS>quit<CR>
nnoremap <Leader>E :qa<CR>
nnoremap <Leader>Q :qa!<CR>
" copy whole buffer to os clipboard
nnoremap <Leader>a gg"+yG

" easy buffer
noremap <leader>bb :buffers<CR>
noremap <leader>bn :bnext<CR>
noremap <leader>bp :bprev<CR>
noremap <leader>bl :blast<CR>
noremap <leader>bc :bwipe<CR>
noremap <leader>bC :bwipe!<CR>

" bind Ctrl+<movement> keys to move around the windows, instead of using Ctrl+w + <movement>
" Every unnecessary keystroke that can be saved is good for your health :)
nnoremap <C-j> <c-w>j
nnoremap <C-k> <c-w>k
nnoremap <C-l> <c-w>l
nnoremap <C-h> <c-w>h

" easier moving between tabs
nnoremap <leader>to :tabnew<CR>
nnoremap <leader>tk :tabnext<CR>
nnoremap <leader>tj :tabprevious<CR>
nnoremap <leader>tc :tabclose<CR>

set splitright
set splitbelow

" map sort function to a key
noremap <Leader>s :sort<CR>
noremap <Leader>S :sort u<CR>

" visual selection does not disappear after using indent
vnoremap < <gv
vnoremap > >gv

" Rozne keybinding
nnoremap j gj
nnoremap k gk
noremap <F2> :set wrap!<CR>
vnoremap <F2> :<BS><BS><BS><BS><BS>set wrap!<CR>gv
nnoremap <leader>x <C-X>

" insert mode bindings
inoremap jk <esc>
inoremap kj <esc>
" vnoremap jk <esc>
" vnoremap kj <esc>
" inoremap <C-e> <C-O>$
" inoremap <C-a> <C-O>^
" inoremap <C-l> <Del>

" Write to file with sudo
cmap w!! !sudo tee >/dev/null%
" command W :execute ':silent w !sudo tee % > /dev/null' | :edit!

" Allow undo for Insert Mode ^u
inoremap <C-u> <C-g>u<C-u>

" New window created vertically
noremap <C-w>n :vnew<CR>

" ==================================================================
" status line change based on mode:
function! InsertStatuslineColor(mode)
    if a:mode == 'i' || a:mode == 'r' || a:mode == 'v'
        " hi statusline guibg=magenta
        set nocursorline
    " elseif a:mode == 'r'
    "     " hi statusline guibg=red
    "     set nocursorline
    " elseif a:mode == 'v'
    "     " hi statusline guibg=orange
    "     set nocursorline
    else
        " hi statusline guibg=green
        set cursorline
    endif
endfunction

au InsertEnter * call InsertStatuslineColor(v:insertmode)
au InsertChange * call InsertStatuslineColor(v:insertmode)
au InsertLeave * call InsertStatuslineColor('no')
" call InsertStatuslineColor('no')

" default the statusline to green when entering Vim
" hi statusline guibg=green
set cursorline
" set cursorcolumn

" :hi CursorLine   cterm=NONE ctermbg=darkyellow ctermfg=white guibg=darkyellow guifg=white
" :hi CursorColumn cterm=NONE ctermbg=darkyellow ctermfg=white guibg=darkyellow guifg=white
" :hi CursorLine   cterm=NONE ctermbg=Blue guibg=darkyellow guifg=white
" :hi CursorColumn cterm=NONE ctermbg=Blue guibg=darkyellow guifg=white
" :nnoremap <Leader>c :set cursorline! cursorcolumn!<CR>

" ==================================================================
" = GUI only
" ==================================================================

if has('gui_running')
 set guioptions=egmrLt " default on windows is: egmrLtT
 set langmenu=en_US
 let $LANG = 'en_US'
 source $VIMRUNTIME/delmenu.vim
 source $VIMRUNTIME/menu.vim
endif


" ==================================================================
" = CYGWIN only
" ==================================================================
if stridx(s:uname, 'CYGWIN') >= 0
    " execute "set <M-h>=\eh"
    " execute "set <M-l>=\el"
    " inoremap <M-h> <C-\><C-O>b
    " inoremap <M-l> <C-\><C-O>w

    if exists('$TMUX')
        let &t_SI = "\<Esc>Ptmux;\<Esc>\e[5 q\<Esc>\\"
        let &t_EI = "\<Esc>Ptmux;\<Esc>\e[2 q\<Esc>\\"
        let &t_ti.= "\<Esc>Ptmux;\<Esc>\e[1 q\<Esc>\\"
        let &t_te.= "\<Esc>Ptmux;\<Esc>\e[0 q\<Esc>\\"
    else
        let &t_SI = "\e[5 q"
        let &t_EI = "\e[2 q"
        let &t_ti.= "\e[1 q"
        let &t_te.= "\e[0 q"
    endif

    " let &t_ti.="\e[1 q"
    " let &t_SI.="\e[5 q"
    " let &t_EI.="\e[1 q"
    " let &t_te.="\e[0 q"

    if filereadable("/cygdrive/d/Kossak/progs/zeal/zeal.exe")
        let g:zv_zeal_directory = "/cygdrive/d/Kossak/progs/zeal/zeal.exe"
    endif
endif

" ==================================================================
" = LINUX only (no cygwin)
" ==================================================================
" if has('unix') && stridx(s:uname, 'CYGWIN') < 0
"     " execute "set <M-h>=\eh"
"     " execute "set <M-l>=\el"
"     " inoremap <M-h> <C-\><C-O>b
"     " inoremap <M-l> <C-\><C-O>w
"     " if stridx(s:hname, 'LMQ') >= 0
"     "     python from powerline.vim import setup as powerline_setup
"     "     python powerline_setup()
"     "     python del powerline_setup
"     " endif
" endif


" ==================================================================
" different Functions
" ==================================================================

" Simple re-format for minified Javascript
command! UnMinify call UnMinify()
function! UnMinify()
    %s/{\ze[^\r\n]/{\r/g
    %s/){/) {/g
    %s/};\?\ze[^\r\n]/\0\r/g
    %s/;\ze[^\r\n]/;\r/g
    %s/[^\s]\zs[=&|]\+\ze[^\s]/ \0 /g
    normal ggVG=
endfunction

" Diff current buffer (before saving) with it's version on disk
com! DiffSaved call DiffSaved()
function! DiffSaved()
  bufdo diffoff
  let filetype=&ft
  diffthis
  vnew | r # | normal! 1Gdd
  diffthis
  exe "setlocal bt=nofile bh=wipe nobl noswf ro ft=" . filetype
  " normal \<C-w>w
  execute "normal \<C-w>w"
endfunction

" [cmd] Scriptnames - list :scriptnames in the buffer:
" Execute 'cmd' while redirecting output.
" Delete all lines that do not match regex 'filter' (if not empty).
" Delete any blank lines.
" Delete '<whitespace><number>:<whitespace>' from start of each line.
" Display result in a scratch buffer.
function! s:Filter_lines(cmd, filter)
  let save_more = &more
  set nomore
  redir => lines
  silent execute a:cmd
  redir END
  let &more = save_more
  new
  setlocal buftype=nofile bufhidden=hide noswapfile
  put =lines
  g/^\s*$/d
  %s/^\s*\d\+:\s*//e
  if !empty(a:filter)
    execute 'v/' . a:filter . '/d'
  endif
  0
endfunction
command! -nargs=? Scriptnames call s:Filter_lines('scriptnames', <q-args>)
