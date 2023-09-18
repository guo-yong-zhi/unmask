conda env create -f environment.yml
conda pack -n holly-environment

set NLTK_DATA=data\nltk_data
set TRANSFORMERS_CACHE=data\transformers_data
python src/unmask.py
python src/check_word.py
del data\nltk_data\taggers\averaged_perceptron_tagger.zip
del data\nltk_data\taggers\universal_tagset.zip
del data\nltk_data\tokenizers\punkt.zip

pause
