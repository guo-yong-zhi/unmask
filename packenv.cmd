conda env create -f environment.yml
conda pack -n unmask-environment

set NLTK_DATA=data\nltk_data
set TRANSFORMERS_CACHE=data\transformers_data
python unmask.py
del data\nltk_data\taggers\averaged_perceptron_tagger.zip
del data\nltk_data\taggers\universal_tagset.zip
del data\nltk_data\tokenizers\punkt.zip

pause
