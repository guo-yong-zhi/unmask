@echo off
if not exist unmask-environment (
    echo Installing...
    mkdir unmask-environment
    tar -xzf unmask-environment.tar.gz -C unmask-environment
    if errorlevel 1 echo Installation failed. Please manually unpack the file unmask-environment.tar.gz to unmask-environment folder.
    )
echo on

call .\unmask-environment\Scripts\activate.bat
call .\unmask-environment\Scripts\conda-unpack.exe

set NLTK_DATA=data\nltk_data
voila "src\Words Excluded.ipynb"

pause