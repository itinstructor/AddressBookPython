cd c:\temp

python -m nuitka ^
    --mingw64 ^
    --lto=no ^
    --onefile ^
    --windows-icon-from-ico=address_book.ico ^
    address_book_cli.py
pause