cd c:\temp

python -m nuitka ^
    --onefile ^
    --mingw64 ^
    --lto=no ^
    --enable-plugin=pyside6 ^
    --windows-console-mode=disable ^
    --windows-icon-from-ico=address_book.ico ^
    address_book_pyside6_dark.py
pause