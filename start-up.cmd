if not exist unmask-environment (
    echo Installing...
    mkdir unmask-environment
    tar -xzf unmask-environment.tar.gz -C unmask-environment
    )
call .\unmask-environment\Scripts\activate.bat
call .\unmask-environment\Scripts\conda-unpack.exe

set NLTK_DATA=data\nltk_data
set TRANSFORMERS_CACHE=data\transformers_data
voila UnmaskApp.ipynb

pause