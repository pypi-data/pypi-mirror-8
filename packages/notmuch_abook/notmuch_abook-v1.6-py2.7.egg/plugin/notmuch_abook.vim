" Address book management


if exists("g:notmuch_addressbook")
    finish
else
    let g:notmuch_addressbook = 1
endif

if !has('python')
    echoerr "Error: Notmuch Addressbook plugin requires Vim to be compiled with +python"
    finish
endif

if !exists("g:notmuchconfig")
    let g:notmuchconfig = "~/.notmuch-config"
endif

let s:scriptpath = expand('<sfile>:p:h')

" Init link to Addressbook database
fun! InitAddressBook()
    py import vim
    py import sys
    py import os.path

    py curpath = vim.eval("getcwd()")
    py libpath = os.path.join(os.path.abspath(os.path.join(vim.eval("s:scriptpath"), '..')), 'pylibs')
    py sys.path = [os.path.dirname(libpath), libpath, curpath] + sys.path

    py import notmuch_abook
    py cfg = notmuch_abook.NotMuchConfig(os.path.expanduser(vim.eval("g:notmuchconfig")))
    py db = notmuch_abook.SQLiteStorage(cfg) if cfg.get("addressbook", "backend") == "sqlite3" else None
endfun

" Addressbook completion
fun! CompleteAddressBook(findstart, base)
    let curline = getline('.')
    if curline =~ '^From: ' || curline =~ '^To: ' || curline =~ 'Cc: ' || curline =~ 'Bcc: '
        if a:findstart
        " locate the start of the word
            let start = col('.') - 1
            while start > 0 && curline[start - 2] != ":" && curline[start - 2] != ","
                let start -= 1
            endwhile
            return start
        else
python << EOP
encoding = vim.eval("&encoding")
if db:
    for addr in db.lookup(vim.eval('a:base')): 
        if addr[0] == "":
            addr = addr[1]
        else:
            addr = addr[0]+" <"+addr[1]+">"
        vim.command('call complete_check()')
        vim.command(('call complete_add("%s")' % addr.replace('"', "")).encode( encoding ))
else:
    vim.command('echoerr "No backend found."')
EOP
            return []
        endif
    endif
endfun

augroup notmuchabook
    au!
    au FileType mail call InitAddressBook()
    au FileType mail setlocal completefunc=CompleteAddressBook
augroup END

