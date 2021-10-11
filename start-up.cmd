call .\unmask-environment\Scripts\activate.bat
call .\unmask-environment\Scripts\conda-unpack.exe

set NLTK_DATA=nltk_data
set TRANSFORMERS_CACHE=transformers_data
voila UnmaskApp.ipynb

pause