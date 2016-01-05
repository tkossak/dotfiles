let s:uname = system("uname -s")
let s:hname = system("uname -n")

set nocompatible " be iMproved, required
let mapleader = " "
" filetype off " required


" ==================================================================
" VIMRC.PLUGINS
" ==================================================================
let $LOCALFILE=expand("~/.vimrc.plugins")
if filereadable($LOCALFILE)
    source $LOCALFILE
endif


" ==================================================================
" VIMRC.LOCAL
" ==================================================================
let $LOCALFILE=expand("~/.vimrc.local")
if filereadable($LOCALFILE)
    source $LOCALFILE
endif


" ==================================================================
" OPTIONS
" ==================================================================
set hlsearch
set fileencodings=ucs-bom,utf-8,default,cp1250,ibm852,latin1,latin2
set showcmd
set showmode
set wildmode=longest,list " tab completion works as in shell

set incsearch " incremental search (show matches as you type)
set ignorecase " ignore case when searching
set smartcase " ignore case when all pattern is lowercase, CASE-SENSITIVE otherwise

set backspace=2 " backspace works on \n characters
set mouse=a " use mouse in all modes
set relativenumber
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
set nowrap
" set tw=79

set listchars=eol:$,tab:>-,trail:~,extends:>,precedes:<
" ↩ ↵ ↲ ␣ • … → » ∎ ¶ ▶ ▸ ▷ ▹
" set listchars=eol:↲,tab:▶▹,nbsp:␣,extends:…,trail:•

set nobackup " do not save backups of the files
" set nowritebackup " writes backup, before saving the file, then deletes backup (if saving was successful)
set noswapfile

" statusline appears all the time:
set laststatus=2
set statusline=%t[%{strlen(&fenc)?&fenc:'none'},%{&ff}]%h%m%r%y%=%c,%l/%L\ %P

set splitright
set splitbelow
set guifont=Source_Code_Pro::cDEFAULT

" diff ignores whitespace
set diffopt+=iwhite
set diffexpr=""

" Make a simple "search" text object.
" Type ys to copy the search hit.
" Type cs to change the hit.
" Type gUs to convert the hit to uppercase.
" Type vs to visually select the hit. If you type another s you will extend the selection to the end of the next hit.
vnoremap <silent> s //e<C-r>=&selection=='exclusive'?'+1':''<CR><CR>
    \:<C-u>call histdel('search',-1)<Bar>let @/=histget('search',-1)<CR>gv
omap s :normal vs<CR>


" ==================================================================
" KEYS
" ==================================================================

" nnoremap <leader>gd :Gdiff<CR>

" easy diff
nnoremap <leader>dd :diffthis<CR>
nnoremap <leader>do :diffoff<CR>
nnoremap <leader>ds :DiffSaved<CR>

" remove trailing whitespace
nnoremap <Leader><BS> :let _s=@/<Bar>:%s/\s\+$//e<Bar>:let @/=_s<Bar>:nohl<CR>

" quickly repeat macro
nnoremap Q @q

noremap <up>    <C-W>+
noremap <down>  <C-W>-
noremap <left>  3<C-W>>
noremap <right> 3<C-W><

" nnoremap ; :
" nnoremap : ;
" vnoremap ; :
" vnoremap : ;

" pasting from clipboard without indeting
nnoremap <F10> :set invpaste paste?<CR>
set pastetoggle=<F10>

" copy to/from os clipboard
vnoremap <Leader>y "+y
nnoremap <Leader>p "+gp
nnoremap <Leader>P "+gP
vnoremap <Leader>p "+gp
vnoremap <Leader>P "+gP
nnoremap <Leader>a gg"+yG

" go to start/end of file
nnoremap <CR> G
nnoremap <BS> gg

" Move visual block
vnoremap J :m '>+1<CR>gv=gv
vnoremap K :m '<-2<CR>gv=gv

