cd c:\temp

python -m nuitka ^
    --onefile ^
    --mingw64 ^
    --lto=no ^
    --enable-plugin=tk-inter ^
    --windows-disable-console ^
    --windows-icon-from-ico=address_book.ico ^
    address_book_gui_bootstrap.py
pause