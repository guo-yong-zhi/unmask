@echo off
if not exist holly-environment (
    echo Installing...
    mkdir holly-environment
    .\tar.exe -xzf holly-environment.tar.gz -C holly-environment
    if errorlevel 1 echo Installation failed. Please manually unpack the file holly-environment.tar.gz to holly-environment folder.
    )
echo on

call .\holly-environment\Scripts\activate.bat
call .\holly-environment\Scripts\conda-unpack.exe

set NLTK_DATA=data\nltk_data
set PYDEVD_DISABLE_FILE_VALIDATION=1
voila "Words Excluded.ipynb"

pause