" save and run make command
nnoremap <F9> :w<CR>:make<CR>
inoremap <F9> <esc>:w<CR>:make<CR>

" center screen after searching/moving:
nnoremap } }zz
nnoremap { {zz

" clear search highlight
nnoremap <Leader>sc :nohl<CR>

" " quick save
nnoremap <Leader>fs :update<CR>

" Quick quit command
nnoremap <Leader>e :quit<CR>
vnoremap <Leader>e :<BS><BS><BS><BS><BS>quit<CR>
nnoremap <Leader>E :qa<CR>
nnoremap <Leader>Q :qa!<CR>

" easy buffers
noremap <leader>bb :buffers<CR>
noremap <leader>bn :bnext<CR>
noremap <leader>bp :bprev<CR>
noremap <leader>bl :blast<CR>
noremap <leader>bc :bwipe<CR>
noremap <leader>bC :bwipe!<CR>

" Window bindings
nnoremap <leader>wj <c-w>j
nnoremap <leader>wk <c-w>k
nnoremap <leader>wh <c-w>h
nnoremap <leader>wl <c-w>l
nnoremap <leader>ws <c-w>s
nnoremap <leader>wv <c-w>v
nnoremap <leader>wm :call MaximizeToggle()<CR>" maximize
nnoremap <leader>wc <c-w>c " close
nnoremap <C-j> <c-w>j
nnoremap <C-k> <c-w>k
nnoremap <C-l> <c-w>l
nnoremap <C-h> <c-w>h

" easy tabs
nnoremap <leader>to :tabnew<CR>
nnoremap <leader>tk :tabnext<CR>
nnoremap <leader>tj :tabprevious<CR>
nnoremap <leader>tc :tabclose<CR>

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
inoremap fd <esc>
inoremap df <esc>

" Write to file with sudo
cmap w!! !sudo tee >/dev/null%
" command W :execute ':silent w !sudo tee % > /dev/null' | :edit!

" Allow undo for Insert Mode ^u
inoremap <C-u> <C-g>u<C-u>

" New window created vertically
noremap <C-w>n :vnew<CR>

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




" ==================================================================
" = LINUX only (no cygwin)
" ==================================================================
" if has('unix') && stridx(s:uname, 'CYGWIN') < 0
" endif

" ==================================================================
" BEHAVIOR
" ==================================================================

" color 80'th column
" set colorcolumn=80
" highlight ColorColumn ctermbg=233

" automatic reloading of .vimrc
autocmd! bufwritepost .vimrc source %
autocmd! bufwritepost .vimrc.functions source %
autocmd! bufwritepost .vimrc.plugins source %

" Show whitespace
" MUST be inserted BEFORE the colorscheme command
autocmd ColorScheme * highlight ExtraWhitespace ctermbg=red guibg=red
au InsertLeave * match ExtraWhitespace /\s\+$/

" Syntax coloring
syntax on " syntax enable
" set t_Co=256
set background=dark
" colorscheme koehler
" colorscheme solarized
colorscheme jellybeans
" colorscheme meta5

" GUI only
if has('gui_running')
 set guioptions=egmrLt " default on windows is: egmrLtT
 set langmenu=en_US
 let $LANG = 'en_US'
 source $VIMRUNTIME/delmenu.vim
 source $VIMRUNTIME/menu.vim
endif

" CYGWIN only
if stridx(s:uname, 'CYGWIN') >= 0
    " execute "set <M-h>=\eh"
    " execute "set <M-l>=\el"

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
endif

" ==================================================================
" VIMRC.FUNCTIONS
" ==================================================================
let $LOCALFILE=expand("~/.vimrc.functions")
if filereadable($LOCALFILE)
    source $LOCALFILE
endif


" ==================================================================
" pretty print / beautify
" ==================================================================
" xml
nnoremap <leader>rx :%!tidy -xml -i<CR>
" html
nnoremap <leader>rh :%!tidy -i<CR>
" javascript
nnoremap <leader>rj :UnMinify<CR>


