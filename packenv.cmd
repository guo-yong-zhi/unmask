conda env create -f environment.yml
conda pack -n unmask-environment
mkdir -p unmask-environment
tar -xzf unmask-environment.tar.gz -C unmask-environment

set NLTK_DATA="./nltk_data"
set TRANSFORMERS_CACHE=".transformers_data"
python unmask.py
